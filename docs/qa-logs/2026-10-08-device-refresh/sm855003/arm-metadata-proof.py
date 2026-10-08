from pathlib import Path
import datetime,hashlib,json,struct
old=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01/build.pixelelated-SM8550.arm/image/system');new=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-02/build.pixelelated-SM8550.arm/image/system');rows=[]
def sections(b):
 assert b[:6]==b'\x7fELF\x01\x01'
 off=struct.unpack_from('<I',b,32)[0];ents,num,names=struct.unpack_from('<HHH',b,46)
 entries=[struct.unpack_from('<10I',b,off+i*ents) for i in range(num)];s=entries[names];strings=b[s[4]:s[4]+s[5]]
 return {strings[e[0]:].split(b'\0',1)[0].decode():(e[4],e[5],e[1]) for e in entries}
for n,times in [('usr/bin/box86',(b'09:27:05',b'21:51:19')),('usr/lib/libretro/pcsx_rearmed32_libretro.so',(b'09:21:19',b'21:51:16'))]:
 a=(old/n).read_bytes();b=(new/n).read_bytes();sa=sections(a);sb=sections(b);assert sa==sb
 changed=[]
 for name,(off,size,typ) in sa.items():
  if typ!=8 and a[off:off+size]!=b[off:off+size]:changed.append(name)
 an=bytearray(a);bn=bytearray(b)
 if '.note.gnu.build-id' in sa:
  off,size,_=sa['.note.gnu.build-id'];an[off:off+size]=bn[off:off+size]=b'\0'*size
 substitutions=[]
 for before,after in [(b'40f80c5151',b'8b5113fa16'),(b'Oct  7 2026',b'Oct  8 2026'),times]:
  assert len(before)==len(after);count=bn.count(after);assert count and an.count(before)==count;bn=bn.replace(after,before);substitutions.append({'old':before.decode(),'new':after.decode(),'occurrences':count})
 assert an==bn,(n,'nonmetadata differences remain')
 rows.append({'path':n,'old_sha256':hashlib.sha256(a).hexdigest(),'new_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(a),'changed_sections':changed,'normalized_exact_byte_equality':True,'substitutions':substitutions,'build_id_section_ignored':'.note.gnu.build-id' in sa})
D=Path('/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-08-device-refresh/sm855003')
(D/'arm-metadata-delta.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','scope':'The only two changed ARM outputs differ solely by embedded distribution revision/build date/time (no build-ID section is present); actual unnormalized new bytes are separately verified in firmware handoff','entries':rows},indent=2)+'\n')
print('PASS both ARM binary changes are exactly bounded build metadata; all other bytes equal')
