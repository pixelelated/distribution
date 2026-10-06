from pathlib import Path
import datetime, hashlib, json, os, subprocess, types
root=Path(__file__).resolve().parent
repo=root.parents[3]
path='projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'
old='7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2'
new='ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'
expected={
'en_US':['id=leave-ask>Close page','<span>Close the sign-in page on your handheld?</span>','id=leave-keep>Keep','id=leave-close>Close'],
'fr_FR':['id=leave-ask>Fermer la page','<span>Fermer la page de connexion sur votre console ?</span>','id=leave-keep>Garder ouverte','id=leave-close>Fermer']}
rows=[]
for label,ref in [('old',old),('fixed',new)]:
 source=subprocess.check_output(['git','-C',str(repo),'show',ref+':'+path])
 module=types.ModuleType('audit_'+label);module.__file__=str(root/(label+'-cloud-oauth'))
 exec(compile(source,module.__file__,'exec'),module.__dict__)
 # Only emulate presence of the display stack. Execute the actual handler's
 # render method unchanged; capture its output in memory instead of a socket.
 module.browser_stack_available=lambda:True
 holder=types.SimpleNamespace(name='QA local page',pin='synthetic-pin')
 handler=module.make_handler(holder,lambda:None).__new__(module.make_handler(holder,lambda:None))
 for lang,strings in expected.items():
  os.environ['LANGUAGE']=lang;output=[];handler._send=lambda body,*args:output.append(body);handler._render()
  assert len(output)==1
  html=output[0];present=[s in html for s in strings]
  (root/(label+'-'+lang+'.html')).write_text(html)
  rows.append(dict(source=label,ref=ref,source_sha256=hashlib.sha256(source).hexdigest(),language=lang,required_controls_present=present,output_sha256=hashlib.sha256(html.encode()).hexdigest()))
  if label=='old' and lang=='fr_FR':assert not any(present),'old source unexpectedly passed French output'
  else:assert all(present),'expected localized output absent'
assert rows[0]['output_sha256']==rows[1]['output_sha256'],'old source was expected to ignore language'
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),passed=True,observations=rows,scope='Host execution of actual old/fixed handler _render, with only display-availability predicate and response sink stood in. No browser, OAuth, network, native-window or old-image execution claim. Actual native EN/FR and full interactions are separately proved on installed candidate15.')
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir()) if p.is_file() and p.name!='sha256.json'},indent=2)+'\n')
print('PASS old actual handler ignores French and fails all four controls; fixed English/French each pass four')
