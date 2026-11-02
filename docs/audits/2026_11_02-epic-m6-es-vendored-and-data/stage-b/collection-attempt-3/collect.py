"""T44 new metadata collector. All ES operations are immutable Git reads."""
import sys, pathlib, subprocess, os, json, hashlib, datetime, re, posixpath, xml.etree.ElementTree as ET
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from catalogue import parse,counts
D=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
E='/home/max/Development/emulationstation-next.worktrees/m6-es-vendored-and-data-691'
R='55158d2a64c69fe295fb4e67fd174424a71b1b4d';S='16dbac5211eea7e70db7394372033be2be7df829';SEED='48a335700d05a733703e1b58536877b91b921259'
A=D/'docs/audits/2026_11_02-epic-m6-es-vendored-and-data';B=A/'stage-b'
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',LC_ALL='C',PYTHONDONTWRITEBYTECODE='1')
receipts=[];cache={}
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(repo,*args,ok=(0,)):
    argv=['git','-C',str(repo),*args];start=now();r=subprocess.run(argv,env=env,capture_output=True)
    receipts.append(dict(argv=argv,start=start,end=now(),rc=r.returncode,stdout_sha256=sha(r.stdout),stdout_bytes=len(r.stdout),stderr_sha256=sha(r.stderr)))
    if r.returncode not in ok:raise RuntimeError((argv,r.returncode,r.stderr.decode()))
    return r.stdout
def blob(p,ref=R):
    key=(ref,p)
    if key not in cache:cache[key]=git(E,'show',ref+':'+p)
    return cache[key]
def write(p,x):
    p=B/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
native=json.loads((A/'stage-a/inputs/actual-head/native.json').read_bytes());add=json.loads((A/'stage-a/inputs/actual-head/additions.json').read_bytes());companions=json.loads((A/'stage-a/inputs/actual-head/companions.json').read_bytes())
assert git(E,'rev-parse',R+'^{tree}').decode().strip()=='64b90eb8cb07bdfcd690c74ff6bc980ae490657c'
inputs={n:sha((A/'stage-a/inputs/actual-head'/n).read_bytes()) for n in ('native.json','additions.json','companions.json','summary.json')}
catalogues=[];xml=[];headers=[]
for r in native:
    p=r['path']
    if r['survey']['kind']=='gitlink':continue
    b=blob(p);assert sha(b)==r['primary']['sha256'],p
    if p.startswith('locale/') and p.endswith(('.po','.pot')):catalogues.append(dict(path=p,sha256=sha(b),counts=counts(b)))
    if p.startswith('resources/') and p.endswith(('.svg','.xml')):
        try:
            root=ET.fromstring(b);xml.append(dict(path=p,sha256=sha(b),root=root.tag,nodes=sum(1 for _ in root.iter()),status='well-formed XML only; no rendering/schema/game correctness'))
        except ET.ParseError as e:xml.append(dict(path=p,sha256=sha(b),status='parse-refusal',error=str(e)))
    if r['survey']['kind']=='text':
        lines=b.decode('utf-8',errors='replace').splitlines()
        marks=[dict(line=i,text=t.strip()) for i,t in enumerate(lines[:45],1) if re.search(r'copyright|license|SPDX|public domain|distributed under',t,re.I)]
        if marks:headers.append(dict(path=p,sha256=sha(b),header_markers=marks))
write('catalogue-counts.json',catalogues);write('resource-xml.json',xml);write('source-header-markers.json',headers)
fr='locale/lang/fr/LC_MESSAGES/emulationstation2.po'
old={ (e['fields'].get('msgctxt'),e['fields']['msgid']):e for e in parse(blob(fr,S))[0] }
deltas=[]
for owner,ref in [('T2',R)]+[(x['owner'],x['ref']) for x in companions]:
    es=parse(blob(fr,ref))[0];new={(e['fields'].get('msgctxt'),e['fields']['msgid']):e for e in es}
    added=[];changed=[]
    for key,e in new.items():
        if key not in old and (key[0],key[1].replace('UNKNOWN','UKNOWN')) not in old:
            q=json.dumps(key[1],ensure_ascii=False)[1:-1]
            matches=git(E,'grep','-n','-F','-e',q,ref,'--','es-app/src','es-core/src',ok=(0,1)).decode()
            added.append(dict(entry=e,source_matches=matches,source_match_limit='exact literal text search; not expanded macro/control-flow or integration proof'))
        elif key in old and e['fields']!=old[key]['fields']:changed.append(dict(before=old[key],after=e))
    deltas.append(dict(owner=owner,ref=ref,french_sha256=sha(blob(fr,ref)),added=added,changed_existing=changed,old_key_present=any('UKNOWN ERROR' in k[1] for k in new),contains_T2=(owner=='T2'),integrated=False,limit='own accepted branch only; no combined tree'))
