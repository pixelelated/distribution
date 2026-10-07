#!/usr/bin/env python3
"""Reconcile fork-touched catalogues/XML with consumers and installed bytes (#344)."""
import argparse,ast,gettext,hashlib,json,re,subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--es',type=Path,required=True);p.add_argument('--es-build',type=Path,required=True);p.add_argument('--tree',type=Path,required=True);p.add_argument('--parsed-theme',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
ES_BASE='bccd715707e794a396e6578a585526658909c427';DISTRO_BASE='9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def git(tree,*args):return subprocess.check_output(['git','-C',str(tree),*args],text=True)
def parse(s):
 entries=[];e={};key=None
 for line in s.splitlines()+['']:
  if not line.strip():
   if e:entries.append(e)
   e={};key=None;continue
  if line.startswith('#~'):e['obsolete']=True;line=line[2:].lstrip()
  if line.startswith('#,') and 'fuzzy' in line:e['fuzzy']=True
  m=re.match(r'(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?) (".*")$',line)
  if m:
   if m[1] in ('msgid','msgctxt') and any(k.startswith('msgstr') for k in e):entries.append(e);e={}
   key=m[1];e[key]=ast.literal_eval(m[2])
  elif line.startswith('"') and key:e[key]+=ast.literal_eval(line)
 result={}
 for e in entries:
  if 'msgid' in e:
   k=(e.get('msgctxt'),e['msgid']);assert k not in result,('duplicate',k);result[k]=e
 return result
rel='locale/lang/fr/LC_MESSAGES/emulationstation2.po'
assert git(a.es,'diff','--name-only',ES_BASE,'HEAD','--','*.po','*.xml').splitlines()==[rel]
base=parse(git(a.es,'show',ES_BASE+':'+rel));source=parse((a.es/rel).read_text());potpath=a.es_build/'locale/emulationstation2.pot';pot=parse(potpath.read_text())
installed_path=a.root/'usr/config/locale/fr/LC_MESSAGES/emulationstation2.po';installed=parse(installed_path.read_text());mo=a.root/'usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo'
with mo.open('rb') as f:catalog=gettext.GNUTranslations(f)
rows=[]
for key,e in source.items():
 if e==base.get(key):continue
 assert key[0] is None and 'msgid_plural' not in e
 if key in pot:
  assert not e.get('fuzzy') and e.get('msgstr')
  assert not installed[key].get('obsolete') and catalog.gettext(key[1])==e['msgstr']
  disposition='current gettext consumer; installed translation exact'
 else:
  assert installed[key].get('obsolete') and key[1] not in catalog._catalog
  disposition='retired msgid; build marks obsolete and omits from compiled catalogue'
 rows.append({'msgid':key[1],'translation':e['msgstr'],'disposition':disposition})
removed=[]
for key in set(base)-set(source):
 assert key not in pot
 removed.append({'msgid':key[1],'disposition':'removed translation of retired source consumer'})
xml_changes=[]
meta='projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml';cemu='projects/ROCKNIX/packages/emulators/standalone/cemu-sa/config/GENERIC_X64/settings.xml'
# Retained prior QA output is documentary XML, not a package input. Match
# the one reviewed path AND bytes; any additional XML/PO path still fails.
documentary_xml={'docs/qa-logs/2026-10-06-pixelelated-replacement-15/sweep-11/artifacts/parsed-theme.xml':'47ffcdcd362aa3e01150c29c1ae3c703d1bfebec8460f9a30c16b836742317b1'}
inputs=json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-16/inputs.json').read_text())
for path,digest in documentary_xml.items():
 assert sha(a.tree/path)==digest
 assert path not in inputs['source_files'] and path not in inputs['qa_source_files']
assert set(git(a.tree,'diff','--name-only',DISTRO_BASE,'HEAD','--','*.po','*.xml').splitlines())=={meta,cemu}|set(documentary_xml)
# The old malformed entity is normalized only to compare semantic entries.
old=ET.fromstring(git(a.tree,'show',DISTRO_BASE+':'+meta).replace('iOS 2 & 3','iOS 2 &amp; 3'))
new=ET.parse(a.tree/meta).getroot()
oldgames={e.findtext('path'):e for e in old.findall('game')}
for e in new.findall('game'):
 path=e.findtext('path');prior=oldgames[path]
 for field in e:
  before=prior.findtext(field.tag)
  if before!=field.text:xml_changes.append({'file':meta,'entry':path,'field':field.tag,'before':before,'after':field.text,'consumer':'Tools metadata row in EmulationStation'})
xml_changes.append({'file':meta,'entry':'./Start touchHLE.sh','field':'desc','disposition':'literal ampersand escaped; rendered text unchanged; #417'})
try:ET.parse(a.root/'usr/config/modules/gamelist.xml');meta_valid=True
except ET.ParseError:meta_valid=False
meta_exact=(a.root/'usr/config/modules/gamelist.xml').read_bytes()==(a.tree/meta).read_bytes()
ct=ET.parse(a.tree/cemu).getroot()
for e in ct.iter():
 if len(e)==0:xml_changes.append({'file':cemu,'entry':e.tag,'value':e.text,'attributes':e.attrib,'consumer':'cemu-sa makeinstall_target copies config/${DEVICE}; Cemu reads settings.xml','disposition':'optional package not installed in this GENERIC_X64 image'})
assert not (a.root/'usr/bin/cemu').exists()
theme=a.root/'usr/share/themes/es-theme-art-book-next';t=ET.parse(a.parsed_theme).getroot();s=ET.parse(theme/'splash.xml').getroot()
include=[e for e in t.iter('include') if e.attrib.get('name')=='rocknix'];assert len(include)==1 and include[0].get('displayName')=='pixelelated'
tool=[e for e in t.iter('path') if e.get('if')=="${system.theme} == 'tools'"];assert any(e.text=='{game:image}' for e in tool)
background=[e for e in s.iter('image') if e.get('name')=='background' and e.get('ifSubset')=='splash-screen:default'];assert len(background)==1
expected={'origin':'0.5 0.5','pos':'0.5 0.36','maxSize':'0.8 0.6','path':'./pixelelated-wordmark.svg','linearSmooth':'false'}
assert all(background[0].findtext(k)==v for k,v in expected.items())
xml_changes += [{'file':'theme.xml','entry':'distribution/rocknix','field':'displayName','value':'pixelelated','consumer':'theme customization selector'}, {'file':'theme.xml','entry':'Tools image path','value':'{game:image}','consumer':'Tools icon in game list'}]
xml_changes += [{'file':'splash.xml','entry':'default background','field':k,'value':v,'consumer':'ES theme default loading screen'} for k,v in expected.items()]
report={'documentary_xml':documentary_xml,'es_base':ES_BASE,'es_commit':git(a.es,'rev-parse','HEAD').strip(),'distribution_base':DISTRO_BASE,'distribution_commit':git(a.tree,'rev-parse','HEAD').strip(),'hashes':{'source_po':sha(a.es/rel),'consumed_pot':sha(potpath),'installed_po':sha(installed_path),'installed_mo':sha(mo)},'catalogue_entries':rows,'removed_entries':removed,'xml_entries':xml_changes,'unclassified_entries':0,'active_orphan_translations':0,'installed_tools_xml_valid':meta_valid,'installed_tools_matches_corrected_source':meta_exact,'known_image_corrections':[] if meta_valid and meta_exact else [416,417]}
a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'catalogue_entries':len(rows),'retired':sum('retired' in r['disposition'] for r in rows),'removed':len(removed),'xml_entries':len(xml_changes),'active_orphans':0,'known_image_corrections':report['known_image_corrections']}))
