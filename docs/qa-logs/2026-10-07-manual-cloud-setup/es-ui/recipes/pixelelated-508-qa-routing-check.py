import hashlib, importlib.machinery, importlib.util, json, subprocess, tempfile
from pathlib import Path
from types import SimpleNamespace
root=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
results=[]
with tempfile.TemporaryDirectory(prefix='pixelelated-508-routing-') as tmp:
    fixture=Path(tmp); (fixture/'tools').mkdir()
    for name,args in [('cloud-pair-migration', []),('rasteratops-vm-cloud-epic',['--output',str(fixture/'must-not-exist')]),('pixelelated-vm-cloud-boundaries',['--tree',str(fixture),'--image','unused','--build-id','unused','--output',str(fixture/'must-not-exist')]),('rasteratops-cloud-layout-test',['--output',str(fixture/'must-not-exist')])]:
        src=root/'tools'/name; dest=fixture/'tools'/name; dest.write_bytes(src.read_bytes());dest.chmod(0o755)
        r=subprocess.run([str(dest),*args],capture_output=True,text=True)
        assert r.returncode != 0 and 'retired' in r.stderr and not (fixture/'must-not-exist').exists(), (name,r.returncode,r.stderr)
        results.append({'case':name+' refuses absent engine before fixture creation','status':'PASS','rc':r.returncode})
    protocol=root/'tools/vm-walks/cloud-epic/migration-protocol.sh'
    r=subprocess.run(['bash','-c','source "$1"; callfile="$2"; G_() { printf "%s\\n" "$*" >> "$callfile"; return 1; }; protocol_init','bash',str(protocol),str(fixture/'calls')],capture_output=True,text=True)
    # The stub is deliberately unable to perform a guest write; it rejects the first probe.
    assert r.returncode==2 and 'no fixture was changed' in r.stderr,(r.returncode,r.stderr)
    assert (fixture/'calls').read_text().splitlines() == ['test -x /usr/bin/cloud_migrate_layout']
    results.append({'case':'sourced protocol refuses unavailable engine','status':'PASS','rc':r.returncode})
    loader=importlib.machinery.SourceFileLoader('layout_fixture',str(root/'tools/rasteratops-cloud-layout-test'))
    spec=importlib.util.spec_from_loader(loader.name,loader);module=importlib.util.module_from_spec(spec);loader.exec_module(module)
    # Give the imported Fixture a worktree whose current source has removed the
    # engine, while git --ref still names the historical bytes.
    historical_root=Path('/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders')
    assert not (historical_root/module.SOURCES/'cloud_migrate_layout').exists()
    module.ROOT=historical_root
    f=module.Fixture(fixture/'historical',SimpleNamespace(ref='7cfdf9f73ae2a064ee4f281461e661301cb2dd65',rclone='/usr/bin/rclone'))
    expected=subprocess.check_output(['git','-C',str(root),'show','7cfdf9f73ae2a064ee4f281461e661301cb2dd65:'+str(module.SOURCES/'cloud_migrate_layout')])
    actual=(f.path/'repo/cloud_migrate_layout').read_bytes()
    assert actual==expected
    results.append({'case':'historical ref restores deleted helper exactly','status':'PASS','sha256':hashlib.sha256(actual).hexdigest()})
output=root/'docs/qa-logs/2026-10-07-manual-cloud-setup/qa-routing/results.json'
output.write_text(json.dumps({'scope':'local runner routing only; no VM or cloud commands executed','cases':results},indent=2)+'\n')
print(len(results),'PASS; temporary fixture removed; no VM or cloud calls')
