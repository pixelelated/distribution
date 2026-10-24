#!/bin/bash
# t10-guard-gaps.sh -- T10's constructed inputs for the shapes the guards'
# own suite (.githooks/hooks-test) does not construct. It runs a hooks
# directory and a forbidden-terms-check against a scratch repository,
# using hooks-test's method:
#   - the wordlist is a stand-in (FORBIDDEN_TERMS_FILE), never the real list;
#   - the credential-shaped value is built at run time from printf pieces,
#     so this file at rest carries no line a scanner would match;
#   - an output is never printed: only each case's exit code, and whether
#     the refusal redacted and stayed silent about the value.
#
#   t10-guard-gaps.sh <hooks-dir> <forbidden-terms-check> [scratch-parent]
#
# Each case prints `CASE <name>: rc=<n> <allowed|refused> [notes]`. A case
# the guard should refuse that prints `allowed` is a gap. Exit 0 when every
# case ran (whatever the verdicts); 2 when the scratch could not be made.
set -u
HOOKS="$(cd "${1:?hooks dir}" && pwd)"; FTC="$(readlink -f "${2:?forbidden-terms-check}")"
PARENT="${3:-/workspace/tmp}"
SCRATCH="$(mktemp -d -p "${PARENT}" t10-gaps.XXXXXX)" || exit 2
trap 'rm -rf "${SCRATCH}"' EXIT
FAKE="$(printf 'dev%s=%s' password QwErTyUiOpAsDfGh)"
WORD="$(printf 'zebra%s quartet' fish)"
printf "FORBIDDEN_PATTERNS='zebrafish[ ]quartet|qzx-estate'\\n" > "${SCRATCH}/wordlist"
export FORBIDDEN_TERMS_FILE="${SCRATCH}/wordlist"
unset FORBIDDEN_PATTERNS SECRET_PATTERNS_FILE
ZERO=0000000000000000000000000000000000000000
mkdir -p "${SCRATCH}/nohooks"
g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${SCRATCH}/nohooks" "$@"; }
report() {  # report <name> <rc>
  local v=allowed n=""; [ "$2" -ne 0 ] && v=refused
  grep -q -F -- "QwErTyUiOpAsDfGh" "${SCRATCH}/out" && n="${n} VALUE-PRINTED"
  grep -q -i -F -- "zebrafish" "${SCRATCH}/out" && n="${n} WORD-PRINTED"
  grep -q -F -- "[REDACTED]" "${SCRATCH}/out" && n="${n} redacted"
  grep -q -F -- "could not be read" "${SCRATCH}/out" && n="${n} (reason: a file could not be read)"
  grep -q -F -- "personal artifacts" "${SCRATCH}/out" && n="${n} (reason: personal artifacts)"
  grep -q -F -- "listed word" "${SCRATCH}/out" && n="${n} (reason: a listed word)"
  grep -q -F -- "credential-shaped" "${SCRATCH}/out" && n="${n} (reason: credential-shaped)"
  echo "CASE $1: rc=$2 ${v}${n}"
}
run() { local name="$1"; shift; "$@" >"${SCRATCH}/out" 2>&1; report "${name}" "$?"; }
push_line() { printf '%s\n' "$1" | "${HOOKS}/pre-push" origin "file://${SCRATCH}/remote.git"; }

cd "${SCRATCH}" && git init -q -b main work && cd work || exit 2
git init -q --bare "${SCRATCH}/remote.git" && git remote add origin "${SCRATCH}/remote.git"
echo base > a.txt; g add a.txt; g commit -q -m base; g push -q origin main; remote="$(git rev-parse HEAD)"

# --- pre-commit
printf 'x\0y\n%s\n' "${FAKE}" > b.bin; g add b.bin
run "pre-commit: a credential in a file git treats as binary (a NUL byte)" "${HOOKS}/pre-commit"
g reset -q; rm b.bin
printf 'x\0y\n%s\n' "${WORD}" > w.bin; g add w.bin
run "pre-commit: a listed word in a file git treats as binary" "${HOOKS}/pre-commit"
g reset -q; rm w.bin
printf 'msgid "x"\nmsgstr "%s"\n' "${FAKE}" > fr.po; g add fr.po
run "pre-commit: a credential in a .po file" "${HOOKS}/pre-commit"
g reset -q; rm fr.po
printf 'msgid "x"\nmsgstr "%s"\n' "${WORD}" > fr.po; g add fr.po
run "pre-commit: a listed word in a .po file" "${HOOKS}/pre-commit"
g reset -q; rm fr.po
printf '%s\n' "${FAKE}" > c.txt; g add c.txt
run "pre-commit: control, the same credential in a text file" "${HOOKS}/pre-commit"
g reset -q; rm c.txt

