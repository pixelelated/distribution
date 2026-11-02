#!/usr/bin/env python3
"""Hash only the explicitly authorized retained final producer receipts."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent
ROOT=Path('/workspace/tmp/m6-t39/final-4eb5dfab8e74')
rows=[];summaries=[]
for f in sorted(ROOT.rglob('*')):
 if f.is_symlink():continue
 if not f.is_file():continue
 rel=f.relative_to(ROOT)
 allowed=(len(rel.parts)==1 and (f.name=='results.json' or f.suffix=='.out')) or (rel.parts[0] in ('normal','withheld-findings') and ((len(rel.parts)==2 and f.suffix=='.out') or (len(rel.parts)==3 and rel.parts[1]=='steps' and f.suffix in ('.txt','.json','.tsv'))))
 if not allowed:continue
 raw=f.read_bytes();text=raw.decode();rows.append({'path':str(rel),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 if f.suffix=='.out':
  summaries.append({'path':str(rel),'first_line':text.splitlines()[0] if text else '',
   'rc':re.findall(r'^rc=(\d+)$',text,re.M),'total':re.findall(r'^TOTAL: .+$',text,re.M),
   'status_lines':[l for l in text.splitlines() if l.startswith(('PASS','FAIL','box-check:','register-check:','work-log','CONTROL','55 screen','forbidden-terms-check:','ok    '))]})
result=json.loads((ROOT/'results.json').read_text())
data={'kind':'retained producer receipts; read only, not rerun; separate from immutable merge packet',
 'root':str(ROOT),'recorded_results':result,'files':rows,'out_summaries':summaries}
(P/'final-receipts.json').write_text(json.dumps(data,indent=2)+'\n')
print('receipt files',len(rows),'total bytes',sum(r['bytes'] for r in rows))
for r in rows:
 if r['path'] in ['results.json','normal/harness.out','withheld-findings/harness.out','record-check.out','forbidden.out']:print(r)
print('nonzero output return codes',[r for r in summaries if r['rc']!=['0'] and not r['path'].endswith('inodes.out')])
