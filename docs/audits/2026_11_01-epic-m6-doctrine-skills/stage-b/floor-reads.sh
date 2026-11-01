#!/usr/bin/env bash
# T38 stage B (#685): the floor the brief's § 3 asks to be read first, at its lines -- the blindspots (item 3),
# the friction log (item 4), T4's deferral (item 6), the doctrine futro's T38 addendum (§ 10), and L-26's checkboxes.
export LC_ALL=C; G=/usr/bin/grep
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== blindspot register (HEAD)"; git show HEAD:docs/blindspot-register.md | awk 'NR==4||NR==10||NR==18||NR==30||NR==36||NR==37||NR==915||NR==1089||NR==1134||NR==1215 {printf ":%d %s\n", NR, substr($0,1,200)}'
echo "== friction log (HEAD)"; git show HEAD:docs/friction-log.md | awk 'NR==7||NR==25||NR==54||NR==58||NR==74||NR==76||NR==244||NR==417||NR==863||NR==868 {printf ":%d %s\n", NR, substr($0,1,220)}'
echo "== T4's punch list, the deferral to this slice"; git show 6ec78bbf8c:docs/audits/2026_10_24-epic-m6-doctrine-rules/05-punch-list.md | sed -n '568p' | cut -c1-200
echo "== the doctrine futro: its headings from the T38 addendum on"
git show HEAD:docs/futros/2026-10-24-m6-doctrine.md | $G -n -E '^#{1,3} ' | awk -F: '$1>=425' | cut -c1-120
echo "== L-26: #314 :14, #287 :16"
for nl in 314:14 287:16; do n=${nl%%:*}; l=${nl##*:}; printf -- '-- #%s :%s: %s\n' "$n" "$l" "$(gh --repo pixelelated/distribution issue view "$n" --json body --jq .body | sed -n "${l}p" | cut -c1-320)"; done
