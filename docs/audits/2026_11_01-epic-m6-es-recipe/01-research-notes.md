# T37 (#684) research notes

Stage A, 2026-11-01, the T3 session (Opus 5.5, high). Every figure below is a tool's own line from
the files under `stage-a/`, named beside it; a line that differs from the brief's expectation is
recorded beside the expectation, not argued with.

## Scope

**§ 2's block**, the brief's lines 408-522 extracted with `sed -n '408,522p'` (115 lines) into
`stage-a/block.sh` and copied below **byte for byte from that file** (never retyped); `sha256sum` of
the block's lines as they stand in this file is checked in the stage-A commit against the brief's
prefix `f3ef373be6535467`
(`f3ef373be653546772d6f4be0a27f9c9913b9aee050f432a31bf8d20286dc1b0`). It was run from the
distribution worktree with `W=/workspace/tmp/m6-coordinator/t11-research/tree`, `P1=2174265e9c`,
`MB=c445081a59` (`block rc=0 wall=6s`, 01:03 UTC):

```bash
mkdir -p .qa-scratch/t37
cat > .qa-scratch/t37/membership.py <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
def gre(g):
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i]=="?": out+="[^/]"; i+=1
        elif g[i]=="{":
            j=g.index("}",i); out+="(?:"+"|".join(gre(x) for x in g[i+1:j].split(","))+")"; i=j+1
        else: out+=re.escape(g[i]); i+=1
    return out
def compile_globs(globs):
    inc=collections.defaultdict(list); exc=collections.defaultdict(list)
    for g in globs:
        neg=g.startswith("!"); g=g[1:] if neg else g
        tree="es" if g.startswith("es:") else "distribution"
        g=g[3:] if tree=="es" else g
        (exc if neg else inc)[tree].append(re.compile(gre(g)+r"\Z"))
    return inc,exc
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
inv=json.load(open("docs/reviews/inventory.json"))
hd=inv["header"]["distribution"]
print("distribution head:",hd["head"]); print("distribution merge_base:",hd["merge_base"]); print("distribution upstream:",hd["upstream"],hd["upstream_head"])
cols=inv["columns"]; print("columns:",cols)
rows=[dict(zip(cols,r)) for r in inv["rows"]]
def match(row,areas,comp,reach,tier):
    if row["area"] not in areas: return False
    if reach and row["reach"] not in reach: return False
    if tier and row["tier"] not in tier: return False
    if comp is None: return True
    inc,exc=comp; t=row["tree"]; p=row["path"]
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
def globhits(p):
    out=[]
    for s,c in sl:
        for a,cm,r,rest,t in c:
            if cm is None: continue
            inc,exc=cm
            if any(x.match(p) for x in inc.get("distribution",())) and not any(x.match(p) for x in exc.get("distribution",())):
                out.append((s["id"],s["k"],"rest" if rest else "non-rest")); break
    return out
kof={s["id"]:s["k"] for s,_ in sl}
mine=[]
for r in rows:
    if r["tree"]!="distribution": continue
    h,kind=hits(r)
    if h==["es-recipe"]: mine.append(r)
mine.sort(key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine), "reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)),"lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"vendor-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="vendor-carried"))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
tree=[l.strip() for l in open(sys.argv[2]) if l.strip()]
named=tree+["projects/ROCKNIX/packages/virtual/es-themes/package.mk","projects/ROCKNIX/packages/virtual/image/package.mk","docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/baseline/package.mk","docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/candidate/package.mk","tools/pkgcheck","tools/es-menu-map-check"]
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY; globs:",globhits(p)); continue
    h,kind=hits(r); print(p, "in-T37" if p in got else "not-in-T37", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"lang",r["language"],"area",r["area"])
print("DEPS")
deps=["toolchain","boost","SDL2","freetype","curl","freeimage","bash","rapidjson","SDL2_mixer","fping","p7zip","alsa","vlc","drm_tool","poppler","pugixml","noto-sans-cjk","zstd","Python3","SDL2_image","SDL2_ttf"]
for d in deps:
    rx=re.compile(r"(?:^|/)packages/(?:.*/)?"+re.escape(d)+r"/package\.mk\Z")
    found=sorted(p for p in byp if rx.search(p))
    if not found: print(d,"NO RECIPE IN INVENTORY")
    for p in found:
        h,kind=hits(byp[p]); print(d,p,kind,[(x,kof[x]) for x in h],"tier",byp[p]["tier"])
print("RECIPE TREES BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and (r["path"].startswith("packages/") or r["path"].startswith("projects/ROCKNIX/packages/")):
        k=("packages/" if r["path"].startswith("packages/") else "projects/ROCKNIX/packages/",)+tuple(hits(r)[0])+(hits(r)[1],)
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:(kv[0][0],-kv[1])): print(v,"paths",ln[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
git -C "$W" ls-tree -r --name-only "$P1" -- projects/ROCKNIX/packages/ui/ > .qa-scratch/t37/tree.txt
python3 -I .qa-scratch/t37/membership.py /dev/null .qa-scratch/t37/tree.txt > .qa-scratch/t37/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t37/block-1.txt > .qa-scratch/t37/paths.txt
wc -l .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt
python3 -I .qa-scratch/t37/membership.py .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt > .qa-scratch/t37/block-2.txt
/usr/bin/grep -E '^(distribution |mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t37/block-2.txt
IH=$(sed -n 's/^distribution head: //p' .qa-scratch/t37/block-2.txt)
git -C "$W" ls-tree -r --name-only "$IH" -- projects/ROCKNIX/packages/ui/ | diff - .qa-scratch/t37/paths.txt && echo "ls-tree at the inventory's head = paths.txt"
diff .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt; echo "paths.txt against ls-tree at $P1: diff rc=$?"
for p in $(cat .qa-scratch/t37/tree.txt); do git -C "$W" show "$P1:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t37/tree.txt); do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t37/paths.txt); do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, the inventory paths at its head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t37/tree.txt | wc -l
git -C "$W" diff --shortstat "$MB" "$P1" -- projects/ROCKNIX/packages/ui/
git -C "$W" diff --shortstat "$IH" "$P1" -- projects/ROCKNIX/packages/ui/
```

