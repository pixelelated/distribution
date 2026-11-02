#!/usr/bin/env python3
"""Derive an isolated D226 T41 candidate from pinned t36 shared code.
Only the verdict/counter/mask/summary code is shared; section predicates are T41's.
This file is owned by Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
Never installs into the shared kit. No environment override of the source hash.
"""
import ast, hashlib, os, pathlib as P, re, sys
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
SOURCE_SHA='e32e28e0145570008d08493594795a878c442e88ed9fb3aac70f95e10d6b5b1b'
def refuse(s):raise ValueError(s)
def unique(s,needle):
    if s.count(needle)!=1:refuse('unmatched replacement shape: '+repr(needle[:80]))
    return s.index(needle)
def replace(s,old,new):
    unique(s,old);return s.replace(old,new)
def confined(path):
    path=P.Path(path).absolute()
    if not path.is_relative_to(OWN) or path==OWN or path.resolve()!=path:refuse('destination escapes owned directory or follows symlink')
    if path.exists() and (not path.is_file() or path.stat().st_nlink!=1):refuse('destination is not a private regular file')
    return path
BOOT=r'''#!/bin/bash
# GENERATED D226 candidate. Accepted producers are reconciled, never replayed.
# Not installed, not a final acceptance; coordinator retains rulings and acceptance.
# Shared verdict/mask/summary from t36-accept.sh, exact pinned SHA below.
# SOURCE_SHA=e32e28e0145570008d08493594795a878c442e88ed9fb3aac70f95e10d6b5b1b
# Author: Codex (GPT-6), /root, wN:p5; session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
# AUDIT_ISSUE=N BUGS="N ..." DISPATCH_TIP=HASH bash t41-accept.sh LANE_TIP COORD_TIP
# ACCEPT_ONLY and ACCEPT_FIXTURE_ROOT select constructed section fixtures only.
# New final gates run in disposable owned clones. Never execute accepted producers.
set -u
set -o pipefail
umask 077
export LC_ALL=C
OWN=/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12
ACCEPT_DIR=${ACCEPT_DIR:-$OWN/run}
OUT=${OUT:-$OWN/run.out}
ACCEPT_ONLY=${ACCEPT_ONLY:-}
export DIST_REPO=${DIST_REPO:-/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649}
export ACCEPT_ONLY ACCEPT_DIR
# Refuse before any write. Both destination files and ancestors must resolve inside
# the assigned root, with no symlink or hardlink targets. No cleanup/deletion.
python3 -I - "$OWN" "$ACCEPT_DIR" "$OUT" "${ACCEPT_FIXTURE_ROOT:-}" <<'T41_PATH_GUARD'
import os,pathlib,sys
root=P=pathlib.Path(sys.argv[1]);root=root.absolute()
try:
 if root.resolve()!=root:raise ValueError()
 accept=pathlib.Path(sys.argv[2]);out=pathlib.Path(sys.argv[3])
 if accept.exists() and not accept.is_dir():raise ValueError()
 if out.exists() and not out.is_file():raise ValueError()
 if out.absolute()==(accept/'verdicts.tsv').absolute():raise ValueError()
 for raw in sys.argv[2:]:
  if not raw:continue
  p=pathlib.Path(raw).absolute()
  if p==root or not p.is_relative_to(root) or p.resolve()!=p:raise ValueError()
  if p.exists() and p.is_file() and p.stat().st_nlink!=1:raise ValueError()
 for raw in [sys.argv[2]+'/verdicts.tsv']:
  p=pathlib.Path(raw)
  if p.is_symlink() or (p.exists() and (not p.is_file() or p.stat().st_nlink!=1)):raise ValueError()
except (ValueError,OSError):sys.exit(1)
T41_PATH_GUARD
rc=$?
if [ "$rc" -ne 0 ]; then
 printf 'VERDICT FAIL confinement -- output or fixture path is not private to the assigned directory\nSUMMARY: pass 0, fail 1, cannot 0, absent 0, ran 0\nACCEPT-RC 1\n'
 exit 1
fi
if [ "$#" -ne 2 ] || [ -z "${DISPATCH_TIP:-}" ] || [ -z "${AUDIT_ISSUE+x}" ] || [ -z "${BUGS+x}" ]; then
 printf 'VERDICT FAIL arguments -- two tips, DISPATCH_TIP, AUDIT_ISSUE and BUGS required\nSUMMARY: pass 0, fail 1, cannot 0, absent 0, ran 0\nACCEPT-RC 1\n'
 exit 1
fi
TIP=$1
COORD=$2
mkdir -p -- "$ACCEPT_DIR" "$(dirname -- "$OUT")"
rc=$?
[ "$rc" -eq 0 ] || exit 1
'''
def derive(src,dst):
    raw=P.Path(src).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:refuse('changed shared-source SHA256')
    s=raw.decode();a=unique(s,'np=0; nf=0; nc=0; na=0; nr=0; S=\n');b=unique(s,'run() {\n')
    if a>=b:refuse('shared helper anchors out of order')
    helper=s[a:b]
    # Counted shape checks remain independent of the immutable-source guard.
    helper=replace(helper,"section() { S=$1; printf '\\n== %s\\n' \"$2\"; }", "section() { S=$1; printf '\\n== %s\\n' \"$2\"; }")
    helper=replace(helper,"printf 'VERDICT %s %s -- %s\\n'", "printf 'VERDICT %s %s -- %s\\n'")
    mask=[l for l in s.splitlines() if l.startswith('MASK=')]
    if len(mask)!=1:refuse('shared mask shape')
    a=unique(s,'# ---------------------------------------------------------------- summary\n')
    summary=s[a:]
    summary=replace(summary,'\ncensus\n','\n# No host/runtime census in T41.\n')
    engine=P.Path(__file__).with_name('t41_checks.py').read_text()
    marker="\nif __name__=='__main__':"
    unique(engine,marker)
    additions='\n'.join(P.Path(__file__).with_name(n).read_text() for n in ['t41_reconcile.py','t41_execution.py'])
    engine=engine.replace(marker,'\n'+additions+marker)
    ast.parse(engine)
    match=re.search(r"^SECTIONS='([^']+)'\.split\(\)$",engine,re.M)
    if not match:refuse('section registry shape')
    names=match[1].split()
    if len(names)!=len(set(names)):refuse('duplicate sections')
    if 'T41_CANDIDATE_PREDICATES' in engine:refuse('embedded heredoc collision')
    wrapper='''\nmain() {\nprintf 'T41 D226 candidate: retained producer reconciliation and executable final gates\\n'\n[ -n "${ACCEPT_FIXTURE_ROOT:-}$ACCEPT_ONLY" ] && printf 'SELF-TEST MODE: section fixtures; never final acceptance\\n'
python3 -I - "$TIP" "$COORD" > "$ACCEPT_DIR/verdicts.tsv" <<'T41_CANDIDATE_PREDICATES'\n'''+engine+'''\nT41_CANDIDATE_PREDICATES\nrc=$?\nif [ "$rc" -ne 0 ]; then\n section internal "candidate predicate process"\n verdict FAIL "predicate process did not finish"\nelse\n while IFS=$'\\t' read -r state name reason; do\n  case "$state" in PASS|FAIL|CANNOT|ABSENT|RAN) ;; *) state=FAIL; reason="invalid predicate state";; esac\n  section "$name" "$name"\n  verdict "$state" "$reason"\n done < "$ACCEPT_DIR/verdicts.tsv"\n if [ $((np + nf + nc + na + nr)) -eq 0 ]; then\n  section internal "empty candidate result"\n  verdict FAIL "no sections checked"\n fi\nfi\n'''
    text=BOOT+'\n'+mask[0]+'\n'+helper+wrapper+summary
    # The prospective authority must remain explicit, and accepted producers stay read-only.
    if 'D226 exact negative input identities absent' not in text or 'D226 final gates' not in text:refuse('D226 reconciliation/execution boundary missing')
    dest=confined(dst)
    if not dest.parent.is_dir():refuse('destination parent absent')
    flags=os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW
    fd=os.open(dest,flags,0o600)
    with os.fdopen(fd,'w') as f:f.write(text)
    print('DERIVED',len(names),'sections; source',SOURCE_SHA,'output',hashlib.sha256(text.encode()).hexdigest())
if __name__=='__main__':
    try:
        if len(sys.argv)!=3:refuse('usage: derive-t41.py source destination')
        derive(*sys.argv[1:])
    except (ValueError,OSError,SyntaxError) as e:
        print('REFUSED:',e);sys.exit(1)
