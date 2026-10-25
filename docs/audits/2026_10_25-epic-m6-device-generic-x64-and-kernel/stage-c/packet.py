"""Build T11's Phase 4.6 packet and its manifest (#658).

Usage: python3 -I -B packet.py <worktree> <out-brief.md> <out-manifest.json>

Sources are read from git (`8ebaf8daad` for the code, `651150fc88` for one
upstream excerpt) or from the worktree (the audit files and the context).
Nothing outside the output paths is written.
"""
import hashlib
import json
import re
import subprocess
import sys

WT, OUT, MANIFEST = sys.argv[1], sys.argv[2], sys.argv[3]
R = "8ebaf8daad"
U = "651150fc88"
A = "docs/audits/2026_10_25-epic-m6-device-generic-x64-and-kernel"


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def worktree(path):
    with open(f"{WT}/{path}", encoding="utf-8") as stream:
        return stream.read()


def numbered(text, start=1):
    lines = text.splitlines()
    width = len(str(start + len(lines)))
    return "\n".join(f"{n:>{width}}  {line}" for n, line in enumerate(lines, start))


def lines_of(text, first, last):
    return "\n".join(text.splitlines()[first - 1:last])


sources = []
parts = []


def add(title, body, path, ref, kind, fence=True):
    data = body if body.endswith("\n") else body + "\n"
    sources.append({"path": path, "ref": ref, "kind": kind,
                    "sha256": hashlib.sha256(data.encode()).hexdigest(), "bytes": len(data.encode())})
    parts.append(f"\n\n## {title}\n\n" + (f"```text\n{data}```" if fence else data))


ask = worktree(f"{A}/stage-c/ask.md")
sources.append({"path": f"{A}/stage-c/ask.md", "ref": "worktree", "kind": "ask",
                "sha256": hashlib.sha256(ask.encode()).hexdigest(), "bytes": len(ask.encode())})
parts.append(ask.rstrip("\n"))

for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    add(f"The first reader's {name} (whole)", worktree(f"{A}/{name}"), f"{A}/{name}", "worktree", "first reader", fence=False)

order = worktree("docs/reviews/order.md")
m = re.search(r"^### T11\..*?(?=^### T12\.)", order, re.S | re.M)
add("Context 1: docs/reviews/order.md § T11", m.group(0), "docs/reviews/order.md § T11", "worktree", "context")

brief = worktree("docs/reviews/briefs/device-generic-x64-and-kernel.md")
m2 = re.search(r"^## 2\. Scope.*?(?=^## 3\.)", brief, re.S | re.M)
m4 = re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M)
add("Context 2: the brief's § 2 and § 4", m2.group(0) + "\n" + m4.group(0),
    "docs/reviews/briefs/device-generic-x64-and-kernel.md § 2 and § 4", "worktree", "context")

reg = worktree("docs/decision-register.md")
rows = [l for l in reg.splitlines() if re.match(r"^\| (D-WORKFLOW-18[567]|D-QA-053) \|", l)]
assert len(rows) == 4, rows
add("Context 3: register rows D-WORKFLOW-185, -186, -187 and D-QA-053", "\n\n".join(rows),
    "docs/decision-register.md rows D-WORKFLOW-185/186/187, D-QA-053", "worktree", "context")

read = worktree(f"{A}/stage-a/read.txt").split()
assert len(read) == 14, len(read)
for path in read:
    add(f"{path} @ {R} (whole, line-numbered)", numbered(git("show", f"{R}:{path}")), path, R, "read file")

for name in ("install", "mkimage", "release", "rkhelper"):
    path = f"projects/ROCKNIX/bootloader/{name}"
    add(f"{path} @ {R} (whole, line-numbered)", numbered(git("show", f"{R}:{path}")), path, R, "boot script")

conf = "projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf"
add(f"{conf} @ {R}: lines 1-8 (the header)", numbered(lines_of(git("show", f"{R}:{conf}"), 1, 8)), f"{conf}:1-8", R, "config header")
gen = git("show", f"{R}:projects/Generic/linux/linux.x86_64.conf")
ours = git("show", f"{R}:{conf}")
SCRATCH = "/workspace/tmp/m6-t11/tmp"
with open(f"{SCRATCH}/gen.conf", "w") as s:
    s.write(gen)
with open(f"{SCRATCH}/ours.conf", "w") as s:
    s.write(ours)
d = subprocess.run(["diff", f"{SCRATCH}/gen.conf", f"{SCRATCH}/ours.conf"], capture_output=True, text=True).stdout
assert d.count("\n<") + d.startswith("<") == 659 and d.count("\n>") + d.startswith(">") == 351, "diff counts moved"
add("diff projects/Generic/linux/linux.x86_64.conf (<) ours (>) @ " + R + " (659 removed, 351 added)", d,
    "diff Generic conf -> GENERIC_X64 conf", R, "config diff")

EXCERPTS = [
    ("scripts/image", 268, 292, R), ("scripts/mkimage", 137, 182, R), ("scripts/mkimage", 222, 275, R),
    ("config/functions", 1179, 1229, R), ("packages/virtual/image/package.mk", 1, 12, R),
    ("packages/tools/syslinux/package.mk", 53, 80, R), ("packages/tools/installer/scripts/installer", 190, 205, R),
    ("packages/tools/installer/scripts/installer", 285, 300, R), ("projects/ROCKNIX/packages/tools/grub/package.mk", 70, 90, R),
    ("projects/ROCKNIX/packages/tools/rocknix-abl/package.mk", 1, 20, R), ("projects/ROCKNIX/devices/H700/packages/u-boot/package.mk", 20, 40, R),
    ("projects/ROCKNIX/packages/sysutils/busybox/scripts/init", 425, 440, R), ("tools/vm-pair", 30, 80, R),
    ("projects/ROCKNIX/devices/AMD64/config/kernel-firmware.dat", 1, 40, R), ("projects/ROCKNIX/devices/H700/config/kernel-firmware.dat", 1, 30, R),
    ("projects/ROCKNIX/devices/SM8550/config/kernel-firmware.dat", 1, 30, R), ("tools/renovation-inventory", 30, 40, "2174265e9c"),
    ("docs/qa-logs/2026-10-11-usb-revision/guest02/run.py", 1, 25, R), ("projects/ROCKNIX/packages/linux/package.mk", 15, 60, U),
]
for path, a, b, ref in EXCERPTS:
    text = git("show", f"{ref}:{path}")
    n = len(text.splitlines())
    b = min(b, n)
    add(f"{path} @ {ref}: lines {a}-{b} (excerpt)", numbered(lines_of(text, a, b), a), f"{path}:{a}-{b}", ref, "excerpt")

body = "\n".join(parts) + "\n"
with open(OUT, "w", encoding="utf-8") as stream:
    stream.write(body)
manifest = {"sources": sources, "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()),
                                           "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as stream:
    json.dump(manifest, stream, indent=2)
    stream.write("\n")
print(len(sources), "sources;", len(body.encode()), "bytes;", manifest["packet"]["sha256"])