**Its output** (`stage-a/block.out`), equal byte for byte to the brief's expected lines 531-560
(`diff` of the two, `rc=0`):

```
  15 .qa-scratch/t37/paths.txt
  19 .qa-scratch/t37/tree.txt
  34 total
distribution head: eb4763e3cc9bcd729830cd85f1719bbd4f28db10
distribution merge_base: c445081a59518f37d9776e5412dd7b14910696f7
distribution upstream: upstream/next c1f1746828ca47dfc751ffe44bb47b6b259883d7
mine: 15 paths.txt: 15 equal: True
only-mine: []
only-paths.txt: []
lines: 4561 reach: {'shipped': 15} tier: {'upstream-carried': 9, 'fork-own': 6} lang: {'shell': 4, 'config': 4, 'recipe': 3, 'systemd': 2, 'text': 1, 'image': 1}
fork-own lines: 572
read lines: 327 of which fork-own: 190 vendor-carried lines: 0
7d6
< projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch
15,17d13
< projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch
< projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch
< projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch
6a7
> projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch
13a15,17
> projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch
> projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch
> projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch
paths.txt against ls-tree at 2174265e9c: diff rc=1
wc -l, every path at the P1 hash: 4649
grep -c, every path at the P1 hash: 4650
grep -c, the inventory paths at its head: 4561
14
 8 files changed, 463 insertions(+), 13 deletions(-)
```

The first pass (against `/dev/null`) wrote `mine: 15 paths.txt: 0 equal: False` into
`stage-a/block-1.txt`. `stage-a/block-2.txt` holds the TSV, `CLAIMS` (the 25 named paths: the 19,
of which the 15 `in-T37 non-rest [('es-recipe', 37)]`, `cpugov.patch` `[('patches-dead', 40)]` and
the three theme patches `rest [('patches-shipped', 42)]`, all four `vendor-carried`; the two
virtual packages `[('image-packages', 8)]`; the two `docs/qa-logs/` copies `[('records', 46)]`;
`tools/pkgcheck` `[('build-engine-upstream-tools', 6)]`; `tools/es-menu-map-check`
`[('tooling-guards', 10)]`), `DEPS` (each of the 21 dependency names with its recipe and slice) and
`RECIPE TREES BY SLICE`, whose slice row is `15 paths 4561 lines ('projects/ROCKNIX/packages/',
'es-recipe', 'non-rest')`.

