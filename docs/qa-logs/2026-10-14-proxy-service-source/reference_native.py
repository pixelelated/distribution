#!/usr/bin/env python3
"""HELD: native proxy integration in one fresh allocated no-NIC GENERIC_X64 VM.

Real pinned Python/native hashing, SQLite, HTTP and signing. Synthetic RA protocol
peer and configured accounts only. No systemd/full-service or emulator launch.
"""
from __future__ import annotations
import argparse
import base64
import contextlib
import copy
import ctypes
import ctypes.util
import encodings.ascii
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler
import io
import json
import os
from pathlib import Path
import re
import resource
import runpy
import signal
import socket
import socketserver
import struct
import sys
import threading
import time
from urllib.parse import parse_qsl, urlencode, urlsplit
from unittest import mock

PACKET=Path(__file__).resolve().parents[1]
BINDINGS_SHA256='d66230e0c13c527b20b00d305b2fd9da4b0f65585aa4591a2a8bd29a1add2682'
PROXY_PORT=8080
STUB_PORT=18081
INPUT_ROOT=Path('/run/pix583-native-inputs')
USER_A='fixture-a';USER_B='fixture-b'
TOKENS={USER_A:'<synthetic-token-a>',USER_B:'<synthetic-token-b>'}
SERVERS=[]
REPORT={'status':'FAIL','evidence':'native bridge + synthetic local protocol, not full service/gameplay','steps':[],'requests':[],'thread_errors':[]}


class Denied(BaseException):pass


def need(value,message):
    if not value:raise AssertionError(message)


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def note(name,**details):
    REPORT['steps'].append({'name':name,**details})


def input_file(root,row,limit=32*1024*1024):
    path=(root/row['path']).resolve(strict=True)
    need(path.is_relative_to(root) and path.is_file(),'input escapes staged root')
    need(path.stat().st_size==row['bytes'] and row['bytes']<=limit,'input size changed')
    need(sha(path)==row['sha256'],'input hash changed: '+row['path'])
    return path


def tcp_listeners():
    return [line.split() for line in Path('/proc/net/tcp').read_text().splitlines()[1:]
            if line.split()[3]=='0A']


def socket_identity(server):
    inode=os.fstat(server.socket.fileno()).st_ino
    fd_link=os.readlink('/proc/self/fd/'+str(server.socket.fileno()))
    need(fd_link==f'socket:[{inode}]','owned listener fd identity mismatch')
    matches=[r for r in tcp_listeners() if r[1]=='0100007F:1F90' and r[9]==str(inode)]
    need(len(matches)==1,'proxy port is not the fixture-owned listening inode')
    raw=Path('/proc/self/stat').read_text();fields=raw.rsplit(')',1)[1].split()
    return {'pid':os.getpid(),'start_ticks':int(fields[19]),'socket_inode':inode,
            'fd':server.socket.fileno(),'network_namespace':os.readlink('/proc/self/ns/net')}


def start(server):
    thread=threading.Thread(target=server.serve_forever,kwargs={'poll_interval':0.05},daemon=True)
    SERVERS.append((server,thread));thread.start();return server


def stop(server):
    pair=next(pair for pair in SERVERS if pair[0] is server)
    server.shutdown();pair[1].join(timeout=2);server.server_close()
    need(not pair[1].is_alive(),'server thread failed to stop')
    SERVERS.remove(pair)


def request(params,headers=None):
    body=urlencode(params).encode();started=time.monotonic()
    wire=(f'POST /dorequest.php HTTP/1.0\r\nHost: 127.0.0.1\r\nContent-Length: {len(body)}\r\n'
          'Content-Type: application/x-www-form-urlencoded\r\n'+
          ''.join(k+': '+v+'\r\n' for k,v in (headers or {}).items())+'\r\n').encode()+body
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as conn:
        conn.settimeout(4);conn.connect(('127.0.0.1',PROXY_PORT));conn.sendall(wire)
        data=bytearray()
        while True:
            chunk=conn.recv(16384)
            if not chunk:break
            data.extend(chunk);need(len(data)<=128*1024,'oversized proxy response')
    head,payload=bytes(data).split(b'\r\n\r\n',1)
    lines=head.decode('ascii').split('\r\n');status=int(lines[0].split()[1])
    fields={k.strip().lower():v.strip() for k,v in (line.split(':',1) for line in lines[1:])}
    parsed=json.loads(payload)
    REPORT['requests'].append({'action':params['r'],'user':params.get('u'),'status':status,
                               'headers':fields,'body':parsed,'elapsed_ms':(time.monotonic()-started)*1000})
    return status,fields,parsed


def ready():
    status,headers,login=request({'r':'login2','u':USER_A,'t':TOKENS[USER_A]})
    need(status==200 and headers.get('x-ra-proxy')=='1' and headers.get('x-ra-offline')=='1','not an offline proxy response')
    need(login.get('Success') is True and login.get('User')==USER_A and login.get('Token')==TOKENS[USER_A],
         'offline login body does not identify the configured synthetic account')
    status,headers,patch=request({'r':'patch','g':'20','u':USER_A})
    need(status==200 and patch.get('PatchData',{}).get('ID')==20,'next game is not ready')


