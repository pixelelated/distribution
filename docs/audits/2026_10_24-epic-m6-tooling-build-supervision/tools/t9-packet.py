#!/usr/bin/env python3
"""Build the GPT seat's one bounded packet for T9 (#656) and its manifest.

    python3 -I t9-packet.py <worktree>   # writes second-opinions/gpt-brief.md and packet-manifest.json

The packet (brief § 5): the ask; 02, 03 and 04 whole; the 18 files whole at
8ebaf8daad, line-numbered; the seven entry lines with context; the controls'
summaries, the two-layer receipts and the record's states. Refuses above
440,000 bytes.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

T = Path(sys.argv[1]); A = T / "docs/audits/2026_10_24-epic-m6-tooling-build-supervision"; Q = T / ".qa-scratch/t9"; H = Q / "at-hash"
def git(*a): return subprocess.run(["git", "-C", str(T), *a], capture_output=True, text=True, check=True).stdout
def numbered(text, lo=1, hi=None):
    ls = text.split("\n"); hi = min(hi or len(ls), len(ls))
    return "\n".join(f"{i:5d}  {ls[i-1]}" for i in range(max(lo, 1), hi + 1))
parts = []; manifest = []
def add(title, body, source):
    body = body.rstrip("\n") + "\n"
    parts.append(f"\n## {title}\n\n```\n{body}```\n" if not title.startswith("!") else f"\n{body}")
    manifest.append({"part": title.lstrip("!"), "source": source, "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()})

ASK = r'''# Second opinion on a code audit -- M6.P2 T9, build supervision and host maintenance, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 18 fork-own files (12 Python, 3 bash, 3 Markdown; 3,795 lines) that supervise a Linux distribution's builds on one shared build host: the runner every build enters (`tools/watch-build`), the status file (`tools/watch-job`), a durable launcher (`tools/watch-build-submit`), a single-use capacity admission (`tools/host-maintenance/build-admission`) with a read-only retention report, a **root-owned swap helper run through a passwordless sudo rule** (`tools/host-maintenance/reclaim-swap`) and its **administrator installer** (`tools/host-maintenance/install`), a preflight, a release-plan preparer and a one-time disk-move script, with their tests and guides. Read at commit `8ebaf8daad`. The build container runs Python 3.10; the host runs 3.14. Nothing was built, reclaimed, installed or published by the first reader; the tests ran in a worktree.

The first reader's draft grades: **Medium** -- F-01 (three recorded controls broken since the admission guard), F-03 (`--stop-vms` kills by `pgrep -f`); **Low** -- F-02, F-04 (`file_digest` vs Python 3.10), F-05 (`died` for an unreadable PID), F-06 (late watcher skips `finish`), F-07 (the lock ends with the runner); F-08 (guards with no control), F-09 and F-10 (legacy layout, the disk-move tool), F-11 (a README control that is not retained).

Answer in three parts, in this order:

1. **Your own findings first, starting with `reclaim-swap`, `install` and `build-admission`** -- the sudo helper, the installer that grants it, and the guard that admits a compiler -- then the rest. List every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. For the helper and installer, look especially at: what a caller who can run the sudo rule, or write the checkout the installer reads from, could make root do; time-of-check against time-of-use on every path and file; signal and timeout paths around `swapoff`/`swapon`; what the policy grants beyond its one command. For the admission: whether a receipt can be reused, replayed across checkouts or registries, or consumed on evidence that does not prove what it claims; and where a refusal can be bypassed.
2. **Refute the first reader.** For every finding F-01 to F-11: agree, disagree, re-grade or narrow, and say what would make it false and whether the packet shows it. Say also whether the guard table in `04` § Q6 lists every guard the code wires, and whether any row marked `yes` rests on a control that does not construct that failure.
3. **What you could not judge.** The claims the packet does not let you verify.

Keep each item to a few lines. At most 7,000 words.

# The packet
'''
parts.append(ASK)
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    add("!" + name, f"## {name} (whole)\n\n" + (A / name).read_text(), name)
for p in (Q / "paths.txt").read_text().split():
    add(f"file, whole, at 8ebaf8daad: {p}", numbered((H / p).read_text(errors="replace")), p)
    manifest[-1]["file_sha256"] = hashlib.sha256((H / p).read_bytes()).hexdigest()
for f in ("Makefile", "scripts/build", "scripts/build_distro", "scripts/image", "scripts/install", "scripts/build_compat"):
    manifest.append({"part": "entry-line file at 8ebaf8daad (context below)", "source": f, "file_sha256": hashlib.sha256((H / f).read_bytes()).hexdigest()})
EX = [("Makefile:30-50", numbered((H / "Makefile").read_text(), 30, 50)),
      ("Makefile:170-212", numbered((H / "Makefile").read_text(), 170, 212))]
for f, line in (("build", 9), ("build_distro", 11), ("image", 9), ("install", 10), ("build_compat", 7)):
    EX.append((f"scripts/{f}:1-{line + 3}", numbered((H / "scripts" / f).read_text(), 1, line + 3)))
EX.append((".github/workflows/fork-checks.yml:30-50", numbered((H / ".github/workflows/fork-checks.yml").read_text(), 30, 50)))
for label, text in EX: add("entry-line context: " + label, text, label)
def rd(f): return (Q / f).read_text()
OUT = [
 ("the eight controls and hooks-test, in the lane's worktree at the hash", rd("controls/summary.txt")),
 ("test-submit.py's receipt, unmodified control (layer 1)", "[Errno 2] No such file or directory: '/tmp/pixelelated-watch-submit-ebkyj88c/tools/host-maintenance/build-admission'"),
 ("test-submit.py's receipt, diagnostic copy with build-admission added (layer 2)", "runner_returncode: 2\ntool-wrapper.rc: 2\nconsole.log: watch-build: build admission required; prepare tools/host-maintenance/build-admission first"),
 ("the record: .build-runs directories and states", rd("record/count.txt") + "build.status first lines over 1,885 runs: finished 1885; runner-error files: 0; 17 run directories without build.status are hand-made folders of tracker readbacks"),
 ("the cost figures", "build.start -> admission.json admitted over 663 recorded runs: median 0.09 s (0.08..0.19)\nwatch-job --build-progress pipeline over the largest recorded build.log (213,562,360 bytes): 0.50, 0.45, 0.44 s; over a 45,743,868-byte log: 0.13 s; watcher.interval 5"),
 ("the container Python record", "device-builds.md:379-380: On 2026-10-08, host Python3.14 accepted a helper using `hashlib.file_digest`, but the build container's Python3.10 lacked it.\nMakefile:138 docker-%: DOCKER_IMAGE_DIGEST := sha256:988c0ba5... (unchanged since 2c349c6d51, 2026-10-01)"),
]
for label, text in OUT: add("output: " + label, text, label)
body = "".join(parts)
out = A / "second-opinions/gpt-brief.md"; out.write_text(body)
n = len(body.encode()); sha = hashlib.sha256(body.encode()).hexdigest()
(A / "second-opinions/packet-manifest.json").write_text(json.dumps({"packet": "gpt-brief.md", "bytes": n, "sha256": sha, "parts": manifest}, indent=1) + "\n")
assert n <= 440000, n
print(n, sha, len(manifest))