**The extended run** (§ 2's second block; `stage-a/extended.out`; outside `CLAIMS` its output
equals `block-2.txt`, `diff` rc 0; the 8 lines, cut here at the slice and tier):

| Path | Slice | Tier, lines |
| --- | --- | --- |
| `projects/ROCKNIX/packages/virtual/swaywm-env/package.mk` | `('image-packages', 8)` | upstream-carried, 15 |
| `projects/ROCKNIX/packages/wayland/compositor/sway/package.mk` | `('image-packages', 8)` | fork-own, 71 |
| `packages/graphics/pango/package.mk` | `('generic-packages-reached', 7)` | upstream-carried, 27 |
| `packages/devel/fribidi/package.mk` | `('generic-packages-reached', 7)` | upstream-carried, 25 |
| `projects/ROCKNIX/packages/graphics/SDL2/package.mk` | `('image-packages', 8)` | upstream-carried, 123 |
| `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` | `('os-launch-control-state', 1)` | fork-own, 626 |
| `projects/ROCKNIX/packages/rocknix/sources/scripts/vertical-check` | `('os-launch-control-state', 1)` | upstream-carried, 182 |
| `projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init` | `('image-packages', 8)` | fork-own, 224 |

**The bases**, from the § 1 commands (`stage-a/s1-first-commands.out`) and the § 5 runs
(`stage-a/s5-runs.out`): the distribution's merge base with `upstream/next` `651150fc88` is
**`c445081a59518f37d9776e5412dd7b14910696f7`**; the pin's merge base with `rocknix/master`
`f6c542872e3850c5f432929ead219547a897cd4a` is **`cada856d86e3115fbbf0bce09dd761b0ee8fa9fd`**; the
pin lacks `14` of `rocknix/master`'s commits (`7` first-parent merges) and is `724` ahead (R08);
`test/qa-integration` and `origin/test/qa-integration` both read `16dbac5211` (R08).

## The § 5 runs at stage A

`stage-a/s5-runs.sh` is the brief's § 5 block, each run wrapped in its own `rc` and a `date +%s`
pair (every wall time was 0-5 s); its output is `stage-a/s5-runs.out`. Four departures from the
block, each a line of the script's header: every read of the ES recipe also withholds `:39` by line
number (the mask `M` leaves that line unchanged, read at stage A by length and a masked-equal test
without printing it); the candidate-provenance line under `/workspace/repos/rocknix` is not run
(open item 16, the dispatch: R3 § 2.3 and cmd 21 are cited, and `069fc2704421` is not in this
repository); the stage-C checker line is not run; the removal check names `94d8ef8e7e`.

