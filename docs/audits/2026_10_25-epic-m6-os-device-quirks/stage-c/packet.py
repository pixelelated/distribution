"""Build T29's Phase 4.6 packet and its manifest (#676), in T28's shape.

Usage: python3 -I -B packet.py <worktree> <out-brief.md> <out-manifest.json>

Code is read from git (`8ebaf8daad`; `2174265e9c` for the order and the
device facts). Every file passes the masking sed's rule. The paths carry
spaces, so every read is by blob id or a quoted path. 02's 333-row coverage
table is trimmed to a note (D-WORKFLOW-195). Nothing outside the output paths
is written.
"""
import hashlib, json, re, subprocess, sys

WT, OUT, MANIFEST = sys.argv[1], sys.argv[2], sys.argv[3]
R, P1 = "8ebaf8daad", "2174265e9c"
A = "docs/audits/2026_10_25-epic-m6-os-device-quirks"
Q = "projects/ROCKNIX/packages/hardware/quirks/devices"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
TIER_B = ["Retroid Pocket Nova", "QEMU Standard PC (Q35 + ICH9, 2009)", "Anbernic RG40XX H", "Anbernic RG40XX V",
          "Anbernic RG CubeXX", "AYANEO Pocket ACE", "AYANEO Pocket DMG", "AYANEO Pocket DS", "AYANEO Pocket EVO",
          "AYANEO Pocket S 2K", "AYANEO Pocket S Mini", "AYN Odin 2", "AYN Odin 2 Portal", "AYN Thor",
          "Retroid Pocket 6", "Retroid Pocket 6 TOP-DPAD"]


def mask(text):
    return "\n".join(MASK.sub(r"\1***", line) for line in text.splitlines()) + "\n"


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def worktree(path):
    with open(f"{WT}/{path}", encoding="utf-8") as s:
        return s.read()


def numbered(text, start=1):
    lines = text.splitlines(); w = len(str(start + len(lines)))
    return "\n".join(f"{n:>{w}}  {l}" for n, l in enumerate(lines, start))


sources, parts, masked = [], [], 0


def add(title, body, path, ref, kind, fence=True):
    global masked
    data = mask(body)
    masked += sum(1 for a, b in zip(body.splitlines(), data.splitlines()) if a != b)
    sources.append({"path": path, "ref": ref, "kind": kind, "sha256": hashlib.sha256(data.encode()).hexdigest(), "bytes": len(data.encode())})
    parts.append(f"\n\n## {title}\n\n" + (f"```text\n{data}```" if fence else data))


ask = worktree(f"{A}/stage-c/ask.md")
sources.append({"path": f"{A}/stage-c/ask.md", "ref": "worktree", "kind": "ask", "sha256": hashlib.sha256(ask.encode()).hexdigest(), "bytes": len(ask.encode())})
parts.append(ask.rstrip("\n"))
f02 = worktree(f"{A}/02-forward-audit.md")
i = f02.index("<!-- begin t29:coverage -->"); j = f02.index("<!-- end t29:coverage -->") + len("<!-- end t29:coverage -->")
f02 = f02[:i] + "*(The 333-row coverage table is trimmed from this packet: one row per path, every row `tree`; § The entries carries the 88 entries.)*" + f02[j:]
add("The first reader's 02-forward-audit.md (whole but for the coverage table)", f02, f"{A}/02-forward-audit.md (coverage trimmed)", "worktree", "first reader", fence=False)
for name in ("03-retrospective.md", "04-analysis.md"):
    add(f"The first reader's {name} (whole)", worktree(f"{A}/{name}"), f"{A}/{name}", "worktree", "first reader", fence=False)

order = git("show", f"{P1}:docs/reviews/order.md")
add("Context 1: docs/reviews/order.md § T29", re.search(r"^### T29\..*?(?=^### T30\.)", order, re.S | re.M).group(0), "docs/reviews/order.md § T29", P1, "context")
brief = worktree("docs/reviews/briefs/os-device-quirks.md")
add("Context 2: the brief's § 2 and § 4", re.search(r"^## 2\. Scope.*?(?=^## 3\.)", brief, re.S | re.M).group(0) + "\n" +
    re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0), "docs/reviews/briefs/os-device-quirks.md § 2 and § 4", "worktree", "context")
