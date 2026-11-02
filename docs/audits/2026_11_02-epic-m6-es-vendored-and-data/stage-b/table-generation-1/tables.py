"""Generate and validate T44 tables from hash-bound source metadata, never ES programs."""
import pathlib,json,hashlib,sys,copy,re
A=pathlib.Path(__file__).resolve().parents[1]
P='55158d2a64c69fe295fb4e67fd174424a71b1b4d'
TREE='64b90eb8cb07bdfcd690c74ff6bc980ae490657c'
HASHES={'native.json':'8b83b4127ec43a0d01320f0de4871f6277df001100b5eeafa3717151693e2f8f','additions.json':'c9ca13392ff478404ddbc4aeca580eb471b09ef39c5b298679fb740439934575','companions.json':'2a1676a51f25d12cc1f1fe131b5cb3b21c3bbc5b9c9d60dd79269ae8a8767f64','summary.json':'e454858048c8b6a16bbd7a372df431153cf5b5bae151ffe80a2d7bd8f5edb240'}
def check(v,name):
    if not v:raise ValueError(name)
def load(p):return json.loads((A/p).read_bytes())
def bound(n):
    p=A/'stage-a/inputs/actual-head'/n;b=p.read_bytes();check(hashlib.sha256(b).hexdigest()==HASHES[n],'BOUND_HELPER_INPUT:'+n);return json.loads(b)
def group(p):
    for g in ['external/libcheevos/libretro-common','external/libcheevos/rcheevos','external/id3v2lib','external/nanosvg','external/doctest','external/pugixml']:
        if p==g or p.startswith(g+'/'):return g.split('/')[-1]
    return p.split('/')[0] if '/' in p else 'root'
