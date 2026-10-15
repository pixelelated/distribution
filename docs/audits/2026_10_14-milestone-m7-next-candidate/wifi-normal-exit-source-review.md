# Supplemental G-01 normal-exit source review

Source only, no compilation, fixture execution, installed image or runtime acceptance. Proposed ES commit `16dbac5211eea7e70db7394372033be2be7df829` based on frozen `3178b832b8d134198b2b4eede4f725d4ed283f8c`; four changed files, no signal/service/catalog/menu/copy change. Exact file hashes follow.

Read the complete four-file delta and relevant existing process helper/main teardown. A main-thread process owner retains the joinable thread separately from its captured result. Reopening uses the same pending Scan. A ready worker is joined before replacement; constructor failure publishes ready without leaving a joinable thread. Normal shutdown first blocks new scan creation, sets the atomic cancellation flag, joins the current worker and clears its result. The repeated atexit call is idempotent and precedes log closure.

Cancellation is checked at entry, immediately before spawn, in both nonblocking read loops, at completion and before saved/current stages. A cancellation after the pre-spawn check still reaches the child owner and group cleanup. Existing Child destructor closes the descriptor, kills the spawned group and waits up to two seconds for the direct child. Output remains capped; no GUI pointer crosses into the worker. Picker Back does not join and retains its earlier behavior.

No new source defect found for the declared normal SDL/SIGINT/main-tail/atexit path. This is not proof of exact exit latency or successful child reaping on the target. Normal-exit controls should retain original parent/child exits and exact descendants; malformed/failed observations must remain failures.

Signal boundary remains: default SIGTERM, fatal exits, SIGKILL and the `KillMode=process` unit are unchanged. D-CLOUD-133 forbids casually routing SIGTERM through the normal teardown path. A normal-exit hook is not universal owner-death custody; final G-01 disposition must preserve this distinction and the already-documented historical termination caveat. No broad service change is recommended by this readback.

```json
{
  "base": "3178b832b8d134198b2b4eede4f725d4ed283f8c",
  "candidate": "16dbac5211eea7e70db7394372033be2be7df829",
  "files": {
    "es-app/src/guis/GuiWifi.cpp": "405b9a93ba7f5c84c6d7591533c3946a4f26af8011c29b3013d338ffd64cffac",
    "es-app/src/guis/GuiWifi.h": "da5cd40eea619f0c19fc04b9037a0a0bad89d0369bbed4fe7d8eaef1e904703d",
    "es-app/src/guis/WifiScanProcess.h": "17955addc4548d75ae17a844a0a89f74f3421782a6aed1f26af5bfc3886623b2",
    "es-app/src/main.cpp": "0d636bab18d15fab6a19ca67ca532e77a2ccd53c84195fb387df93c5a7065a4b"
  },
  "diff_sha256": "63a666cd3efe07e41f4136a2b01ad7e61da410cc20249de086a56fad3bd1f0a0"
}
```
