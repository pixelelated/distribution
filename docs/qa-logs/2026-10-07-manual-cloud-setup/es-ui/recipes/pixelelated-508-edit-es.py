from pathlib import Path
import re,subprocess,json
root=Path('/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup')
def edit(name,fn):
 p=root/name;s=p.read_text();n=fn(s);assert n!=s,name;p.write_text(n)
edit('es-app/src/CloudText.h',lambda s: s.replace('// Move: cloud_migrate_layout --apply, the folder move the dialog offers\n\t// (#353); Create: cloud_setup --seed-folders, the folder the offer\n\t// makes.', '// Create: cloud_setup --seed-folders, the selected folders setup creates.').replace('Scan, Move, Create','Scan, Create').replace('cloud_migrate_layout --state and cloud_setup --content-location','cloud_setup --folder-state and --content-location').replace(s[s.index('\t// What cloud_migrate_layout --check'):s.index('\t// "route=',s.index('\t// What cloud_migrate_layout --check'))],''))
edit('es-app/src/CloudText.cpp',lambda s: re.sub(r'CloudText::TidyPlan CloudText::parseTidyPlan\(.*?(?=std::string CloudText::deviceNameFromLabel)', '', s, flags=re.S).replace('\t// The folder the offer creates runs the re-point and the seeding in one\n\t// command (GuiMenu\'s cloudOfferFolder): the seeding names the kind.','\t// Setup creates the selected folders without relocating existing files.').replace('\tif (cmd.find("cloud_migrate_layout") != std::string::npos && cmd.find("--apply") != std::string::npos)\n\t\treturn TransferKind::Move;\n',''))
edit('es-app/src/guis/GuiCloudTransfer.cpp',lambda s: '\n'.join(l for l in s.split('\n') if not re.match(r'\s*case CloudText::TransferKind::Move:',l)).replace('restore ? _("RESTORED")\n\t\t\t\t\t: CloudText::transferKind(job.mCommand) == CloudText::TransferKind::Move ? _("MOVED") : _("BACKED UP")','restore ? _("RESTORED") : _("BACKED UP")'))
edit('es-app/src/CloudTransferJob.cpp',lambda s:s.replace('\t\t\t// scan and compare are cloud_scan\'s (fork #350); copy, verify and\n\t\t\t// remove are the folder move\'s (cloud_migrate_layout --apply, #353).','\t\t\t// Keep generic progress verbs for scripts sharing this protocol.'))
p=root/'es-app/tests/unit/CloudTextTests.cpp';s=p.read_text();s=re.sub(r'TEST_CASE\("parseTidyPlan.*?\n}\n?', '', s, flags=re.S)
s=s.replace('\tCHECK(verbOf("/usr/bin/cloud_migrate_layout") == Verb::Other);\n','')
s=re.sub(r'\t// The folder move the dialog offers.*?(?=\tCHECK\(transferKind\("/usr/bin/cloud_scan"\))','\t// A scan and folder seeding retain their own progress labels.\n',s,flags=re.S)
s=re.sub(r'CHECK\(transferKind\("/usr/bin/cloud_migrate_layout.*?== TransferKind::Create\);','CHECK(transferKind("/usr/bin/cloud_setup --seed-folders") == TransferKind::Create);',s)
s=s.replace(', cloud_migrate_layout:98','').replace('; cloud_migrate_layout:330','').replace('; cloud_migrate_layout --apply','')
s='\n'.join(l for l in s.split('\n') if 'cloud_migrate_layout' not in l)
p.write_text(s)
# Keep only reasons that the retained scripts still emit; migration has no caller.
p=root/'es-app/src/CloudText.cpp';s=p.read_text();removed=['THE PREVIOUS CLOUD MOVE NEEDS ITS ORIGINAL CONNECTION','YOUR CLOUD FOLDER CHOICES CHANGED DURING THE MOVE',"YOUR CLOUD FOLDER MOVE DIDN'T FINISH",'THE NEW FOLDER ALREADY HAS FILES IN IT']
s='\n'.join(l for l in s.split('\n') if not any('"'+x+'"' in l for x in removed));p.write_text(s)
p=root/'es-app/src/guis/GuiMenu.cpp';s=p.read_text()
s=s.replace('const std::vector<std::string>& seeded)\n{\n\tauto info', 'const std::vector<std::string>& seeded, bool seedOk)\n{\n\tauto info')
s=s.replace('LOG(LogInfo) << "cloud_setup wizard: complete, remote="', 'LOG(LogInfo) << "cloud_setup wizard: folders=" << (seedOk ? "ready" : "incomplete") << " remote="')
s=s.replace('auto s = new GuiSettings(window, _("CLOUD SETUP COMPLETE"));\n\ts->setSubTitle(_("YOUR CLOUD STORAGE IS READY"));','auto s = new GuiSettings(window, seedOk ? _("CLOUD SETUP COMPLETE") : _("CLOUD SETUP"));\n\ts->setSubTitle(seedOk ? _("YOUR CLOUD STORAGE IS READY") : _("YOUR CLOUD FOLDERS COULD NOT BE CREATED"));')
a=s.index('\t// A new remote is an empty folder',s.index('static void cloudSetupBuildDoneStep'))
b=s.index('\tbool anyOk',a)
s=s[:a]+'''\t// Only confirmed folder readback is presented as ready. A partial failure
\t// keeps the connection and paths, and offers a retry on this page.
\ts->addGroup(_("YOUR CLOUD FOLDERS"));
'''+s[b:]
s=s.replace('_("YOUR CLOUD FOLDERS COULDN\'T BE SET UP YET. THEY ARE CREATED AT YOUR FIRST BACKUP.")','_("CHECK YOUR CONNECTION, THEN TRY AGAIN TO CREATE YOUR CLOUD FOLDERS.")')
s=s.replace('\ts->addGroup(_("OPTIONAL NEXT STEPS"));\n\tconst std::string syncpath', '''\tif (seedOk)
\t\tcloudSetupAddInfoRow(s, window, _("IF YOU MOVE YOUR CLOUD FOLDER, USE CHANGE CLOUD FOLDER ON EACH DEVICE."));
\telse
\t\ts->addEntry(_("TRY AGAIN"), true, [window, s, remote] { cloudSetupShowDoneStep(window, remote, s); });

\ts->addGroup(_("OPTIONAL NEXT STEPS"));
\tconst std::string syncpath''')
s=s.replace('cloudSetupAddFact(s, window, _("CLOUD FOLDER"), syncpath, [window, s, remote, syncpath]','cloudSetupAddFact(s, window, _("CHANGE CLOUD FOLDER"), syncpath, [window, s, remote, syncpath]')
s=s.replace('\ts->addEntry(_("BACK UP SETTINGS AND SAVES NOW"), true, [window, s]', '\tif (seedOk)\n\ts->addEntry(_("BACK UP SETTINGS AND SAVES NOW"), true, [window, s]')
s=s.replace('new GuiLoading<std::vector<std::string>>(window, _("SETTING UP YOUR CLOUD FOLDERS"),','new GuiLoading<std::pair<std::vector<std::string>, int>>(window, _("SETTING UP YOUR CLOUD FOLDERS"),')
s=s.replace('return ApiSystem::executeScriptLegacy("timeout 90 /usr/bin/cloud_setup --seed-folders");','''std::vector<std::string> lines;
\t\t\tconst int rc = ApiSystem::executeScriptLegacy("timeout 90 /usr/bin/cloud_setup --seed-folders",
\t\t\t\t[&lines](const std::string& line) { lines.push_back(line); }).second;
\t\t\treturn std::make_pair(lines, rc);''')
s=s.replace('[window, remote, prev](std::vector<std::string> seeded)\n\t\t{\n\t\t\tcloudSetupBuildDoneStep(window, remote, prev, seeded);','[window, remote, prev](std::pair<std::vector<std::string>, int> result)\n\t\t{\n\t\t\tcloudSetupBuildDoneStep(window, remote, prev, result.first, result.second == 0);')
p.write_text(s)
# Remove only retired msgids from changed source files, retaining entries used elsewhere.
pattern=r'_\("((?:\\.|[^"\\])*)"\)'
def ids(s):
 out=set()
 for raw in re.findall(pattern,s):
  try:out.add(json.loads('"'+raw+'"'))
  except ValueError:pass
 return out
