from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
O=Path(__file__).resolve().parent
(O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
 for name,h in json.loads((O/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,name
 rows=[]
 for p in json.loads((O/'profiles.json').read_text()):
  assert hashlib.sha256(Path(p['original_inputs']).read_bytes()).hexdigest()==p['original_inputs_sha256']
  original=json.loads(Path(p['original_inputs']).read_text());bundle=json.loads(Path(p['bundle'],'manifest.json').read_text());assert bundle['inputs']==original
  d=O/'artifacts'/p['name'];print('BEGIN '+p['name'],flush=True)
  assert not json.loads((d/'source-inventory.json').read_text())['errors']
  row={'profile':p['name'],'source_inventory_rc':0,'source_inventory_carried_from':'inventory04 exact sealed successful source report','component_map_rc':None}
  if True:
   proc2=subprocess.run(['python3','-I',str(O/'component-map.py'),'--tree',p['tree'],'--inputs',p['inputs'],'--inventory',str(d/'source-inventory.json'),'--output',str(d/'components.json')]);row['component_map_rc']=proc2.returncode
  rows.append(row);print('END '+p['name']+' '+json.dumps(row),flush=True)
 rc=0 if all(r['source_inventory_rc']==0 and r['component_map_rc']==0 for r in rows) else 1
 (O/'artifacts/result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_INVENTORY_WITH_PUBLICATION_GAPS' if rc==0 else 'INVENTORY_INCOMPLETE','profiles':rows,'scope':'Post-build source/component mapping only; recovered prebuilt archives, Nix/FEX closure, notices and publication-source custody require separate qualification; no RC/publication clearance'},indent=2)+'\n')
finally:
 (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
