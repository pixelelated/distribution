#!/usr/bin/env python3
"""New S1 metadata contract derived only from accepted immutable D records."""
import collections,functools,hashlib,json,os,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
AUDIT=str(ROOT.relative_to(pathlib.Path.cwd()))
D='676115271e9bbaa9e8db81f6de73a7b49094c5b4'
AUTH='https://github.com/pixelelated/distribution/issues/690#issuecomment-6590563116'
OWNER_IDS={'devices-unshipped':'T25 #672','image-packages':'T8 #655','emulators-standalone':'T30 #677','packages-dead-ends':'T23 #670','device-generic-x64-and-kernel':'T11 #658'}
def sha(b):return hashlib.sha256(b).hexdigest()
class Inputs:
 def __init__(self):
  assert set(os.sched_getaffinity(0))<=set(range(8,24))
  self.tree={}
  for line in subprocess.check_output(['git','ls-tree','-rz',D,'--',AUDIT]).split(b'\0'):
   if not line:continue
   meta,path=line.decode().split('\t',1);mode,kind,oid=meta.split()
   self.tree[path.removeprefix(AUDIT+'/')]={'mode':mode,'type':kind,'blob':oid}
  self.used={}
 @functools.lru_cache(None)
 def bytes(self,path):
  b=subprocess.check_output(['git','cat-file','blob',self.tree[path]['blob']])
  self.used[path]={**self.tree[path],'stored_sha256':sha(b),'stored_bytes':len(b)}
  return b
 def read(self,path):return json.loads(self.bytes(path))
 def binding(self,path):
  self.bytes(path)
  return {'path':path,'commit':D,**self.used[path]}
def mechanism(p,limits,positive):
 if positive:return 'Retain this exact consumer result and its offset/fuzz qualification; no new applicability or runtime claim. Other open consumers remain open.'
 actions=[]
 if any('SHA256 does not match' in x for x in limits):actions.append('Existing owner must identify an exact input matching the recorded recipe URL/pin and expected SHA256; the mismatching candidate is not eligible.')
 if any('absent' in x for x in limits):actions.append('Existing owner must first supply an authorized exact-source identity for '+p['name']+' at '+p['pin']+'; no fetch or archive qualification is authorized by this records-only stream.')
 if any('checksum' in x or 'no archive SHA256' in x or 'lacks archive SHA256' in x for x in limits):actions.append('A separate source-owner qualification must bind the exact Git/submodule revision and archive/content integrity; no checksum is inferred from a filename.')
 if any('post_unpack' in x or 'custom unpack' in x or 'overlay' in x for x in limits):actions.append('A separately scoped source-owner proof must establish the exact transformation inputs/preimage: '+'; '.join(x for x in limits if 'post_unpack' in x or 'custom unpack' in x or 'overlay' in x)+'. Do not execute the recipe/config here.')
 assert actions,limits
 actions.append('Only after all named inputs bind may a separately authorized normal source application establish a new consumer result; runtime correctness remains separate.')
 return ' '.join(actions)
def contract():
 s=Inputs();original=s.read('stage-b/open-inputs.json')
 assert sha(s.bytes('stage-b/open-inputs.json'))=='33f6fa2d74055d63a2ede951e8c8ba58473d36109921edf83d149c5fb35aaa3c'
 plans=s.read('stage-b/plans.json');out={}
 for row in original:
  path=row['path'];consumers=[]
  for p in plans:
   if path not in p['native_paths']:continue
   f='stage-b/application-overlay/'+p['id']+'.json'
   if f not in s.tree:f='stage-b/application/'+p['id']+'.json'
   report=s.read(f);matches=[x for x in report.get('rows',[]) if x['path']==path]
   if report['status']=='open-item':
    assert not matches and report['limits'];status='open-item';limits=report['limits'];normal=None;positive=False
   else:
    assert len(matches)==1
    result=matches[0];assert result['normal_called'] and result['normal']['exit']==0 and result['promoted']
    status=result['status'];assert status in ('applies','offset','fuzz');limits=[];positive=True
    normal={k:result['normal'][k] for k in ('exit','stdout_sha256','stderr_sha256')}
   consumers.append({'group':p['id'],'consumer':p['consumer'],'recipe':p['recipe'],'recipe_owner':p['owner'],'owner_issues':[OWNER_IDS[x] for x in p['owner']],'pin':p['pin'],'url':p['url'],'expected_sha256':p['expected_sha256'],'plan_binding':s.binding('stage-b/plans.json'),'evidence':s.binding(f),'status':status,'source_input_status':'qualified-at-D' if positive else 'open','missing_inputs':limits,'retained_normal_result':normal,'next_qualification_mechanism':mechanism(p,limits,positive)})
  assert consumers and any(x['status']=='open-item' for x in consumers)
  out[path]={k:row[k] for k in ('owner','application','receipts')}
  out[path].update(source_input_status='open',custody_outcome='recorded; source gap remains open',original_binding=s.binding('stage-b/open-inputs.json'),mixed=any(x['status']!='open-item' for x in consumers),consumers=consumers)
 counts=collections.Counter(v['owner'].split(':',1)[0] for v in out.values())
 assert dict(counts)=={'T25 #672':9,'T11 #658':72,'T30 #677':3,'T23 #670':7,'T8 #655':2},counts
 assert len(out)==93 and sum(x['mixed'] for x in out.values())==6
 return {'schema_version':1,'authority':AUTH,'accepted_at':D,'qualification':'Outcome custody only. All93 input gaps remain open:87 wholly open and6 mixed; no new source application or owner action.','outcomes':out},s.used
