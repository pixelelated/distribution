import os,subprocess,pathlib,json,hashlib,datetime
P=pathlib.Path(__file__).resolve().parent
ES='/home/max/Development/emulationstation-next'
D='/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649'
PIN='16dbac5211eea7e70db7394372033be2be7df829'
T2='55158d2a64c69fe295fb4e67fd174424a71b1b4d'
ENV=os.environ.copy(); ENV.update(GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
assert sorted(os.sched_getaffinity(0))==list(range(8,24))
commands=[]
def git(repo,*args):
    x=subprocess.run(['git','-C',repo,*args],env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    commands.append({'argv':x.args,'rc':x.returncode,'stdout_sha256':hashlib.sha256(x.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(x.stderr).hexdigest()})
    assert x.returncode==0,(args,x.stderr)
    return x.stdout
def show(ref,path):return git(ES,'show',ref+':'+path)
def oid(ref,path):return git(ES,'rev-parse',ref+':'+path).decode().strip()
rename='a1cbc0ccd96cbd95f3355375609f71f1b50c7113'
parent=git(ES,'rev-parse',rename+'^').decode().strip()
paths=git(ES,'diff','--name-only',parent,rename).decode().splitlines()
po=[s for s in paths if s.startswith('locale/lang/') and s.endswith('.po')]
assert len(po)==35 and set(paths)==set(po+['locale/emulationstation2.pot','es-app/src/FileData.cpp'])
rows=[]
for path in paths:
    before=show(parent,path);after=show(rename,path)
    assert before.replace(b'UKNOWN ERROR',b'UNKNOWN ERROR')==after,path
    if path.endswith('.po'):
        # Assert every non-en_GB translation byte is unchanged, not just entry count.
        expected=before.replace(b'msgid "UKNOWN ERROR"',b'msgid "UNKNOWN ERROR"')
        if '/en_GB/' in path:expected=expected.replace(b'msgstr "UKNOWN ERROR"',b'msgstr "UNKNOWN ERROR"')
        assert expected==after,path
        assert b'msgid "UNKNOWN ERROR"' in show(T2,path) and b'msgid "UKNOWN ERROR"' not in show(T2,path)
    rows.append({'path':path,'before_blob':oid(parent,path),'after_blob':oid(rename,path),'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'replacement_occurrences':before.count(b'UKNOWN ERROR')})
assert sum(x['replacement_occurrences'] for x in rows)==38
owners={'T2':T2,'T21':'3ae9610b0f3fb61d23eb6a2c3459ad19f962e2b1','T34':'52f0ff5128cf96bfcdec9082ded75347ecea11e6','T35':'b7fdb3a24c859ce91f9fd381bb0956901b8d23cb','T36':'9c1bd5f093cfc1ccd42640282226b7b970442ef1'}
owner_records=[]
for owner,ref in owners.items():
    git(ES,'cat-file','-e',ref+'^{commit}')
    dif=git(ES,'diff','--name-status',PIN,ref,'--','.',':(exclude)es-app/**',':(exclude)es-core/**').decode()
    outside=[l for l in dif.splitlines()]
    loc=git(ES,'diff','--no-ext-diff','--no-textconv','--unified=2',PIN,ref,'--','locale').decode()
    log=git(ES,'log','--format=%H %s',PIN+'..'+ref,'--','locale').decode()
    ancestor=subprocess.run(['git','-C',ES,'merge-base','--is-ancestor',T2,ref],env=ENV).returncode
    commands.append({'argv':['git','-C',ES,'merge-base','--is-ancestor',T2,ref],'rc':ancestor})
    assert ancestor in [0,1]
    fr=show(ref,'locale/lang/fr/LC_MESSAGES/emulationstation2.po')
    unchanged_external=git(ES,'diff','--name-only',PIN,ref,'--','external')==b''
    owner_records.append({'owner':owner,'accepted_es':ref,'outside_app_core_changes':outside,'locale_diff':loc,'locale_commits':log,'T2_is_ancestor':ancestor==0,'fr_still_has_old_key':b'msgid "UKNOWN ERROR"' in fr,'external_unchanged_from_survey':unchanged_external})
assert all(x['external_unchanged_from_survey'] for x in owner_records)
versions={}
for path in ['external/doctest/doctest.h','external/libcheevos/rcheevos/src/rc_version.h','external/libcheevos/rcheevos/src/rcheevos/rc_version.h','external/libcheevos/rcheevos/CHANGELOG.md','external/id3v2lib/CMakeLists.txt','external/nanosvg/nanosvg.h','external/libcheevos/libretro-common/src/7zip/7zVersion.h','.gitmodules','external/CMakeLists.txt']:
    data=show(PIN,path);versions[path]={'blob':oid(PIN,path),'sha256':hashlib.sha256(data).hexdigest(),'last_change':git(ES,'log','-1','--format=%H %aI %s',PIN,'--',path).decode().strip()}
doctest_import='324f9c483d9b4a11249c47888b40fb5cc691be7f'
assert show(doctest_import,'external/doctest/doctest.h')==show(PIN,'external/doctest/doctest.h')
distpins={}
for ref in ['7041b0d710363ddac7ae1b047ebae3e182548631','92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1']:
    path='projects/ROCKNIX/packages/ui/emulationstation/package.mk';data=git(D,'show',ref+':'+path)
    distpins[ref]={'sha256':hashlib.sha256(data).hexdigest(),'PKG_VERSION_lines':[l for l in data.decode().splitlines() if l.startswith('PKG_VERSION=')]}
result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cpus':sorted(os.sched_getaffinity(0)),'survey_es':PIN,'rename_commit':rename,'rename_parent':parent,'catalogues':len(po),'changed_files':len(paths),'replacement_occurrences':38,'rename_rows':rows,'owners':owner_records,'vendor_markers':versions,'doctest_unchanged_since_import':doctest_import,'pugixml_gitlink':git(ES,'ls-tree',PIN,'--','external/pugixml').decode().strip(),'distribution_recipe_pins':distpins}
(P/'readback.json').write_text(json.dumps(result,indent=2)+'\n');(P/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print('PL024: 35 catalogues, 37 changed files, 38 one-word replacements; translations preserved except corrected en_GB; accepted T2 retains correction.')
for x in owner_records:print(x['owner'],x['accepted_es'],'T2 ancestor',x['T2_is_ancestor'],'old-key',x['fr_still_has_old_key'],'external unchanged',x['external_unchanged_from_survey'])
print(json.dumps(distpins,indent=2))
