#!/usr/bin/env python3
"""T45 (#692): the 52-row provenance table, from the inventory rows, the bytes
against the export's SUMS at 8ebaf8daad and on the branch, the pins on both
trees, the IMPORTED-FROM adaptation items and the last fork commit.
    python3 -I provenance.py <worktree>   (prints Markdown rows and a JSON sidecar)
"""
import json, subprocess, sys
from pathlib import Path

W = Path(sys.argv[1]); S = W / '.qa-scratch/t45'
HASH = '8ebaf8daad'
def git(*a):
    return subprocess.run(['git', '-C', str(W), *a], capture_output=True, text=True, check=True).stdout
rows = {r['path']: r for r in json.loads((S / 'rows.json').read_text())}
def prov(f):
    return {l.split()[0]: l.split()[-1] for l in (S / f).read_text().splitlines()}
at, br = prov('provenance-8ebaf8daad.txt'), prov('provenance-HEAD.txt')
pins_at = json.loads(git('show', f'{HASH}:verifier-pins.json'))['pins']
pins_br = json.loads((W / 'verifier-pins.json').read_text())['pins']
delta = set(git('diff', '--name-only', HASH, 'HEAD', '--', *rows).split())
# The adaptation items of IMPORTED-FROM.md (at the hash) that account for a file's bytes, read from the
# list and checked in 02 by marker: 1 the anchor on the fork's repository (run-start; the two Forge tests),
# 2 the wordlist sweep, 3 the ten fixture literals built at run time, 5 the five-seat description.
items = {
    'scripts/council-run-start.ts': '1, 2',
    'scripts/council-toolchain.node-test.mjs': '1, 2',
    'scripts/council-invoke.ts': '2',
    'scripts/forge-write-status.mjs': '2',
    'scripts/lint-council-run.ts': '2',
    'seed/corpus/manifest.json': '2',
    'scripts/__tests__/council-invoke-routing.node-test.ts': '2, 3',
    'scripts/__tests__/lint-council-seat-efforts.node-test.ts': '3',
    'verifier-pins.json': '2 (one pin reason); the re-pins',
}
out = []
for p in sorted(rows):
    r = rows[p]
    pa, pb = pins_at.get(p), pins_br.get(p)
    def pin(v):
        if not v: return 'no'
        ra = (v.get('repinned_at') or '')[:10]
        r = (v.get('repin_reason') or '')
        tag = r.split(':', 1)[0].split(' (')[0][:28] if r else ''
        if r.startswith('Preserve'): tag = 'scaffold (no issue named)'
        return f"yes, re-pinned {ra} ({tag})" if ra else 'yes'
    listed = 'unlisted' if at[p] == 'unlisted' else 'listed'
    eq = {'equal': 'yes', 'DIFFERS': 'no', 'unlisted': '--'}[at[p]]
    branch = 'equal to the hash' if p not in delta else ('changed by ' + ', '.join(
        c for c in ('033eb7ed23', '0ceb2994c5') if p in git('show', '--name-only', '--format=', c).split()))
    out.append({'path': p, 'lines': r['lines'], 'sums': listed, 'equal_at_hash': eq, 'pinned_at_hash': pin(pa),
                'pinned_on_branch': pin(pb), 'imported_from': items.get(p, '--'),
                'last_fork_commit': (r['last_fork_commit'] or '').split()[0], 'branch': branch,
                'branch_sums': br[p]})
for o in out:
    print(f"| `{o['path']}` | {o['lines']} | {o['sums']} | {o['equal_at_hash']} | {o['pinned_at_hash']} | "
          f"{o['imported_from']} | `{o['last_fork_commit']}` | {o['branch']}"
          f"{'' if o['branch'] == 'equal to the hash' else ' (pin: ' + o['pinned_on_branch'] + '; SUMS ' + o['branch_sums'] + ')'} |")
(S / 'provenance-table.json').write_text(json.dumps(out, indent=1))
print(len(out), 'rows', file=sys.stderr)
