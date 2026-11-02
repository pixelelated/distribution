"""Pure immutable readback of T44's published audit manifest; never runs producers."""
import argparse,subprocess,json,hashlib,pathlib,os
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--ref',required=True);args=p.parse_args()
A='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
def git(*a):return subprocess.check_output(['git','-C',args.repo,*a],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
ref=git('rev-parse',args.ref+'^{commit}').decode().strip();mb=git('show',ref+':'+A+'stage-d/payload-manifest.json');m=json.loads(mb)
keys=set(git('ls-tree','-r','--name-only',ref,'--',A).decode().splitlines())
expected={A+x for x in m['files']}|{A+'stage-d/payload-manifest.json'}
assert keys==expected,('MANIFEST_KEYSET','not_committed',sorted(expected-keys),'not_manifested',sorted(keys-expected))
for path,row in m['files'].items():
    assert not path.startswith('/') and all(x not in ('','.','..') for x in path.split('/')),'NONCANONICAL_PATH'
    b=git('show',ref+':'+A+path);assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],('PAYLOAD_BYTES',path)
print(json.dumps(dict(ref=ref,audit_files=len(keys),payload_files_verified=len(m['files']),manifest_sha256=hashlib.sha256(mb).hexdigest(),result='PASS immutable committed payload exact keyset and bytes'),indent=2))
