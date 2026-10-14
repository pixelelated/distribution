#!/usr/bin/env python3
"""Exact owned-container inspection/retirement; no broad process/container matching."""
import fcntl
import os
from pathlib import Path
import re
import time
from common import absent, command, host_cgroup, identity, read, require, same_process, write

DOCKER=['docker','--host','unix:///var/run/docker.sock']
FORMAT='{"id":{{json .Id}},"state":{{json .State}},"labels":{{json .Config.Labels}},"memory":{{.HostConfig.Memory}},"nano_cpus":{{.HostConfig.NanoCpus}}}'


class DockerOwner:
    def __init__(self, stage, record_dir):
        self.stage=Path(stage);self.meta=read(self.stage/'container-owner.json')
        require(os.stat('/proc/self/ns/pid').st_ino==self.meta['host_pid_namespace'],'wrong host PID namespace')
        self.directory=Path(record_dir);self.directory.mkdir();self.index=0

    def call(self,label,*args,seconds=20):
        self.index+=1
        return command(self.directory/(str(self.index)+'-'+label),DOCKER+list(map(str,args)),seconds)

    def inspect(self,ref):
        code,out,err=self.call('inspect','inspect','--type','container','--format',FORMAT,ref)
        if code:
            if re.fullmatch('[0-9a-f]{64}',ref):missing=absent(code,out.decode(),err.decode(),ref)
            else:
                require(ref==self.meta['name'],'only exact owned name lookup allowed')
                missing=(code==1 and out in (b'',b'\n') and re.fullmatch(
                    r'(?i:(?:error: |error response from daemon: )?no such (?:object|container): )'+re.escape(ref)+r'\n?',err.decode()) is not None)
            require(missing,'Docker inspect failed without exact absence proof')
            return None
        import json
        value=json.loads(out)
        require(re.fullmatch('[0-9a-f]{64}',value['id']) and not err,'malformed inspect response')
        require(value['labels'].get('pix574.owner')==self.meta['nonce']
                and value['labels'].get('pix574.stage')==self.meta['stage'],'container ownership differs')
        if re.fullmatch('[0-9a-f]{64}',ref):require(value['id']==ref,'wrong inspected CID')
        require(value['memory']==4*1024**3 and value['nano_cpus']==2000000000,'container limits differ')
        return value

    def locate(self):
        cidfile=self.stage/'container.cid'
        cid=cidfile.read_text().strip() if cidfile.exists() else ''
        if cid:require(re.fullmatch('[0-9a-f]{64}',cid),'malformed cidfile')
        return self.inspect(cid or self.meta['name'])

    def cleanup(self):
        receipt={'status':'FAIL','forced_stop':False,'started':time.time()}
        lock=(self.stage/'cleanup.lock').open('a')
        try:
            until=time.monotonic()+90
            while True:
                try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
                except BlockingIOError:
                    require(time.monotonic()<until,'cleanup lock deadline');time.sleep(.2)
            initial=self.locate();receipt['initial']=initial
            cid=(initial or {}).get('id')
            if initial:
                if initial['state']['Running']:
                    receipt['forced_stop']=True
                    pid=initial['state']['Pid'];receipt['init_before_stop']=identity(pid)
                    if receipt['init_before_stop'] is not None:
                        group=host_cgroup(pid,cid)
                        receipt['guard_observed']=[x for n in (group/'cgroup.procs').read_text().split() if (x:=identity(int(n))) is not None]
                        receipt['guard_cgroup']=str(group)
                    code,_,_=self.call('stop','stop','--time','10',cid,seconds=25)
                    receipt['stop_original_exit']=code
                    after=self.inspect(cid)
                    if after and after['state']['Running']:
                        code,_,_=self.call('kill','kill',cid);receipt['kill_original_exit']=code
                        require(code==0,'owned container kill failed')
                final=self.inspect(cid)
                if final:
                    require(not final['state']['Running'],'container remains running')
                    receipt['container_terminal_state']=final['state']
                    code,_,_=self.call('remove','rm',cid)
                    require(code==0,'owned container removal failed')
                require(self.inspect(cid) is None,'exact CID still present')
            else:
                cidfile=self.stage/'container.cid'
                cid=cidfile.read_text().strip() if cidfile.exists() else None
            code,out,err=self.call('all-container-ids','ps','-a','--no-trunc','--format','{{.ID}}')
            ids=out.decode().splitlines()
            require(code==0 and not err and all(re.fullmatch('[0-9a-f]{64}',x) for x in ids)
                    and len(ids)==len(set(ids)) and (not cid or cid not in ids),'Docker absence inventory failed')
            receipt['exact_cid']=cid;receipt['exact_id_absent']=True
            observed=self.stage/'observed-host-processes.json'
            originals=read(observed) if observed.exists() else []
            originals+=receipt.get('guard_observed',[])
            survivors=[x for x in originals if same_process(x)]
            receipt['observed_host_processes']=originals;receipt['survivors']=survivors
            require(not survivors,'recorded host container processes survive')
            groupfile=self.stage/'host-cgroup.json'
            if groupfile.exists():
                group=Path(read(groupfile)['path']);members=group/'cgroup.procs'
                receipt['remaining_cgroup_pids']=members.read_text().split() if members.exists() else []
                require(not receipt['remaining_cgroup_pids'],'owned cgroup still populated')
            if receipt.get('guard_cgroup'):
                members=Path(receipt['guard_cgroup'])/'cgroup.procs'
                require(not members.exists() or not members.read_text().split(),'guard-observed cgroup still populated')
            receipt['status']='PASS'
        except BaseException as exc:receipt['error']=repr(exc)
        finally:
            receipt['ended']=time.time();write(self.directory/'cleanup.json',receipt);lock.close()
        return receipt
