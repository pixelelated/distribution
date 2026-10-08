import ast,gettext,json,pathlib,subprocess
o=pathlib.Path(__file__).resolve().parent;m=json.loads((o/'commands.json').read_text());es=pathlib.Path(m['source']);tc=pathlib.Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/toolchain/bin')
files=sorted(str(p) for part in ['es-app','es-core'] for p in (es/part).rglob('*') if p.suffix in ['.cpp','.h'])
subprocess.run([str(tc/'xgettext'),'--add-comments=TRANSLATION','-f','-','-o',str(o/'extracted.pot'),'--no-location','--keyword=_'],input='\n'.join(files)+'\n',text=True,check=True)
def ids(p):
 result=[];value=None
 for line in p.read_text().splitlines()+['']:
  if line.startswith('msgid '):
   if value is not None:result.append(value)
   value=ast.literal_eval(line[6:])
  elif line.startswith('"') and value is not None:value+=ast.literal_eval(line)
  elif value is not None:result.append(value);value=None
 return result
expected=json.loads((o/'new-messages.json').read_text());extracted=ids(o/'extracted.pot');committed=ids(es/'locale/emulationstation2.pot')
with (o/'fr.mo').open('rb') as f:fr=gettext.GNUTranslations(f)
for en,want in expected.items():
 assert en in extracted,('missing extraction',en)
 assert en in committed,('missing POT entry',en)
 assert fr.gettext(en)==want,('wrong French translation',en,fr.gettext(en),want)
print('PASS',len(expected),'new message extractions, checked-in POT entries and exact French translations')
