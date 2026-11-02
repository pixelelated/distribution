#!/usr/bin/env bash
# T39 (#686) stage C: t39-checks.sh's FAIL-first runs (brief § 5, :1474-1484), in order: (i) the baseline,
# (ii) one mutation per step, each on its own scratch copy of the export or in a throwaway clone under
# /workspace/tmp/m6-t39/ (never the worktree), (iii) the tip with allow-findings.txt withheld, and the refusals.
# Run (iv), after stage E, is the same as (iii) at fixed-at.
#   bash checks-runs.sh <worktree> <since> <outdir>
# Every run prints its command's exit as `rc=<n>` on its own line and its wall time; the checker's own lines follow.
R=${1:?worktree}; SINCE=${2:?since}; O=${3:?outdir}
export LC_ALL=C
G=/usr/bin/grep
T=/workspace/tmp/m6-t39
S=$T/stage-c
E=$T/export
A=$R/docs/audits/2026_11_01-epic-m6-doctrine-reference
C=$A/tools/t39-checks.sh
P=$R/.qa-scratch/t39/paths.txt
mkdir -p "$O" "$S"
rm -rf "${S:?}/mut" "${S:?}/out" "${S:?}/clone" "${S:?}/allow-bad"
mkdir -p "$S/mut" "$S/out"

run() {  # run <name> <checker args...>: the run's output to $O/<name>.out, with its rc and wall time
  local name=$1; shift
  local t0 t1 rc
  t0=$(date +%s.%N)
  bash "$C" "$@" > "$O/$name.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf 'rc=%s\nwall=%.2fs\n' "$rc" "$(echo "$t1 - $t0" | bc)" >> "$O/$name.out"
  printf '%-34s rc=%s  %s\n' "$name" "$rc" "$($G -E '^TOTAL:|refused' "$O/$name.out" | head -n 1)"
  $G -E '^FAIL ' "$O/$name.out" | sed 's/^/    /'
}
std() { echo --repo "$R" --commit HEAD --since "$SINCE" --paths "$P" --allow "$A/tools"; }
mk() {  # mk <name>: a scratch copy of the export
  cp -a "$E" "$S/mut/$1"
}

echo "== (i) the baseline: the export at the dispatch tip, all three allowlists"
run i-baseline --tree "$E" $(std) --out "$S/out/i-baseline"

echo "== (ii) one mutation per step; each stub is first checked against the unfixed text (it must print 0 there)"
# inventory: one text file removed from the copy
mk inventory; rm "$S/mut/inventory/licenses/0BSD.txt"
run ii-inventory --tree "$S/mut/inventory" $(std) --out "$S/out/ii-inventory"

# scope: a throwaway clone whose commit flips one licence row's tier in the inventory (--since that commit, so
# the history steps see nothing): the carve reads the inventory, so its class sizes move
git clone --quiet --shared --no-checkout "$R" "$S/clone"
CH=$(git -C "$R" rev-parse HEAD)
commit_with() {  # commit_with <path> <file holding the new bytes> <message>: a commit on CH in the clone, no checkout
  local blob idx tree c
  idx=$(mktemp "$S/idx.XXXXXX")
  blob=$(git -C "$S/clone" hash-object -w "$2")
  GIT_INDEX_FILE=$idx git -C "$S/clone" read-tree "$CH"
  GIT_INDEX_FILE=$idx git -C "$S/clone" update-index --cacheinfo "100644,$blob,$1"
  tree=$(GIT_INDEX_FILE=$idx git -C "$S/clone" write-tree)
  rm -f "${idx:?}"
  c=$(GIT_AUTHOR_NAME=t39 GIT_AUTHOR_EMAIL=t39@invalid GIT_COMMITTER_NAME=t39 GIT_COMMITTER_EMAIL=t39@invalid \
      git -C "$S/clone" commit-tree "$tree" -p "$CH" -m "$3")
  echo "$c"
}
git -C "$R" show HEAD:docs/reviews/inventory.json | python3 -I -c '
import json, sys
d = json.load(sys.stdin); ix = {k: i for i, k in enumerate(d["columns"])}
n = 0
for r in d["rows"]:
    if r[ix["tree"]] == "distribution" and r[ix["path"]] == "licenses/0BSD.txt":
        assert r[ix["tier"]] == "upstream-carried", r[ix["tier"]]; r[ix["tier"]] = "fork-own"; n += 1
