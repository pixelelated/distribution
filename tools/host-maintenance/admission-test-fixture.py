"""Synthetic host-only admission inputs. Never authorizes production allocation."""
import importlib.machinery
import importlib.util
import json
import os
import subprocess
from pathlib import Path


def load(path, name='admission_fixture_module'):
    loader=importlib.machinery.SourceFileLoader(name,str(path))
    spec=importlib.util.spec_from_loader(loader.name,loader)
    mod=importlib.util.module_from_spec(spec);loader.exec_module(mod);return mod


def filesystem_reservation(root, state_home, amount):
    """Create an isolated schema-1 ledger matching the frozen filesystem route."""
    device, fsid = root.stat().st_dev, os.statvfs(root).f_fsid
    route = state_home / 'pixelelated' / 'build-admission' / f'{device:x}-{fsid:x}'
    route.mkdir(mode=0o700, parents=True)
    (route / 'lock').touch(mode=0o600)
    output = root / 'build.peer'
    output.mkdir()
    row = dict(id='filesystem-owner', state='running', required_bytes=amount, volume_device=device,
               volume=str(root), registry=str(route), checkout=str(root),
               run=str(root / '.build-runs/peer'),
               outputs=[dict(path=str(output), issue=493, kind='build-cache', release_when='fixture complete')])
    data = dict(schema=1, generation=1, jobs={row['id']: row})
    (route / 'jobs.json').write_text(json.dumps(data))
    return route, row


def fixture_registry_binding(root, scope):
    # Bind the synthetic default account root explicitly. Allow a fixture to
    # exercise XDG route changes inside its own scratch scope.
    return f'''
def registry_state_roots():
    root = Path({str(root.resolve())!r})
    scope = Path({str(scope.resolve())!r})
    state = Path(os.environ.get('XDG_STATE_HOME') or root / 'state')
    if not state.is_absolute() or '..' in state.parts or not state.is_relative_to(scope):
        state = root / 'state'
    return sorted({{str(root / 'default-state'), str(state)}})

'''


def prepare_fixture(root, source, configure=None, *, prepare=True, registry_scope=None):
    folder=root/'tools/host-maintenance';folder.mkdir(exist_ok=True)
    suppliers = source / 'tools' / 'host-maintenance'
    admission = folder / 'build-admission'
    body = (suppliers / 'build-admission').read_bytes()
    binding = fixture_registry_binding(root, registry_scope or root.parent)
    watched = (root / 'tools' / 'watch-build').is_file()
    if watched:
        # Bind the copied tool before its CLI entry. The fixture and all
        # watcher/CLI children then use the same bytes and receipt digest.
        marker = b'\nif __name__'
        assert body.count(marker) == 1, 'fixture admission entrypoint changed'
        before, after = body.split(marker)
        body = before + binding.encode() + marker + after
    admission.write_bytes(body)
    (folder/'retention-report').write_bytes((suppliers/'retention-report').read_bytes())
    kept=root/'kept';kept.mkdir();(kept/'measurement.json').write_text('{"synthetic_required_bytes":1048576}\n')
    for args in [['init','-q'],['add','tools','scripts','Makefile'],['-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic admission fixture']]:
        subprocess.run(['git',*args],cwd=root,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    mod=load(admission)
    if not watched:
        # The archive handoff tests compare the canonical supplier bytes.
        # Their direct, in-process calls can use the binding without a copy edit.
        exec(compile(binding, __file__, 'exec'), vars(mod))
    budget={'name':'fixture','terms_bytes':{'growth':1048576},'basis':'synthetic 1MiB test allowance; no compilation',
            'evidence':[{'path':str(kept/'measurement.json'),'sha256':mod.digest(kept/'measurement.json')}]}
    plan={'volume':str(root),'scan_roots':[str(root)],'reference_stores':[], 'protected':[str(kept)],'candidates':[],'builds':[budget]}
    rp=root/'retention-plan.json';rp.write_text(json.dumps(plan))
    report={'schema':1,'utc':mod.utc(),'result':'REPORT_COMPLETE','deletion_performed':False,'inventory':{'errors':[]},
            'plan_sha256':mod.digest(rp),'tool_sha256':mod.digest(folder/'retention-report'),
            'protected':[{'path':str(kept),'identity':mod.path_identity(kept)}],
            'builds':[dict(budget,required_bytes=1048576,fits_now=True)]}
    rr=root/'retention-report.json';rr.write_text(json.dumps(report))
    ap={'checkout':str(root),'retention_plan':str(rp),'retention_report':str(rr),'stage':'fixture',
        'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
        'outputs':[{'path':str(root/'build.fixture'),'issue':493,'kind':'build-cache','release_when':'synthetic fixture result accepted'}]}
    if configure is not None:
        configure(ap)
    af=root/'admission-plan.json';af.write_text(json.dumps(ap));receipt=root/'admission.json'
    if prepare:
        mod.prepare(af,receipt)
    return mod,af,receipt