| Run | Expected (the brief's comment) | Printed | Differs |
| --- | --- | --- | --- |
| R01 scope | 19; 15 | `19`; `15` | -- |
| R02 lines | `wc -l 19: 4649`; `grep -c 19: 4650`; `grep -c 15: 4561`; the four patches 89 | the same; `grep -c the four patches: 89 files: 4` | -- |
| R03 `next` vs tip on `ui/` | no line | `lines=0` | -- |
| R04 the fork's delta | ` 8 files changed, 463 insertions(+), 13 deletions(-)`; 251; 5; 246 | the same, and `241` non-merge commits touching the ES recipe | -- |
| R05 upstream's delta | 16; ` 8 files changed, 72 insertions(+), 75 deletions(-)`; ` 14 files changed, 83 insertions(+), 536 deletions(-)` | the same; name-status `M` es_features.cfg, package.mk, start_es.sh, emustation.service, essway.service; `A` patches/RK3566/fix_multistateinput.patch and the two `20-thp.conf` | -- |
| R06 by side | `upstream-only 6 fork-only 6 both 2` | the same; both: `emulationstation/package.mk`, `system.d/essway.service` | -- |
| R07 pins | ES `cada856d86` / `f6c542872e` / `16dbac5211` on `test/qa-integration` with the fork's site; lowerdeck `ab735114ab` and the theme `9a50ef366e` at every hash | the same (ES site `ROCKNIX/emulationstation-next` at MB and UN, `pixelelated/emulationstation` at the tip) | -- |
| R08 ES side | 14; 724; `cada856d86...`; the pin for both refs | `14`; `724`; `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd`; `16dbac5211` twice; `7` first-parent merges | -- |
| R09 the define | GLES3 at `CMakeLists.txt:164-165`, `:213-214`, `:362-363`; `es-core/CMakeLists.txt:278-283` | `164:elseif(GLES3)`, `165:` GLSystem "OpenGL ES 3.0"; `213`-`214` `find_package(OpenGLES3 REQUIRED)`; `362`-`363` `add_definitions(-DUSE_OPENGLES_30)`; es-core 278-283 the `Renderer_GLES30` / else `Renderer_GLES20` lists | -- |
| R10 fribidi; the build names | `:230-244`; `:303-330` through the mask; `HfsDBScraper.cpp:1`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33` | `:236` `pkg_check_modules(FRIBIDI QUIET fribidi)`, `:241` `-DHAVE_FRIBIDI`; the six names' `if(DEFINED ENV{...})` blocks, values masked; **`HfsDBScraper.cpp:181` also** | **one more reader**: `:181` |
| R11 `bash -n` | rc=0 for the seven | `rc=0` for each of the seven | -- |
| R12 `pkgcheck` | one path and rc=0 for each recipe; the control no path, rc=0 | each recipe's one path and `rc=0 lines=0 FAIL-lines=0 WARN-lines=0`; `find es-theme-no-such-package:` empty, `rc=0 lines=0` (the fail-open, L-21) | -- |
| R13 the export | `export rc=0`, the tip, `worktree build roots: 0` | `export rc=0 tip=9fa740a91ba9fcaa21a26cc72f0b50fac10f32df path=/workspace/tmp/m6-t37/export worktree build roots: 0`; 133,480 files, no `.git` | -- |
| R14 effective fields, GENERIC_X64 | R3 § 1.5's table (C8) | `source rc=0` for each; the pin; `https://github.com/pixelelated/emulationstation.git`, `PKG_SHA256=` empty; the theme's `7ee1e93f...` and lowerdeck's `2677d3ce...`; ES depends `boost toolchain SDL2 freetype curl freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool poppler pugixml noto-sans-cjk zstd mesa`; ES cmake options ending `-DGLES3=1 -DSCREENSCRAPER_RUNTIME_DEV_LOGIN=***`; `auto`/`manual`/`manual`; `busybox`/`-gold`; `PKG_PATCH_DIRS=` empty; `BASE_ONLY=` and `BATTERYPLUS_SUPPORT=` empty, `VULKAN_SUPPORT=yes`, `EMULATION_DEVICE=yes`; the stamps `9e618e4ac667...`, `e31c625d7692...`, `7dd9f9575727...` | **the mask's**: `=***` is `M` matching `LOGIN *=`; `:30` carries `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1` (`grep -c -F` on `:30`: `1`) |
| R15 the call's writes | two cache files in the export; 0 in the worktree | `.cache_package_global` 76,994 and `.cache_package_local` 45,384 bytes under `build.pixelelated-GENERIC_X64.x86_64/`; `worktree build roots: 0` | -- |
| R16 patch reach | `patches/x86_64/: NOT REACHED` for GENERIC_X64 and H700 | `GENERIC_X64/x86_64: emulationstation PATCH_ARCH=x86 PKG_PATCH_DIRS=[] -> patches/x86_64/: NOT REACHED`; `H700/aarch64: emulationstation PATCH_ARCH=aarch64 PKG_PATCH_DIRS=[] -> patches/x86_64/: NOT REACHED`; the theme's `patches/: REACHED` on both; lowerdeck has no `patches/`; no project-side or device-side patch directory for the three | -- |
| R17 install text | `:101` among the `${INSTALL}` targets; `rm -f` `:79`; `\|\| true` `:73-75`; `PKG_NEED_UNPACK` `:14`; no `PKG_PATCH_DIRS` | `14:PKG_NEED_UNPACK="busybox"`; `75: ... \|\| true`; `79:` and `83:` `rm -f`; `84:`, `97:`, `100:`, `134:`, `137:`, `140:` `ln -sf` with device targets; `93:` a commented link; **`101:` `ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ...`**; no `PKG_PATCH_DIRS` line | -- |
| R18 credential names | `count lines: 5` -- `:30`, `:40`, `:42`, `:43`, `:44` | `count lines: 5`; `30:` `SCREENSCRAPER_RUNTIME_DEV_LOGIN`; `40:` `SCREENSCRAPER_DEV_LOGIN` twice; `42:` `SCREENSCRAPER_DEV_LOGIN`; `43:` `GAMESDB_APIKEY`; `44:` `CHEEVOS_DEV_LOGIN` | -- |
| R19 armsx2, vulkan | `1331 1333 1393`; 15 | `1331 1333 1393`; `15` | -- |
| R20 text checks over the 15 | `NON-ASCII FILES 0`, `SECRET-PATTERN FILES 0`, forbidden-terms rc=0, each after a planted positive | secret patterns compile `rc=1`; planted positive `1`, plain `0`; planted non-ASCII `1`; per file `non-ascii=0 secret=0` for all 15 and the four patches; `NON-ASCII FILES 0 SECRET-PATTERN FILES 0`; a stand-in `FORBIDDEN_PATTERNS` positive `rc=1`; `forbidden-terms over the 15 rc=0` (`0 hits on stdin`); `XML FAILS 0` over the four `.cfg` | -- |
| R21 freshness `--list` | `lines=48 ui=0` | `freshness --list rc=0 lines=48 ui=0` | -- |
| R22 removal check | no line before stage E | `lines=0` | -- |

## Open items read at stage A

- **2 (L-03): no rewrite.** `scripts/install` (196 lines) and `scripts/image` (481 lines), read whole
  at the tip: `scripts/install:164-185` copies the package's install tree into the image root with
  `tar -cf - . | tar -xf -`, which keeps a link's target as written; `scripts/image` makes its own
  links (`:127-134`, `:224`, `:227`), adds `chown -R 0:0` to the fakeroot script (`:90`) and squashes
  `${BUILD}/image/system` (`:250`, run at `:253`), with no pass over links between; what follows
  `:253` copies bootloader files into the release directory. During `makeinstall_target`
  `INSTALL` is `${PKG_INSTALL}` (`scripts/build:140`), `$BUILD/install_pkg/${PKG_NAME}-${PKG_VERSION}`
  (`config/functions:1380`). So `:101`'s link reaches the image with a build-host target (`proved:
  tree`; the candidate's corrected link is G-03's, ruling (h)). `stage-a/open-items.out`.
- **3 (L-08): the gettext tools come by build order.** ES's own plan in the export
  (`scripts/pkgjson | scripts/genbuildplan.py --build emulationstation`, `stage-a/plans.*`) holds
  `gettext:host` on GENERIC_X64 and H700, reached `emulationstation:target -> toolchain:target ->
  gcc:host -> autoconf:host -> gettext:host` (`stage-a/trace.out`); the ES recipe names no
  `gettext`. Whether ES's CMake finds `msgfmt` in that build is a configure log's (`CANNOT`, the
  integration's).
- **5 (L-09): an `arm` build does not compile ES.** `scripts/build_distro:89-97` builds
  `scripts/build_compat arm` for `ARCH=arm`; the `arm` plan for RK3566 (`DEVICE_ROOT=RK3566`, the
  Makefile's `:65` form) has 271 steps and **no `emulationstation:target`** (plans.out), while
  `virtual/arm/package.mk:26-33` adds `${WINDOWMANAGER}` only off `arm`. SDL2's `arm` branch reaches
  no ES build.
- **9 (Q2): every device's mesa enables GLES 2.** Sourced in the export for all 15 devices
  (`stage-a/mesa-gles.out`): `source rc=0 OPENGLES=mesa OPENGLES_SUPPORT=yes`,
  `mesa-dir=projects/ROCKNIX/packages/graphics/mesa`, `-Dgles1=enabled -Dgles2=enabled`
  (`projects/ROCKNIX/packages/graphics/mesa/package.mk:92-96`). That mesa installs the GLES 3
  headers with `gles2` is mesa's build, not read here `[unverified]`; an image build's sysroot
  settles it.
- **13: the blindspot entries** (`docs/blindspot-register.md`, `grep -n`): 47 *A dependency the
  build fetched for itself* (`:531`), with *"A pinned version in a recipe is a claim about the image
  only once the image is read"* at `:558`; 39 *A new suite that passed over a table of dashes*
  (`:326`) and the table's row 14 (`:23`), the "no observed positive" lines `:344`, `:376`; 54 *A
  measurement on a guest whose renderer was not the device's* (`:720`); 74 *A fixture or a stub that
  silently did not engage* (`:1200`); 75 *A corpus read on the wrong tree* (`:1206`).
- **15 (G-05): the state check is not on the image.** `tools/pixelelated-state-check`'s arguments
  are `--root` or `--payload`, `--mode {clean-image,first-boot,retained-upgrade}` and
  `--require-ready` (`:874-877`), for `--root / --mode first-boot` on a ready guest; no line under
  `packages/` or `projects/` names it at the tip (`0`), so the image does not ship it, and running
  it on the guest means carrying it there -- which the window's "the guest writes nothing" forbids
  unless it runs without a file. Put to the coordinator with the window request at stage B.
- **16:** answered by the dispatch; nothing run under `/workspace/repos/rocknix`; R3 § 2.3 and cmd 21
  cited; `069fc2704421` is not in this repository.
- **17: the 0 now holds for all 19.** In the hooks' form (R20), the planted private-key line counted
  `1` and a plain line `0`, then every one of the 15 and the four patches counted `secret=0`.
- **Fribidi's `libass` path: not ES's.** ES's plan holds no `libass:target` on GENERIC_X64 or H700;
  `vlc`'s effective target dependencies (`toolchain libdvbpsi gnutls ffmpeg libmpeg2 zlib flac
  libvorbis libxml2 pulseaudio SDL2 x264 x265 aom libogg`, pkgjson) carry no `libass`. ES's plan
  reaches fribidi by R2's chain only: `emulationstation:target -> SDL2:target -> swaywm-env:target
  -> sway:target -> pango:target -> fribidi:target` on both devices (trace.out). **And T36's G-01
  on the same image** (`BUILD_ID=069fc270442134fe771258418adf4e666e0473fb`, T36's `00` line 54 at
  `775d0893fe`): *"`libfreetype.so.6` and `libvlc.so.5` linked, **`libfribidi` NOT linked** (the
  `ldd ... -c` count is 3: freetype, vlc, vlccore)"*. The pin's CMake links `${FRIBIDI_LIBRARIES}`
  when the `QUIET` find succeeds (`CMakeLists.txt:236-241`, `:375`, `:462`), so the candidate's
  build did not find fribidi though the chain orders it first -- why is that build's configure log
  (`CANNOT` here); a stage-B lead under L-09, cited, not repeated on the guest (R5 § A).

## L-22: where the shipped theme names its fonts

Read by hash (errata): the theme's tarball from the shared download cache, `/workspace/cache/rocknix-sources/es-theme-art-book-next/es-theme-art-book-next-9a50ef366e750aabfab29e6915a2867607212971.tar.gz` (in bounds for reads, the coordinator's answer 1 of 6551707733; read only), its sha256
`7ee1e93f2c4e4f7385b78680ecfa3828acf12bc616e2111d23cc66a524231125` equal to the recipe's
`PKG_SHA256`; its 28 XML members extracted to scratch (`stage-a/open-items.out`).

- **25 `fontPath` elements** (`theme.xml` 15, the three `aspect-ratio-*.xml` 3 each, `splash.xml`
  1), **none without a `fontSize` in the same element** (a tag-stack scan; `theme.xml:49` carries a
  raw `&&` in an `if=` attribute that a strict XML parser refuses). T42's
  `0001-system-style-...patch` adds one more, `${fontLogo}` with its `fontSize` (`+` lines 12-13).
- They name `${fontBold}` 19, `${fontRegular}` 2, `${fontLogo}` 2, `${fontLight}` 1 and
  `./_inc/fonts/Roboto-Bold.ttf` 1; `fonts.xml:3-7` (`ifSubset="fonts:default|custom"`) maps the four
  variables to `./_inc/fonts/Roboto-Bold.ttf`, `Roboto-Regular.ttf`, `Roboto-Light.ttf` and
  `ChangaOne-Italic.ttf` -- **the tarball's only four fonts, each present** (`1` each).
- The `fonts:custom` subset includes `${themeCustomizationsPath}fonts.xml` (`theme.xml:156`), a file
  the player provides under `${distributionPath}theme-customizations/art-book-next/`; the tarball's
  `resources/customizations/fonts.xml` is its template (each variable `.../fonts/`, a directory until
  edited). By design; noted only.
- **The one absolute font path is the recipe's**: the `zh` block (`themes/.../package.mk:21-27`)
  names `/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` four times, the same file the
  ES recipe's CJK fallback link names (`emulationstation/package.mk:84`); it comes from
  `noto-sans-cjk` (T8's, in both recipes' dependencies). **Whether it is on the image is a guest
  read**: a G-02 line (`ls -l` of that path), labelled `candidate` because the file is
  `noto-sans-cjk`'s, not a `ui/` file's.
- The wordmark SVG has no `font` or `<text>` line (`0`): the Tiny5 licence ships beside letterforms
  drawn as paths, and no font file is needed at run time for it.

`proved: tree` (the tarball by hash, the recipe and T42's patch at the tip); the image half is
G-02's.

## The issues at stage A

`gh --repo pixelelated/distribution issue view` at 01:12 UTC (`stage-a/issues.out`): #684 OPEN;
#1072 OPEN `bug`; #613 OPEN; #1193 OPEN `bug`; #990 OPEN `bug`; #716 OPEN `bug`; #69 OPEN; #64 OPEN;
#256 OPEN; #322 OPEN; #585 OPEN; #528 OPEN; #566 CLOSED/COMPLETED; #586 OPEN (Backlog); #1137 OPEN
(Backlog); #1013 OPEN (Backlog); #791 OPEN (Backlog); #700 OPEN `epic`; #682 OPEN (T35, accepted
00:24 and complete at `d828355e0a`, its issue open until the integration); #683 OPEN (T36); #1293
OPEN. The brief's § 3 item 9 states hold.

## The lanes' tips at stage A

Distribution: T35 `origin/feature/m6-es-core-window-input-682` `d828355e0ac3b9c639c394adbcf9aeb65c0db22c`;
T36 `origin/feature/m6-es-core-utils-resources-683` `775d0893fe89781149e6f7aac9b8f56ff84608e1` at
01:14 (`5521c7cc49` at 01:12: T36 is committing). ES: T35 `b7fdb3a24c859ce91f9fd381bb0956901b8d23cb`
(local and `origin`, 9 ahead of the pin); T36 `feature/m6-es-core-utils-resources-683` local only, at
the pin (`0` ahead), `origin/...683` `fatal: Needed a single revision`; T34
`origin/feature/m6-es-core-components-681` `52f0ff5128cf96bfcdec9082ded75347ecea11e6`.

## Read first, this session (`working-principles.md` § Pre-flight)

Read in this session at stage A: the brief whole (its §§ 1-10, the open items, the corrections and
the errata); the dispatch comment; the pointer; the rules that load every session
(`engineering-practices.md`, `upgrade-and-install.md`, `issue-tracking.md`, `vm-first.md`,
`bugs-are-agent-first.md`, `time-to-play.md`, `release-candidates.md`, `device-builds.md`,
`fork-workflow.md`, `es-native-ui.md`, `decision-register.md`, `ceremonies.md`,
`learning-capture.md`, `worktrees.md`, `instruction-files.md`, `milestone-phase-naming.md`); the
scripts `scripts/install`, `scripts/image`, `scripts/unpack:120-165`, `scripts/build_distro:86-101`,
`scripts/build_compat`, `scripts/pkgjson`, `config/options:125-145`, `config/functions:795-805` and
`:1105-1135`, `config/multithread:40-60`, `tools/forbidden-terms-check`'s header,
`.githooks/guard-lib:25-45`, `tools/pixelelated-state-check:865-909`. **Owed at stage B**, with
their lines: `packaging-and-patches.md`, `packages/README.md`, `generic-x64-vm-testing.md`, the
register's cited rows (§ 9), the audits of § 3 item 8 by `git show`.

## The register

At `566398105e`, the decided table above `## Open decisions` (`:779`): `decided rows 699`; the
highest per area **D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052,
D-SYS-013, D-UI-137, D-WORKFLOW-217** (this slice's ownership row at `:777`);
`tools/register-check` printed *"713 IDs, each once; every citation in the live documents names a
row"*, `register-check rc=0`.