assert n == 1, n
json.dump(d, sys.stdout)' > "$S/inventory-mut.json"
echo "stub check: the python above asserted licenses/0BSD.txt's tier at HEAD is upstream-carried before the flip, rc=$?"
SC=$(commit_with docs/reviews/inventory.json "$S/inventory-mut.json" "t39 mutation: one tier flipped")
run ii-scope --tree "$E" --repo "$S/clone" --commit "$SC" --since "$SC" --paths "$P" --allow "$A/tools" --out "$S/out/ii-scope"

# links: a planted relative link to an absent file in README.md
echo "stub check: README.md carries docs/no-such.md $($G -c 'no-such' "$E/README.md") times (expect 0)"
mk links; printf '\nSee [x](docs/no-such.md).\n' >> "$S/mut/links/README.md"
run ii-links --tree "$S/mut/links" $(std) --out "$S/out/ii-links"

# paths: a planted backticked directory path that does not exist
echo "stub check: docs/releases/versioning.md carries no-such-dir $($G -c 'no-such-dir' "$E/docs/releases/versioning.md") times (expect 0)"
mk paths; printf '\nThe files are under `docs/no-such-dir/`.\n' >> "$S/mut/paths/docs/releases/versioning.md"
run ii-paths --tree "$S/mut/paths" $(std) --out "$S/out/ii-paths"

# tools: a planted backticked tool that does not exist
echo "stub check: docs/releases/versioning.md carries no-such-tool $($G -c 'no-such-tool' "$E/docs/releases/versioning.md") times (expect 0)"
mk tools; printf '\nRun `tools/no-such-tool` first.\n' >> "$S/mut/tools/docs/releases/versioning.md"
run ii-tools --tree "$S/mut/tools" $(std) --out "$S/out/ii-tools"

# identity: a planted capitalised brand heading and the retired name as the OS's
echo "stub check: README.md carries Pixelelated $($G -c 'Pixelelated' "$E/README.md") and Rasteratops OS $($G -c 'Rasteratops OS' "$E/README.md") times (expect 0 and 0)"
mk identity; printf '\n# Pixelelated\n\nRasteratops OS 0.0.1 is out.\n' >> "$S/mut/identity/README.md"
run ii-identity --tree "$S/mut/identity" $(std) --out "$S/out/ii-identity"

# retired: the retired PR recipe and the retired script in the present tense
echo "stub check: docs/pixelelated/cloud-folders.md carries rebase --onto $($G -c 'rebase --onto' "$E/docs/pixelelated/cloud-folders.md") and cloud_migrate_layout $($G -c 'cloud_migrate_layout' "$E/docs/pixelelated/cloud-folders.md") times (expect 0 and 0)"
mk retired; printf '\ngit rebase --onto upstream/next next pr/x\n\ncloud_migrate_layout runs at startup.\n' >> "$S/mut/retired/docs/pixelelated/cloud-folders.md"
run ii-retired --tree "$S/mut/retired" $(std) --out "$S/out/ii-retired"

# cites: a planted decision ID that names no row
echo "stub check: the register at HEAD has D-CLOUD-9999 $(git -C "$R" show HEAD:docs/decision-register.md | $G -c 'D-CLOUD-9999') times (expect 0)"
mk cites; printf '\nAs decided in D-CLOUD-9999.\n' >> "$S/mut/cites/docs/releases/versioning.md"
run ii-cites --tree "$S/mut/cites" $(std) --out "$S/out/ii-cites"

# untouched: a scratch commit editing a ledger row (docs/reviews/order.md), and one editing a licences file
git -C "$R" show HEAD:docs/reviews/order.md > "$S/order-mut.md"; printf '\nedited by hand\n' >> "$S/order-mut.md"
UC1=$(commit_with docs/reviews/order.md "$S/order-mut.md" "t39 mutation: a ledger row edited")
run ii-untouched-order --tree "$E" --repo "$S/clone" --commit "$UC1" --since "$CH" --paths "$P" --allow "$A/tools" --out "$S/out/ii-untouched-order"
git -C "$R" show HEAD:licenses/0BSD.txt > "$S/0bsd-mut.txt"; printf 'edited by hand\n' >> "$S/0bsd-mut.txt"
UC2=$(commit_with licenses/0BSD.txt "$S/0bsd-mut.txt" "t39 mutation: a licence edited")
run ii-untouched-licence --tree "$E" --repo "$S/clone" --commit "$UC2" --since "$CH" --paths "$P" --allow "$A/tools" --out "$S/out/ii-untouched-licence"

