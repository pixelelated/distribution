"""Build T28's Phase 4.6 packet and its manifest (#675), in T27's shape.

Usage: python3 -I -B packet.py <worktree> <out-brief.md> <out-manifest.json>

Code is read from git (`8ebaf8daad`; `651150fc88` for upstream's replacement;
`2174265e9c` for the order and the device facts). Every file passes the
masking sed's rule (a value after key=/token=/user=/pass...=/psk= becomes
***). Nothing outside the output paths and TMPDIR is written.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

WT, OUT, MANIFEST = sys.argv[1], sys.argv[2], sys.argv[3]
R, U, P1 = "8ebaf8daad", "651150fc88", "2174265e9c"
A = "docs/audits/2026_10_25-epic-m6-device-sm8550"
S = "projects/ROCKNIX/devices/SM8550"
TMP = os.environ.get("TMPDIR", "/workspace/tmp/m6-t28/tmp")
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
m = re.search(r"^### T28\..*?(?=^### T29\.)", order, re.S | re.M)
add("Context 1: docs/reviews/order.md § T28", m.group(0), "docs/reviews/order.md § T28", P1, "context")
brief = worktree("docs/reviews/briefs/device-sm8550.md")
m2 = re.search(r"^## 2\. Scope.*?(?=^## 3\.)", brief, re.S | re.M)
m4 = re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M)
add("Context 2: the brief's § 2 and § 4", m2.group(0) + "\n" + m4.group(0), "docs/reviews/briefs/device-sm8550.md § 2 and § 4", "worktree", "context")
reg = worktree("docs/decision-register.md")
ids = ["D-QA-015", "D-QA-023", "D-QA-027", "D-WORKFLOW-114", "D-WORKFLOW-123", "D-WORKFLOW-150", "D-WORKFLOW-185",
       "D-WORKFLOW-187", "D-WORKFLOW-195", "D-WORKFLOW-209"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {i} |") for i in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 3: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")
facts = git("show", f"{P1}:docs/releases/device-facts.md").splitlines()
add("Context 4: device-facts rows L17-L20, L27, L28, L31 (with the header)",
    "\n".join(facts[:4] + [facts[i - 1] for i in (17, 18, 19, 20, 27, 28, 31)]),
    "docs/releases/device-facts.md rows 17-20, 27, 28, 31", P1, "context")
rule = worktree(".claude/rules/device-builds.md").splitlines()
add("Context 5: .claude/rules/device-builds.md lines 16-26 (the device table)", numbered("\n".join(rule[15:26]), 16),
    ".claude/rules/device-builds.md:16-26", "worktree", "context")

paths = [l for l in worktree(f"{A}/stage-a/paths.txt").split() if not l.endswith(".disabled")]
assert len(paths) == 28, len(paths)
for path in paths:
    add(f"{path} @ {R} (whole, line-numbered, masked)", numbered(git("show", f"{R}:{path}")), path, R, "slice file")
pd = f"{S}/patches/linux/0053-add-hynitron-touchscreen.patch.disabled"
add(f"{pd}: lines 1-12 @ {R} (of 20,593)", numbered("\n".join(git("show", f"{R}:{pd}").splitlines()[:12])), f"{pd}:1-12", R, "excerpt")
C = f"{S}/linux/linux.aarch64.conf"
conf_r, conf_u = git("show", f"{R}:{C}"), git("show", f"{U}:{C}")
for name, text in (("pk-up.conf", conf_u), ("pk-ours.conf", conf_r)):
    with open(f"{TMP}/{name}", "w") as s:
        s.write(text)
d = subprocess.run(["diff", f"{TMP}/pk-up.conf", f"{TMP}/pk-ours.conf"], capture_output=True, text=True).stdout
assert sum(1 for l in d.splitlines() if l.startswith("<")) == 7 and sum(1 for l in d.splitlines() if l.startswith(">")) == 7
add(f"{C}: lines 1-6 @ {R}", numbered("\n".join(conf_r.splitlines()[:6])), f"{C}:1-6", R, "config header")
add(f"diff {C} @ {U} (<) against @ {R} (>) (7 removed, 7 added)", d, f"diff {C} {U}..{R}", R, "config diff")
add("CONFIG_DRM_MSM and CONFIG_EXTRA_FIRMWARE in the four Qualcomm configurations @ " + R,
    "\n".join(f"{dv}: " + " ".join(l for l in git("show", f"{R}:projects/ROCKNIX/devices/{dv}/linux/linux.aarch64.conf").splitlines()
                                   if re.match(r"^CONFIG_(DRM_MSM|EXTRA_FIRMWARE)=", l)) for dv in ("SM8550", "SM8650", "SM8750", "SM8250")),
    "the four confs' DRM_MSM and EXTRA_FIRMWARE lines", R, "excerpt")

EXCERPTS = [
    ("projects/ROCKNIX/packages/linux/package.mk", 1, 120, R), ("projects/ROCKNIX/packages/linux/package.mk", 190, 290, R),
    ("projects/ROCKNIX/packages/linux/package.mk", 380, 432, R), ("projects/ROCKNIX/packages/linux/package.mk", 1, 60, U),
    ("scripts/mkimage", 250, 270, R), ("projects/ROCKNIX/bootloader/mkimage", 1, 115, R),
    ("projects/ROCKNIX/bootloader/install", 1, 75, R), ("distributions/ROCKNIX/config/functions", 220, 235, R),
    ("distributions/ROCKNIX/config/functions", 380, 402, R), ("projects/ROCKNIX/config.xml", 125, 150, R),
    ("projects/ROCKNIX/config.xml", 130, 150, U), ("scripts/unpack", 140, 162, R),
    ("projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl", 1, 80, R),
    ("projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl", 1, 100, U),
    ("projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk", 1, 95, R),
    ("projects/ROCKNIX/packages/tools/qcom-abl/package.mk", 1, 20, R), ("projects/ROCKNIX/packages/tools/rocknix-abl/package.mk", 1, 30, R),
    ("projects/ROCKNIX/packages/tools/rocknix-abl/sources/README", 1, 20, R), ("projects/ROCKNIX/packages/tools/openabl/package.mk", 1, 40, U),
    ("projects/ROCKNIX/packages/tools/mkbootimg/package.mk", 1, 40, R), ("projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk", 1, 40, R),
    ("projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk", 1, 40, U), ("projects/ROCKNIX/packages/tools/inputplumber/package.mk", 1, 60, R),
    ("projects/ROCKNIX/packages/tools/inputplumber/package.mk", 1, 60, U), ("projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk", 1, 40, R),
    (f"{S}/bootloader/update.sh", 1, 50, U), (f"{S}/options", 1, 90, U),
    ("projects/ROCKNIX/packages/virtual/arm-efi/package.mk", 1, 40, U), ("distributions/ROCKNIX/options", 14, 20, R),
    ("distributions/ROCKNIX/options", 198, 206, R), ("projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart", 1, 15, R),
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
