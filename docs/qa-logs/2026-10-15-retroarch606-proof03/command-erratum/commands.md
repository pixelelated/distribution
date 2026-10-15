# Root-owned later commands — UNRUN

Use actual-host access and only after the previous allocation is consumed. Commands remain separated at preflight/report/admission for original review.

```bash
TASK_PACKET=/tmp/pix-m7-retroarch-exit-proof-source-20261015-03
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03
TASK_COORD=/workspace/repos/rocknix.worktrees/m7-player-setup
TASK_VERIFY=/workspace/tmp/pix-m7-zerotier-generic-readback-20261015-02/artifacts/result.json
TASK_OWNER=/workspace/tmp/pix-m7-retroarch-exit-proof-20261015-03
TASK_EXPORT=/workspace/tmp/pix-m7-retroarch-exit-evidence-20261015-03
TASK_VNC=ACTUAL_OBSERVED_FREE_DISPLAY
python3 -I -S -B "$TASK_PACKET/fresh/prepare.py" \
  --checkout "$TASK_TREE" --clean-checkout "$TASK_COORD" \
  --verification "$TASK_VERIFY" --owner "$TASK_OWNER" --vnc "$TASK_VNC"
cd "$TASK_TREE"
tools/build-preflight
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_OWNER/retention-plan.json" --output "$TASK_OWNER/retention-report.json"
# Inspect exact original exits/capacity/closure before admission.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_OWNER/admission-plan.json" --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" --activity-dir "$TASK_OWNER" --recursive-activity -- \
  python3 -I -B "$TASK_OWNER/vm-lifecycle.py"
```

Actively supervise at intervals ≤60 seconds. Wait for actual `visual-ready.json`; its1200-second deadline is already running. Only this action route may touch this proof's guest/input/frame. It queues one request; the lifecycle remains the serial/QMP operator. Never run a parallel direct serial or frame command.

```bash
ra_action() { python3 -I -S -B "$TASK_OWNER/action.py" "$@" --owner "$TASK_OWNER"; }
ra_action status
ra_action capture --label es-initial
# View emitted PNG; follow its actual menu and installed input mapping.
ra_action ui-key --key a
# More individually observed ui-key steps as needed to Game Options/Save States.
ra_action capture --label manager-before
ra_action review --label manager-before --review 'ACTUAL TITLE, EMPTY MANAGER AND VISIBLE ITEMS'
# Return to game list without launching a manager tile.
ra_action launch
ra_action capture --label ra-running
ra_action review --label ra-running --review 'ACTUAL FULL-PANEL PROBE PRESENTATION; NO GAMEPLAY CLAIM'
ra_action engine-command --key slot-up
ra_action engine-command --key slot-up
# These emitted original PNGs already exist; do not issue duplicate captures with their labels.
ra_action review --label slot-one --review 'ACTUAL SLOT1 INDICATION'
ra_action engine-command --key save
ra_action review --label manual-saved --review 'ACTUAL SAVED NOTIFICATION/OBSERVATION, WITH FILE READBACK CORROBORATION'
ra_action snapshot --label manual
ra_action snapshot --label pre-exit
# Inspect actual numbered state and AUTO absence before normal Quit.
# One logical quit sends exactly two fixed QUIT requests; do not invoke it twice.
ra_action engine-command --key quit
ra_action snapshot --label stopped
ra_action capture --label es-return
ra_action review --label es-return --review 'ACTUAL SAME FRONTEND RETURN'
# Navigate from current frame to same ExitProbe Game Options/Save States.
ra_action capture --label manager-after
ra_action review --label manager-after --review 'ACTUAL AUTO AND SLOT1 TILES/TIMESTAMPS; CITE ADDITIONAL FRAMES IF REQUIRED'
ra_action status
ra_action finish
```

The action sequence is a review plan, not a script to paste without viewing frames. Additional `ui-key`, `capture`, `review`, and `status` requests stay within their fixed bounds. No extra launch/save/slot/quit is permitted. On ambiguity or a criterion failure, `ra_action abort` preserves originals and lets the exact lifecycle stop; do not repeat input or edit owner files.

After the original launcher/runner/VM exits:

```bash
TASK_RUN=$(cat "$TASK_OWNER/run.path")
python3 -I -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" --output "$TASK_EXPORT"
# Root reviews all original channels, named state bytes/stat records, process/log mapping,
# original frames, unchanged clean gate, and exact owner absence before consumption.
python3 -I tools/host-maintenance/build-admission consume --run "$TASK_RUN" \
  --evidence "$TASK_EXPORT/consumption-draft.json"
```

Then root retains/verifies compact original custody. Only after that verification and consumed receipt, root performs the existing guarded removal of this owner's `vm/disk.qcow2`, `vm/OVMF.fd` and private TMPDIR, retaining exact deleted-path/owner/absence receipt. No unlink command is silently coupled to export or consumption; #606's final no-retained-disk criterion remains incomplete until the actual retirement receipt exists. The source image and all historical originals remain held.
