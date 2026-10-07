#!/usr/bin/env python3
"""Executable controls for the artifact sweep; synthetic tokens are never printed."""
import argparse,hashlib,importlib.machinery,json,os,re,shlex,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--scanner',type=Path,required=True);p.add_argument('--patterns',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
m=importlib.machinery.SourceFileLoader('artifact_scan',str(a.scanner)).load_module()
line,=[x for x in a.patterns.read_text().splitlines() if x.startswith('SECRET_PATTERNS=')]
patterns=re.compile(shlex.split(line)[0].split('=',1)[1].encode());results=[]
def check(name,value):
 results.append({'case':name,'pass':bool(value)});assert value,name
with tempfile.TemporaryDirectory(prefix='pixelelated-sweep-controls-') as temp:
 parent=Path(temp);root=parent/'image';root.mkdir();path=root/'proof.txt'
 allow={'branding':[],'public_patterns':[]}
 def scan():return m.scan(root,allow,patterns)
 path.write_bytes(b'pixelelated release')
 check('clean input passes',scan()['pass'])
 path.write_bytes(b'The old product is ROCKNIX.')
 check('unclassified old product text fails',not scan()['pass'])
 context,=m.contexts(path.read_bytes())
 allow['branding']=[{'path':'proof.txt','context_sha256':context,'disposition':'KEEP'}]
 check('reviewed exact context passes',scan()['pass'])
 path.write_bytes(b'The old product is ROCKNIX with changed unreviewed words.')
 check('changed text is not covered by prior approval',not scan()['pass'])
 context,=m.contexts(path.read_bytes());allow['branding']=[{'path':'proof.txt','context_sha256':context,'disposition':'FIX','issue':416}]
 check('known unresolved defect still fails',not scan()['pass'])
 allow['branding']=[];path.write_bytes(('AK'+'IA'+'Z'*16).encode())
 assert patterns.search(path.read_bytes())
 check('credential injection fails',not scan()['pass'])
 allow['public_patterns']=[{'path':'proof.txt','file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'matches':1}]
 check('exact reviewed public-pattern file passes',scan()['pass'])
 path.write_bytes(path.read_bytes()+b' changed')
 check('changed public-pattern file fails',not scan()['pass'])
 outside=parent/'host-data';path.rename(outside);(root/'absolute-link').symlink_to(outside)
 report=scan();check('absolute guest link is recorded, never followed',report['pass'] and report['counts']['symlinks']==1 and report['counts'].get('credential_pattern_matches',0)==0)
 path.write_bytes(b'unreadable');path.chmod(0)
 try:
  try:scan()
  except (OSError,RuntimeError):refused=True
  else:refused=False
  check('unreadable input refuses a verdict',refused)
 finally:path.chmod(0o600)
a.output.write_text(json.dumps({'passed':len(results),'failed':0,'results':results,'scanner_sha256':hashlib.sha256(a.scanner.read_bytes()).hexdigest(),'patterns_sha256':hashlib.sha256(a.patterns.read_bytes()).hexdigest()},indent=2)+'\n')
print('PASS',len(results),'artifact sweep controls; no matching value printed')