class Stub(socketserver.ThreadingMixIn,socketserver.TCPServer):
    allow_reuse_address=True
    daemon_threads=True


class ProtocolState:
    def __init__(self,digest):
        self.digest=digest;self.mode='normal';self.calls=[];self.applied=[]
        self.unlocks={(10,USER_A):{103},(10,USER_B):{104},(20,USER_A):set()}
        self.thread_errors=[];self.secret=None;self.queued={}

    def reply(self,method,path,body):
        need(len(self.calls)<128,'stub request budget exceeded')
        params=dict(parse_qsl(urlsplit(path).query));params.update(dict(parse_qsl(body)))
        action=params.get('r','HEAD');user=params.get('u','')
        self.calls.append({'method':method,'action':action,'user':user,'params':params,'mode':self.mode})
        if method=='HEAD':return 200,{'Success':True}
        need(urlsplit(path).path=='/dorequest.php','unexpected stub endpoint')
        if action=='login2' and self.mode in ('login401','login403'):
            return int(self.mode[-3:]),{'Success':False,'Error':'Synthetic credential rejection'}
        if user not in TOKENS or params.get('t')!=TOKENS[user]:
            return 401,{'Success':False,'Error':'Synthetic credential rejection'}
        if action=='login2':return 200,{'Success':True,'User':user,'Token':TOKENS[user],'Score':0}
        if action=='gameid':return 200,{'Success':True,'GameID':10 if params.get('m')==self.digest else 0}
        game=(10 if params.get('m')==self.digest else 20) if action=='achievementsets' else int(params.get('g','10'))
        definitions=[{'ID':aid,'Title':'Synthetic '+str(aid),'Description':'Public fixture only','Flags':3,'Points':5,'MemAddr':'0xH000000=1'}
                     for aid in ([101,102,103,104] if game==10 else [201])]
        if action=='patch':
            if self.mode=='patch500':return 500,{'Success':False,'Error':'Synthetic patch failure'}
            return 200,{'Success':True,'PatchData':{'ID':game,'Title':'Synthetic Game '+str(game),'Achievements':definitions}}
        if action=='achievementsets':
            return 200,{'Success':True,'GameId':game,'Sets':[{'ID':game,'Type':'core','Achievements':definitions}]}
        if action=='unlocks':return 200,{'Success':True,'UserUnlocks':sorted(self.unlocks.get((game,user),set()))}
        if action=='awardachievement':
            aid=int(params['a']);need(params.get('h')=='0','stub received a hardcore award')
            need(self.secret is not None,'award before signing secret bound')
            original=self.queued[aid]
            need(all(params[field]==original[key] for field,key in
                     (('ra_chain_payload_hash','payloadHash'),('ra_chain_prev_hash','prevHash'),('ra_chain_sig','signature'))),
                 'outgoing chain identity does not match this queued achievement')
            message=(params['ra_chain_payload_hash']+':'+params['ra_chain_prev_hash']).encode()
            expected=base64.b64encode(hmac.new(self.secret,message,hashlib.sha256).digest()).decode()
            need(hmac.compare_digest(expected,params['ra_chain_sig']),'stub rejected invalid independent HMAC')
            expected_key=base64.b64encode(hashlib.sha256(self.secret).hexdigest().encode()).decode()
            need(params.get('ra_chain_pubkey')==expected_key,'stub key identity differs')
            offset=int(params.get('o','0'));material=str(aid)+user+'0'+(str(aid)+str(offset) if offset else '')
            if offset:need(params.get('v')==hashlib.md5(material.encode()).hexdigest(),'award validation hash differs')
            if self.mode=='award401':return 401,{'Success':False,'Error':'Synthetic token rejection'}
            if self.mode=='award500':return 500,{'Success':False,'Error':'Synthetic award failure'}
            need((user,aid) not in self.applied,'duplicate successful submission')
            self.applied.append((user,aid));self.unlocks.setdefault((10,user),set()).add(aid)
            return 200,{'Success':True}
        raise AssertionError('unexpected synthetic action '+action)


def upstream(state):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_HEAD(self):self.handle_call()
        def do_GET(self):self.handle_call()
        def do_POST(self):self.handle_call()
        def handle_call(self):
            try:
                size=int(self.headers.get('Content-Length','0'));need(0<=size<=65536,'stub input too large')
                status,payload=state.reply(self.command,self.path,self.rfile.read(size).decode())
            except BaseException as error:
                state.thread_errors.append(type(error).__name__+': '+str(error));status=500;payload={'Success':False,'Error':'Fixture assertion failed'}
            data=json.dumps(payload).encode();self.send_response(status);self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(data)));self.send_header('Connection','close');self.end_headers()
            if self.command!='HEAD':self.wfile.write(data)
    return start(Stub(('127.0.0.1',STUB_PORT),Handler))


