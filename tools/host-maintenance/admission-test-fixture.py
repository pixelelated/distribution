"""Synthetic host-only admission inputs. Never authorizes production allocation."""
import importlib.machinery
import importlib.util
import json
import subprocess
from pathlib import Path


def load(path, name='admission_fixture_module'):
    loader=importlib.machinery.SourceFileLoader(name,str(path))
    spec=importlib.util.spec_from_loader(loader.name,loader)
    mod=importlib.util.module_from_spec(spec);loader.exec_module(mod);return mod


def prepare_fixture(root, source):
    folder=root/'tools/host-maintenance';folder.mkdir(exist_ok=True)
    for name in ['build-admission','retention-report']:
        (folder/name).write_bytes((source/'tools/host-maintenance'/name).read_bytes())
    kept=root/'kept';kept.mkdir();(kept/'measurement.json').write_text('{"synthetic_required_bytes":1048576}\n')
    for args in [['init','-q'],['add','tools','scripts','Makefile'],['-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic admission fixture']]:
        subprocess.run(['git',*args],cwd=root,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    mod=load(folder/'build-admission')
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
    af=root/'admission-plan.json';af.write_text(json.dumps(ap));receipt=root/'admission.json';mod.prepare(af,receipt)
    return mod,af,receipt
