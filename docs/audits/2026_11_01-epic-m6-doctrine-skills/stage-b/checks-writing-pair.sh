#!/usr/bin/env bash
# T38 stage B (#685): the checks the auditor's read of the writing pair names (stage-b/notes-writing-pair.md).
# Reads only: git at HEAD (the tools' sources, never run) and this repository's tracker and releases.
export LC_ALL=C; G=/usr/bin/grep
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== L-27: the open checkboxes the brief names, by issue and line"
for nl in 333:17 326:25 341:19 645:25 953:11 955:12 268:17; do n=${nl%%:*}; l=${nl##*:}
  gh --repo pixelelated/distribution issue view "$n" --json body --jq .body > /workspace/tmp/m6-t38/tmp/body-$n.md
  printf -- '-- #%s :%s: %s\n' "$n" "$l" "$(sed -n "${l}p" /workspace/tmp/m6-t38/tmp/body-$n.md | cut -c1-300)"
  printf '   open checkboxes in #%s: %s\n' "$n" "$($G -c '^- \[ \]' /workspace/tmp/m6-t38/tmp/body-$n.md)"
done
echo "== L-11: tools/fork-publish-release's own usage lines (read from its source, never run)"
git show HEAD:tools/fork-publish-release | $G -n -i -E 'usage|--prepare|upload|retired|refus' | head -n 10 | cut -c1-150
echo "== the releases this repository has published"
gh release list --repo pixelelated/distribution --limit 5 2>&1 | cut -c1-120
echo "== prose-check's PROSE_FIRST_PERSON default, and pr-stack-check's description scan"
git show HEAD:tools/prose-check | $G -n -E 'PROSE_FIRST_PERSON' | head -n 4 | cut -c1-150
git show HEAD:tools/pr-stack-check | $G -n -i -E 'description|assistant|Co-Authored|Generated with' | head -n 6 | cut -c1-150
echo "== paths named"
for p in tools/vm-walks/docs tools/png-blackout tools/prose-check tools/pr-stack-check docs/cloud-sync-changelog.md; do git cat-file -e "HEAD:$p" 2>/dev/null && echo "present $p" || echo "absent  $p"; done
