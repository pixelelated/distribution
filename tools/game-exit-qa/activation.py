"""Read-only binding to the existing standing slot; no admission or unit control."""
import contextlib,json,os,time
from pathlib import Path
from common import load,parse_utc,sha,verify_inputs
UNIT='pixelelated-m7-functional.service'

@contextlib.contextmanager
def local_user_bus(slot):
 """Only while reading systemd: trusted UID runtime discovery, no inherited bus."""
 runtime=slot.runtime_dir() # Existing canonical UID/owner/0700/non-symlink checks.
 assert os.getuid()==1000 and runtime==Path('/run/user/1000')
 keys=('XDG_RUNTIME_DIR','DBUS_SESSION_BUS_ADDRESS');previous={k:os.environ.get(k) for k in keys}
 os.environ['XDG_RUNTIME_DIR']=str(runtime)
 os.environ.pop('DBUS_SESSION_BUS_ADDRESS',None) # Derive the local user bus; never copy an arbitrary address.
 try:yield
 finally:
  for key,value in previous.items():
   if value is None:os.environ.pop(key,None)
   else:os.environ[key]=value

def validate_activation(o,c,r,a,claim,props,sample,required,request_sha,boot_id,uid,environment,own_cgroup,mono,wall):
 """Pure receipt/readback checks; synthetic tests never acquire a real slot."""
 assert uid==1000 and r['uid']==uid and r['purpose']=='functional'
 assert r['owner']==str(o) and r['checkout']==c['checkout']==r['cwd']
 assert r['admission_path']==str(o/'admission.json')
 expected=[c['tools']['watch'],'--admission',str(o/'admission.json'),'--','/usr/bin/python3','-I','-B',str(o/'code/owner.py'),'--owner',str(o)]
 assert r['argv']==expected,'only exact foreground watched owner is allowed'
 assert 'PIXELELATED_SUBMISSION_OWNER' not in environment,'detached submission environment refused'
 assert environment.get('M7_SLOT_ACTIVATION')==str(o/'slot/activation.json')
 assert a['schema']=='pixelelated.m7-slot.receipt.v1' and a['state']=='ACTIVE' and a['authority']=='standing-functional-systemd'
 assert a['unit']==UNIT==claim['unit']==props['Id']
 assert a['owner']==str(o)==claim['owner'] and claim['state']=='running'
 assert a['nonce']==r['nonce']==claim['nonce'] and props['Description']=='pixelelated-m7:'+r['nonce']
 assert a['activation_id']==claim['invocation_id']==props['InvocationID']==environment.get('INVOCATION_ID')
 assert a['boot_id']==r['boot_id']==claim['boot_id']==boot_id
 assert a['request_sha256']==request_sha==claim['request_sha256'] and claim['request']==str(o/'slot/request.json')
 assert a['command_sha256']==r['command_sha256']
 assert a['source_inputs']==r['inputs'] and all(r['inputs'].get(k)==v for k,v in required.items()),'owner source/config is not fully bound'
 assert a['runtime_seconds']==r['runtime_seconds']==c['slot_seconds']==1800
 assert r['minimum_available_mib']==24576 and a['available_memory_bytes']>=24576*1024**2
 assert a['host_memory_max_bytes']==12*1024**3 and a['cpu_quota_percent']==400 and a['tasks_max']==512
 cg=a['cgroup'];assert cg==claim['cgroup']==props['ControlGroup'] and own_cgroup=='0::'+cg+'\n'
 assert props['LoadState']=='loaded' and props['ActiveState']=='active'
 assert props['KillMode']=='control-group' and props['TimeoutStopUSec']=='15s' and props['SendSIGKILL']=='yes' and props['Delegate']=='no'
 assert props['RuntimeMaxUSec']=='30min' and props['OOMPolicy']=='kill'
 assert sample['exists'] and sample['metrics'] is not None
 for observed in (sample,a['kernel_limits']):
  m=observed['metrics'];quota,period=map(int,m['cpu.max'].split());assert period>0 and quota==4*period
  assert int(m['memory.max'])==12*1024**3 and m['memory.swap.max']=='0' and m['pids.max']=='512'
 began=int(props['ExecMainStartTimestampMonotonic'])/1e6
 assert props['ExecMainStartTimestampMonotonic']==a['systemd']['ExecMainStartTimestampMonotonic']
 assert a['deadline_monotonic']==began+1800 and 0<=mono-began<1800
 assert 0<=wall-parse_utc(a['issued_utc'])<900
 assert abs((parse_utc(a['expires_utc'])-wall)-(a['deadline_monotonic']-mono))<5,'wall/monotonic expiry disagree'
 assert a['deadline_monotonic']-mono>900,'fresh activation required before starting this slice'
 return a

def check_activation(o,c):
 assert __debug__
 assert sha(o/'config.json')==(o/'config.sha256').read_text().strip();verify_inputs(o,c)
 # Load only the exact source already verified above. Reuse its read-only
 # request/registry/unit/cgroup validation, not submit, execute, post or stop.
 slot=load(c['tools']['slot'],'m7_bound_slot')
 path=o/'slot/request.json';digest=sha(path)
 assert digest==json.loads((o/'slot/request-seal.json').read_text())['sha256']
 r=slot.validate_request(path,digest)
 required=dict(c['inputs']);required.update({str(o/rel):h for rel,h in c['owner_files'].items()})
 for p in (o/'config.json',o/'config.sha256'):required[str(p)]=sha(p)
 assert r['inputs'][str(o/'slot/standing-slot.py')]==c['inputs'][c['tools']['slot']]
 claim=slot.Registry(slot.runtime_dir()/'pixelelated-m7-slot').current()
 sd=slot.Systemd()
 with local_user_bus(slot):props=sd.show()
 slot.same_unit(props,claim)
 a=json.loads((o/'slot/activation.json').read_text());sample=sd.sample(a['cgroup'])
 return validate_activation(o,c,r,a,claim,props,sample,required,digest,slot.boot(),os.getuid(),os.environ,Path('/proc/self/cgroup').read_text(),time.monotonic(),time.time())
