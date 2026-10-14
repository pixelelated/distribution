#!/usr/bin/env python3
"""Static AST, source identity, whitespace and bash -n only; never import the fixture."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PACKET=Path(__file__).resolve().parent
ROOT=PACKET.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
report={'status':'FAIL','evidence':'static AST/hash/source/whitespace and bash -n only',
        'python':sys.version,'runtime':'UNRUN','checks':[]}
try:
    bindings_bytes=(PACKET/'bindings.json').read_bytes();bindings=json.loads(bindings_bytes)
    tree=ast.parse((PACKET/'fixtures/probe.py').read_text(),filename='fixtures/probe.py')
    constants={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    assert ast.literal_eval(constants['BINDINGS_SHA256'])==sha(bindings_bytes)
    for name,expected in bindings['fixture_inputs'].items():
        assert sha((PACKET/name).read_bytes())==expected,name
    for f in [PACKET/'fixtures/probe.py',PACKET/'static-check.py',PACKET/'source/proxy-main.py.txt']:
        ast.parse(f.read_text(),filename=str(f.relative_to(PACKET)))
    profile=ast.literal_eval(constants['PROFILE'])
    tables=ast.literal_eval(constants['TABLES'])
    assert len(tables)==11 and set(tables)=={'ipv4','wildcard4','mapped6','loopback6','wildcard6',
                                          'wrong-port','established','other-address','empty','missing','unreadable'}
    cases=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases')
    loops=[n for n in cases.body if isinstance(n,ast.For)]
    assert ast.literal_eval(loops[0].iter)==('0','1','','unknown')
    hardcore=next(n for n in loops[0].body if isinstance(n,ast.For))
    assert ast.literal_eval(hardcore.iter)==('0','1','','unknown')
    assert ast.literal_eval(loops[2].iter)==('disabled','empty-enabled','missing-token')
    report['prepared_cases_per_variant']=32+22+6+3
    report['prepared_script_invocations']=2*(32+22+6+3)
    before=(PACKET/'source/cheevos_dolphin.before.sh').read_text()
    after=(PACKET/'source/cheevos_dolphin.after.sh').read_text()
    assert (ROOT/bindings['product_path']).read_text()==after
    added=after[after.index('# The offline toggle routes'):after.index('cat <<EOF')]
    assert after.replace('hardcore_raw="${hardcore}"\n','',1).replace(added,'',1)==before
    assert after[after.index('cat <<EOF'):]==before[before.index('cat <<EOF'):]
    def predicate(s):
        start=s.index('proxy_listening() {\n');end=s.index('\n}\n',start)+3
        return s[start:end]
    listener=(PACKET/'source/ppsspp-listener.sh').read_text()
    assert predicate(after)==listener==predicate((PACKET/'source/cheevos_ppsspp.sh').read_text())
    report['listener_equal_ppsspp']=True
    report['original_body_preserved_except_additions']=True
    for relative,identity in bindings['distribution_references'].items():
        assert sha((ROOT/relative).read_bytes())==identity['sha256'],relative
    for relative,expected in bindings['dolphin_patch_sha256'].items():
        assert sha((ROOT/relative).read_bytes())==expected,relative
    for source in ['source/cheevos_dolphin.before.sh','source/cheevos_dolphin.after.sh','source/cheevos_ppsspp.sh']:
        argv=['bash','-n',str(PACKET/source)]
        got=subprocess.run(argv,capture_output=True,text=True,timeout=10)
        report['checks'].append({'argv':argv,'original_exit':got.returncode,'stdout':got.stdout,'stderr':got.stderr})
        assert got.returncode==0,source+' syntax failed'
    argv=['bash','-n']
    got=subprocess.run(argv,input=profile,capture_output=True,text=True,timeout=10)
    report['checks'].append({'argv':argv,'stdin':'synthetic PROFILE literal','original_exit':got.returncode,'stdout':got.stdout,'stderr':got.stderr})
    assert got.returncode==0,'synthetic profile syntax failed'
    argv=['git','diff','--check','--',bindings['product_path']]
    got=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=10)
    report['checks'].append({'argv':argv,'original_exit':got.returncode,'stdout':got.stdout,'stderr':got.stderr})
    assert got.returncode==0,'product whitespace failed'
    for f in PACKET.rglob('*'):
        if f.is_file() and f.name not in ('static-result.json','SHA256SUMS'):
            text=f.read_text()
            assert text.endswith('\n'),str(f)+' missing final newline'
            assert all(line.rstrip()==line for line in text.splitlines()),str(f)+' trailing whitespace'
    # Verify immutable819 and the separately committed review revision without
    # executing either packet's checks or prepared probes.
    report['prior_packet_entries_verified']={}
    for name in ('2026-10-14-proxy-rvz-source','2026-10-14-proxy-rvz-revision-source'):
        base=PACKET.parent/name;lines=(base/'SHA256SUMS').read_text().splitlines()
        for line in lines:
            expected,filename=line.split('  ',1)
            assert sha((base/filename).read_bytes())==expected,filename
        report['prior_packet_entries_verified'][name]=len(lines)
    report['bindings_sha256']=sha(bindings_bytes)
    report['before_sha256']=bindings['before_sha256'];report['after_sha256']=bindings['after_sha256']
    report['status']='PASS'
except BaseException as error:
    report['error']=type(error).__name__+': '+str(error)
    raise
finally:
    (PACKET/'static-result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
