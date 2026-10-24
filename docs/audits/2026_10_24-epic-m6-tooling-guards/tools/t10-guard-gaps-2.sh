#!/bin/bash
# t10-guard-gaps-2.sh -- the second-opinion seats' constructed inputs (T10,
# Phase 4.6), built by the method of t10-guard-gaps.sh:
#   - a stand-in wordlist, never the real one;
#   - every credential-shaped value built at run time from printf pieces;
#   - nothing printed but each case's exit code and tags.
#
#   t10-guard-gaps-2.sh <hooks-dir> [scratch-parent]
#
# Each line reads `CASE <name>: rc=<n> <allowed|refused> [tags]`. The tags
# come from the hook's own refusal headings: `cred` for a credential
# refusal, `word` for a listed-word refusal, `unread` for a file the tip
# scan could not read, `personal` for the personal-path refusal, `nobase`
# for no base, `count` for the one-commit rule. VALUE-PRINTED or
# WORD-PRINTED marks output that carried the fixture. Exit 0 when every case
# ran.
set -u
HOOKS="$(cd "${1:?hooks dir}" && pwd)"; PARENT="${2:-/workspace/tmp}"
SCRATCH="$(mktemp -d -p "${PARENT}" t10-gaps2.XXXXXX)" || exit 2
trap 'rm -rf "${SCRATCH}"' EXIT
FAKE="$(printf 'dev%s=%s' password QwErTyUiOpAsDfGh)"
WORD="$(printf 'zebra%s quartet' fish)"
LOWER="$(printf 'pass%s = %s' word Ab12Cd34Ef56Gh78Ij90)"                 # a lowercase assignment
SLASHTOK="$(printf '"refresh_%s": "1//0%s"' token gAbCdEfGhIjKlMnOpQrStUvWx)" # a slash-bearing OAuth refresh token
printf "FORBIDDEN_PATTERNS='zebrafish[ ]quartet|qzx-estate'\\n" > "${SCRATCH}/wordlist"
export FORBIDDEN_TERMS_FILE="${SCRATCH}/wordlist"
unset FORBIDDEN_PATTERNS SECRET_PATTERNS_FILE
ZERO=0000000000000000000000000000000000000000
mkdir -p "${SCRATCH}/nohooks"
g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${SCRATCH}/nohooks" "$@"; }
report() {
  local v=allowed n=""; [ "$2" -ne 0 ] && v=refused
  grep -q -F -- "QwErTyUiOpAsDfGh" "${SCRATCH}/out" && n="${n} VALUE-PRINTED"
  grep -q -F -- "Ab12Cd34Ef56Gh78" "${SCRATCH}/out" && n="${n} VALUE-PRINTED"
  grep -q -i -F -- "zebrafish" "${SCRATCH}/out" && n="${n} WORD-PRINTED"
  grep -q -E -- "carries a credential-shaped|add a credential-shaped|adds a credential-shaped" "${SCRATCH}/out" && n="${n} cred"
  grep -q -E -- "carries a listed word|add a listed word|adds a listed word" "${SCRATCH}/out" && n="${n} word"
  grep -q -F -- "could not be read" "${SCRATCH}/out" && n="${n} unread"
  grep -q -F -- "personal artifacts" "${SCRATCH}/out" && n="${n} personal"
  grep -q -F -- "no upstream/next or origin/next" "${SCRATCH}/out" && n="${n} nobase"
  grep -q -F -- "commits past" "${SCRATCH}/out" && n="${n} count"
  echo "CASE $1: rc=$2 ${v}${n}"
}
run() { local name="$1"; shift; "$@" >"${SCRATCH}/out" 2>&1; report "${name}" "$?"; }
push_line() { printf '%s\n' "$1" | "${HOOKS}/pre-push" origin "file://${SCRATCH}/remote.git"; }

cd "${SCRATCH}" && git init -q -b main work && cd work || exit 2
git init -q --bare "${SCRATCH}/remote.git" && git remote add origin "${SCRATCH}/remote.git"
printf -- '-- old note\nkeep\n' > a.txt; g add a.txt; g commit -q -m base; g push -q origin main; remote="$(git rev-parse HEAD)"

# 1. the diff parser's header state (both seats): a deleted `-- ` line, then an added `++ b/` line
printf '++ b/%s\nkeep\n' "${FAKE}" > a.txt; g add a.txt
run "pre-commit: a deleted '-- ' line replaced by an added '++ b/<credential>' line" "${HOOKS}/pre-commit"
printf '++ b/the %s notes\nkeep\n' "${WORD}" > a.txt; g add a.txt
run "pre-commit: the same with a listed word" "${HOOKS}/pre-commit"
printf '++ %s\nkeep\n' "${FAKE}" > a.txt; g add a.txt
run "pre-commit: control, '++ <credential>' without b/ (hooks-test's shape)" "${HOOKS}/pre-commit"
g reset -q; git checkout -q -- a.txt
g checkout -q -b hdr "${remote}"; printf '++ b/%s\nkeep\n' "${FAKE}" > a.txt; g add a.txt; g commit -q -m h1; printf -- '-- old note\nkeep\n' > a.txt; g add a.txt; g commit -q -m h2
run "pre-push: the '++ b/<credential>' line in a middle commit, gone at the tip" push_line "refs/heads/hdr $(git rev-parse HEAD) refs/heads/hdr ${ZERO}"

