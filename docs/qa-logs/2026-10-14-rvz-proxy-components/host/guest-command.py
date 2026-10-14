from pathlib import Path
import argparse,subprocess,json,time,re,uuid
p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--file',type=Path,required=True);p.add_argument('--limit',type=int,default=90);a=p.parse_args();r=Path(__file__).parent;d=r/a.name;d.mkdir();tag='PIX_RC_'+uuid.uuid4().hex;cmd='( '+a.file.read_text().strip()+'\n ); pxrc=$?; printf "\\n'+tag+':%s\\n" "$pxrc"';assert len(cmd.encode())<3900
(d/'command.txt').write_text(cmd+'\n');result={'rc':1,'started':time.time()}
try:
 c=subprocess.run(['/workspace/repos/rocknix.worktrees/m7-player-setup/tools/vm-serial','--socket',str(r/'vm/serial.sock'),'--timeout',str(a.limit),'sh',cmd],capture_output=True,text=True,timeout=a.limit+10)
 (d/'stdout').write_text(c.stdout);(d/'stderr').write_text(c.stderr);matches=re.findall(r'^'+tag+r':([0-9]+)\r?$',c.stdout,re.M);result.update(transport_rc=c.returncode,guest_rc=int(matches[0]) if len(matches)==1 else None);print(c.stdout,flush=True)
 assert c.returncode==0 and result['guest_rc']==0,result;result['rc']=0
finally:
 result['ended']=time.time();(d/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
