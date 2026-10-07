from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,subprocess
repo=Path.cwd();old=Path('/workspace/tmp/pixelelated-m7-p4-empty-library-02');extra=Path('/workspace/tmp/pixelelated-m7-p4-extra-fixes-01');matrix=Path('/workspace/tmp/pixelelated-m7-p4-build16-installed-matrix-01');owner=Path('/workspace/tmp/pixelelated-m7-p4-build16-supplemental-01')
assert not owner.exists();owner.mkdir(mode=0o700)
s=(old/'run.py').read_text().replace('m7-pixelelated-replacement15','m7-pixelelated-replacement16').replace('ed5a6a51f5974deec8748fbf0dbd2f4984b690f5','ee014909137e03706e0b3020b8396be589aaa705');ast.parse(s);(owner/'run.py').write_text(s)
s=(old/'extra-boundaries.py').read_text();start=s.index('  cases = ');end=s.index('  for name,action in cases:',start)
prior=(extra/'extra-boundaries.py').read_text();a=prior.index('  cases=');b=prior.index('  for name,action in cases:',a)
s=s[:start]+prior[a:b]+s[end:];ast.parse(s);(owner/'extra-boundaries.py').write_text(s)
(owner/'verify-inputs.py').write_bytes((matrix/'verify-inputs.py').read_bytes())
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'prepared_only':True,'scope':'Renew ten existing installed audit criteria on candidate16: unreadable active sibling, record/marker write failures and retry, actual closed endpoint, three predecessor partial-pointer recoveries, and three empty-local supported-membership cases.','parents':[str(old),str(extra)],'fixture':'Preserve the corrected empty bind-mount observer from empty-library02, including exact original directory-list restoration. Other case functions are unchanged.','reason':'The85 matrix does not include these supplemental acceptance boundaries; their prior installed evidence was candidate15, and candidate16 changed migration and content-scanner code.','sequence':'After root-reasons1280 and verified cleanup, before connection-recovery UI640/1280.','installed_scripts_replaced':False,'source_tree':'/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16'},indent=2)+'\n')
manifest=Path('/workspace/tmp/pixelelated-m7-replacement-16/inputs.json');inputs=json.loads(manifest.read_text());assert inputs['distribution_commit']=='ee014909137e03706e0b3020b8396be589aaa705'
seals={str(manifest):hashlib.sha256(manifest.read_bytes()).hexdigest()};seals.update(inputs['qa_source_files'])
for p in sorted(owner.iterdir()):
 if p.is_file():seals[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(owner/'seal.json').write_text(json.dumps(seals,indent=2)+'\n')
# Verify case function equality against the already qualified corrected observer.
old_ast=ast.parse((old/'extra-boundaries.py').read_text());new_ast=ast.parse(s)
def methods(t):return {node.name:ast.dump(node,include_attributes=False) for cls in t.body if isinstance(cls,ast.ClassDef) for node in cls.body if isinstance(node,ast.FunctionDef) and node.name!='run_cases'}
assert methods(old_ast)==methods(new_ast)
print(owner,len(seals),'sealed inputs;10existing cases, corrected empty-mount fixture unchanged')
