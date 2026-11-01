#!/usr/bin/env bash
# T38 (#685) stage C: t38-checks.sh FAIL-first. One planted positive per probe, each on its own scratch copy of
# the export at the tip (never a checkout); the bundle's informational positive; and the refusals.
#   bash t38-checks-firstfail.sh <export> <repo> <tools-dir> <scratch> <outdir>
E=${1:?export}; R=${2:?repo}; T=${3:?tools}; S=${4:?scratch}; O=${5:?outdir}; G=/usr/bin/grep
case "$S" in /workspace/tmp/m6-t38/*) ;; *) echo "refused: scratch must be under /workspace/tmp/m6-t38/"; exit 2;; esac
mkdir -p "$S" "$O"
mk() { rm -rf "${S:?}/$1"; mkdir -p "$S/$1"; cp -a "$E/.claude" "$S/$1/"; }
run() { local name=$1 want=$2; shift 2
  bash "$T/t38-checks.sh" "$@" > "$O/$name.out" 2>&1; local rc=$?
  printf '%-34s want %s rc=%s | %s | %s\n' "$name" "$want" "$rc" "$($G -m1 '^TOTAL:' "$O/$name.out")" \
    "$($G -m1 -E '^      FAIL|refused' "$O/$name.out" | sed -E 's/^ +//' | cut -c1-120)"; }
args() { echo --tree "$1" --repo "$R" --commit HEAD --allow "$T" --out "$S/out-$2"; }
mk inventory; printf '# planted\n' > "$S/inventory/.claude/rules-planted.md"; mkdir -p "$S/inventory/.claude/rules"; printf '# planted\n' > "$S/inventory/.claude/rules/zz-planted.md"; rm "$S/inventory/.claude/rules-planted.md"
run inventory-outside-skills 1 $(args "$S/inventory" inventory)
mk front1; sed -i '1d' "$S/front1/.claude/skills/futro/SKILL.md"
run front-first-line-removed 1 $(args "$S/front1" front1)
mk front2; sed -i 's/^name: release-notes$/name: release-note/' "$S/front2/.claude/skills/release-notes/SKILL.md"
run front-name-not-directory 1 $(args "$S/front2" front2)
mk refs1; printf '\nSee [the planted reference](references/no-such-file.md).\n' >> "$S/refs1/.claude/skills/session-resume/SKILL.md"
run refs-no-such-reference 1 $(args "$S/refs1" refs1)
mk refs2; printf '\nRun `tools/no-such-tool` before the stash.\n' >> "$S/refs2/.claude/skills/begin-delivery/SKILL.md"
run refs-no-such-tool 1 $(args "$S/refs2" refs2)
mk stale; printf '\nInvoke the `rubber-duck` agent to challenge the plan.\n' >> "$S/stale/.claude/skills/futro/SKILL.md"
run stale-rubber-duck 1 $(args "$S/stale" stale)
mk roster; sed -i 's#"openai/gpt-6-astra (OpenRouter#"openai/gpt-5.6-sol (OpenRouter#' "$S/roster/.claude/agents/council-member-gpt.agent.md"
run roster-gpt-slug 1 $(args "$S/roster" roster)
mk pins; printf ' ' >> "$S/pins/.claude/agents/council-member-claude.agent.md"
run pins-one-byte 1 $(args "$S/pins" pins)
mk contract; sed -i 's/05-punch-list\.md/05-list.md/g' "$S/contract/.claude/skills/code-auditor/references/templates.md"
run contract-05-removed 1 $(args "$S/contract" contract)
mk bundle; python3 -I - "$S/bundle/.claude" <<'PY'
import hashlib, pathlib, sys
b = pathlib.Path(sys.argv[1]); s = b / "skills/council/COUNCIL-BUNDLE.SHA256SUMS"
lines = s.read_text().split("\n")
for i, l in enumerate(lines):
    if not l.strip():
        continue
    h, p = l.split(None, 1); p = p.lstrip("*")
    f = b / p[len(".claude/"):] if p.startswith(".claude/") else None
    if f and f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == h:
        lines[i] = "f" * 64 + l[64:]; break
s.write_text("\n".join(lines)); print("bundle: one matching entry's sum replaced")
PY
run bundle-one-sum-changed 0 $(args "$S/bundle" bundle)
printf '%-34s %s\n' "  (bundle line)" "$($G -m1 '^info' "$O/bundle-one-sum-changed.out")"
run refuse-no-tree 2 --repo "$R" --commit HEAD --allow "$T" --out "$S/out-r1"
mk checkout; mkdir -p "$S/checkout/.git"
run refuse-a-checkout 2 $(args "$S/checkout" r2)
PATH=/nonexistent /bin/bash "$T/t38-checks.sh" $(args "$E" r3) > "$O/refuse-no-python3.out" 2>&1; rc=$?
printf '%-34s want 2 rc=%s | %s\n' refuse-no-python3 "$rc" "$($G -m1 refused "$O/refuse-no-python3.out")"
run refuse-lint-unreadable 2 --tree "$E" --repo "$R" --commit 0000000000 --allow "$T" --out "$S/out-r4"
rm -rf "${S:?}/allow-bad"; mkdir -p "$S/allow-bad"; cp "$T"/allow-*.txt "$S/allow-bad/"; printf '.claude/skills/futro/SKILL.md:1 L-02\n' >> "$S/allow-bad/allow-findings.txt"
run refuse-entry-without-reason 2 --tree "$E" --repo "$R" --commit HEAD --allow "$S/allow-bad" --out "$S/out-r5"
rm -rf "${S:?}/allow-star"; mkdir -p "$S/allow-star"; cp "$T"/allow-*.txt "$S/allow-star/"; printf '.claude/skills/futro/SKILL.md:* L-15 a finding for every line\n' >> "$S/allow-star/allow-findings.txt"
run refuse-finding-with-star 2 --tree "$E" --repo "$R" --commit HEAD --allow "$S/allow-star" --out "$S/out-r6"
rm -rf "${S:?}/allow-gone"; mkdir -p "$S/allow-gone"; cp "$T"/allow-legit.txt "$T"/allow-inherited.txt "$S/allow-gone/"
run refuse-allowlist-missing 2 --tree "$E" --repo "$R" --commit HEAD --allow "$S/allow-gone" --out "$S/out-r7"