def install_guard(out,prepared,libraries):
    allowed_read=[p.resolve() for p in (out,INPUT_ROOT,PACKET,prepared,Path(sys.base_prefix)/'lib')]
    allowed_files={Path(p).resolve() for p in ('/etc/os-release','/proc/self/stat','/proc/self/maps','/proc/net/tcp','/proc/net/route')}
    lib_paths={str(Path(row['path']).resolve()):row for row in libraries.values()}
    dl_names=set(lib_paths)|{row['path'] for row in libraries.values()}|{row['soname'] for row in libraries.values()}
    def audit(event,args):
        if event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','socket.sendto','socket.gethostbyname','socket.gethostbyaddr'):
            raise Denied(event)
        if event=='socket.getaddrinfo' and (args[0]!='127.0.0.1' or args[1] not in (None,PROXY_PORT,STUB_PORT)):
            raise Denied('non-numeric/allocated name resolution')
        if event=='socket.__new__' and args[1:3]!=(socket.AF_INET,socket.SOCK_STREAM):raise Denied('socket family/type')
        if event in ('socket.bind','socket.connect') and args[1] not in (('127.0.0.1',PROXY_PORT),('127.0.0.1',STUB_PORT)):
            raise Denied('unallocated endpoint')
        if event=='ctypes.dlopen' and args[0] not in dl_names:raise Denied('unbound native library')
        if event=='sqlite3.connect':
            value=str(args[0]).removeprefix('file:').split('?',1)[0]
            if not Path(value).resolve().is_relative_to(out):raise Denied('non-fixture SQLite')
        if event=='open' and not isinstance(args[0],int):
            path=Path(os.fsdecode(args[0])).resolve();write=args[2] & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
            if write and not path.is_relative_to(out):raise Denied('write outside fixture: '+str(path))
            if not write and not (path in allowed_files or str(path) in lib_paths or any(path.is_relative_to(root) for root in allowed_read)):
                raise Denied('read outside fixture/runtime: '+str(path))
        if event in ('os.remove','os.rmdir','os.mkdir','os.chmod'):
            if not Path(os.fsdecode(args[0])).resolve().is_relative_to(out):raise Denied('mutation outside fixture')
        if event in ('os.rename','os.replace'):
            if not all(Path(os.fsdecode(p)).resolve().is_relative_to(out) for p in args[:2]):raise Denied('rename outside fixture')
    sys.addaudithook(audit)
    for event,args in [('socket.connect',(None,('192.0.2.1',443))),('socket.getaddrinfo',('provider.invalid',443,0,0,0)),
                       ('sqlite3.connect',('/storage/forbidden.sqlite3',)),('open',('/storage/forbidden','r',0)),
                       ('open',('/etc/forbidden','w',os.O_WRONLY)),('subprocess.Popen',('false',[],None,None))]:
        try:sys.audit(event,*args)
        except Denied:continue
        raise AssertionError('guard negative control failed: '+event)
    note('guard-negative-controls',status='PASS')


