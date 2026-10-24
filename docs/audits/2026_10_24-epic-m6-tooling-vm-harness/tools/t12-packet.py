#!/usr/bin/env python3
"""Build the GPT seat's one bounded packet for T12 (#659) and its manifest.

    python3 -I t12-packet.py <worktree>   # writes second-opinions/gpt-brief.md and packet-manifest.json

The packet (brief § 5): the ask; 02, 03 and 04 whole; the 57 text files of
the slice whole at 8ebaf8daad, line-numbered; the three PNG fixtures named
with size and sha256; generic-x64-vm-testing.md and vm-first.md from next
(what the harness promises); the cycle's outputs. Refuses above 760,000 bytes.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

T = Path(sys.argv[1]); A = T / "docs/audits/2026_10_24-epic-m6-tooling-vm-harness"; Q = T / ".qa-scratch/t12"; H = Q / "at-hash"
def git(*a): return subprocess.run(["git", "-C", str(T), *a], capture_output=True, text=True, check=True).stdout
def numbered(text):
    ls = text.split("\n")
    return "\n".join(f"{i:5d}  {l}" for i, l in enumerate(ls, 1))
parts = []; manifest = []
def add(title, body, source, **extra):
    body = body.rstrip("\n") + "\n"
    parts.append(f"\n## {title}\n\n```\n{body}```\n" if not title.startswith("!") else f"\n{body}")
    manifest.append(dict({"part": title.lstrip("!"), "source": source, "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}, **extra))

ASK = r'''# Second opinion on a code audit -- M6.P2 T12, the VM test harness, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 60 fork-own files (30 scripts: 20 Python, 10 bash; 22 `.steps` walk files, 3 text, 2 Markdown, 3 PNG fixtures named below by size and sha256; 8,790 lines) that make up a Linux distribution's **VM test harness**: the runner that runs 17 suites against one GENERIC_X64 image and writes one report (`tools/vm-qa`), the two-guest launcher (`tools/vm-pair`), the exact-owner stop (`tools/vm-stop`), the UI walk driver (`tools/vm-visual-qa`) with its step files, the frame comparator and its claims contract (`tools/frame-diff`, `tools/vm-walks/claims.txt`), the time-to-play measurement (`tools/time-to-play`), the exit-hotkey test, memory measurements, the offline-achievements scenarios, and their controls. Read at commit `8ebaf8daad`. The audit's lens is **cost against value**: what each suite costs in minutes and host, what it has caught, what it would miss. The first reader ran the three no-guest controls and **one bounded guest cycle** (its outputs are at the end of the packet); nothing was built, nothing touched a handheld.

Answer in three parts, in this order:

1. **Your own findings first, starting with these four**:
   - `vm-qa`'s accounting: can a run exit 0, or a suite read PASS, without having proved what it names? Where is the exit code computed, and what does a SKIP do?
   - `time-to-play`'s headline rule (`headline_missing`, `over_budget`): which inputs make it pass with nothing measured or with a number it should not trust?
   - `frame-diff`'s claims contract: can a claim, a mask or the baseline make a changed pixel invisible, and can a run pass with frames missing?
   - `vm-stop`'s wait: what it waits for, what happens on a timeout, and whether any caller can lose a guest or stop the wrong process.

   Then the rest. List every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. Look especially for: a pass that does not depend on the thing measured; a wait that cannot time out; host state (`/tmp`, ports, the QA cloud) two sessions could share; a guest found or stopped by pattern; a credential printed.
2. **Refute the first reader.** For every finding F-01 to F-20 in `02` § Findings: agree, disagree, re-grade or narrow, and say what would make it false and whether the packet shows it. Say also whether `04` § Q3's suite-by-suite table misses a suite or a constructed input, and whether any row of `04` § Q5 or § Q6 is wrong on the packet's evidence.
3. **What you could not judge.** The claims the packet does not let you verify (the record's reports and the work logs are summarised, not included).

Keep each item to a few lines. At most 7,000 words.

# The packet
'''
parts.append(ASK)
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    add("!" + name, f"## {name} (whole)\n\n" + (A / name).read_text(), name)
for p in (Q / "paths.txt").read_text().split():
    b = (H / p).read_bytes()
    if p.endswith(".png"):
        manifest.append({"part": "PNG fixture, named not attached", "source": p, "bytes": len(b), "file_sha256": hashlib.sha256(b).hexdigest()})
        parts.append(f"\n## PNG fixture (not attached): {p}\n\n{len(b)} bytes, sha256 {hashlib.sha256(b).hexdigest()}\n")
        continue
    add(f"file, whole, at 8ebaf8daad: {p}", numbered(b.decode(errors="replace")), p, file_sha256=hashlib.sha256(b).hexdigest())
for rule in (".claude/rules/vm-first.md", ".claude/rules/generic-x64-vm-testing.md"):
    text = git("show", "next:" + rule)
    add(f"read-only context, from next: {rule}", numbered(text), "next:" + rule, file_sha256=hashlib.sha256(text.encode()).hexdigest())
C = A / "cycle"
OUT = [
 ("the no-guest controls at stage A", (Q / "controls/summary.txt").read_text() if (Q / "controls/summary.txt").exists() else
  "vm-pair-test rc=0 PASS 9 VM launch controls\nvm-upgrade-readiness-test rc=0 PASS 7 storage-readiness controls\nvm-stop-test rc=0 PASS 7 vm-stop controls\nvm-qa --list rc=0 (17 names)\nes-syntax-check (no args) rc=2\nvm-manager-system-check --help rc=1 FAIL manager system: not enough values to unpack"),
 ("the cycle: vm-qa --skip-up --only fresh,round-trip,exit,time-to-play,frame-diff (report.md)", (C / "vm-qa/report.md").read_text()),
 ("the cycle: time-to-play --repeat 0 --only launch,exit,g2g --vm (stdout)", (C / "ttp-repeat0.out").read_text()),
 ("the cycle: emulator-exit-test --vm --only X (stdout)", (C / "exit-onlyX.out").read_text()),
 ("the cycle: guest checks", (C / "guest-checks.txt").read_text()),
 ("host probe: vm-manager-system-check with and without PYTHONOPTIMIZE", (Q / "probes/manager-check-optimize.txt").read_text()),
]
for label, text in OUT: add("output: " + label, text, label)
body = "".join(parts)
out = A / "second-opinions/gpt-brief.md"; out.parent.mkdir(exist_ok=True); out.write_text(body)
n = len(body.encode()); sha = hashlib.sha256(body.encode()).hexdigest()
(A / "second-opinions/packet-manifest.json").write_text(json.dumps({"packet": "gpt-brief.md", "bytes": n, "sha256": sha, "parts": manifest}, indent=1) + "\n")
assert n <= 760000, n
print(n, sha, len(manifest))
