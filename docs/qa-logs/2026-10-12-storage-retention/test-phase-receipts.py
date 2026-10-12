"""Exercise actual verify/apply sequencing; mock process readback and stop before deletion."""
from pathlib import Path
import importlib.util,json,shutil,sys,tempfile
SOURCE=Path(__file__).with_name('execute.py')
class BeforeDeletion(Exception):pass
def exercise(source,mutated):
 with tempfile.TemporaryDirectory(prefix='pixelelated-phase-receipt-') as temporary:
  root=Path(temporary);(root/'artifacts').mkdir()
  text=source.read_text()
  if mutated:text=text.replace("'apply-preflight' if args.apply else 'verify-preflight'","'preflight'")
  local=root/'execute.py';local.write_text(text);shutil.copyfile(source.with_name('guards.py'),root/'guards.py');(root/'seal.json').write_text('{}\n')
  spec=importlib.util.spec_from_file_location('phase_test',local);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  m.validate=lambda plan,owner:None # Preservation is exercised by the separate full validation receipt.
  phase=[0]
  def live(targets,owner,label):
   m.g.write(owner/'artifacts'/(label+'-live.json'),{'fixture':True,'phase':phase[0]})
   if phase[0]==1:raise BeforeDeletion()
  m.g.live_check=live
  argv=sys.argv
  try:
   sys.argv=[str(local)];m.main();phase[0]=1;sys.argv=[str(local),'--apply']
   try:m.main()
   except BeforeDeletion:pass
   else:raise AssertionError('apply did not stop before mutation')
  finally:sys.argv=argv
  assert sorted(p.name for p in (root/'artifacts').iterdir())==['apply-preflight-live.json','verify-preflight-live.json']
exercise(SOURCE,False)
try:exercise(SOURCE,True)
except FileExistsError:pass
else:raise AssertionError('old shared-receipt mutation was accepted')
print(json.dumps({'result':'PASS','controls':['actual verify-only then apply keeps two exclusive receipts','old shared-receipt mutation fails as expected'],'process_check_mocked':True,'stopped_before_deletion':True,'production_targets_changed':False},indent=2))
