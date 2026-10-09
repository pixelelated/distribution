from pathlib import Path
import hashlib,json,tarfile,datetime,shutil
R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');D=R/'docs/qa-logs/2026-10-09-notice-scope';D.mkdir(exist_ok=True)
old=R/'docs/qa-logs/2026-10-08-source-custody/git-complete/licence-basis.json'
m=json.loads(old.read_text());row=next(x for x in m['components'] if x['component']=='glsl-shaders');original=json.loads(json.dumps(row))
sha='2607e40d468e31ea5bb96e557db8dbbaada683afec189523a7b9d31ef57ed296'
archive=Path('/workspace/artifacts/pixelelated-release-sources/m7-archives-a7022b76da76a9f6771bb7693d6f6e25854c6731db0750bb46dde29f14d49fce/archives')/sha
h=hashlib.sha256(archive.read_bytes()).hexdigest();assert h==sha
notices=[];top=[]
with tarfile.open(archive) as t:
 for member in t:
  rel='/'.join(member.name.split('/')[1:])
  if member.isfile() and '/' not in rel:top.append(rel)
  if member.isfile() and ('licen' in Path(rel).name.lower() or 'copying' in Path(rel).name.lower()):
   data=t.extractfile(member).read();digest=hashlib.sha256(data).hexdigest();(D/digest).write_bytes(data);notices.append({'relative_path':rel,'archive_member':member.name,'bytes':len(data),'sha256':digest})
assert any(n['relative_path']=='nnedi3/LICENSE' and n['sha256']==row['notice_evidence'][0]['sha256'] for n in notices)
assert not any('/' not in n['relative_path'] for n in notices)
row['observed_licence_basis']='LGPL-3.0 text located in nnedi3/LICENSE only; collection-wide basis not established'
row['scope_and_remaining_work']='The earlier root-licence description was wrong: its retained evidence is nnedi3/LICENSE. Do not extend that notice to the complete shader collection. Review exact per-file/subdirectory notices and their installed scope.'
row['correction_evidence']='docs/qa-logs/2026-10-09-notice-scope/archive-review.json'
m['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();m['supersedes']={'path':str(old.relative_to(R)),'sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'correction':'GLSL notice scope only; original sealed record remains unchanged'}
m['components_without_aggregate_basis']=['common-shaders','glsl-shaders','retropie-shaders','slang-shaders','rocknix-abl']
m['components_with_identified_root_or_scoped_basis']=13
(D/'licence-basis-corrected.json').write_text(json.dumps(m,indent=2)+'\n')
review={'utc':m['utc'],'component':'glsl-shaders','profile':'h70002-aarch64','pinned_source':'4f4eb801b2dbcaed0a9669a9deec1a098f3623d8','archive_sha256':sha,'archive_bytes':archive.stat().st_size,'top_level_regular_files':sorted(top),'notice_filename_members':notices,'prior_record':original,'correction':'Nested LGPL text was incorrectly described as a root licence. No collection-wide basis established. This filename census is not a complete per-file licence assessment.','component_count_note':'13 components have some root or scoped basis, not13 cleared components; five lack an established aggregate basis. All release dispositions remain open.','original_packet_changed':False,'firmware_changed':False}
(D/'archive-review.json').write_text(json.dumps(review,indent=2)+'\n');shutil.copyfile(__file__,D/'review.py')
print('Verified exact archive; corrected nested notice scope; retained',len(notices),'notice files')