# generated: a row appended to the catalog by hand, as a commit (which is also an out-of-scope commit, so the
# untouched step names it too: two guards over one edit) and in the read tree alone (generated by itself)
git -C "$R" show HEAD:docs/releases/catalog.md > "$S/catalog-mut.md"; printf '| `hand-added` | x | x | x | x | x |\n' >> "$S/catalog-mut.md"
GC=$(commit_with docs/releases/catalog.md "$S/catalog-mut.md" "t39 mutation: a catalog row by hand")
run ii-generated-commit --tree "$E" --repo "$S/clone" --commit "$GC" --since "$CH" --paths "$P" --allow "$A/tools" --out "$S/out/ii-generated-commit"
mk generated; printf '| `hand-added` | x | x | x | x | x |\n' >> "$S/mut/generated/docs/releases/catalog.md"
run ii-generated-tree --tree "$S/mut/generated" $(std) --out "$S/out/ii-generated-tree"

# binaries: one byte appended to a PNG
mk binaries; printf 'x' >> "$S/mut/binaries/docs/pixelelated/art/raster/1x/dual.png"
run ii-binaries --tree "$S/mut/binaries" $(std) --out "$S/out/ii-binaries"

# leads: a second copy of L-06's defect sentence, at a line no allowlist names
mk leads; printf '\nM7 order remains #515 -> #508.\n' >> "$S/mut/leads/docs/cloud-save-integrity.md"
run ii-leads --tree "$S/mut/leads" $(std) --out "$S/out/ii-leads"

echo "== (iii) the tip with allow-findings.txt withheld: exit 1, naming each of the slice's own findings"
run iii-tip-withheld --tree "$E" $(std) --withhold findings --out "$S/out/iii-tip-withheld"

echo "== refusals: exit 2, nothing checked"
run refuse-no-tree $(std) --out "$S/out/refuse"
mkdir -p "$S/mut/checkout/.git"
run refuse-checkout --tree "$S/mut/checkout" $(std) --out "$S/out/refuse"
run refuse-no-paths --tree "$E" --repo "$R" --commit HEAD --since "$SINCE" --allow "$A/tools" --out "$S/out/refuse"
head -n 253 "$P" > "$S/paths-253.txt"
run refuse-paths-253 --tree "$E" --repo "$R" --commit HEAD --since "$SINCE" --paths "$S/paths-253.txt" --allow "$A/tools" --out "$S/out/refuse"
t0=$(date +%s.%N); env PATH=/nonexistent /bin/bash "$C" --tree "$E" $(std) --out "$S/out/refuse" > "$O/refuse-no-python3.out" 2>&1; rc=$?
printf 'rc=%s\nwall=%.2fs\n' "$rc" "$(echo "$(date +%s.%N) - $t0" | bc)" >> "$O/refuse-no-python3.out"
printf '%-34s rc=%s  %s\n' refuse-no-python3 "$rc" "$($G refused "$O/refuse-no-python3.out")"
run refuse-register --tree "$E" --repo "$R" --commit 651150fc88 --since "$SINCE" --paths "$P" --allow "$A/tools" --out "$S/out/refuse"
mkdir -p "$S/allow-bad"; cp "$A/tools/allow-inherited.txt" "$A/tools/allow-findings.txt" "$S/allow-bad/"
cp "$A/tools/allow-legit.txt" "$S/allow-bad/"; printf 'README.md:9 historical\n' >> "$S/allow-bad/allow-legit.txt"
run refuse-entry-no-reason --tree "$E" --repo "$R" --commit HEAD --since "$SINCE" --paths "$P" --allow "$S/allow-bad" --out "$S/out/refuse"
echo "(end)"
