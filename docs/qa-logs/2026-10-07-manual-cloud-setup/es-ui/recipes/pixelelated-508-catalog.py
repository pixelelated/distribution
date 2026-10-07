from pathlib import Path
import re,subprocess,json
root=Path("/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup")
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
  if p.suffix in ['.cpp','.h']:current|=ids(p.read_text(errors="replace"))
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
