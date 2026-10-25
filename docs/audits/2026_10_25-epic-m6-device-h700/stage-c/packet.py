"""Build T27's Phase 4.6 packet and its manifest (#674).

Usage: python3 -I -B packet.py <worktree> <out-brief.md> <out-manifest.json>

Code is read from git (`8ebaf8daad`; `651150fc88` and T5's branch for the atf
excerpts; `2174265e9c` for the order). Every file passes the masking sed's
rule (a value after key=/token=/user=/pass...=/psk= becomes ***). Nothing
outside the output paths is written.
"""
import hashlib
import json
import re
import subprocess
import sys

WT, OUT, MANIFEST = sys.argv[1], sys.argv[2], sys.argv[3]
R, U, P1, T5 = "8ebaf8daad", "651150fc88", "2174265e9c", "feature/m6-build-engine-652"
A = "docs/audits/2026_10_25-epic-m6-device-h700"
H = "projects/ROCKNIX/devices/H700"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)


def mask(text):
    return "\n".join(MASK.sub(r"\1***", line) for line in text.splitlines()) + "\n"


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def worktree(path):
    with open(f"{WT}/{path}", encoding="utf-8") as stream:
        return stream.read()


def numbered(text, start=1):
    lines = text.splitlines()
    width = len(str(start + len(lines)))
    return "\n".join(f"{n:>{width}}  {line}" for n, line in enumerate(lines, start))


sources, parts, masked_lines = [], [], 0


def add(title, body, path, ref, kind, fence=True):
    global masked_lines
    data = mask(body)
    masked_lines += sum(1 for a, b in zip(body.splitlines(), data.splitlines()) if a != b)
    sources.append({"path": path, "ref": ref, "kind": kind,
                    "sha256": hashlib.sha256(data.encode()).hexdigest(), "bytes": len(data.encode())})
    parts.append(f"\n\n## {title}\n\n" + (f"```text\n{data}```" if fence else data))


ask = worktree(f"{A}/stage-c/ask.md")
sources.append({"path": f"{A}/stage-c/ask.md", "ref": "worktree", "kind": "ask",
                "sha256": hashlib.sha256(ask.encode()).hexdigest(), "bytes": len(ask.encode())})
parts.append(ask.rstrip("\n"))
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    add(f"The first reader's {name} (whole)", worktree(f"{A}/{name}"), f"{A}/{name}", "worktree", "first reader", fence=False)

order = git("show", f"{P1}:docs/reviews/order.md")
m = re.search(r"^### T27\..*?(?=^### T28\.)", order, re.S | re.M)
add("Context 1: docs/reviews/order.md § T27", m.group(0), "docs/reviews/order.md § T27", P1, "context")
brief = worktree("docs/reviews/briefs/device-h700.md")
m2 = re.search(r"^## 2\. Scope.*?(?=^## 3\.)", brief, re.S | re.M)
m4 = re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M)
add("Context 2: the brief's § 2 and § 4", m2.group(0) + "\n" + m4.group(0), "docs/reviews/briefs/device-h700.md § 2 and § 4", "worktree", "context")
reg = worktree("docs/decision-register.md")
ids = ["D-SYS-002", "D-SYS-003", "D-SYS-004", "D-WORKFLOW-033", "D-WORKFLOW-185", "D-WORKFLOW-114", "D-QA-027",
       "D-WORKFLOW-100", "D-WORKFLOW-150", "D-WORKFLOW-123", "D-WORKFLOW-187", "D-WORKFLOW-209", "D-WORKFLOW-195",
       "D-WORKFLOW-193", "D-WORKFLOW-194"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {i} |") for i in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 3: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")
facts = worktree("docs/releases/device-facts.md").splitlines()
add("Context 4: device-facts rows L15, L16, L29 (with the header)", "\n".join(facts[:4] + [facts[14], facts[15], facts[28]]),
    "docs/releases/device-facts.md rows 15, 16, 29", "worktree", "context")
rule = worktree(".claude/rules/device-builds.md").splitlines()
add("Context 5: .claude/rules/device-builds.md lines 16-24 (the device table)", numbered("\n".join(rule[15:24]), 16),
    ".claude/rules/device-builds.md:16-24", "worktree", "context")

paths = [l for l in worktree(f"{A}/stage-a/paths.txt").split() if not l.endswith((".conf", ".disabled"))]
assert len(paths) == 26, len(paths)
for path in paths:
    add(f"{path} @ {R} (whole, line-numbered, masked)", numbered(git("show", f"{R}:{path}")), path, R, "slice file")
C = f"{H}/linux/linux.aarch64.conf"
conf_r, conf_u = git("show", f"{R}:{C}"), git("show", f"{U}:{C}")
with open("/workspace/tmp/m6-t27/tmp/pk-up.conf", "w") as s:
    s.write(conf_u)
with open("/workspace/tmp/m6-t27/tmp/pk-ours.conf", "w") as s:
    s.write(conf_r)
d = subprocess.run(["diff", "/workspace/tmp/m6-t27/tmp/pk-up.conf", "/workspace/tmp/m6-t27/tmp/pk-ours.conf"], capture_output=True, text=True).stdout
assert sum(1 for l in d.splitlines() if l.startswith("<")) == 12 and sum(1 for l in d.splitlines() if l.startswith(">")) == 13
add(f"{C}: lines 1-6 @ {R}", numbered("\n".join(conf_r.splitlines()[:6])), f"{C}:1-6", R, "config header")
add(f"diff {C} @ {U} (<) against @ {R} (>) (12 removed, 13 added)", d, f"diff {C} {U}..{R}", R, "config diff")
pd = f"{H}/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled"
add(f"{pd}: lines 1-12 @ {R} (of 4,036)", numbered("\n".join(git("show", f"{R}:{pd}").splitlines()[:12])), f"{pd}:1-12", R, "excerpt")

EXCERPTS = [
    ("projects/ROCKNIX/bootloader/mkimage", 1, 113, R), ("projects/ROCKNIX/config.xml", 1, 50, R),
    ("distributions/ROCKNIX/config/functions", 215, 232, R), ("scripts/unpack", 140, 162, R),
    ("projects/ROCKNIX/packages/linux/package.mk", 15, 60, R), ("projects/ROCKNIX/packages/linux/package.mk", 218, 246, R),
    ("projects/ROCKNIX/packages/linux/package.mk", 410, 432, R),
    ("projects/ROCKNIX/packages/tools/atf/package.mk", 1, 60, R), ("projects/ROCKNIX/packages/tools/atf/package.mk", 1, 35, U),
    ("projects/ROCKNIX/packages/tools/atf/package.mk", 1, 35, T5), ("scripts/get_archive", 1, 80, T5),
    ("projects/ROCKNIX/packages/sysutils/busybox/scripts/init", 420, 440, R),
]
for path, a, b, ref in EXCERPTS:
    text = git("show", f"{ref}:{path}")
    b = min(b, len(text.splitlines()))
    add(f"{path} @ {ref}: lines {a}-{b} (excerpt)", numbered("\n".join(text.splitlines()[a - 1:b]), a), f"{path}:{a}-{b}", ref, "excerpt")

body = "\n".join(parts) + "\n"
with open(OUT, "w", encoding="utf-8") as stream:
    stream.write(body)
manifest = {"sources": sources, "masked_lines": masked_lines,
            "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as stream:
    json.dump(manifest, stream, indent=2)
    stream.write("\n")
print(len(sources), "sources;", len(body.encode()), "bytes;", masked_lines, "lines masked;", manifest["packet"]["sha256"])
