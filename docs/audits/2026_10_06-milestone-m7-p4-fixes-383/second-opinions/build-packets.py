#!/usr/bin/env python3
"""Compose a reproducible criterion/source/evidence packet; no provider invocation."""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent.parent; ROOT=A.parents[2]; OUT=A/'second-opinions'
C=json.loads((A/'inputs/scoped-criteria.json').read_text())['rows'];V=json.loads((A/'evidence/forward-verdicts.json').read_text());cm={r['id']:r for r in C}
neutral={
'I352-L33':'cloud_setup --content-location production source and seven actual candidate14 case outputs are included below (content-probe01 and repeatedrefutation03). Cloud/pointer before/after hashes are in the raw result records.',
'I352-L44':'Same production setup path and raw seven-case outputs below; ES consumer is included with source line numbers.',
'I356-L76':'cloud_migrate_layout read_marker and cloud_scan read_folder/why_for_rc source included. UI26 future-script output and refusal text are in the retained excerpt. Before/after target hashes establish write refusal.',
'I363-L76':'cloud_scan --folder source and actual UI26 transcript below; opening scan/state scope and output semantics are separately inspectable.',
'I351-L62':'D-CLOUD-164 text and actual cloud_oauth phone confirmation plus cloud-signin-window FINISHING_PAGE source are included. Exact installed payload equality was verified; no new French-mode runtime run is supplied.',
'I462-L31':'Installed phone/window payload continuity and EN target frame receipts retained; assess required languages against source and approved contract.',
'I354-L69':'D-CLOUD-164 approves thirteen strings with French; current ES catalog and standalone phone/window sources are in the packet. Public website work is ordered P5.'}
parts=['''# Independent blind code review — pixelelated M7 P4, Milestone tier

You are the external Anthropic reviewer in a two-model code audit, not a five-seat council. You cannot open files or run tools: all source and observations you may cite are in this packet. Primary verdicts, hypotheses, prior-audit answers and proposed findings are withheld. Find defects, unsafe interactions, scope/evidence gaps and contradictions independently. For each item give a stable ID B-01 etc., severity Critical/High/Medium/Low, precise packet file:line, concrete trigger, actual versus required behavior, and a falsifying observation. Distinguish an observed code defect from an unexecuted exact criterion. State what you cannot judge. Do not assume a missing excerpt proves missing code. Do not treat future P5 device/publication work as newly discovered implementation failure.

Frozen distribution7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2, ESf6f0c134212bc696f2f6a747c8d390a588f2f0ce, proxy879b158995d412af434301ebdae581f66b8b6d57; immutable bundleb77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1. Current scope is P1–P3 product fixes and qualified VM behavior; P5 physical/device/source/publication is subsequent. New identity is lowercase pixelelated; only ROCKNIX→pixelelated adoption is required. Stored interfaces and upstream credits remain compatible. Dropbox authenticated trust-page observation is owner-waived as a gate; WebDAV/SFTP/S3 local runtime and dedicated RA real award have run. No product edits occurred during the audit.

Evidence domain: actual14 is current;09→10 changed rendering,10→14 changed proxy/native/consent only. Older target evidence is reused only for byte-identical relevant installed payloads, never asserted as a fresh current14 run. Host controls are not target execution. A synthetic local HTTP flusher test is not a real provider run. No physical-board observation is inferred from a VM.

## Exact forward criteria and primary observations (verdict columns removed)
''']
for v in V:
 c=cm[v['id']];parts.append(f"\n### {v['id']} — {c['file']}:{c['line']}\n\nRequirement: {c['text']}\n\nArtifact observations: {neutral.get(v['id'],v['evidence'])}\n")
# Supply actual changed source, not only the primary reader's references.
paths=[A/'inputs/distribution-product-diff.patch',A/'inputs/es-diff.patch']
R=ROOT/'projects/ROCKNIX/packages/network/rclone/sources'
paths += [R/n for n in ['cloud_setup','cloud_scan','cloud_migrate_layout','cloud_content_backup','cloud_content_restore']]
segments=[(R/'cloud_oauth',570,780),(R/'cloud_oauth',975,1190),(ROOT/'projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c',420,480),(Path('/home/max/Development/emulationstation-next.worktrees/qa-integration/es-app/src/guis/GuiMenu.cpp'),4860,4910),(Path('/home/max/Development/emulationstation-next.worktrees/qa-integration/es-app/src/guis/GuiMenu.cpp'),5185,5270)]
paths += [A/'evidence/refutation-03/probe.py',A/'evidence/refutation-03/artifacts/results.json',A/'evidence/refutation-03/console.log',A/'evidence/proxy-source-equality.json',A/'evidence/memory-recalculation.json',ROOT/'docs/qa-logs/2026-10-06-ra-ui/qualification.json']
files=[]
def include(p,start=None,end=None):
 data=p.read_text();lines=data.splitlines();lo=start or 1;hi=min(end or len(lines),len(lines));label=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p);parts.append('\n## SOURCE '+label+(f':{lo}–{hi}' if start else '')+'\n\n```text\n'+'\n'.join(f'{i}: {lines[i-1]}' for i in range(lo,hi+1))+'\n```\n');files.append({'path':label,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':[lo,hi]})
for p in paths:include(p)
for p,lo,hi in segments:include(p,lo,hi)
# Exact approved language contract, and actual refusal text, with no diagnosis.
dec=ROOT/'docs/decision-register.md'
for i,l in enumerate(dec.read_text().splitlines(),1):
 if l.startswith('| D-CLOUD-164 '):parts.append(f'\n## {dec.relative_to(ROOT)}:{i}\n\n{l}\n')
q=ROOT/'docs/qa-logs/2026-10-05-pixelelated-replacement-09'
for p in sorted(q.rglob('*UI26*')):
 if p.suffix in ['.log','.txt'] and p.stat().st_size<50000:include(p)
blind='\n'.join(parts);(OUT/'claude-blind-brief.md').write_text(blind)
manifest={'frozen_distribution':'7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','frozen_es':'f6f0c134212bc696f2f6a747c8d390a588f2f0ce','criteria':len(V),'primary_verdict_fields_included':False,'prior_comparison_included':False,'source_excerpt_inputs':files,'brief_sha256':hashlib.sha256(blind.encode()).hexdigest(),'brief_bytes':len(blind.encode())};(OUT/'blind-packet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:manifest[k] for k in ['criteria','brief_sha256','brief_bytes']},indent=2))
