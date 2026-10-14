#!/usr/bin/env python3
"""Static AST/hash/bash-parser checks only; do not import prepared runner modules."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def assigned(tree,name):
    found=[n.value for n in tree.body if isinstance(n,ast.Assign)
           and any(isinstance(x,ast.Name) and x.id==name for x in n.targets)]
    assert len(found)==1,name
    return ast.literal_eval(found[0])


def functions(tree):
    return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}


def main():
    assert sys.flags.optimize==0
    binding=json.loads((HERE/'bindings.json').read_text())
    prior=Path(binding['lifecycle_source_path'])
    trees={p.name:ast.parse(p.read_bytes(),filename=str(p),feature_version=(3,10)) for p in HERE.glob('*.py')}
    for name,digest in binding['lifecycle_input_sha256'].items():assert sha(prior/name)==digest
    for name in binding['unchanged_copies']:assert (HERE/name).read_bytes()==(prior/name).read_bytes()
    old_common=functions(ast.parse((prior/'common.py').read_bytes()))
    new_common=functions(trees['common.py'])
    unchanged=[name for name in old_common if name not in ('source_root','verify_source')]
    assert all(old_common[n]==new_common[n] for n in unchanged)
    old_run=functions(ast.parse((prior/'run-stage.py').read_bytes()))
    new_run=functions(trees['run-stage.py'])
    assert all(old_run[n]==new_run[n] for n in ('replace_state','disk_usage','verify_inputs'))
    old_inner=ast.parse((prior/'inner.py').read_bytes())
    assert functions(old_inner)['telemetry']==functions(trees['inner.py'])['telemetry']
    assert functions(old_inner)['disk_usage']==functions(trees['inner.py'])['disk_usage']
    for name in ('sample','child'):
        old=next(n for n in ast.walk(old_inner) if isinstance(n,ast.FunctionDef) and n.name==name)
        new=next(n for n in ast.walk(trees['inner.py']) if isinstance(n,ast.FunctionDef) and n.name==name)
        assert ast.dump(old)==ast.dump(new),name
    assert assigned(trees['common.py'],'SEQUENCES')=={'chdman':binding['stages']}
    assert assigned(trees['common.py'],'LIMITS')=={'chdman':1800}
    plan=HERE/'plan';assert sha(plan/'SHA256SUMS')==binding['sealed_plan_manifest_sha256']
    original=prior.parent/'2026-10-13-rvz-regression-source/format-tool-build-plan'
    for p in plan.iterdir():assert p.is_file() and p.read_bytes()==(original/p.name).read_bytes(),p.name
    for line in (plan/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);assert sha(plan/name)==digest,name
    inputs=json.loads((plan/'input-bindings.json').read_text())
    assert inputs['chdman']['archive']['bytes']==213471628
    assert inputs['chdman']['archive']['sha256']=='4867bee5dbd4129e6eea095fe8f8e9725563998710cc9620190e90529ef8931b'
    assert inputs['chdman']['members']==33835 and inputs['chdman']['regular_bytes']==897821359
    exports=[n for n in ast.walk(trees['export.py']) if isinstance(n,ast.Call)]
    assert not any(isinstance(n.func,ast.Attribute) and n.func.attr in ('extract','extractall') for n in exports)
    assert any(isinstance(n.func,ast.Attribute) and n.func.attr=='extractfile' for n in exports)
    run=(HERE/'run-stage.py').read_text();inner=(HERE/'inner.py').read_text()
    for flag in ["'--network','none'","'--read-only'","'--memory','4g'","'--memory-swap','4g'","'--cpus','2'","'--pids-limit','256'","'--pull=never'"]:
        assert flag in run,flag
    assert "time.monotonic()+LIMITS[family]" in run and "if not clock.exists():" in run
    assert "['bash','/plan/build-stage.sh',stage]" in inner
    assert 'dolphin-' not in run+inner+(HERE/'plan.py').read_text()
    shell=subprocess.run(['bash','-n',str(plan/'build-stage.sh')],capture_output=True,timeout=10)
    assert shell.returncode==0,shell.stderr.decode()
    print(json.dumps({'status':'STATIC_ONLY_PASS','python_3_10_grammar':sorted(trees),
       'unchanged_lifecycle_files':binding['unchanged_copies'],
       'unchanged_common_functions':unchanged,'unchanged_host_functions':['replace_state','disk_usage','verify_inputs'],
       'unchanged_inner_functions':['telemetry','disk_usage','sample','child'],
       'sealed_plan_byte_identical':True,'build_stage_sha256':sha(plan/'build-stage.sh'),
       'patch_sha256':sha(plan/'chdman-shared-libstdcxx.patch'),'bash_n_exit':shell.returncode,
       'stages':binding['stages'],'family_seconds':1800,
       'runner_imported':False,'archive_exported':False,'configure_build_container_or_target_execution':False,
       'runtime':'UNRUN; no behavior/readiness claim from AST or prior lifecycle qualification'},indent=2))


if __name__=='__main__':main()
