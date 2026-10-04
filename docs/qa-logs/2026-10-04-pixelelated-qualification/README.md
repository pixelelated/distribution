# pixelelated candidate qualification — in progress

Refs #383, #409, #395. Can this be done on the VM? Yes: two fresh GENERIC_X64
guests from the verified22533e35b95a bundle, then an actual ROCKNIX RC2 update
rehearsal and exact installed payload readbacks. No handheld or personal cloud.

First stage started06:54:19UTC on2026-10-04. Owner
`/workspace/tmp/pixelelated-m7-qa-01`; run
`/workspace/repos/rocknix.worktrees/m7-pixelelated/.build-runs/20261004T065419Z-2eb808cf`.
Runner2152966/watcher2152982, shared5s heartbeat/5min suspected inactivity,
recursive owned artifacts. Tool session4686 is actively supervised at most60s
apart; no disconnected delivery is configured. At06:56UTC both guests had
bootedb137d8c373 and answered SSH; the scripts suite was writing fresh output.
No suite or whole-image verdict is claimed by this launch record.

The prepared qualify/source/payload harness hashes verify. Source copies are
in the earlier build-preparation directory. The fixed `outer.sh` writes its
qualification wrapper result **inside the watched command boundary**, before
the runner/outer tool can finish. `inner.rc`, `outer.rc`, run build.rc/status
and eventual tool-session exit remain distinct observations. This improves
result retention; it does not claim to resolve #395's prior143 discrepancy.

The ordered prepared link/guest/runtime stages follow this stage only on0.
Their source copies and commands are in the build-preparation directory.
Later pair/localisation/memory/proxy/image sweeps and P4 remain required.
