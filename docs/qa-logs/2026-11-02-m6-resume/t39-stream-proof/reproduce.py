#!/usr/bin/env python3
"""Read the candidate and named immutable artifacts; print counts, write nothing."""
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = '/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
TIP = '96ef183aae39da587e5dc51d19d7c1fc9e850704'
AUDIT = 'docs/audits/2026_11_01-epic-m6-doctrine-reference/'

def show(path):
    return subprocess.check_output(['git', '-C', REPO, 'show', f'{TIP}:{path}'], text=True)

def rows(section):
    return [[c.strip() for c in line.strip('|').split('|')]
            for line in section.splitlines() if line.startswith('| `')]

candidate = Path('/tmp/m6-lane-progress/t39-streams-v1.md').read_bytes()
brief = candidate.decode()
route = [item for line in brief.splitlines() if line.startswith('| PL-')
         for item in re.findall(r'PL-\d+', line.split('|')[1])]
forward = show(AUDIT + '02-forward-audit.md')
coverage = rows(forward.split('## Coverage\n', 1)[1].split('\n## ', 1)[0])
classes = {r[0].strip('`'): r[5] for r in coverage}
q5 = show(AUDIT + 'stage-c/tables/q5.md')
low = rows(q5.split('| low-inbound document |', 1)[1])
stream_text = brief.split('## S1 ', 1)[1].split('## S6 ', 1)[0]
named = sorted(set(re.findall(r'`((?:docs/[^`\s]+|README\.md))`', stream_text)))
explicit = {p: classes.get(p, 'ABSENT') for p in named}
edit_paths = {p for p, c in explicit.items() if c in ('edit-scope', 'edit-under-naming')}
edit_paths.update(r[0].strip('`') for r in low if r[2] == 'edit-scope')
runbook = show('docs/device-flashing-runbook.md')
menu = show('docs/es-menu-map.md')
log = show(AUDIT + '00-running-log.md')
print(json.dumps({
    'candidate_sha256': hashlib.sha256(candidate).hexdigest(),
    'routing': {'items': len(route), 'unique': len(set(route)),
                'missing': sorted({f'PL-{i:02d}' for i in range(1,47)} - set(route)),
                'duplicates': [k for k,v in collections.Counter(route).items() if v > 1]},
    'coverage_rows': len(coverage),
    'coverage_kinds': dict(collections.Counter(r[4] for r in coverage)),
    'coverage_classes': dict(sorted(collections.Counter(r[5] for r in coverage).items())),
    'q5_lower_table': {'files': len(low), 'logical_lines': sum(int(r[1]) for r in low),
                       'classes': dict(collections.Counter(r[2] for r in low)),
                       'ledger': [r[0].strip('`') for r in low if r[2] != 'edit-scope']},
    'explicit_S1_S4_paths': explicit,
    'S1_S5_unique_edit_population': len(edit_paths),
    'runbook_ROCKNIX_matching_lines': sum('ROCKNIX' in l for l in runbook.splitlines()),
    'runbook_ROCKNIX_occurrences': runbook.count('ROCKNIX'),
    'map_pending_headings': [(i,l) for i,l in enumerate(menu.splitlines(),1)
                             if re.search(r'^#+ .*(Pending|under qualification)',l)],
    'accepted_proof_cells': forward.count('proved:'),
    'accepted_PROOF_lines': sum(l.startswith('PROOF:') for l in log.splitlines())
}, indent=2))
