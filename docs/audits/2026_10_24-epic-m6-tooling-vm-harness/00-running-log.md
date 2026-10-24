# Running log — M6.P2 T12, the VM harness (#659)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`).
- **Brief:** `docs/reviews/briefs/tooling-vm-harness.md`, version 2 (`74de5c1610`).
- **Dispatch:** the coordinator's comment on #659, 19:04 UTC.
- **Depth:** Independent: one GPT-6 Astra seat at `max`, through the Facilitator.
- **`reviewed-at`:** `facb2ae523`, the branch `HEAD` at stage A. Its 60 paths are byte-equal to `8ebaf8daad`.
- **The lens:** cost against value. Q5's cost table and Q6's value table are the slice's output.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u`.

## [Stage A] 19:05 to 19:06 UTC — scope, host, no-guest controls

- **The first commands** (`.qa-scratch/t12/first-commands.txt`):
  - fetch rc 0; branch `feature/m6-tooling-vm-harness-659` at `facb2ae523`, stacked on P1 (`2174265e9c`); `inventory.json` present;
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, exactly the dispatch's eight paths;
  - `df -i /tmp`: 40 % used; `/workspace`: 20 %.
- **The host before anything ran:**
  - The host file's last line is the coordinator's 18:24 UTC ask to the M7 lane, about the local QA WebDAV backend's obscured `pass =` in four QA logs (#962). It is not this lane's, and it ends `Census: qemu 0, M6 compilers 0`.
  - The census at 19:05:09Z: `pgrep -c -x qemu-system-x86` gives 0.
- **Membership** (§ 2's block; `.qa-scratch/t12/membership.txt`):
  - `paths 60 lines 8790 {'fork-own': 60} {'n/a': 60} {'shell': 10, 'python': 20, 'markdown': 2, 'other': 22, 'text': 3, 'image': 3}`;
  - `the glob also selects, in other areas: 0 paths`;
  - `wc -l` over the 60 at the hash gives 8,813, the 23 newline bytes inside the three PNGs, as the brief says.
  - Equal to the brief.
- **The hash:**
  - the 60 exported from `8ebaf8daad` to `.qa-scratch/t12/at-hash/` (60 files);
  - `git diff --stat 8ebaf8daad HEAD -- <the 60>` is empty;
  - 484,627 bytes;
  - 0 of 60 on `upstream/next`;
  - 145 fork commits since `c445081a59`, 144 without merges.
- **The checkers:** `tools/rules-check --quiet` rc 0. `tools/register-check`: `674 IDs, each once; every citation in the live documents names a row`, rc 0.
- **The push:** `git push -u origin feature/m6-tooling-vm-harness-659` rc 0.
- **The VM question, before any proof:** *Can this be done on the VM?* Yes, for the harness's own behaviour (how `vm-qa` accounts a suite that cannot run, what `vm-stop` waits for, what a walk's frames are). That is one bounded GENERIC_X64 cycle (brief § 5), not yet run. Everything else is the host and the no-guest controls below. Nothing runs on a device.

### The no-guest controls (19:05:45 to 19:05:46 UTC; census 0 before and after; logs in `.qa-scratch/t12/controls/`)

| Command | Exit | Summary |
| --- | ---: | --- |
| `python3 -I tools/vm-pair-test` | 0 | `PASS 9 VM launch controls; fixtures are not a real boot claim` |
| `python3 -I tools/vm-upgrade-readiness-test` | 0 | `PASS 7 storage-readiness controls; actual guest query, synthetic states, no boot claim` |
| `python3 -I tools/vm-stop-test` | 0 | `PASS 7 vm-stop controls` |
| `python3 -I tools/vm-manager-system-check --help` | 1 | `FAIL manager system: not enough values to unpack (expected 2, got 1)`: the tool takes no `--help` (two arguments and stdin) and fails closed on anything else. A lead for stage B: its four checks are `assert` statements, stripped under `-O` or `PYTHONOPTIMIZE`. |
| `python3 -I tools/raofflineproxy-integration-test --help` | 0 | the usage; it needs an unpacked patched proxy source, read at stage B, not run |
| `tools/vm-qa --list` | 0 | 17 names: `scripts lifetime wrapper vocabulary register french quoting menumap pair-identity fresh round-trip exit time-to-play link ra-offline walks frame-diff` |
| `tools/time-to-play --help` | 0 | the usage, ending `Never for a handheld.` |
| `tools/frame-diff --help` | 0 | the usage |
| `tools/vm-visual-qa --help` | 0 | the usage (`--monitor MONITOR  QEMU monitor unix socket`) |
| `tools/vm-pair` (no arguments) | 2 | the usage; the default scratch is `/tmp/rocknix-vm-pair` (a host `/tmp` root: a stage-B Q1/Q2 lead) |
| `tools/es-syntax-check` (no arguments) | 2 | `es-syntax-check: name at least one .cpp`. **Not a pass** (`es-native-ui.md`). |

- **The find/stop grep** (§ 5's `pgrep|pkill|kill` over eight tools): 41 lines (`controls/kill-grep.txt`).
  - Every `pgrep`, `pkill` and `kill` is inside a guest-side call (`S`, `SER`, `SSH`, `g.sh`, `ssh(...)`, `guest(...)`), against RetroArch, EmulationStation, WebKit, rclone or `xprobe`.
  - None finds or stops a host QEMU, as the stranger's proof found.
  - `vm-pair`, `vm-stop` and `vm-qa` have no host-side kill; `vm-pair down`'s own stop path is read at stage B.
- **The `/tmp` grep** over the 60: 84 lines (`controls/tmp-grep.txt`). Most are guest-side (the guest's own `/tmp`). The host-side ones are leads for stage B:
  - `vm-pair:37`'s `DIR` default, `/tmp/rocknix-vm-pair`, where each `up` rebuilds a guest's disk from the image;
  - the default monitor and serial sockets and the QA key path (`ra-offline-test:65-66`, the usage lines of `time-to-play` and `emulator-exit-test`);
  - `ra-offline-test:259`'s `/tmp/ra-offline-acct.$$` and `:345`'s `.steps`;
  - `time-to-play:158`'s SSH control socket `/tmp/ttp-cm-<pid>`.