old=set();current=set()
for name in subprocess.check_output(['git','diff','--name-only'],cwd=root,text=True).splitlines():
 if name.endswith(('.cpp','.h')):
  old|=ids(subprocess.check_output(['git','show','HEAD:'+name],cwd=root,text=True))
for part in ['es-app','es-core']:
 for p in (root/part).rglob('*'):
  if p.suffix in ['.cpp','.h']:current|=ids(p.read_text())
retired=old-current
for p in (root/'locale').rglob('*.po'):
 text=p.read_text();parts=re.split(r'\n\n+',text);out=[]
 for part in parts:
  match=re.search(r'^msgid (".*")((?:\n".*")*)',part,re.M)
  msg=''.join(json.loads(x) for x in (match.group(1)+match.group(2)).splitlines()) if match else None
  if msg not in retired:out.append(part)
 new='\n\n'.join(out)
 if new!=text:p.write_text(new)
p=root/'locale/lang/fr/LC_MESSAGES/emulationstation2.po'
translations={"YOUR CLOUD FOLDERS COULD NOT BE CREATED":"IMPOSSIBLE DE CRÉER VOS DOSSIERS CLOUD","CHECK YOUR CONNECTION, THEN TRY AGAIN TO CREATE YOUR CLOUD FOLDERS.":"VÉRIFIEZ VOTRE CONNEXION, PUIS RÉESSAYEZ DE CRÉER VOS DOSSIERS CLOUD.","IF YOU MOVE YOUR CLOUD FOLDER, USE CHANGE CLOUD FOLDER ON EACH DEVICE.":"SI VOUS DÉPLACEZ VOTRE DOSSIER CLOUD, UTILISEZ CHANGER DE DOSSIER CLOUD SUR CHAQUE APPAREIL."}
s=p.read_text()
for en,fr in translations.items():
 if 'msgid '+json.dumps(en) not in s:s+='\n\nmsgid '+json.dumps(en,ensure_ascii=False)+'\nmsgstr '+json.dumps(fr,ensure_ascii=False)+'\n'
p.write_text(s)
print('removed retired msgids:',len(retired))
