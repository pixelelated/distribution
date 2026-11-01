#!/bin/bash
# T37 (#684) stage A: the brief's open items 2, 13 and 15, lead L-22, the lanes' tips and T36's G-01
# line, each read only. Items 3, 5, 9 and fribidi's libass path are plans.sh + trace.py; item 17 is
# s5-runs.sh R20; item 16 is the dispatch's (nothing run under /workspace/repos/rocknix).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
export LC_ALL=C; G=/usr/bin/grep; P1=2174265e9c; U=projects/ROCKNIX/packages/ui/
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
S=/workspace/tmp/m6-t37/tmp; L=/workspace/tmp/m6-t37/stage-a/l22
echo "== item 2: does scripts/install or scripts/image rewrite an absolute link? (both read whole at the tip)"
for f in scripts/install scripts/image; do echo "$f lines=$(git show "$P1:$f" | wc -l) link-or-rewrite-lines: $(git show "$P1:$f" | $G -n -E 'readlink|symlink|-type l|ln -s' | tr '\n' ';')"; done
echo "scripts/install:164-185 tars PKG_INSTALL into INSTALL (tar keeps a symlink's target as written):"; git show "$P1:scripts/install" | sed -n '164p;185p'
echo "what INSTALL is in makeinstall_target:"; git show "$P1:scripts/build" | $G -n 'INSTALL="${PKG_INSTALL}"'; git show "$P1:config/functions" | $G -n 'PKG_INSTALL="$BUILD/install_pkg'
echo "scripts/image squashes \${BUILD}/image/system after a chown (no link pass between):"; git show "$P1:scripts/image" | $G -n -E 'chown -R 0:0|mksquashfs "|fakeroot -- '
echo "the ES recipe's :101 (the link) as written:"; git show "$P1:${U}emulationstation/package.mk" | sed -n '101p'
echo
echo "== item 13: the blindspot entries the rules name for a recipe's shapes (grep -n for their words)"
B=docs/blindspot-register.md
$G -n -E '^## (39|47|54|74|75)\. ' "$B"
$G -n -E 'A pinned version in a recipe is a claim about the image only once the image' "$B"
$G -n -E 'with no observed positive' "$B" | cut -d: -f1 | tr '\n' ' '; echo "(lines naming a guard with no observed positive)"
$G -n -E '^\| 14 \|' "$B" | cut -c1-90
echo
echo "== item 15: tools/pixelelated-state-check's usage, and whether the image ships it"
$G -n -E 'add_argument\("--(root|payload|mode|require-ready)"' tools/pixelelated-state-check
echo "packages/projects lines naming it at the tip: $(git grep -c 'pixelelated-state-check' "$P1" -- packages projects | wc -l)"
$G -n -E '^#   vm-serial (sh|script) ' tools/vm-serial
echo
echo "== the lanes' tips (read at stage A, recorded whole)"
for r in origin/feature/m6-es-core-window-input-682 origin/feature/m6-es-core-utils-resources-683; do printf 'distribution %s ' "$r"; git rev-parse --verify "$r" 2>&1; done
for r in origin/feature/m6-es-core-window-input-682 feature/m6-es-core-window-input-682 origin/feature/m6-es-core-utils-resources-683 feature/m6-es-core-utils-resources-683 origin/feature/m6-es-core-components-681; do printf 'ES %s ' "$r"; git -C "$Q" rev-parse --verify "$r" 2>&1; done
echo "ES T36 local branch ahead of the pin: $(git -C "$Q" rev-list --count "$PIN..feature/m6-es-core-utils-resources-683")"
echo "ES T35 b7fdb3a24c ahead of the pin: $(git -C "$Q" rev-list --count "$PIN..b7fdb3a24c")"
R6=$(git rev-parse origin/feature/m6-es-core-utils-resources-683); D6=docs/audits/2026_10_31-epic-m6-es-core-utils-resources
echo "T36's G-01 on the same image, at $R6 (its 00 line 54, the ldd part):"
git show "$R6:$D6/00-running-log.md" | sed -n '54p' | $G -o -E 'BUILD_ID=[0-9a-f]+|`libfreetype[^;]*NOT linked\*\* \([^)]*\)'
echo
echo "== L-22: where the shipped theme names its fonts, read by hash"
C=/workspace/cache/rocknix-sources/es-theme-art-book-next/es-theme-art-book-next-9a50ef366e750aabfab29e6915a2867607212971.tar.gz
echo "tarball sha256 $(sha256sum "$C" | cut -d' ' -f1)"
echo "recipe PKG_SHA256 $(git show "$P1:${U}themes/es-theme-art-book-next/package.mk" | $G -o -E '^PKG_SHA256="[0-9a-f]+"')"
mkdir -p "$L/xml"; tar -xzf "$C" -C "$L/xml" --wildcards '*.xml'; rc=$?
echo "xml extract rc=$rc files=$(find "$L/xml" -name '*.xml' | wc -l) fonts-in-tarball=$(tar -tzf "$C" | $G -c -E '\.(ttf|otf|TTF|OTF)$')"
tar -tzf "$C" | $G -E '\.(ttf|otf|TTF|OTF)$' | sed 's#^[^/]*/##'
cd "$L/xml"/art-book-next-es-* || exit 2
echo "fontPath lines per file: $($G -r -c fontPath --include='*.xml' . | $G -v ':0$' | sort | tr '\n' ' ')"
echo "the variables the fontPath lines use: $($G -r -h -o -E '<fontPath>[^<]*</fontPath>' --include='*.xml' . | sort | uniq -c | sed -E 's/^ +//' | tr '\n' ';')"
echo "their definitions:"; $G -n -E '<font(Bold|Regular|Light|Logo)>' fonts.xml; $G -n -E 'ifSubset' fonts.xml resources/customizations/fonts.xml; $G -n -E 'customizations|fonts.xml' theme.xml | $G -i -E 'include' | sed -E 's/^[[:space:]]+//'
for f in Roboto-Bold Roboto-Regular Roboto-Light ChangaOne-Italic; do echo "_inc/fonts/$f.ttf in tarball: $(tar -tzf "$C" | $G -c "/_inc/fonts/$f.ttf$")"; done
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
echo "the recipe's zh block (themes/es-theme-art-book-next/package.mk:21-27) names:"; git show "$P1:${U}themes/es-theme-art-book-next/package.mk" | sed -n '21,27p' | $G -o -E '/usr/share/fonts/[^<]*' | sort | uniq -c
echo "the ES recipe's CJK fallback link (:83-85) names: $(git show "$P1:${U}emulationstation/package.mk" | sed -n '84p' | $G -o -E '/usr/share/fonts/[^ ]*')"
echo "T42's three patches, font lines: $(for p in 0001-system-style-the-logo-text-for-fullscreen-artwork 001-pixelelated-splash 001-tools-always-show-image; do printf '%s=%s ' "$p" "$(git show "$P1:${U}themes/es-theme-art-book-next/patches/$p.patch" | $G -c -i font)"; done)"
git show "$P1:${U}themes/es-theme-art-book-next/patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch" | $G -n -E '^\+.*font' | sed -E 's/[[:space:]]+/ /g'
echo "the wordmark SVG's font or text lines: $(git show "$P1:${U}themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg" | $G -c -i -E 'font|<text')"
python3 -B -I - "$L" <<'PY'
import re, glob, os, sys
os.chdir(glob.glob(os.path.join(sys.argv[1], "xml", "art-book-next-es-*"))[0])
tok = re.compile(r"<(/?)([A-Za-z_][\w.-]*)([^>]*?)(/?)>|<!--.*?-->", re.S)
tot = 0; bad = []
for f in sorted(glob.glob("**/*.xml", recursive=True)):
    s = open(f).read(); stack = []; kids = {}
    for m in tok.finditer(s):
        if m.group(0).startswith("<!--"): continue
        close, tag, selfc = m.group(1), m.group(2), m.group(4)
        if close:
            while stack:
                t, i = stack.pop()
                if t == tag:
                    k = kids.pop(i, set())
                    if "fontPath" in k:
                        tot += 1
                        if "fontSize" not in k: bad.append((f, tag, s.count("\n", 0, m.start()) + 1))
                    break
            if stack: kids.setdefault(stack[-1][1], set()).add(tag)
        elif selfc:
            if stack: kids.setdefault(stack[-1][1], set()).add(tag)
        else:
            stack.append((tag, m.start()))
print("elements with fontPath (tag-stack scan, tolerant of theme.xml:49's raw &&):", tot, "without a fontSize in the same element:", len(bad))
for b in bad: print("  no fontSize:", *b)
PY