# 2. history simplification (gpt G-01): a side branch adds and removes a credential; the merge equals its first parent
g checkout -q -b side "${remote}"; printf '%s\n' "${FAKE}" > s.txt; g add s.txt; g commit -q -m s1; g rm -q s.txt; g commit -q -m s2
g checkout -q -b mrg "${remote}"; echo more >> a.txt; g add a.txt; g commit -q -m m1; g merge -q --no-ff -m merge side
run "pre-push: a credential added and removed on a merged side branch" push_line "refs/heads/mrg $(git rev-parse HEAD) refs/heads/mrg ${ZERO}"
g checkout -q -b mrgword "${remote}"; g commit -q --allow-empty -m m1; g merge -q --no-ff -m merge side
run "pre-push: the same where the merge's only change is the side branch's (net nothing)" push_line "refs/heads/mrgword $(git rev-parse HEAD) refs/heads/mrgword ${ZERO}"

# 3. the range boundary by date (gpt G-04): C carries the listed word in its message; two children D and E of C, D dated earliest; M merges them
g checkout -q -b dates "${remote}"
GIT_COMMITTER_DATE='2020-01-02T00:00:00' g commit -q --allow-empty -m "c: the ${WORD} notes"; C=$(git rev-parse HEAD)
GIT_COMMITTER_DATE='2020-01-01T00:00:00' g commit -q --allow-empty -m d; D=$(git rev-parse HEAD)
g checkout -q -b dates-e "${C}"; GIT_COMMITTER_DATE='2020-01-03T00:00:00' g commit -q --allow-empty -m e
g checkout -q dates; GIT_COMMITTER_DATE='2020-01-04T00:00:00' g merge -q --no-ff -m m dates-e
echo "  rev-list's last for the new branch: $( [ "$(git rev-list HEAD --not --remotes=origin | tail -1)" = "${D}" ] && echo 'D (a child of C)' || echo other)"
run "pre-push: a listed word in the message of the pushed range's oldest commit, under a date order" push_line "refs/heads/dates $(git rev-parse HEAD) refs/heads/dates ${ZERO}"

# 4. an annotated tag's annotation (gpt G-05)
g checkout -q main; g tag -a -m "release: the ${WORD} notes" t1 "${remote}"
run "pre-push: an annotated tag whose annotation carries a listed word" push_line "refs/tags/t1 $(git rev-parse t1) refs/tags/t1 ${ZERO}"

# 5. one line carrying both shapes (both seats): the refusal must not print the word
printf 'note %s and the %s\n' "${FAKE}" "${WORD}" > b.txt; g add b.txt
run "pre-commit: a line carrying a credential and a listed word" "${HOOKS}/pre-commit"
g reset -q; rm b.txt

# 6. credential shapes the patterns may not cover (gemini G-02)
printf '%s\n' "${LOWER}" > l.txt; g add l.txt
run "pre-commit: a lowercase 'password = <20 characters>' assignment" "${HOOKS}/pre-commit"
g reset -q; rm l.txt
printf '{%s}\n' "${SLASHTOK}" > t.json; g add t.json
run "pre-commit: a slash-bearing OAuth refresh token in JSON" "${HOOKS}/pre-commit"
g reset -q; rm t.json

# 7. a listed word in a file NAME (gpt G-08)
echo clean > "notes-$(printf 'zebra%s' fish)-quartet.txt"; mv "notes-$(printf 'zebra%s' fish)-quartet.txt" "notes $(printf 'zebra%s' fish) quartet.txt"; g add -A
run "pre-commit: a clean file whose name carries a listed word" "${HOOKS}/pre-commit"
g reset -q; rm -f notes*.txt

# 8. pr/* pushes: a quoted personal .po path (gpt on F-10); the origin/next fallback base (gpt G-06); hooks-test's quoted case, read for its reason
g update-ref refs/remotes/upstream/next "${remote}"
g checkout -q -b pr/po "${remote}"; mkdir -p docs; echo 'msgid ""' > "docs/$(printf 'caf\303\251').po"; g add docs; g commit -q -m 'po: a note'
run "pre-push: a pr/* branch adding docs/<non-ASCII name>.po" push_line "refs/heads/pr/po $(git rev-parse HEAD) refs/heads/pr/po ${ZERO}"
g checkout -q -b quoted "${remote}"; g config diff.noprefix true; echo "${FAKE}" > 'odd"name.txt'; g add 'odd"name.txt'; g commit -q -m quoted
run "pre-push: hooks-test's quoted-name credential case, read for its reason" push_line "refs/heads/quoted $(git rev-parse HEAD) refs/heads/quoted ${ZERO}"
g config --unset diff.noprefix
g update-ref -d refs/remotes/upstream/next
g checkout -q -b fakenext "${remote}"; mkdir -p docs; echo personal > docs/plan.md; g add docs; g commit -q -m 'the fork overlay'
g update-ref refs/remotes/origin/next "$(git rev-parse HEAD)"
g checkout -q -b pr/z fakenext; echo feature > feature.txt; g add feature.txt; g commit -q -m 'z: a feature'
run "pre-push: a pr/* branch carrying docs/plan.md, with only origin/next (holding docs/plan.md) as base" push_line "refs/heads/pr/z $(git rev-parse HEAD) refs/heads/pr/z ${ZERO}"
exit 0
