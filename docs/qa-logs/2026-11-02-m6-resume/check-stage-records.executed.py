import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees')
OUT = pathlib.Path('/tmp/m6-resume-20261102')

def check(slug, sha, folder, stage):
    repo = ROOT / slug
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args])
    def blob(path):
        return git('show', f'{sha}:{folder}/{path}')
    def txt(path):
        return blob(path).decode()
    files = git('ls-tree', '-r', '--name-only', sha, '--', folder).decode().splitlines()
    names = {p.removeprefix(folder + '/') for p in files}
    required = ['00-running-log.md', '01-research-notes.md']
    if stage == 'C':
        required += ['02-forward-audit.md', '03-retrospective.md', '04-analysis.md',
                     '05-punch-list.md', 'second-opinions/review-plan.json',
                     'tools/t39-checks.sh', 'tools/t39-checks.py', 'tools/t39-tables.py',
                     'stage-c/checks-runs.out', 'stage-c/lint-pre-issue.out']
    assert all(p in names for p in required), 'required stage artifact absent'
    assert not any(p.startswith('guest-cycle/') for p in names)
    result = {'tip': git('rev-parse', sha).decode().strip(), 'folder': folder,
              'stage': stage, 'required_artifacts': len(required),
              'tree_files': len(names), 'verification': 'committed artifact inspection; historical tests not rerun'}
    if stage == 'C':
        plan = json.loads(txt('second-opinions/review-plan.json'))
        assert plan['depth'] == 'local' and plan['reviewers'] == []
        assert plan['tier_exception'] == 'D-WORKFLOW-184'
        assert [p for p in names if p.startswith('second-opinions/')] == ['second-opinions/review-plan.json']
        audit = txt('02-forward-audit.md')
        counts = {}
        for heading, expected in [('Coverage',254), ('Binaries',31), ('Art bytes',18)]:
            section = re.split(r'^## '+re.escape(heading)+r'(?: \([^\n]*\))?\n',audit,maxsplit=1,flags=re.M)[1].split('\n## ',1)[0]
            counts[heading] = len(re.findall(r'^\| `',section,re.M))
            assert counts[heading] == expected, counts
        assert audit.count('proved:') == len(re.findall(r'^PROOF:', txt('00-running-log.md'), re.M)) == 12
        assert len(set(re.findall(r'\bL-\d{2}\b', audit))) == 46
        summary = txt('stage-c/checks-runs.out')
        assert re.search(r'^i-baseline\s+rc=0\s+TOTAL: 13 of 13 steps$',summary,re.M)
        mutations = re.findall(r'^(ii-\S+)\s+rc=(\d+)', summary,re.M)
        refusals = re.findall(r'^(refuse-\S+)\s+rc=(\d+)',summary,re.M)
        assert len(mutations)==14 and all(rc=='1' for _,rc in mutations)
        assert len(refusals)==7 and all(rc=='2' for _,rc in refusals)
        for name,rc in mutations+refusals:
            raw=txt('stage-c/runs/'+name+'.out')
            assert re.search(r'rc\s*=\s*'+rc+r'\b',raw),name
        lint=txt('stage-c/lint-pre-issue.out')
        assert 'PASS pre-issue artifacts (does not certify resolution)' in lint and 'rc=0' in lint
        paths=txt('stage-a/paths.txt').splitlines()
        assert len(paths)==254
        assert git('diff','--name-only','86ebb6dffc',sha,'--',*paths)==b''
        result.update(counts=counts, proof_lines=12, leads=46, mutation_receipts=14,
                      refusal_receipts=7, scope_changed_paths=0, local_plan=plan['primary'])
    else:
        def normalize(s):
            return s.replace('\\u002d','-')
        paths=normalize(txt('stage-a/p1-qa-scratch/paths.txt')).splitlines()
        assert len(paths)==len(set(paths))==107
        block=normalize(txt('stage-a/block.out'))
        assert block==normalize(txt('stage-a/block-tip.out'))
        assert block==normalize(txt('stage-a/p1-qa-scratch/block-expected.txt'))
        assert len(block.splitlines())==99
        body=blob('stage-a/p1-qa-scratch/block.sh')
        assert hashlib.sha256(body).hexdigest().startswith('4d300124a6bf116f')
        sums={'splitlines':0,'newlines':0,'patch':0,'conf':0,'from':0,'subject':0}
        for path in paths:
            raw=git('show', '2174265e9c:'+path)
            assert raw==git('show','f03b64419f:'+path)==git('show',sha+':'+path)
            sums['splitlines']+=len(raw.splitlines());sums['newlines']+=raw.count(b'\n')
            if path.endswith('.patch'):
                sums['patch']+=1
                sums['from']+=bool(re.search(rb'^From:',raw,re.M))
                sums['subject']+=bool(re.search(rb'^Subject:',raw,re.M))
            else:sums['conf']+=1
        assert sums=={'splitlines':40474,'newlines':40473,'patch':106,'conf':1,'from':87,'subject':89},sums
        orders={device:len(txt('stage-a/order-'+device+'.txt').splitlines()) for device in ['GENERIC_X64','H700','SM8550']}
        assert orders=={'GENERIC_X64':8,'H700':42,'SM8550':65},orders
        assert 'PASS' in txt('stage-a/lint-local-pass.out')
        assert 'local-only cannot satisfy Epic/Milestone' in txt('stage-a/lint-local-fail.out')
        assert git('diff','--name-only','d7dd766659',sha,'--','*.patch','*.conf','packages','projects','tools','scripts')==b''
        result.update(membership=107, expected_lines=99, sums=sums, orders=orders,
                      scope_changed_paths=0, escaped_path_normalization='literal \\u002d to hyphen for comparison only')
    return result

results = [check('m6-doctrine-reference-686','c61bcdcb5f','docs/audits/2026_11_01-epic-m6-doctrine-reference','C'),
           check('m6-patches-shipped-kernel-688','cffe3f869c','docs/audits/2026_11_02-epic-m6-patches-shipped-kernel','A')]
(OUT/'stage-records.json').write_text(json.dumps(results,indent=2)+'\n')
for result in results:
    print('PASS stage record',result['stage'],result['tip'][:10],json.dumps({k:v for k,v in result.items() if k not in ['local_plan','folder','tip','stage']}))
