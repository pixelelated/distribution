#!/usr/bin/env bash
# T38 stage A (#685): the issues the brief's § 3 item 9 lists, re-read with gh and their states
# recorded (a read of this repository's tracker only), then #685's comments, one line each.
#   bash issues.sh > issues.txt 2>&1
date -u +%Y-%m-%dT%H:%M:%SZ
for n in 685 807 651 686 911 810 342 640 1044 1045 343 850 314 287 260 378 261 333 326 341 645 953 955 268 235 943 254 809 540 1308 585 1373; do
  gh --repo pixelelated/distribution issue view "$n" --json number,state,stateReason,comments,title \
    --jq '"#\(.number) \(.state) \(.stateReason // "") comments=\(.comments|length) \(.title[0:90])"' 2>&1
done
echo "-- #685's comments:"
gh --repo pixelelated/distribution issue view 685 --json comments \
  --jq '.comments[] | "\(.createdAt) \(.author.login) \(.body | split("\n")[0] | .[0:110])"'