def build():
    native=bound('native.json');add=bound('additions.json');companions=bound('companions.json');summary=bound('summary.json')
    read={x['path']:x for x in load('stage-b/reading-register.json')['records']}
    heads={x['path']:x for x in load('stage-b/source-header-markers.json')}
    consumers=load('stage-b/consumer-lines.json')['lines']
    interfaces=load('stage-b/interfaces.json')
    out={'schema':1,'source_ref':P,'source_tree':TREE,'input_hashes':HASHES,'provenance':[],'coverage':[],'supplemental':[],'companions':[]}
    for r in native:
        p=r['path'];g=group(p);kind=r['survey']['kind'];v=r['primary'];s=r['survey']
        origin=('unchanged identity at fixed upstream e282b05627c0d2193c19d7cc526176e047530c3d' if s['fixed_upstream_same_identity'] else s['base_comparison']+' relative to cada856d86e3115fbbf0bce09dd761b0ee8fa9fd; exact lineage not inferred from tier')
        licence=('source header markers: '+','.join(str(x['line']) for x in heads[p]['header_markers'])+'; stage-b/source-header-markers.json (not a legal completeness verdict)' if p in heads else 'no license marker in first 45 source lines; group/source notice proof below; individual attribution remains unproved')
        vendor=g in ['libretro-common','rcheevos','id3v2lib','nanosvg','doctest','pugixml']
        if vendor:origin+='; group '+g+' in stage-b/vendor-groups.json (version/import/license/carry reason)'
        refs=[]
        for f in interfaces:
            if not f['path'].endswith('CMakeLists.txt'):continue
            parent=str(pathlib.PurePosixPath(f['path']).parent)
            for mark in f['markers']:
                text=mark['text'].replace('${CMAKE_CURRENT_SOURCE_DIR}',parent).replace('${CMAKE_CURRENT_LIST_DIR}',parent)
                paths=re.findall(r'[\w./-]+\.(?:cpp|c|h|png|mp3)',text)
                if any(str(pathlib.PurePosixPath(x))==p or __import__('posixpath').normpath(x)==p for x in paths):refs.append(f['path']+':'+str(mark['line']))
        if p.startswith('resources/'):
            name=pathlib.PurePosixPath(p).name
            refs.extend(':'.join(x.split(':')[1:3]) for x in consumers if name in x)
        if refs:consumer='literal source references '+', '.join(sorted(set(refs)))+'; stage-b/interfaces.json / consumer-lines.json; configuration not executed'
        elif p.startswith('resources/'):consumer='recipe:81-85 copies resources directory; dynamic ResourceManager lookup may apply; no literal basename found in selected app/core traces; absence is not deadness'
        elif p.startswith('locale/'):consumer='locale/CMakeLists.txt:1-33; root CMake:614-616 requires gettext tools+Intl; recipe:67-68 copies locale outputs'
        elif p.startswith('tests/'):consumer='manual test entry point or tests/app-unit/CMakeLists.txt:24-106; not automatically claimed by root ES_BUILD_TESTS; existing behavior owner retained'
        elif p.startswith('.githooks/'):consumer='Git hook installation selects these files; public guard-lib loads pattern inputs; installation/private input not verified or invoked'
        elif p.startswith('CMake/'):consumer='root CMakeLists.txt:109-112 adds module directory; package finder use depends on configuration; not all modules proven selected'
        elif vendor:consumer='group '+g+' source selection in stage-b/vendor-groups.json; not named by examined explicit CMake list, may be transitively included; no deadness verdict'
        elif p.startswith('.github/'):consumer='GitHub issue template metadata; not application runtime source'
        else:consumer='root documentation/configuration entry; exact content identity retained; no runtime consumer claimed'
        if p=='external/pugixml':consumer='external/CMakeLists.txt:5-7 only NOT USE_SYSTEM_PUGIXML; recipe selects system=1; gitlink not expanded'
        if p=='external/doctest/doctest.h':consumer='tests/app-unit/CMakeLists.txt includes external; es-app/tests/unit belongs T18; test-only header, not configured here'
        if p in read:reading=read[p]['observation'];credit=read[p]['range'][1];method='full-code-read'
        elif kind in ('binary','gitlink'):reading='mode/OID/size/kind metadata only; no source or visual reading';credit=0;method='metadata-only'
        elif p.startswith('locale/') and p.endswith(('.po','.pot')):reading='whole-blob syntactic parser; stage-b/catalogue-counts.json; no translation quality or format argument equivalence claim';credit=0;method='syntactic-parse'
        elif p.endswith(('.svg','.xml')) and p.startswith('resources/'):reading='whole XML structure parse only; stage-b/resource-xml.json; no rendering';credit=0;method='syntactic-parse'
        else:reading='identity/provenance table plus named header/interface excerpts only; no complete semantic reading credit';credit=0;method='table-provenance'
        owner='T44 #691 table; coordinator #700 disposition/integration'
        if p in read:owner+='; behavior owner per stage-b/reading-register.json, not reopened'
        if g in ('libretro-common','rcheevos'):owner+='; T20 #667 owns nine excluded fork source/adapter paths'
        if g=='pugixml':owner+='; system recipe owner outside native table, T37 #684 context'
        if p.startswith('resources/'):owner+='; T36 #683 consumer/renderer and T37 #684 recipe context'
        row=dict(path=p,kind=kind,mode=v['mode'],blob=v['oid'],sha256=v.get('sha256') or 'not-a-blob',survey_tier=s['tier'],survey_lines=s['inventory_lines'],primary_lines=v.get('text_logical_lines'),changed_since_survey=r['changed_since_survey'],group=g,origin=origin,license=licence,consumer=consumer,reading=reading,read_lines=credit,fork_written=(s['tier']=='fork-own' and p!='external/doctest/doctest.h'),method=method,currency=('dated vendor comparison/open input in stage-b/vendor-groups.json' if vendor else 'retain exact source; no update/removal verdict'),limit=('gitlink source unavailable and not fetched' if kind=='gitlink' else 'binary not decoded/rendered' if kind=='binary' else 'source identity/reach only; installed behavior and transitive configurations unproved'),owner=owner,receipt='stage-a/inputs/actual-head/native.json; stage-b/collector-binding.json')
        out['provenance'].append(row);out['coverage'].append(copy.deepcopy(row))
    for r in add:
        out['supplemental'].append(dict(**r,reading=read[r['path']]['observation'],read_lines=r['text_logical_lines'],source_ref=P,integrated=False))
    for r in companions:out['companions'].append(dict(**r,integrated=False,receipt='stage-b/french-deltas-and-calls.json; separate accepted owner branch, not combined source'))
    return out
