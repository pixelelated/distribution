#!/usr/bin/env python3
"""Static AST/hash/source comparisons only. Never import or execute a fixture."""
import ast
import hashlib
import json
from pathlib import Path
import sys

PACKET=Path(__file__).resolve().parent
REPO=PACKET.parents[2]


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def functions(path,names):
    text=path.read_text()
    return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body
            if isinstance(n,ast.FunctionDef) and n.name in names}


def main():
    binding=json.loads((PACKET/'bindings.json').read_text());binding_sha=digest(PACKET/'bindings.json')
    files=sorted(PACKET.rglob('*.py'))
    for path in files:ast.parse(path.read_bytes(),filename=str(path))
    for relative,expected in binding['evidence_sha256'].items():
        assert digest(PACKET/relative)==expected,relative
    for relative,expected in binding['references'].items():assert digest(REPO/relative)==expected,relative
    package=REPO/'projects/ROCKNIX/packages/network/raofflineproxy'
    assert digest(package/'package.mk')==binding['recipe_sha256']
    assert {p.name:digest(p) for p in (package/'patches').glob('*.patch')}==binding['patches']
    assert binding['baseline'].keys()==binding['candidate'].keys()
    delta=[key for key,value in binding['baseline'].items() if binding['candidate'][key]!=value]
    assert delta==['linux/raofflineproxy/rvz_datasource.py'],delta
    assert binding['candidate'][delta[0]]==digest(PACKET/'evidence/rvz_datasource.py')
    ctl=(PACKET/'evidence/raofflineproxy-ctl').read_text()
    start=ctl.index("<<'PY'",ctl.index('list_jobs() {'))
    scanner=ctl[start:].split('\n',1)[1].split('\nPY\n',1)[0]+'\n'
    assert scanner.encode()==(PACKET/'evidence/list_jobs.py').read_bytes()
    for name in ('prepare.py','admit.py','run.py'):
        text=(PACKET/'fixtures'/name).read_text()
        assert "BINDINGS_SHA256='"+binding_sha+"'" in text,name
    transcript=PACKET/'preparation-offset-followup/qualified-source.json'
    assert digest(transcript)=='bbd19421935929cda116124199b0e81d0023cb8eb78ce627f3379ec76d61e3d6'
    qualified=json.loads(transcript.read_text())
    assert qualified['baseline']==binding['baseline']
    assert {r['name']:r['sha256'] for r in qualified['patches']}==binding['patches']
    attempt=json.loads((PACKET/'preparation-offset-followup/attempt01-source.json').read_text())
    original={r['name']:r for r in qualified['patches']}
    assert attempt['status']=='FAIL' and attempt['patches'][-1]['original_exit']==0
    assert all(r['stdout']==original[r['name']]['output'] and not r['stderr'] for r in attempt['patches'])
    names={'proc_identity','direct_children','signal_child'}
    original=REPO/'docs/qa-logs/2026-10-14-dolphin-proxy-routing-census-source/fixtures/probe.py'
    assert functions(original,names)==functions(PACKET/'fixtures/census.py',names)
    seal=json.loads((PACKET/'runner-seal.json').read_text())
    assert set(seal)=={'run.py','owner.py','census.py'}
    for name,expected in seal.items():assert digest(PACKET/'fixtures'/name)==expected,name
    assert not list(PACKET.rglob('*.pyc'))
    print(json.dumps({'status':'PASS','evidence':'static only; no fixture imports/execution',
        'python':sys.version,'ast_files':len(files),'evidence_files':len(binding['evidence_sha256']),
        'patches':len(binding['patches']),'bound_python_files':len(binding['candidate']),
        'candidate_delta':delta,'census_functions_identical':sorted(names),
        'bindings_sha256':binding_sha},indent=2))


if __name__=='__main__':main()