# --- commit-msg, through a real commit as git runs it (-m, default cleanup)
git checkout -q -b msg
echo m > m.txt; git add m.txt
git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${HOOKS}" commit -q -m 'tidy' -m "# the ${WORD} notes" >"${SCRATCH}/out" 2>&1; rc=$?
report "commit-msg: a listed word on a # line given with git commit -m" "${rc}"
echo "  the stored message keeps the # line: $(git log -1 --format=%B | grep -c '^# ') line(s)"
git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${HOOKS}" commit -q --allow-empty -m 'tidy' -m "the ${WORD} notes" >"${SCRATCH}/out" 2>&1; rc=$?
report "commit-msg: control, the same word on an ordinary line" "${rc}"
run "pre-push: the branch carrying the # line, pushed" push_line "refs/heads/msg $(git rev-parse HEAD~0) refs/heads/msg ${ZERO}"
git checkout -q main

# --- pre-push
g checkout -q -b bin "${remote}"; printf 'x\0y\n%s\n' "${FAKE}" > s.bin; g add s.bin; g commit -q -m s; g rm -q s.bin; g commit -q -m gone
run "pre-push: a credential in a binary file in a middle commit, gone at the tip" push_line "refs/heads/bin $(git rev-parse HEAD) refs/heads/bin ${ZERO}"
g checkout -q -b bintxt "${remote}"; printf '%s\n' "${FAKE}" > s.txt; g add s.txt; g commit -q -m s; g rm -q s.txt; g commit -q -m gone
run "pre-push: control, the same in a text file" push_line "refs/heads/bintxt $(git rev-parse HEAD) refs/heads/bintxt ${ZERO}"
g checkout -q -b po "${remote}"; printf 'msgid "x"\nmsgstr "%s"\n' "${FAKE}" > fr.po; g add fr.po; g commit -q -m po
run "pre-push: a credential in a .po file at the tip" push_line "refs/heads/po $(git rev-parse HEAD) refs/heads/po ${ZERO}"
g checkout -q -b powd "${remote}"; printf 'msgid "x"\nmsgstr "%s"\n' "${WORD}" > fr.po; g add fr.po; g commit -q -m po
run "pre-push: a listed word in a .po file at the tip" push_line "refs/heads/powd $(git rev-parse HEAD) refs/heads/powd ${ZERO}"
# a pr/* branch, one commit on upstream/next, adding a personal path whose name git quotes
g update-ref refs/remotes/upstream/next "${remote}"
g checkout -q -b pr/x "${remote}"; mkdir -p docs; echo note > "docs/$(printf 'caf\303\251').md"; g add docs; g commit -q -m 'x: a note'
run "pre-push: a pr/* branch adding docs/<non-ASCII name>.md (a personal path git quotes)" push_line "refs/heads/pr/x $(git rev-parse HEAD) refs/heads/pr/x ${ZERO}"
g -c core.quotePath=false log -1 >/dev/null
git config core.quotePath false
run "pre-push: the same with core.quotePath=false" push_line "refs/heads/pr/x $(git rev-parse HEAD) refs/heads/pr/x ${ZERO}"
git config --unset core.quotePath
g checkout -q -b pr/y "${remote}"; mkdir -p docs; echo note > docs/plain.md; g add docs; g commit -q -m 'y: a note'
run "pre-push: control, a pr/* branch adding docs/plain.md" push_line "refs/heads/pr/y $(git rev-parse HEAD) refs/heads/pr/y ${ZERO}"

# --- forbidden-terms-check
cd "${SCRATCH}" && git init -q -b main ftc && cd ftc || exit 2
ln -s "notes-on-the-${WORD// /-}" link; printf '%s\n' "${WORD}" > plain.txt; g add link plain.txt; g commit -q -m f
FORBIDDEN_PATTERNS='zebrafish[ -]quartet' run "forbidden-terms-check: a tree with a listed word in a file and one in a symlink's target" "${FTC}" "${SCRATCH}/ftc"
echo "  hits named: $(grep -c -E '^(link|plain\.txt):' "${SCRATCH}/out") ($(grep -o -E '^(link|plain\.txt)' "${SCRATCH}/out" | sort -u | tr '\n' ' '))"
rm plain.txt link
FORBIDDEN_PATTERNS='zebrafish[ -]quartet' run "forbidden-terms-check: the same tree with its tracked files deleted from the checkout" "${FTC}" "${SCRATCH}/ftc"
echo "  says: $(grep -o -E '[0-9]+ hits? in [0-9]+ tracked files' "${SCRATCH}/out")"
exit 0