reg = worktree("docs/decision-register.md")
ids = ["D-WORKFLOW-185", "D-WORKFLOW-187", "D-WORKFLOW-195", "D-WORKFLOW-209", "D-UI-121", "D-QA-015", "D-QA-027", "D-QA-053"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 3: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")
facts = git("show", f"{P1}:docs/releases/device-facts.md").splitlines()
add("Context 4: device-facts rows L14, L16, L27, L31 (with the header)", "\n".join(facts[:4] + [facts[i - 1] for i in (14, 16, 27, 31)]),
    "docs/releases/device-facts.md rows 14, 16, 27, 31", P1, "context")

# tier B: each distinct blob once, line-numbered, with every path that carries it
seen = {}
for e in TIER_B:
    for ent in git("ls-tree", "-r", "-z", R, "--", f"{Q}/{e}").split("\0"):
        if not ent: continue
        meta, path = ent.split("\t", 1); mode, _, oid = meta.split()
        if mode == "120000":
            seen.setdefault(("link", path), (oid, [path]))
            continue
        seen.setdefault(oid, (path, []))[1].append(path)
links = sorted(v[1][0] + " -> " + git("cat-file", "-p", v[0]).strip() for k, v in seen.items() if isinstance(k, tuple))
add("Tier B: the symlinks", "\n".join(links), "tier B symlinks", R, "slice file")
blobs = sorted(((v[0], k, v[1]) for k, v in seen.items() if not isinstance(k, tuple)), key=lambda x: x[0])
assert len(blobs) == 26, len(blobs)
for first, oid, paths in blobs:
    shared = "; also " + ", ".join(p[len(Q) + 1:] for p in paths[1:]) if len(paths) > 1 else ""
    add(f"{first[len(Q) + 1:]} @ {R} (blob {oid[:10]}{shared})", numbered(git("cat-file", "-p", oid)), first, R, "slice file")

add("The fixture: tools/t29-battery-unset.py", numbered(worktree(f"{A}/tools/t29-battery-unset.py")), f"{A}/tools/t29-battery-unset.py", "worktree", "fixture")
add("The fixture's output (stage-b/b04_fixture.out)", worktree(f"{A}/stage-b/b04_fixture.out"), f"{A}/stage-b/b04_fixture.out", "worktree", "fixture")

EX = [("projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart", 1, 15), ("projects/ROCKNIX/packages/sysutils/autostart/sources/autostart", 20, 60),
      ("projects/ROCKNIX/packages/hardware/quirks/package.mk", 1, 25), ("projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol", 1, 25),
      ("projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/battery_led_status", 1, 25),
      ("projects/ROCKNIX/packages/sysutils/system-utils/system.d/batteryledstatus.service", 1, 20),
      ("projects/ROCKNIX/packages/hardware/quirks/platforms/H700/001-device_config", 1, 20), ("projects/ROCKNIX/packages/hardware/quirks/platforms/H700/010-led_control", 1, 20),
      ("projects/ROCKNIX/packages/hardware/quirks/platforms/H700/030-analog_leds", 1, 20), ("projects/ROCKNIX/packages/hardware/quirks/platforms/H700/bin/ledcontrol", 1, 80),
      ("projects/ROCKNIX/packages/emulators/libretro/retroarch/scripts/call_achievements_hooks.sh", 1, 25),
      ("projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info", 1, 15), ("projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool", 278, 310),
      ("projects/ROCKNIX/packages/sysutils/powerstate/sources/powerstate.sh", 1, 20),
      (f"{Q}/Powkiddy x55/040-hdmi", 1, 20), (f"{Q}/AYN Odin 3/050-game-configs", 1, 12)]
for path, a, b in EX:
    text = git("show", f"{R}:{path}"); b = min(b, len(text.splitlines()))
    add(f"{path} @ {R}: lines {a}-{b} (excerpt)", numbered("\n".join(text.splitlines()[a - 1:b]), a), f"{path}:{a}-{b}", R, "excerpt")

body = "\n".join(parts) + "\n"
with open(OUT, "w", encoding="utf-8") as s:
    s.write(body)
manifest = {"sources": sources, "masked_lines": masked, "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as s:
    json.dump(manifest, s, indent=2); s.write("\n")
print(len(sources), "sources;", len(body.encode()), "bytes;", masked, "lines masked;", manifest["packet"]["sha256"])
