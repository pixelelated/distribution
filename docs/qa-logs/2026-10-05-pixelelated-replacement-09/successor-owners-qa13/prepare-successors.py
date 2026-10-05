from pathlib import Path
import ast,datetime,hashlib,json,subprocess
base=Path('/workspace/tmp');record=base/'pixelelated-m7-continuation-owners-01'
assert not record.exists()
pairs=[('boot-qualification-03','boot-qualification-04'),('image-10','image-11'),
 ('sweep-07','sweep-08'),('settings-09','settings-10'),('link-09','link-10'),
 ('guest-09','guest-10'),('runtime-10','runtime-11'),('proxy-08','proxy-09'),
 ('optins-08','optins-09'),('memory-08','memory-09'),('ui-10','ui-11'),
 ('predecessor-06','predecessor-07'),('subset-05','subset-06'),
 ('cloud-ui-04','cloud-ui-05'),('signin-ui-04','signin-ui-05'),('signin-1g-04','signin-1g-05')]
mapping={str(base/('pixelelated-m7-'+a)):str(base/('pixelelated-m7-'+b)) for a,b in pairs}
mapping[str(base/'pixelelated-m7-qa-11')]=str(base/'pixelelated-m7-qa-13')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((base/'pixelelated-m7-qa-13/completion.json').read_text())
assert receipt['actual_tool_rc']==0 and receipt['qemu_absent'] and all(v==0 for v in receipt['result_channels'].values())
plans=[]
for oldname,newname in pairs:
 old=base/('pixelelated-m7-'+oldname);new=base/('pixelelated-m7-'+newname);assert not new.exists()
 if oldname!='boot-qualification-03':
  for name in ['qa.start','start','inner.rc','outer.rc','tool-wrapper.rc']:assert not (old/name).exists(),(old,name)
 members=[]
 for line in (old/'harness.sha256').read_text().splitlines():
  wanted,filename=line.split(None,1);src=Path(filename);assert sha(src)==wanted,src
  data=src.read_bytes()
  if src.suffix in {'.py','.sh','.json','.steps','.txt'}:
   text=data.decode()
   for before,after in mapping.items():text=text.replace(before,after)
   if src.suffix=='.py':ast.parse(text)
   data=text.encode()
  members.append((src,data))
 plans.append((old,new,members))
record.mkdir();rows=[]
for old,new,members in plans:
 new.mkdir();(new/'artifacts').mkdir()
 for src,data in members:
  dst=new/src.name;dst.write_bytes(data)
  dst.chmod(0o755 if src.suffix=='.sh' else 0o644)
  if dst.suffix=='.sh':subprocess.run(['bash','-n',str(dst)],check=True)
 provenance={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_owner':str(old),
  'new_owner':str(new),'old_harness_sha256':sha(old/'harness.sha256'),'qa_dependency':'/workspace/tmp/pixelelated-m7-qa-13',
  'assertions_unchanged':True,'mapping':mapping,'state':'UNSTARTED','issue':441}
 (new/'successor-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
 sources=sorted(p for p in new.iterdir() if p.is_file())
 (new/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in sources))
 for p in sources:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
 (new/'harness.sha256').chmod(0o400)
 assert (new/'artifacts').is_dir()
 rows.append({'owner':str(new),'source_owner':str(old),'members':len(sources),'harness_sha256':sha(new/'harness.sha256')})
# Re-read every sealed member and ensure no old runtime dependency remains.
for row in rows:
 owner=Path(row['owner'])
 for line in (owner/'harness.sha256').read_text().splitlines():
  wanted,filename=line.split(None,1);p=Path(filename);assert sha(p)==wanted
  if p.suffix in {'.py','.sh'}:
   for old in mapping:assert old not in p.read_text(),(p,old)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'owners':rows,
 'qa13_completion_sha256':sha(base/'pixelelated-m7-qa-13/completion.json'),'original_owners_unchanged':True}
(record/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'owners':len(rows),'sealed_members':sum(r['members'] for r in rows),'record':str(record/'manifest.json')}))
