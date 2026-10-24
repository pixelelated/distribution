#!/usr/bin/env python3
"""Build the GPT seat's one bounded packet for T8 (#655) and its manifest.

    python3 -I t8-packet.py <worktree>   # writes second-opinions/gpt-brief.md and packet-manifest.json

The packet (brief § 5): 02 without its generated rows, 03, 04 without its
generated Q4 rows, the Q4 table, the 35 fork-own files whole, the
upstream-carried paths that differ from upstream/next as their diff, line-
numbered excerpts of every cited line +/-20 (or the whole file where it is
short), the mechanical outputs, and the ask. A redirect's query string (a
signed, expiring token) is cut before anything is written. Refuses above
440,000 bytes.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

T = Path(sys.argv[1]); A = T / "docs/audits/2026_10_24-epic-m6-image-packages"; Q = T / ".qa-scratch/t8"; H = Q / "at-hash"
P = "projects/ROCKNIX/packages/"
def git(*a): return subprocess.run(["git", "-C", str(T), *a], capture_output=True, text=True, check=True).stdout
def numbered(text, lo=1, hi=None):
    ls = text.split("\n"); hi = min(hi or len(ls), len(ls))
    return "\n".join(f"{i:5d}  {ls[i-1]}" for i in range(max(lo, 1), hi + 1))
def nosig(s): return re.sub(r"(https?://\S+?)\?\S*", r"\1?<query cut>", s)
parts = []; manifest = []
def add(title, body, source):
    body = nosig(body).rstrip("\n") + "\n"
    parts.append(f"\n## {title}\n\n```\n{body}```\n" if not title.startswith("!") else f"\n{body}")
    manifest.append({"part": title.lstrip("!"), "source": source, "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()})

ASK = r'''# Second opinion on a code audit -- M6.P2 T8, the image's own packages, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the command output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 485 paths of a handheld Linux distribution's own package recipes (`projects/ROCKNIX/packages/`, 260 `package.mk` and 225 scripts, units and configs), read at one commit (`8ebaf8daad`) against three movers -- the merge of the upstream distribution (`upstream/next` at `e0f9deb899`, base `c445081a59`), the never-run `make update`, and the fork's own currency. No build ran; nothing was changed. The tables are generated and their counts asserted by script.

The first reader's draft grades: **Medium** -- F-02 (a recipe writes a symlink at load, #852), F-11 (the upstream merge's `glslang` modify/delete would downgrade it under a coupled pin); **Low** -- F-03 and F-04 (dead primary URLs the mirror covers), F-05 (`cairo` behind), F-06 (the freshness tool's blind spots), F-07 (short hash pins), F-08 (a lint's false positive), F-09 (nine conflicts at the merge), F-10 (a unit and udev rule wired to an absent script), F-12 (eleven orphans and their pin changes). F-01 is another lane's issue (#890), already fixed in a packet.

Answer in three parts, in this order:

1. **Your own findings first.** Read the fork-own files, the diffs, the excerpts and the outputs, and list every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. Look especially at: the fork's scripts and units (`sway-ready`, `111-sway-init`, `installer`, `avahi-daemon.service`), the overrides that reset a pin after sourcing a generic recipe, the conflict list's dispositions, and any recipe that writes outside its own build step.
2. **Refute the first reader.** For every finding: agree, disagree, re-grade or narrow, and in each case say what would make the finding false and whether the packet shows it. Say also whether the conflict list's eleven dispositions and the orphan table's "after the base merge" column hold on the packet's own evidence, and whether any Q4 row reads `current` on evidence the packet does not carry.
3. **What you could not judge.** The claims the packet does not let you verify, so the orchestrator knows where its evidence was thin.

Keep each item to a few lines. At most 7,000 words.

# The packet
'''
parts.append(ASK)
f02 = (A / "02-forward-audit.md").read_text(); f02 = f02[:f02.index("| Path | Tier | Reach | Lines |")] + "(the 485 generated coverage rows are omitted from this packet)\n"
add("!02", "## 02-forward-audit.md (whole, less the generated coverage rows)\n\n" + f02, "02-forward-audit.md")
add("!03", "## 03-retrospective.md (whole)\n\n" + (A / "03-retrospective.md").read_text(), "03-retrospective.md")
f04 = (A / "04-analysis.md").read_text()
i = f04.index("| Recipe path | Name | Pin"); j = f04.index("### Q5 Efficiency")
f04 = f04[:i] + "(the 260 generated Q4 rows are the next part, `q4-table.md`)\n\n" + f04[j:]
add("!04", "## 04-analysis.md (whole, less the Q4 rows, which follow)\n\n" + f04, "04-analysis.md")
add("!q4", "## q4-table.md (whole)\n\n" + (A / "q4-table.md").read_text(), "q4-table.md")
fork = [l.split("\t")[1].strip() for l in (Q / "prov-base.txt").read_text().splitlines()]
for p in fork:
    f = H / p
    add(f"fork-own file, whole, at 8ebaf8daad: {p}", numbered(f.read_text(errors="replace")), p)
ups = [l for l in (Q / "upcarried-differs.txt").read_text().splitlines() if l]
add("the upstream-carried paths that differ from upstream/next (64): `git diff upstream/next 8ebaf8daad -- <path>` (minus is upstream's, plus is the fork's tree)",
    git("diff", "upstream/next", "8ebaf8daad", "--", *ups), "git diff upstream/next 8ebaf8daad -- <64 paths>")
EX = [  # (label, text) excerpts of cited lines, at the hash unless named
 (P + "network/simple-http-server/package.mk (whole)", numbered((H / (P + "network/simple-http-server/package.mk")).read_text())),
 (P + "virtual/image/package.mk:89-113", numbered((H / (P + "virtual/image/package.mk")).read_text(), 89, 113)),
 (P + "apps/moonlight/package.mk (whole)", numbered((H / (P + "apps/moonlight/package.mk")).read_text())),
 (P + "x11/xserver/xwayland/package.mk (whole)", numbered((H / (P + "x11/xserver/xwayland/package.mk")).read_text())),
 (P + "x11/xserver/xwayland/system.d/xorg-configure@.service (whole)", numbered((H / (P + "x11/xserver/xwayland/system.d/xorg-configure@.service")).read_text())),
 (P + "x11/xserver/xwayland/udev.d/97-xorg.rules (whole)", numbered((H / (P + "x11/xserver/xwayland/udev.d/97-xorg.rules")).read_text())),
 (P + "devel/libaio/package.mk (whole)", numbered((H / (P + "devel/libaio/package.mk")).read_text())),
 ("upstream/next:packages/graphics/vulkan/glslang/package.mk:1-24", numbered(git("show", "upstream/next:packages/graphics/vulkan/glslang/package.mk"), 1, 24)),
 ("8ebaf8daad:scripts/update_packages (whole)", numbered(git("show", "8ebaf8daad:scripts/update_packages"))),
 ("8ebaf8daad:scripts/get_archive:1-60", numbered(git("show", "8ebaf8daad:scripts/get_archive"), 1, 60)),
 ("52e6794ba7:scripts/get_archive:1-20 (T5's branch, merging before this one)", numbered(git("show", "52e6794ba7:scripts/get_archive"), 1, 20)),
 ("8ebaf8daad:distributions/ROCKNIX/options:180-190", numbered(git("show", "8ebaf8daad:distributions/ROCKNIX/options"), 180, 190)),
 ("8ebaf8daad:tools/fork-package-freshness:36-101", numbered(git("show", "8ebaf8daad:tools/fork-package-freshness"), 36, 101)),
 ("8ebaf8daad:tools/pkgcheck:134-170", numbered(git("show", "8ebaf8daad:tools/pkgcheck"), 134, 170)),
 ("8ebaf8daad:" + P + "virtual/network/package.mk (the fork's, whole above; its :26 adds simple-http-server)", ""),
]
for label, text in EX:
    if text: add("excerpt: " + label, text, label)
def rd(f): return (Q / f).read_text()
OUT = [
 ("effective.txt: every row whose checksum is empty or unset beside a non-git URL", "\n".join(l for l in rd("effective.txt").splitlines() if re.search(r"sha=\[\] ", l) and re.search(r"url=\[(https?|ftp)://", l) and not re.search(r"url=\[[^]]*\.git\]", l))),
 ("effective.txt: the rows whose pin differs between the three plans", "\n".join(l for l in rd("effective.txt").splitlines() if l.split()[1] in ("libfmt",))),
 ("probe/head.txt: every row that did not answer 200 or a redirect", "\n".join(l for l in rd("probe/head.txt").splitlines() if l.split()[1] not in ("200", "301", "302", "303", "308"))),
 ("probe/head.txt: the status-code histogram", "\n".join(f"{c} {n}" for n, c in sorted(__import__('collections').Counter(l.split()[1] for l in rd("probe/head.txt").splitlines()).items()))),
 ("probe/controls.txt", rd("probe/controls.txt")),
 ("probe/fetch.txt: every redirected archive that did not match", "\n".join(l for l in rd("probe/fetch.txt").splitlines() if "sha-match" not in l) + f"\n(and {sum(1 for l in rd('probe/fetch.txt').splitlines() if 'sha-match' in l)} rows `sha-match`)"),
 ("probe/git.txt", rd("probe/git.txt")),
 ("base-merge.txt: the CONFLICT lines (the whole tree; 9 of them on this slice's paths)", "\n".join(l for l in rd("base-merge.txt").splitlines() if l.startswith("CONFLICT"))),
 ("pkgcheck: the FAIL lines, the tree's copy then T6's", "\n".join(l for l in rd("pkgcheck-pkgcheck.txt").splitlines() if l.startswith("FAIL")) + "\n--\n" + "\n".join(l for l in rd("pkgcheck-pkgcheck-t6.txt").splitlines() if l.startswith("FAIL"))),
 ("units-exec.txt", rd("units-exec.txt")),
 ("update-set: this slice's names in RK3588's set, then config/blocklist", "\n".join(sorted(set(rd("update-set-RK3588.txt").split()) & {Path(p).parent.name for p in rd("recipes.txt").split()})) + "\n--\n" + rd("blocklist.txt")),
 ("q4c.txt (the freshness tool, rc 2)", rd("q4c.txt")),
 ("q4c-hash.txt (the hash pins' compare)", rd("q4c-hash.txt")),
 ("record-stamps.txt: names with no stamp in any root (empty means none)", "\n".join(l for l in rd("record-stamps.txt").splitlines() if l.startswith("0 ")) or "(none)"),
 ("grep-fixture.sh and each pattern's count on it (1 each)", rd("grep-fixture.sh") + "counts: eval 1, xargs 1, redirection 1, rm-then-ln 1"),
]
for label, text in OUT: add("output: " + label, text, label)
body = "".join(parts)
out = A / "second-opinions/gpt-brief.md"; out.write_text(body)
n = len(body.encode()); sha = hashlib.sha256(body.encode()).hexdigest()
(A / "second-opinions/packet-manifest.json").write_text(json.dumps({"packet": "gpt-brief.md", "bytes": n, "sha256": sha, "parts": manifest}, indent=1) + "\n")
assert n <= 440000, n
print(n, sha, len(manifest))
