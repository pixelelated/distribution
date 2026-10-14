# Actual proxy service lifecycle — October 14

Attempt05 passes the bounded current-Python/main/systemd lifecycle in139.59s.
Original payload, owner, lifecycle, runner and launcher exit0; monitor0; no forced
cleanup or surviving owners. All five worker starts, graceful joins before SQLite
close, signed-queue preservation across manual/automatic restarts, exactly-once
normal reconnect, real bulk-lock hold/release across two60s polls, empty folder
polling and consent-disabled usage are observed. Hourly refresh only waits.

Scope: source ad733a64 manifest, exact112 prepared Python files and packaged unit/
controller, older installed native ELFs. The disposable VM has one explicitly
verified private unified-cgroup boot with kernel memory/task limits. This is not
current-native-source provenance, default hybrid boot or final-image acceptance.
#588 separately tracks the potential startup reconnect window; a stable offline
baseline before normal reconnect does not disprove that race.

Original failures remain:
- attempt01: VM20 default hybrid hierarchy fails fixture prerequisite before start.
- attempt02: unified limits pass; staged controller0664 fails203/EXEC. Package uses0755.
- attempt03: readiness/clean Python shutdown pass; unreferenced inactive-unit GC
  resets systemd execution fields. Live RefUnit fixture preserves original status.
- attempt04: stop/manual/automatic restart pass; peer opens before initial monitor
  probe is known offline, yielding online state but no flush. This drives #588.
- attempt05: observes actual background false before reconnect; full scoped PASS.

Every original result is preserved, admission consumed and completed VM/media
retired. Source/protocol/staged-input hashes, guest archives and host-exit proofs
are in each attempt. startup-window-upstream.json checks exact current upstream
2d19684e with the same initialization sequence; no upstream submission.