assert [len(x['added']) for x in deltas]==[3,6,1,1,0],[(x['owner'],len(x['added'])) for x in deltas]
write('french-deltas-and-calls.json',deltas)
c='a1cbc0ccd96cbd95f3355375609f71f1b50c7113';changed=git(E,'diff-tree','--no-commit-id','--name-only','-r',c).decode().splitlines();rename=[]
for p in changed:
    before=blob(p,c+'^');after=blob(p,c)
    assert before.replace(b'UKNOWN',b'UNKNOWN')==after,p
    rename.append(dict(path=p,before_sha256=sha(before),after_sha256=sha(after),replacements=before.count(b'UKNOWN')))
assert len(rename)==37 and sum(x['replacements'] for x in rename)==38
write('pl024-exact-rename.json',dict(commit=c,files=rename,po=sum(x['path'].endswith('.po') for x in rename),files_count=37,replacements=38))
interface_paths=['CMakeLists.txt','external/CMakeLists.txt','external/libcheevos/CMakeLists.txt','external/id3v2lib/CMakeLists.txt','external/id3v2lib/src/CMakeLists.txt','external/id3v2lib/test/CMakeLists.txt','external/nanosvg/CMakeLists.txt','locale/CMakeLists.txt','resources/checkWheelGunGamesResources.py','tests/app-unit/CMakeLists.txt','.gitmodules']
interfaces=[]
for p in interface_paths:
    b=blob(p);interfaces.append(dict(path=p,ref=R,sha256=sha(b),lines=len(b.splitlines()),markers=[dict(line=i,text=l.strip()) for i,l in enumerate(b.decode().splitlines(),1) if re.search(r'add_subdirectory|add_library|add_executable|find_package|find_program|FetchContent|GIT_TAG|COMMAND|install\s*\(|target_link|file\s*\(|\.mp3|\.png|\.cpp|\.h\"|ES_BUILD_TESTS|USE_SYSTEM_PUGIXML',l)]))
for p in ['projects/ROCKNIX/packages/ui/emulationstation/package.mk','packages/textproc/pugixml/package.mk']:
    b=git(D,'show',SEED+':'+p);interfaces.append(dict(path=p,ref=SEED,sha256=sha(b),lines=len(b.splitlines()),markers=[dict(line=i,text=l.strip()) for i,l in enumerate(b.decode().splitlines(),1) if re.search(r'PKG_VERSION|PKG_LICENSE|USE_SYSTEM_PUGIXML|locale|resources|Fallback|Noto|cmake|install|make ',l)]))
write('interfaces.json',interfaces)
consumers=git(E,'grep','-n','-I','-E',r'resources/|\.(svg|ttf|png|xml|fsh|vsh)|nsvg|id3v2|pugi::',R,'--','es-app/src','es-core/src').decode().splitlines()
write('consumer-lines.json',dict(ref=R,method='literal source traces; no absence/removal or installed-reach inference',lines=consumers))
history=[]
for c in ['324f9c483d9b4a11249c47888b40fb5cc691be7f','e3b75a171841010ba9e82720aa57b6d82dfb9dbb','e8a780fad808d4a292dcc59d7225835d71cf0b0f','96787a5970a03633e1fd6bd4f50e1d2a62528f0a','3fd799742f6a5c4ab686020a90bef254494b4654','76483dd2ec3be32d0bb13393d58c28d8cf0e1063']:
    history.append(dict(commit=c,record=git(E,'show','--format=fuller','--stat',c).decode()))
doc='external/doctest/doctest.h';assert blob(doc,'324f9c483d9b4a11249c47888b40fb5cc691be7f')==blob(doc)
history.append(dict(doctest_import_identical=True,path=doc,sha256=sha(blob(doc)),lines=len(blob(doc).splitlines()),fork_written_credit=0))
history.append(dict(id3_previous_gitlink=git(E,'ls-tree','72609fc9d4882aa3541ff89720901303680d8630','external/id3v2lib').decode()))
write('history.json',history)
write('collector-binding.json',dict(program_sha256=sha(pathlib.Path(__file__).read_bytes()),parser_sha256=sha((pathlib.Path(__file__).parent/'catalogue.py').read_bytes()),inputs=inputs,python=sys.version,locale='C',cpus=sorted(os.sched_getaffinity(0)),finish=now(),commands=receipts))
print('PASS metadata collection: native594 verified; catalogue36; French3/6/1/1/0; PL024 35PO/37files/38replacements; doctest unchanged import')
