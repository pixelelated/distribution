#!/usr/bin/env python3
import copy,hashlib,importlib.util,json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('scan',R/'tools/final-record-scan.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
good=m.collect('commit','d4a25244a80c6459b22e044f6ae6d1e5dc946886');F=R/'stage-f/fixtures';F.mkdir(exist_ok=True)
cases=[('scan-missing',copy.deepcopy(good),1,'scan membership mismatch'),('scan-changed',copy.deepcopy(good),1,'scan byte identity mismatch'),('scan-positive',good,0,None)]
cases[0][1]['files'].pop(next(iter(good['files'])));cases[1][1]['files'][next(iter(good['files']))]['sha256']='0'*64
out=[]
for name,value,expected,reason in cases:
 f=F/(name+'.json');f.write_text(json.dumps(value,indent=2)+'\n');argv=['python3',str(R/'tools/final-record-scan.py'),'validate',str(f)]
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);(F/(name+'.stdout')).write_bytes(p.stdout);(F/(name+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==expected and (reason is None or reason.encode() in p.stderr)
 out.append({'name':name,'argv':argv,'exit':p.returncode,'fixture_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'reader_sha256':hashlib.sha256((R/'tools/final-record-scan.py').read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'expected_refusal':reason})
(R/'stage-f/scan-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS new scan controls: missing entry and changed identity refused, exact immutable S1 record manifest accepted; no source/producer replay')
