# Source-to-acceptance handoff — all runtime controls UNRUN

No checkbox is complete. Coordinator records the next VM-first plan and fresh
resource admission before compilation/runtime. Use the exact proposed ES
source plus the two French entries, bind actual executable bytes after service
readiness, and keep independent trim/source changes identifiable. A passed
fixture with a baseline binary is not proof for the proposal.

| #577 criterion | Prepared source | Required new evidence (UNRUN) |
| --- | --- | --- |
| Stable bounds, in-list status, EN/FR at 640×480 and 1280×800 | Constructor reserves menu/list/status/footer once; row insertion suppresses menu resizing | Initial, populated, refresh, empty, error and retained-error frame sequences for all four language/panel combinations; reviewed rectangle bounds and unclipped status/footer |
| Initial pending, retained refresh, empty/error and retry | In-list Busy/Text, separate range-success flag, fresh metadata on failure, REFRESH retry | `layout-plan.json`, `retry-plan.json`, exact command transcript and happy/error/retry frames; no premature no-networks copy |
| Long-list scrolling and focus survival/disappearance | Unchanged rows are retained; changed list matches SSID then clamps former index | `long-plan.json`; scroll to network 24, refresh with it present, then absent; input walk + frames showing valid selection, native scrolling and unchanged footer; inspect changed-result scroll anchoring and mouse-drag case separately |
| Duplicate scan/back/late completion/retry and worker exits | UI guard + shared pending job; value-only worker; mouse hit filtering; bounded process helper | Repeated confirm/refresh during 8-second delay; BACK immediately, reopen before completion and after completion; no overlapping list/scanlist requests, no join/connect/forget from stale input; hold mouse press across completion; actual frontend/thread/child exits, lifetime sanitizer/control evidence; `scan-process-fixture.cpp` |
| Saved/connected/open/protected/unknown/manual/profile/forget | Existing routing retained; saved/current protocol parsing retained | `routing-plan.json` + `routing-state.json`; synthetic real-UI input through every branch below, exact command transcripts and reviewed frames; unchanged isolated account/offline state before/after |
| Canonical flow, exact-source index, syntax/build/VM/public docs | `flow-and-copy.md` + machine-readable planned coverage | Coordinator applies canonical reference/catalogue changes, compiler `tools/es-syntax-check`, actual build and affected VM suites; reviewed frame index binds commit/binary/locale/panel/branch; public-doc follow-up; no pin promotion before these |

## Fixture provisioning contract

`wifictl-fixture.py` performs no setup or mount and never invokes another
network command. It only reads/writes its own synthetic state/transcript. The
coordinator chooses a new `/storage/qa-wifi-577-<owner>` directory, writes
`ALLOW-SYNTHETIC-WIFI` as `577\n`, copies one plan to `plan.json` and a matching
state to `state.json`, and exposes the script through the fresh guest's private
`wifictl` substitution with `PIXELELATED_WIFI_577_DIR` set. Record mountinfo,
private propagation, original/replacement hashes, and later restoration. No
retired baseline key, port, disk, script owner or original fixture is reused.

The plans are finite: an extra list/scanlist call returns2 and logs
`unexpected-extra-scan`, exposing unintended automatic/duplicate scans. Each
command logs pid/pgid, monotonic start/end and rc. A deadline-killed fixture may
have no end event; require runner failure and actual process-group disappearance,
never reinterpret the missing event as completion. Do not infer whole-worker
exit from its final log alone. Check actual guest threads/children and watched
outer-owner channels. The UI normally performs one range, saved and current
query per scan; NETWORK SETTINGS may independently request current metadata.

Use `state-empty.json` for geometry/long-list plans. For a fresh failure before
any successful scan, use `initial-failure-plan.json`; `retry-plan.json` first
populates rows, then emits partial output with exit2, then succeeds. The partial
row must never appear. The successful-empty plan must remove previous range
rows when current reports no connection. Metadata-failure plan exercises the
existing guarded Check Again route; do not confuse it with range failure.
`initial-empty-plan.json` covers successful zero results on the very first scan.

The initial walk starts at NETWORK SETTINGS with IP ADDRESS focused, matching
the baseline. Its key mapping is that guest's recorded mapping, not a universal
controller-letter promise. Other branch actions below need coordinate/input
walks adapted to the actual new frames, with no blind action on a player's device.

## Routing branches

- Connected Home row: join `Home profile`, never the displayed SSID by guess.
- Saved Cafe row: CONNECT / FORGET / CANCEL. Cancel and confirmation BACK must
  produce no mutation; accepted forget removes only the chosen synthetic profile.
- Two `Shared SSID` profiles, neither active nor named as the SSID: choose the
  profile before join/forget. Preserve the sibling profile.
- Unsaved `Open guest`: security check, `connect-open`, no key editor. Repeat
  with `open_changed=true`: failure/advice, no fallback with an empty key.
- `Protected guest` and `Unknown guest`: existing key editor; cancel writes
  nothing. Only a deliberate synthetic key acceptance may reach `connect`.
- INPUT MANUALLY: saved profile routing and hidden/unknown security behavior;
  names with spaces/colon/backslash stay literal. Never record key argv values.
- `saved_rc=2` / `current_rc=2`: unknown metadata must not turn into an unsaved
  network; fresh check/retry is required. Include empty-success metadata separately.
- Join/connect/forget refusals via plan rc controls retain their existing
  notices and do not report connection/forget success.

The command fixture models backend outcomes, not NetworkManager behavior. A
separate synthetic-nmcli test of the actual repaired wifictl script must cover
rescan/list/pipeline failure propagation. The source-only backend finding in
README remains a production-acceptance blocker until that evidence exists.

## Process helper control

Build `scan-process-fixture.cpp` against the actual `WifiScanProcess.h`, with
assertions enabled, in an admitted disposable Linux job/VM. Run under an outer
deadline/job cleanup mechanism. It covers success, empty, nonzero with partial
output, signal, missing executable, output cap, timeout, a pipe-holding child
after driver exit, and background-child cleanup after normal completion.
Require the expected child/grandchild identity lines as preconditions, direct
and adopted-child reaping, no surviving recorded PID/group, original exit codes
and elapsed times. A missing spawn identity invalidates that timeout case.
ASan/UBSan builds and actual GuiWifi pending-exit/reopen tests remain separate;
the helper fixture alone cannot prove UI lifetime or geometry.

The next executable source experiment, only after the coordinator allocates
its toolchain/output/runner, is compilation of that helper fixture:

```bash
"$WIFI577_CXX" -std=c++14 -UNDEBUG \
  -I "$WIFI577_ES/es-app/src/guis" \
  "$WIFI577_PACKET/fixtures/scan-process-fixture.cpp" \
  -o "$WIFI577_NEW_OUTPUT"
```

`WIFI577_NEW_OUTPUT` must be a fresh path. Execute it only through that job's
bounded outer runner, then qualify GuiWifi itself with the actual ES toolchain
and rendering/lifetime controls. This command is a prepared instruction, not
an execution receipt; it does not provision dependencies or allocate resources.

Nominal command deadlines plus cleanup give an initial scan up to61 seconds,
explicit refresh up to76 seconds, plus spawn/scheduling overhead. These are
worst-case failure bounds, not measured latency. BACK does not wait for them.
An escaped group or uninterruptible process needs outer-runner teardown. No
runtime containment PASS, timing result or resource release is claimed here.
