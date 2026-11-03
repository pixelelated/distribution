"""New desired-wording proof for the one authorized README paragraph."""
import argparse,hashlib,json,pathlib,subprocess,sys
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];E=A/'stage-e';p=argparse.ArgumentParser();p.add_argument('--input',required=True);a=p.parse_args();c=json.loads((E/'source-contract.json').read_text());before=(E/'source/before.md').read_bytes();b=pathlib.Path(a.input).read_bytes();expected=before[:-len(c['old_paragraph'].encode())]+c['replacement_paragraph'].encode();target=(R/'docs/audits'/ '../../.claude/rules/instruction-files.md').resolve();canonical=target.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
assert sha(before)=='17269ce0820878e809890a9f737cd665c77d32ff07a20e779aed4fac1b745d79' and len(before)==666
assert sha(canonical)=='ca638c32b6bbf991c02a865b9c3ab19279416806e7baa0a320713989610da845'
result={'input':a.input,'bytes':len(b),'sha256':sha(b),'before_sha256':sha(before),'exact_delta':b==expected,'canonical_target':str(target.relative_to(R)),'canonical_sha256':sha(canonical),'desired_wording':b==expected and len(b)==813 and sha(b)==c['expected_after_sha256']}
print(json.dumps(result,sort_keys=True));print(('PASS' if result['desired_wording'] else 'REFUSE')+' desired paths/every-session wording and exact paragraph delta');sys.exit(0 if result['desired_wording'] else 1)