def validate_admission(args,out):
    need(INPUT_ROOT.resolve(strict=True)==INPUT_ROOT,'staged root must not redirect')
    admission=args.admission.resolve(strict=True)
    need(admission.is_relative_to(INPUT_ROOT) and admission.stat().st_size<=65536,'bad admission location/size')
    need(re.fullmatch('[0-9a-f]{64}',args.admission_sha256) and sha(admission)==args.admission_sha256,'admission identity changed')
    need(sha(PACKET/'bindings.json')==BINDINGS_SHA256,'packet bindings changed')
    binding=json.loads((PACKET/'bindings.json').read_text());a=json.loads(admission.read_text())
    need(a['schema']==1 and a['synthetic_only'] is True,'synthetic admission required')
    need(a['image_sha256']==binding['accepted_image_sha256'],'unreviewed image')
    need(a['boot_id']==Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'allocation belongs to another boot')
    need(a['ports']==[PROXY_PORT,STUB_PORT],'endpoint allocation differs')
    need(not any(os.environ.get(key) for key in ('LD_PRELOAD','LD_LIBRARY_PATH','LD_AUDIT')),'unqualified native loader override')
    need(set(p.name for p in Path('/sys/class/net').iterdir())=={'lo'},'requires fresh no-NIC VM')
    need(int(Path('/sys/class/net/lo/flags').read_text().strip(),16)&1,'loopback must already be up')
    need(not any(int(row[1].split(':')[1],16) in a['ports'] for row in tcp_listeners()),'allocated endpoint is already occupied; do not stop it')
    need(Path('/proc/net/route').read_text().splitlines()[1:]==[],'unexpected IPv4 route')
    for path,digest in binding['evidence_sha256'].items():need(sha(PACKET/path)==digest,'packet reference changed')
    prepared=(INPUT_ROOT/a['prepared']).resolve(strict=True);need(prepared.is_relative_to(INPUT_ROOT),'source tree escaped staging')
    need(sha(prepared/'source.json')==a['prepared_source_sha256'],'preparation receipt changed')
    source=json.loads((prepared/'source.json').read_text())
    need(source['status']=='PASS' and source['bindings_sha256']==BINDINGS_SHA256 and source['files']==binding['candidate'],'unqualified prepared source')
    tree=prepared/'tree';need(not any(tree.rglob('*.pyc')),'refuse unbound bytecode')
    actual={str(f.relative_to(tree)):sha(f) for f in sorted(tree.rglob('*.py'))}
    need(actual==binding['candidate'],'exact prepared Python composition changed')
    need(sha(prepared/'scanner.py')==binding['evidence_sha256']['evidence/list_jobs.py'],'scanner candidate changed')
    need(sha(prepared/'raofflineproxy-ctl')==binding['evidence_sha256']['evidence/raofflineproxy-ctl'],'ctl candidate changed')
    need(set(a['inputs'])=={'iso','rvz_none','rvz_zstd'},'exact ISO + two independent RVZ inputs required')
    inputs={name:input_file(INPUT_ROOT,row,2*1024*1024) for name,row in a['inputs'].items()}
    need(inputs['iso'].stat().st_size==0x60000 and inputs['iso'].read_bytes()[:6]==b'PX5740','not the public #574 synthetic disc')
    need(re.fullmatch('[0-9a-f]{32}',a['expected_hash']) and a['expected_hash']!='0'*32,'explicit independent hash required')
    manifest=json.loads(input_file(INPUT_ROOT,a['synthetic_manifest'],65536).read_text())
    raw=next(r for r in manifest if r['name']=='synthetic.iso')
    need(raw['bytes']==a['inputs']['iso']['bytes'] and raw['sha256']==a['inputs']['iso']['sha256'] and
         raw['expected']==a['expected_hash'] and raw['console']=='gamecube','synthetic generator manifest differs')
    oracle=a['oracle'];need(oracle['dolphin_pin']==binding['dolphin_pin'],'DolphinTool pin differs')
    result=json.loads(input_file(INPUT_ROOT,oracle['result'],1024*1024).read_text())
    need(result['result']=='PASS' and result['dolphin_sha256']==oracle['dolphin_sha256'],'independent converter proof absent')
    outputs={row['label']:row['output_sha256'] for row in result['cases']}
    for mode in ('none','zstd'):
        need(outputs['encode-'+mode]==a['inputs']['rvz_'+mode]['sha256'],'independent encoder output changed')
        need(outputs['roundtrip-'+mode]==a['inputs']['iso']['sha256'],'full decoded ISO equality not established')
        for label in ('encode-'+mode,'roundtrip-'+mode,'hash-'+mode):
            receipt=json.loads(input_file(INPUT_ROOT,oracle['receipts'][label],1024*1024).read_text())
            need(receipt['returncode']==0 and receipt['timed_out'] is False,'original oracle child did not succeed: '+label)
            expected=oracle['dolphin_sha256'] if not label.startswith('hash-') else result['hash_binary_sha256']
            need(receipt['executable_sha256']==expected,'oracle executable identity differs')
            argv=receipt['argv']
            if label.startswith('hash-'):
                need(argv[1:3]==['1','gamecube'] and Path(argv[3]).name=='dolphin-'+mode+'.rvz','independent hash command differs')
            else:
                need(argv[1]=='convert','not an independent conversion command')
                def option(flag):return argv[argv.index(flag)+1]
                need(option('-f')==('rvz' if label.startswith('encode-') else 'iso'),'oracle output format differs')
                if label.startswith('encode-'):
                    need(option('-b')=='131072' and option('-c')==mode and option('-l')=='3','oracle compression settings differ')
        output=input_file(INPUT_ROOT,oracle['hash_stdout'][mode],1024).read_text()
        need(output==a['expected_hash']+'\n','independent hash output differs')
    need(set(a['libraries'])=={'rchash','zstd','crypto'},'all native identities required')
    for role,row in a['libraries'].items():
        path=Path(row['path']);resolved=path.resolve(strict=True)
        need(path.is_absolute() and resolved.is_relative_to(Path('/usr/lib')),'native library must be installed in /usr/lib')
        need(str(resolved)==row['resolved_path'] and sha(resolved)==row['sha256'],'installed native identity changed: '+role)
        with resolved.open('rb') as stream:header=stream.read(64)
        need(header[:6]==b'\x7fELF\x02\x01' and struct.unpack_from('<H',header,18)[0]==62,'not installed x86-64 ELF64')
    need(a['native_provenance']['image_sha256']==a['image_sha256'],'native provenance belongs to another image')
    need(type(a['native_provenance']['source_pins_verified']) is bool and
         a['native_provenance']['qualification'],'explicit native provenance qualification required')
    if a['native_provenance']['source_pins_verified']:
        provenance=input_file(INPUT_ROOT,a['native_provenance']['build_receipt'],1024*1024)
        need(provenance.stat().st_size>0,'empty native build receipt')
    REPORT.update(admission_sha256=args.admission_sha256,bindings_sha256=BINDINGS_SHA256,
                  source_receipt_sha256=a['prepared_source_sha256'],libraries=a['libraries'],
                  native_provenance=a['native_provenance'],oracle=oracle,python=sys.version,
                  interpreter={'path':sys.executable,'sha256':sha(sys.executable)},boot_id=a['boot_id'])
    REPORT['native_current_source_qualified']=a['native_provenance']['source_pins_verified']
    return a,binding,prepared,inputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission',type=Path,required=True);parser.add_argument('--admission-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();out=args.output.absolute()
    owner=Path('/run/pix583-native-owner')
    need(out.parent.parent==owner and out.parent.resolve(strict=True).parent==owner and owner.resolve(strict=True)==owner and not out.exists() and not out.is_symlink(),'fresh owner payload under /run/pix583-native-owner required')
    mounts=[r.split() for r in Path('/proc/self/mountinfo').read_text().splitlines()]
    need(any(r[4]==str(owner) and r[r.index('-')+1]=='tmpfs' for r in mounts),'coordinator must allocate private scratch tmpfs')
    fs=os.statvfs(owner)
    need(48*1024*1024<=fs.f_bavail*fs.f_frsize and fs.f_blocks*fs.f_frsize<=64*1024*1024,'requires 48MiB free inside <=64MiB scratch tmpfs')
    out.mkdir(mode=0o700);started=time.monotonic();store=None;peer=None
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE,(8*1024*1024,8*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    def expired(*_):raise TimeoutError('180-second native integration deadline')
    signal.signal(signal.SIGALRM,expired);signal.alarm(180)
    previous_hook=threading.excepthook
    def thread_error(args):
        REPORT['thread_errors'].append(str(args.exc_type.__name__)+': '+str(args.exc_value));previous_hook(args)
    threading.excepthook=thread_error
    try:
        admission,binding,prepared,inputs=validate_admission(args,out)
        for name in list(os.environ):
            if name.startswith(('RAOFFLINEPROXY_','LISTEN_')) or name.lower().endswith('_proxy'):
                os.environ.pop(name)
        state=out/'account-state';state.mkdir();home=out/'home';home.mkdir()
        os.environ.update(HOME=str(home),XDG_CONFIG_HOME=str(home/'config'),RAOFFLINEPROXY_CONFIG_DIR=str(state),
                          RAOFFLINEPROXY_CACHE_IMAGES='0',RAOFFLINEPROXY_RCHASH_LIB=admission['libraries']['rchash']['path'])
        cfg={'proxy_host':'127.0.0.1','proxy_port':PROXY_PORT,'upstream_host':f'http://127.0.0.1:{STUB_PORT}',
             'cache_images':False,'upload_logs':False,'retroarch_cfg':str(state/'retroarch.cfg'),
             'rocknix_system_cfg':str(state/'system.cfg'),'ppsspp_ini':str(state/'empty-ppsspp.ini'),
             'dolphin_config_dir':str(state/'empty-dolphin')}
        (state/'config.json').write_text(json.dumps(cfg))
        (state/'retroarch.cfg').write_text(f'cheevos_username = "{USER_A}"\ncheevos_token = "{TOKENS[USER_A]}"\ncontent_history_path = "{state}/content_history.lpl"\n')
        (state/'system.cfg').write_text('# no account or settings from the image\n')
        (state/'content_history.lpl').write_text('{"items":[]}')
        (state/'empty-ppsspp.ini').write_text('[Recent]\n');(state/'empty-dolphin').mkdir()
        protected={str(p):sha(p) for p in (state/'retroarch.cfg',state/'system.cfg',state/'config.json')}
        sys.dont_write_bytecode=True;sys.path.insert(0,str(prepared/'tree/linux'))
        install_guard(out,prepared,admission['libraries'])
        # Only dependency discovery is replaced: the actual CDLL load, exports,
        # hash entrypoints and callbacks remain untouched. No ldconfig/compiler subprocess.
        library_names={'raproxy_rchash':admission['libraries']['rchash']['path'],
                       'zstd':admission['libraries']['zstd']['path'],'crypto':admission['libraries']['crypto']['path']}
        def find_library(name):
            if name not in library_names:raise Denied('unbound library lookup '+name)
            return library_names[name]
        with mock.patch.object(ctypes.util,'find_library',side_effect=find_library):
            from raofflineproxy import auth,award_signing,cache_keys,cache_queue,config,flusher,native_codecs,network,proxy_service,rom_browser,rom_cache,rom_hashing,storage
            need(config.CONFIG_DIR==state and config.DATABASE_FILE==state/'proxy.sqlite3','config escaped synthetic account')
            need(sha(Path(proxy_service.__file__))==binding['candidate']['linux/raofflineproxy/proxy_service.py'],'wrong imported service source')
            native_results={}
            for name,path in inputs.items():
                result=rom_hashing.hash_rom_candidates_result(path)
                native_results[name]={'candidates':result.candidates,'error':result.error,'sha256':sha(path)}
                need(result.error is None and result.candidates==[admission['expected_hash']],'native '+name+' hash differs: '+str(native_results[name]))
            REPORT['native_hashes']=native_results
            need(rom_hashing._LIBRCHASH._name==admission['libraries']['rchash']['path'],'native bridge fallback selected')
            need(native_codecs._zstd_cache is not None,'independent Zstd input did not exercise installed decompressor')
            native_codecs._crypto()  # load/export resolution only; no Wii qualification
            maps=Path('/proc/self/maps').read_text()
            for role,row in admission['libraries'].items():need(row['resolved_path'] in maps,'library absent from actual mappings: '+role)
            (out/'native-maps.txt').write_text(maps)
            note('native-ISO-independent-RVZ',status='PASS',expected=admission['expected_hash'])
            store=storage.Storage();need(store.backend=='sqlite','requires actual SQLite backend')
            REPORT['sqlite_version']=storage.sqlite3.sqlite_version
            # One real scanner->native->cache path, not the completed44-case source probe.
            roms=out/'roms';folder=roms/'gamecube';folder.mkdir(parents=True)
            selected=folder/'independent.rvz';selected.write_bytes(inputs['rvz_zstd'].read_bytes())
            es=out/'es';es.mkdir()
            (es/'es_systems_custom.cfg').write_text(f'<systemList><system><name>gamecube</name><path>{folder}</path></system></systemList>')
            (folder/'gamelist.xml').write_text('<gameList><game><path>./independent.rvz</path><cheevosHash>'+'0'*32+'</cheevosHash></game></gameList>')
            need(not any(p.name.startswith('es_systems_') and p.suffix=='.cfg' for p in Path('/usr/bin').iterdir()),'unexpected installed ES additions; refuse scanner boundary')
            jobs=out/'jobs';previous_argv=sys.argv;buf=io.StringIO();os.environ['RA_SCAN_USER']=USER_A
            try:
                sys.argv=['scanner',str(jobs),'all',str(roms),str(es),'gamecube',str(out/'cursor')]
                with contextlib.redirect_stdout(buf):runpy.run_path(str(prepared/'scanner.py'),run_name='__main__')
            finally:sys.argv=previous_argv
            need(jobs.read_text()=='H\t\t\t'+str(selected)+'\n','scanner did not hand off exactly the failed indexed RVZ')
            note('scanner-native-handoff',stdout=buf.getvalue(),job_sha256=sha(jobs))
            hashes=rom_hashing.hash_rom_candidates_result(selected)
            need(hashes.error is None and hashes.candidates==[admission['expected_hash']],'scanner job native hash differs')
            peer=ProtocolState(admission['expected_hash']);up=upstream(peer)
            credentials={'user':USER_A,'token':TOKENS[USER_A]}
            queued=cache_queue.QueuedRom(hashes.candidates,str(selected),'Synthetic independent RVZ',int(time.time()*1000))
            outcome,gid,message=rom_browser.cache_queued_rom(store,cfg,credentials,'Synthetic #583 fixture',queued,rom_browser.LocalGameIdAnswer(),set())
            need(outcome is rom_browser.QueuedRomOutcome.CACHED and gid==10,'native cache preparation failed: '+str((outcome,gid,message)))
            for key in (cache_keys.game_id(admission['expected_hash']),cache_keys.patch(10,USER_A),cache_keys.unlocks(10,USER_A),cache_keys.achievementsets(admission['expected_hash'],USER_A)):
                need(store.get_cache(key) is not None,'missing prepared cache row '+key)
            # Distinct account cache + next game are public synthetic protocol payloads.
            rom_cache.cache_game(10,admission['expected_hash'],{'user':USER_B,'token':TOKENS[USER_B]},'Synthetic fixture',store,cfg,cache_images=False)
            rom_cache.cache_game(20,'2'*32,credentials,'Synthetic fixture',store,cfg,cache_images=False)
            account_b={key:store.get_cache(key)['responseBody'] for key in (cache_keys.patch(10,USER_B),cache_keys.unlocks(10,USER_B),cache_keys.achievementsets(admission['expected_hash'],USER_B))}
            # No-NIC is the only physical input substituted. Real numeric-loopback
            # HEAD/HTTP and reachability decisions run against the owned peer.
            with mock.patch.object(network,'has_active_network_interface',return_value=True):
                server=start(proxy_service.ProxyRuntimeServer(cfg,store))
                for user in TOKENS:
                    status,_,login=request({'r':'login2','u':user,'t':TOKENS[user]})
                    need(status==200 and login.get('User')==user and login.get('Token')==TOKENS[user],'online synthetic cache sign-in differs')
                stop(up);need(not server.refresh_reachability(force_probe=True),'closed upstream still reachable')
                stop(server)
                class Impostor(BaseHTTPRequestHandler):
                    def log_message(self,*args):pass
                    def do_POST(self):
                        self.rfile.read(int(self.headers.get('Content-Length','0')))
                        data=b'{"Success":true,"User":"unrelated","Token":"<unrelated>"}'
                        self.send_response(200);self.send_header('X-RA-Proxy','1');self.send_header('X-RA-Offline','1');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
                wrong=start(Stub(('127.0.0.1',PROXY_PORT),Impostor))
                try:
                    try:ready()
                    except AssertionError:note('HTTP200-impostor-rejected',status='PASS')
                    else:raise AssertionError('unrelated200 counted as readiness')
                finally:stop(wrong)
                server=start(proxy_service.ProxyRuntimeServer(cfg,store));ready()
                REPORT['service_identity']=socket_identity(server)
                REPORT['service_identity']['source_sha256']=sha(Path(proxy_service.__file__))
                for user,want in ((USER_A,[103]),(USER_B,[104])):
                    status,_,data=request({'r':'unlocks','g':'10','u':user})
                    need(status==200 and data['UserUnlocks']==want,'account cache isolation failed')
                note('offline-account-cache-isolation',status='PASS')
                status,_,data=request({'r':'patch','g':'10','u':'unconfigured-fixture-user'})
                need(status==503 and data.get('Success') is False,'other account received cached patch')
                status,_,data=request({'r':'login2','u':'unconfigured-fixture-user','t':'<unknown>'})
                need(status==503 and data.get('Success') is False,'uncached account received another login')
                for aid in (101,101,102):
                    status,_,data=request({'r':'awardachievement','a':str(aid),'g':'10','u':USER_A,'t':TOKENS[USER_A],'h':'0'})
                    need(status==200 and data.get('Error')=='queued_offline','offline award not queued')
                pending=store.get_pending_awards();need([r['achievementId'] for r in pending]==[101,102],'award dedup/order failed')
                REPORT['queued_signed_rows']=copy.deepcopy(pending)
                peer.queued={row['achievementId']:copy.deepcopy(row) for row in pending}
                peer.secret=config.AWARD_SECRET_FILE.read_bytes();need(len(peer.secret)==32,'synthetic signing secret length')
                previous='genesis'
                for row in pending:
                    payload=hashlib.sha256(f"{row['achievementId']}|{row['queryString']}|{row['requestBody']}|{row['queuedAt']}".encode()).hexdigest()
                    signature=base64.b64encode(hmac.new(peer.secret,(payload+':'+previous).encode(),hashlib.sha256).digest()).decode()
                    need(row['payloadHash']==payload and row['prevHash']==previous and hmac.compare_digest(row['signature'],signature),'independent queue HMAC/chain verification failed')
                    previous=payload
                need(flusher.verify_chain(pending)[0],'product chain verification failed')
                note('offline-signing-and-dedup',status='PASS',submitted=3,retained=2)
                status,_,data=request({'r':'awardachievement','a':'201','g':'20','u':USER_A,'t':TOKENS[USER_A],'h':'1'})
                need(status==403 and store.get_pending_awards()==pending,'hardcore refusal changed queue')
                for user,want in ((USER_A,[101,102,103]),(USER_B,[104])):
                    status,_,data=request({'r':'startsession','g':'10','u':user})
                    need(status==200 and sorted(r['ID'] for r in data['Unlocks'])==want,'pending unlocks crossed account boundary')
                stop(server);store.close();store=storage.Storage()
                need(store.get_pending_awards()==pending,'close/reopen changed pending signed awards')
                note('SQLite-reopen-preserved-queue',status='PASS')
                server=start(proxy_service.ProxyRuntimeServer(cfg,store));ready()
                # A separate synthetic database carries the tamper control.
                tampered=storage.Storage(out/'tampered.sqlite3')
                try:
                    bad=copy.deepcopy(pending[0]);bad['requestBody']+='&tampered=1';tampered.upsert_pending_award(bad)
                    saved=tampered.get_pending_awards();before_calls=len(peer.calls)
                    result=flusher.flush_pending_awards(tampered,cfg)
                    need(result.flushed==0 and result.pending_remaining==1 and result.last_error and tampered.get_pending_awards()==saved and len(peer.calls)==before_calls,'tampered award was sent or removed')
                    note('tamper-refused-before-HTTP',status='PASS',last_error=result.last_error)
                finally:tampered.close()
                up=upstream(peer);need(server.refresh_reachability(force_probe=True),'reconnected numeric peer not reachable')
                for mode,status_expected in (('login401',401),('login403',403)):
                    peer.mode=mode;status,headers,data=request({'r':'login2','u':USER_A,'t':TOKENS[USER_A]})
                    need(status==status_expected and data.get('Success') is False and 'x-ra-offline' not in headers,'auth rejection became cached success')
                note('upstream-auth-rejection-preserved',status='PASS')
                peer.mode='patch500';before=store.get_pending_awards();result=server.flush_pending_awards()
                need(result['flushed']==0 and result['pending_remaining']==2 and store.get_pending_awards()==before and not peer.applied,'patch failure lost/changed pending awards')
                note('patch-failure-retained',status='PASS',outcome=result,rows=store.get_pending_awards())
                immutable=('achievementId','requestBody','queryString','queuedAt','payloadHash','prevHash','signature','signedAt')
                for mode in ('award401','award500'):
                    peer.mode=mode;result=server.flush_pending_awards();after=store.get_pending_awards()
                    need(result['flushed']==0 and result['pending_remaining']==2 and len(after)==2 and not peer.applied,'failed award lost pending data')
                    for old,row in zip(pending,after):
                        need(all(row[k]==old[k] for k in immutable) and row['status']=='pending' and row['lastError'],'signed payload changed on failure')
                        need(row['retryCount']==(1 if mode=='award500' else 0),'retry accounting differs')
                    note(mode+'-retained',status='PASS',outcome=result,rows=after)
                peer.mode='normal';result=server.flush_pending_awards()
                need(result['flushed']==2 and result['pending_remaining']==0 and store.get_pending_awards()==[],'reconnect did not flush exactly2')
                need(peer.applied==[(USER_A,101),(USER_A,102)],'wrong account/duplicate submission')
                award_calls=sum(r['action']=='awardachievement' for r in peer.calls)
                again=server.flush_pending_awards();need(again['total']==0 and sum(r['action']=='awardachievement' for r in peer.calls)==award_calls,'empty flush resubmitted awards')
                need(config.CONFIG_DIR.joinpath('last-flush').read_text().split()[1]=='2','successful flush stamp differs')
                need(all(store.get_cache(k)['responseBody']==v for k,v in account_b.items()),'flush changed other account cache')
                stop(up);need(not server.refresh_reachability(force_probe=True),'final disconnect not detected')
                stop(server);store.close();store=storage.Storage();server=start(proxy_service.ProxyRuntimeServer(cfg,store));ready()
                status,_,data=request({'r':'startsession','g':'10','u':USER_A})
                need(sorted(r['ID'] for r in data['Unlocks'])==[101,102,103],'flushed unlocks not ready after reopen')
                status,_,data=request({'r':'startsession','g':'20','u':USER_A})
                need(data['Unlocks']==[],'pending/previous game contaminated next game')
                need(store._connection.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity failure')
                need({str(p):sha(p) for p in map(Path,protected)}==protected,'synthetic credential/settings inputs changed')
                need(not peer.thread_errors and not REPORT['thread_errors'],'background fixture errors occurred')
                note('reconnect-dedup-next-game',status='PASS',outcome=result)
                stop(server)
            REPORT['status']='PASS'
    except BaseException as error:
        REPORT['status']='FAIL';REPORT['error']=type(error).__name__+': '+str(error)
        raise
    finally:
        # A native hang still needs the allocated external owner deadline. Give
        # Python cleanup a separate bounded interval after any main alarm.
        signal.alarm(10)
        errors=[]
        for server,thread in list(SERVERS):
            try:stop(server)
            except BaseException as error:errors.append(type(error).__name__+': '+str(error))
        if store is not None:
            try:store.close()
            except BaseException as error:errors.append(type(error).__name__+': '+str(error))
        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                try:thread.join(timeout=0.25)
                except BaseException as error:errors.append(type(error).__name__+': '+str(error))
        if peer is not None:
            REPORT['stub_requests']=peer.calls;REPORT['stub_errors']=peer.thread_errors;REPORT['synthetic_applied']=peer.applied
        REPORT['cleanup_errors']=errors;REPORT['elapsed_seconds']=time.monotonic()-started
        try:
            REPORT['remaining_threads']=[t.name for t in threading.enumerate() if t is not threading.main_thread()]
            REPORT['remaining_listeners']=[r[1] for r in tcp_listeners() if int(r[1].split(':')[1],16) in (PROXY_PORT,STUB_PORT)]
            REPORT['retained_bytes']=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
            if REPORT['remaining_threads'] or REPORT['remaining_listeners'] or REPORT['retained_bytes']>64*1024*1024 or errors or REPORT['thread_errors'] or (peer and peer.thread_errors):REPORT['status']='FAIL'
        except BaseException as error:
            REPORT['status']='FAIL';REPORT['observation_error']=type(error).__name__+': '+str(error)
        try:(out/'result.json').write_text(json.dumps(REPORT,indent=2)+'\n')
        except BaseException as error:
            REPORT['status']='FAIL';REPORT['receipt_error']=str(error);print(json.dumps(REPORT),flush=True);raise
        finally:signal.alarm(0)
        print(json.dumps({'status':REPORT['status'],'result':str(out/'result.json')}),flush=True)
    need(REPORT['status']=='PASS','integration fixture failed')


if __name__=='__main__':main()
