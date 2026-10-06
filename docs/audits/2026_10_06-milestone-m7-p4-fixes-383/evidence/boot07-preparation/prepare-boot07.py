from pathlib import Path
import ast, datetime, hashlib, json, shutil, struct, subprocess, socket

repo=Path.cwd();old=Path('/workspace/tmp/pixelelated-m7-boot-qualification-06');new=Path('/workspace/tmp/pixelelated-m7-boot-qualification-07')
assert json.loads((old/'guest-cleanup-verification.json').read_text())['passed']
new.mkdir();(new/'artifacts').mkdir();controls=new/'classifier-controls';controls.mkdir()
for line in (old/'harness.sha256').read_text().splitlines():
    digest,name=line.split('  ',1);p=Path(name)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
    dest=new/p.name;shutil.copy2(p,dest)
    if p.suffix in ('.py','.sh','.json'):
        dest.chmod(dest.stat().st_mode|0o200);dest.write_text(dest.read_text().replace(str(old),str(new)))
shutil.copy2(repo/'.build-runs/classify-guest-pcap.py',new/'classify-guest-pcap.py')
provenance=json.loads((new/'provenance.json').read_text());provenance.update(prepared_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),supersedes_failed=str(old),issue=475,correction='Bounded RFC8200 option/routing extension parsing, strict lengths and fail-closed unknown/fragment protocols. Unchanged image, splash predicate and boot/update exercises. Actual PCAP stays private.')
(new/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
for f in new.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
for f in new.glob('*.sh'):subprocess.run(['bash','-n',str(f)],check=True)

mac=bytes.fromhex('525400524e5b');destmac=bytes.fromhex('525400123456')
def ethernet(kind,body):return destmac+mac+struct.pack('!H',kind)+body
def tcp(port,data=b''):
    return struct.pack('!HHII',12345,port,0,0)+bytes([0x50,0x18])+bytes(6)+data
def udp(port,data=b''):
    return struct.pack('!HHHH',12345,port,8+len(data),0)+data
def v4(proto,data,frag=0):
    h=bytearray(20);h[0]=0x45;h[2:4]=struct.pack('!H',20+len(data));h[6:8]=struct.pack('!H',frag);h[8]=64;h[9]=proto;h[12:16]=socket.inet_pton(socket.AF_INET,'10.0.2.15');h[16:20]=socket.inet_pton(socket.AF_INET,'10.0.2.2')
    return ethernet(0x0800,bytes(h)+data)
def v6(proto,data):
    h=bytes([0x60,0,0,0])+struct.pack('!HBB',len(data),proto,64)+socket.inet_pton(socket.AF_INET6,'fe80::1')+socket.inet_pton(socket.AF_INET6,'ff02::16')
    return ethernet(0x86dd,h+data)
def ext(proto,length=0):return bytes([proto,length])+bytes(6)
def pcap(frames):
    return struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1)+b''.join(struct.pack('<IIII',i+1,0,len(f),len(f))+f for i,f in enumerate(frames))
positive=v4(6,tcp(9045,b'GET /pixelelated-network-positive-control HTTP/1.1\r\n\r\n'))
icmp=v6(0,ext(58)+bytes([143,0,0,0,0,0,0,0]))
dns=struct.pack('!HHHHHH',1,0x100,1,0,0,0)+b'\x06github\x03com\0'+struct.pack('!HH',1,1)
cases=[
 ('hbh-icmp-positive',[positive,icmp],True),
 ('direct-ipv6-positive',[positive,v6(58,bytes([143,0,0,0]))],True),
 ('routing-destination-chain-positive',[positive,v6(43,ext(60)+ext(58)+bytes([143,0,0,0]))],True),
 ('tcp443-behind-two-extensions',[positive,v6(0,ext(60)+ext(6)+tcp(443))],False),
 ('udp443-behind-hbh',[positive,v6(0,ext(17)+udp(443))],False),
 ('dns-behind-destination',[positive,v6(60,ext(17)+udp(53,dns))],False),
 ('truncated-extension-body',[positive,v6(0,ext(58,2)+bytes(4))],False),
 ('truncated-extension-header',[positive,v6(0,bytes([58,0]))],False),
 ('ipv6-fragment',[positive,v6(44,bytes(8)+tcp(443))],False),
 ('unsupported-esp',[positive,v6(50,bytes(8))],False),
 ('ipv4-fragment',[positive,v4(6,tcp(443),0x2000)],False),
 ('invalid-tcp-header',[positive,v6(0,ext(6)+bytes(20))],False),
 ('invalid-udp-length',[positive,v6(0,ext(17)+struct.pack('!HHHH',1,53,500,0))],False),
 ('overlong-extension-chain',[positive,v6(43,ext(43)*8+ext(58)+bytes(4))],False),
 ('no-positive-control',[icmp],False),
 ('direct-ipv4-web',[positive,v4(6,tcp(80))],False)]
rows=[]
def classify(label,path,expected,script=new/'classify-guest-pcap.py'):
    result=subprocess.run(['python3','-I',str(script),str(path),str(controls/(label+'.json'))],text=True,capture_output=True)
    (controls/(label+'.log')).write_text(result.stdout+result.stderr)
    assert (result.returncode==0)==expected,(label,result.returncode,result.stderr)
    rows.append(dict(case=label,expected_pass=expected,returncode=result.returncode,script_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
for label,frames,expected in cases:
    p=controls/(label+'.pcap');p.write_bytes(pcap(frames));classify(label,p,expected)
p=controls/'truncated-record.pcap';p.write_bytes(pcap([positive])[:-1]);classify('truncated-record',p,False)
actual=old/'artifacts/clean-640.pcap'
classify('old-parser-actual-capture',actual,False,old/'classify-guest-pcap.py')
classify('corrected-parser-actual-capture',actual,True)
with (controls/'tcpdump-hbh.log').open('w') as f:
    subprocess.run(['tcpdump','-nn','-r',str(actual),'ip6[6] = 0'],stdout=f,stderr=subprocess.STDOUT,check=True)
report=json.loads((controls/'corrected-parser-actual-capture.json').read_text())
assert report['ipv6_extensions']=={'0':12} and report['passed']
(controls/'verification.json').write_text(json.dumps(dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),controls=rows,all_expected_outcomes=True,actual_capture_sha256=hashlib.sha256(actual.read_bytes()).hexdigest(),actual_capture_private=True,rfc='https://www.rfc-editor.org/rfc/rfc8200.html#section-4.3'),indent=2)+'\n')
(new/'harness.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f)+'\n' for f in sorted(new.iterdir()) if f.is_file() and f.name!='harness.sha256'))
dest=repo/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/boot07-preparation';dest.mkdir()
for f in new.iterdir():
    if f.is_file():shutil.copy2(f,dest/f.name)
shutil.copytree(controls,dest/'classifier-controls',ignore=lambda d,n:[x for x in n if x.endswith('.pcap')])
shutil.copy2(repo/'.build-runs/prepare-boot07.py',dest/'prepare-boot07.py')
(dest/'sha256.json').write_text(json.dumps({str(f.relative_to(dest)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(dest.rglob('*')) if f.is_file()},indent=2)+'\n')
print('PASS',len(rows),'positive/negative parser observations, actual closed capture, independent tcpdump; fresh boot07 sealed and unsubmitted')
