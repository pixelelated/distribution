from pathlib import Path
import hashlib,json,datetime,runpy,struct
old=Path('/tmp/pixelelated-cleanup-runtime-01');new=Path('/tmp/pixelelated-cleanup-runtime-02');new.mkdir()
helper='''def classify(h):
    if h[:4] != b"\\x7fELF": return None
    if len(h) < 20: return {"kind": "opaque-ELF-fixture", "reason": "short header", "elf_type": None}
    if h[4] not in (1,2): return {"kind": "opaque-ELF-fixture", "reason": "invalid class", "elf_type": None}
    if h[5] not in (1,2): return {"kind": "opaque-ELF-fixture", "reason": "invalid byte order", "elf_type": None}
    return {"kind": "ELF-header", "elf_type": int.from_bytes(h[16:18], "little" if h[5]==1 else "big")}
'''
(new/'elf-header.py').write_text(helper);classify=runpy.run_path(str(new/'elf-header.py'))['classify']
fixture=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement03/build.pixelelated-GENERIC_X64.x86_64/build/pypackaging-26.3/tests/manylinux/hello-world-invalid-data').read_bytes()
old_rejected=False
try:assert fixture[5] in (1,2)
except AssertionError:old_rejected=True
assert old_rejected and classify(fixture[:20])['kind']=='opaque-ELF-fixture'
controls=[('real-invalid-data',fixture[:20],None),('truncated-ELF',b'\x7fELF'+b'\0'*8,None),('invalid-class',b'\x7fELF\0\1'+b'\0'*14,None)]
for label,cls,endian,kind in [('ELF32little',1,1,2),('ELF64little',2,1,3),('ELF32big',1,2,2),('ELF64big',2,2,3)]:
 h=b'\x7fELF'+bytes([cls,endian])+b'\0'*10+kind.to_bytes(2,'little' if endian==1 else 'big')+b'\0'*2;controls.append((label,h,kind))
for label,h,kind in controls:assert classify(h)['elf_type']==kind,label
assert classify(b'plain text') is None
(new/'classifier-controls.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_actual_fixture_rejects':old_rejected,'actual_fixture_sha256':hashlib.sha256(fixture).hexdigest(),'controls':[x[0] for x in controls]+['non-ELF'],'count':8,'all_pass':True,'scope':'Header classification only; opaque malformed fixtures are retained by the copier, not validated or executed'},indent=2)+'\n')
s=(old/'preserve.py').read_text().replace('issue-456-runtime-01','issue-456-runtime-02')
s=s.replace("checked=set();summaries=[]", "checked=set();summaries=[]\nimport runpy\nclassify=runpy.run_path(str(out/'elf-header.py'))['classify']\nfailed_objects=Path('/workspace/artifacts/pixelelated-build-custody/issue-456-runtime-01/objects')")
a="   if len(h)<20 or h[:4]!=b'\\x7fELF':continue\n   assert h[5] in (1,2),str(p)\n   kind=int.from_bytes(h[16:18],'little' if h[5]==1 else 'big')\n   if kind not in (2,3) and not (kind==1 and name.endswith(('.ko','.debug'))):continue\n   digest=sha(p);dest=prior/digest if (prior/digest).is_file() else objects/digest"
b="   classification=classify(h)\n   if classification is None:continue\n   kind=classification['elf_type']\n   if classification['kind']!='opaque-ELF-fixture' and kind not in (2,3) and not (kind==1 and name.endswith(('.ko','.debug'))):continue\n   digest=sha(p);dest=next((base/digest for base in [prior,failed_objects] if (base/digest).is_file()),objects/digest)"
assert a in s;s=s.replace(a,b).replace("'elf_type':kind})","'elf_type':kind,'classification':classification})")
(new/'preserve.py').write_text(s)
for name in ['run.sh','outer.sh','source-inventory.py']:(new/name).write_text((old/name).read_text().replace('cleanup-runtime-01','cleanup-runtime-02'))
(new/'harness.sha256').write_text(''.join(hashlib.sha256((new/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in ['source-inventory.py','preserve.py','elf-header.py','classifier-controls.json','run.sh','outer.sh']))
print('PASS old fixture rejects;8 new controls; fresh runtime02 prepared')
