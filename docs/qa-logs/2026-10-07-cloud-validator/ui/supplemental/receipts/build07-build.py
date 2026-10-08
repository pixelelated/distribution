import pathlib,hashlib,json,subprocess,time
O=pathlib.Path('/workspace/tmp/pixelelated-510-coverage02/build07');S=pathlib.Path('/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup');B=pathlib.Path('/workspace/tmp/pixelelated-510-coverage02/build04');C=json.loads((O/'commands.json').read_text());T=pathlib.Path(C['commands']['es-app/src/guis/GuiMenu.cpp'][0]).parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={pathlib.Path(e['path']) for e in json.loads((B/'inputs-before.json').read_text())};inputs.update(p for p in B.glob('*.o'));inputs.add(B/'libes-core.a')
def snap():return [{'path':str(p),'sha256':h(p)} for p in sorted(inputs)]
before=snap();(O/'inputs-before.json').write_text(json.dumps(before,indent=2));start=time.monotonic()
subprocess.run(C['commands']['es-app/src/guis/GuiMenu.cpp'],cwd=C['cwd'],check=True)
with (O/'artifacts/link.log').open('w') as log:subprocess.run(C['link'],cwd=C['cwd'],check=True,stdout=log,stderr=subprocess.STDOUT)
subprocess.run([str(T/'msgfmt'),'--check','-o',str(O/'artifacts/fr.mo'),str(S/'locale/lang/fr/LC_MESSAGES/emulationstation2.po')],check=True)
after=snap();(O/'inputs-after.json').write_text(json.dumps(after,indent=2));assert before==after
receipt={'base_commit':'6b473c26e8cc03cbd509b3056c60aaf84cb8dbc0','kind':'issue514 source patch; source overlay not firmware','compile_units':1,'inputs_unchanged':len(before),'elapsed_seconds':round(time.monotonic()-start,3),'outputs':[{'path':str(p),'sha256':h(p),'bytes':p.stat().st_size} for p in [O/'emulationstation',O/'artifacts/fr.mo']]};(O/'artifacts/outputs.json').write_text(json.dumps(receipt,indent=2));print('PASS',json.dumps(receipt))
