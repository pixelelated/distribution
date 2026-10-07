import datetime,json,pathlib,subprocess
owner=pathlib.Path(__file__).resolve().parent
def gh(*args):
 r=subprocess.run(['gh',*args],text=True,capture_output=True)
 if r.returncode: raise SystemExit(r.stderr)
 return r.stdout
current=json.loads(gh('issue','view','502','--repo','pixelelated/distribution','--json','body,state'))
assert current['state']=='OPEN'
body=current['body']
(owner/'issue502-before.md').write_text(body)
for prefix in ('Revised English/French source uses PREVIOUS OS','VM frames at640x480 show complete English/French'):
 assert body.count('- [ ] '+prefix)==1,prefix
 body=body.replace('- [ ] '+prefix,'- [x] '+prefix)
old='Follow-up to #501. Initial read-only source investigation preceded filing; no product edit or device/cloud operation has occurred. The preceding request explicitly asked for comparison without immediate changes. This issue retains the wording proposal for the next UI change; it does not restart or modify the frozen device builds.'
new='Follow-up to #501. Initial read-only source investigation preceded filing; at that point no product edit or device/cloud operation had occurred. The preceding request asked for comparison without immediate changes. The maintainer subsequently approved implementation and parallel work. The verified source change below does not restart or modify the frozen device builds.'
assert old in body
body=body.replace(old,new)
old='This is proposed wording and tracked UI work, not a claim that the installed build has changed.'
new='The source change is now verified and published as described below. The installed H700 build has not changed; distribution pin integration and a future image are tracked separately.'
assert old in body
body=body.replace(old,new)
body+='''\n## Verified source and scoped VM proof — 2026-10-07\n\nPublished ES commit [5d2fcb9b71f363cfa4813d5356f02c48ab58e139](https://github.com/pixelelated/emulationstation/commit/5d2fcb9b71f363cfa4813d5356f02c48ab58e139) changes only the English prompt and matching French catalog entry. Both `feature/m7-migration-copy` and `test/qa-integration` point to that commit after a clean fast-forward and normal-hook push; remote hashes were read back. The exact approved final English sentence is preserved.\n\nPASS: `tools/es-syntax-check`, vocabulary, `msgfmt --check --check-format`, the existing build-style xgettext command, `git diff --check`, and register citations. C++ Unicode escapes retain the supported quotation marks while allowing the existing xgettext invocation to extract the matching French msgid. Migration logic, runtime paths, automatic following, button labels/order, and confirmation conditions are unchanged.\n\nActual EN/FR frames at **640x480 and 1280x800** were directly inspected. All prompt text and three choices are visible; no scrolling is needed. The French button row's slight overhang outside its dialog background remains inside the screen and was separately reproduced with the original source; this copy change does not introduce it. Accepted frame hashes and both reviewers' scope are captured in the compact evidence packet `docs/qa-logs/2026-10-07-migration-copy/acceptance.json` (local; distribution evidence publication follows).\n\nThe narrow proof used one owner-local recompiled object and relink, retained candidate16 build inputs read-only, and one disposable guest with a local QA alias. No migration was selected. All guest/compiler/watch processes exited; the named guest disk, keys, and runtime binaries were removed after proof capture, reclaiming 2,556,751,872 allocated bytes. Failed harness attempts are retained in the compact logs and excluded from visual acceptance.\n\nThe distribution pin and accepted candidate16/H700 artifacts remain unchanged by this source lane. Leave this issue open for the parent lane's distribution integration/build handoff.\n'''
path=owner/'issue502-after.md';path.write_text(body)
print(gh('issue','edit','502','--repo','pixelelated/distribution','--body-file',str(path)),end='')
readback=json.loads(gh('issue','view','502','--repo','pixelelated/distribution','--json','body,state'))
assert readback['body']==body and readback['state']=='OPEN'
(owner/'issue502-readback.json').write_text(json.dumps({'result':'PASS','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':readback['state'],'checked_criteria':body.count('- [x] '),'body_matches':True},indent=2)+'\n')
print('PASS #502 criteria/source status updated and exact body read back')