def validate(model):
    expected=build();keys={r['path'] for r in expected['provenance']}
    check(model.get('source_ref')==P and model.get('source_tree')==TREE and model.get('input_hashes')==HASHES,'SOURCE_IDENTITY')
    for table in ['provenance','coverage']:
        rows=model.get(table,[]);check(len(rows)==len(keys) and {r['path'] for r in rows}==keys,'NATIVE_KEYS:'+table)
        for r in rows:
            if r['kind']=='gitlink':check(r['read_lines']==0 and r['method']=='metadata-only','GITLINK_READ_CREDIT')
            if r['path']=='external/doctest/doctest.h':check(not r['fork_written'] and r['read_lines']==0,'DOCTEST_AUTHORSHIP')
    check(len(model.get('supplemental',[]))==3 and {x['path'] for x in model['supplemental']}=={x['path'] for x in expected['supplemental']},'SUPPLEMENTAL_KEYS')
    check(len(model.get('companions',[]))==4 and {x['ref'] for x in model['companions']}=={x['ref'] for x in expected['companions']},'COMPANION_KEYS')
    check(all(x.get('integrated') is False and x.get('contains_primary') is False for x in model['companions']),'COMPANION_INTEGRATION')
    check(model==expected,'EXACT_BOUND_ROWS')
    print('PASS T44 table assertions: native594 x2 / supplemental3 / companions4; exact bound rows; honest credits')
def cell(x):return str(x if x is not None else 'N/A').replace('|','&#124;').replace('\n','<br>')
def render(model):
    out=[]
    for name in ['provenance','coverage']:
        out+=['## '+name.title(),'','| Path | Kind/mode/blob/SHA256 | Survey tier/lines; primary lines/delta | Group; origin/license | Source consumer/condition | Reading/credit | Currency/disposition | Specific limit | Next owner/action; receipt |','| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
        for r in model[name]:
            cols=[r['path'],f"{r['kind']}/{r['mode']}<br>{r['blob']}<br>{r['sha256']}",f"{r['survey_tier']}/{r['survey_lines']}; {r['primary_lines']}; changed={r['changed_since_survey']}",r['group']+'; '+r['origin']+'; '+r['license'],r['consumer'],r['method']+'; '+r['reading']+f"; full-read lines={r['read_lines']}; fork-written={r['fork_written']}",r['currency'],r['limit'],r['owner']+'; '+r['receipt']]
            out.append('| '+' | '.join(cell(c) for c in cols)+' |')
        out+=['',f"Computed keys: {len(model[name])}; unique: {len({x['path'] for x in model[name]})}; inventory lines: {sum(x['survey_lines'] for x in model[name])}; primary text lines: {sum(x['primary_lines'] or 0 for x in model[name])}.",'']
    out+=['## Supplemental post-survey tests (separate)','','| Path | Source/OID/SHA256 | Lines | Owner and read limits |','| --- | --- | --- | --- |']
    for r in model['supplemental']:out.append('| '+' | '.join(cell(x) for x in [r['path'],r['source_ref']+'/'+r['oid']+'/'+r['sha256'],r['read_lines'],r['owner']+'; '+r['reading']])+' |')
    out+=['','## Accepted companion branches (separate)','','| Owner | Ref | French OID/SHA256 | Contains T2 / integrated | Evidence |','| --- | --- | --- | --- | --- |']
    for r in model['companions']:out.append('| '+' | '.join(cell(x) for x in [r['owner'],r['ref'],r['french']['oid']+'/'+r['french']['sha256'],'false / false',r['receipt']])+' |')
    return '\n'.join(out)+'\n'
if __name__=='__main__':
    if len(sys.argv)>1:
        model=json.loads(pathlib.Path(sys.argv[1]).read_bytes());validate(model)
    else:
        model=build();validate(model)
        (A/'stage-b/tables.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
        (A/'stage-b/tables.md').write_text(render(model))
