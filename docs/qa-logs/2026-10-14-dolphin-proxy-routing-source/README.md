# Dolphin offline-proxy routing — #584 — 2026-10-14

Source-only candidate. The full configuration-script fixture is **UNRUN**. No
Dolphin/proxy process, listener, account, provider, service operation, build,
compiler, or device operation was performed. #583's original819 packet and its
separate review revision remain immutable; neither is a prerequisite for testing
this routing change.

The product change is limited to
`projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/cheevos_dolphin.sh`.
It retains the raw hardcore setting before the existing Boolean conversion and
selects `HostUrl = 127.0.0.1:8080` only when the offline toggle is exactly `1`,
raw hardcore is exactly `0`, and the PPSSPP listener predicate succeeds. The
function is byte-identical to PPSSPP's existing read-only predicate. There are
no new external commands or dependency changes.

Every fallback retains the configured custom host, including an empty host.
The existing enabled/token refusals precede the new routing branch. Unknown or
empty hardcore still has the existing INI conversion, but does **not** authorize
proxy routing. Generated username/token fields remain the original pass-through;
no saved credentials, `system.cfg`, custom host, global hardcore, service state,
queue, or save path is changed to arrange routing. The normal output INI and
existing diagnostic log remain the script's outputs. #581's launcher/save-path
work is separate and untouched; this packet makes no whole-launcher safety claim.

The predicate accepts listening IPv4 loopback, IPv4 wildcard, or IPv4-mapped
IPv6 loopback on port8080. It rejects pure IPv6, other addresses/ports, and
non-listening states. Both absent/unreadable tables produce the unreadable
fallback; readable tables without a match produce the absent-listener fallback.
One matching readable table suffices. This is a socket-presence gate, **not**
proof of service ownership, identity, authentication, or protocol readiness.
A socket can disappear after the check. These limitations match the existing
PPSSPP policy and are not strengthened into a readiness claim here.

## Exact source and upstream disposition

[Issue584](https://github.com/pixelelated/distribution/issues/584) and its complete
comments were read at02:49UTC; retained bodies, search scope, dates and original
read exits are in `research/`. Current upstream ROCKNIX `next`
`becc8cb2a97b8b44b25d39dd5b6aa8f77b0af1c5` still only reads customhost.
[PR3038](https://github.com/ROCKNIX/distribution/pull/3038) already added HostUrl
support and is included; it is not another fix to import. Local history
`c6f87a606d94e27cf084bde64ce55101c2b10f39` confirms that intent. The fork's existing
new/legacy unofficial-setting compatibility is preserved. The scoped public
HostUrl issue/PR searches found no additional matching fix; this is not an
exhaustive upstream-clear claim.

[RAOfflineProxy PR50](https://github.com/misantronic/RAOfflineProxy/pull/50) supplies
upstream Dolphin configuration support, also already present. The packaged unit
instead invokes `python3 -m raofflineproxy.main run-service`, bypassing that
interactive configuration path. `source/proxy-main.py.txt` and
`source/raofflineproxy.service` retain exact source proof. Merely enabling that
unit cannot fill the launcher's missing toggle routing.

Dolphin pin `6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4` (2606), with bundled
rcheevos `926e4608f8dca7989267c787bbefb3ab1c835ac5`, supplies the actual HostUrl
contract. Six cached files were checked byte-for-byte against their git objects;
`bindings.json` records whole-file SHA256/git blobs and all16 distribution patch
hashes. None of those patches changes the HostUrl/rc_client/rc_api path. Readable
line-bound extracts are in [host-url-excerpts.md](source/host-url-excerpts.md):

1. `AchievementSettings.cpp` maps the INI's `Achievements/HostUrl` to RA_HOST_URL.
2. `AchievementManager::Init` passes a nonempty value to `rc_client_set_host`.
3. `rc_client_set_host` stores that host. `rc_api_url_build_dorequest_url` adds
   `http://` when it lacks a scheme, then appends `/dorequest.php`.
4. Thus this candidate's bare host yields
   `http://127.0.0.1:8080/dorequest.php`. The bundled upstream no-protocol test
   corroborates the source contract; that C test was **read, not run**. The
   default-host `RCHEEVOS_URL_SSL` definition does not override the custom host.
5. Dolphin's request callback uses the resulting URL. This proves source
   interpretation, not the identity or behavior of an installed Dolphin binary.

Contribution disposition (D-WORKFLOW-164): this is distribution integration
owned by `pixelelated/distribution`, with a possible focused
`ROCKNIX/distribution` contribution if its offline service/toggle contract is
adopted. A standalone upstream PR needs those dependencies or an explicit
adaptation, not a blind copy of a fork-only setting. No Dolphin or rcheevos
engine patch is justified by these bytes; no duplicate submission of3038/50.
The separate #583 RVZ decoder/index candidates retain their own upstream targets.
No upstream submission was made.

## Prepared VM proof and smallest next command

Can this be done on the VM? **Yes.** One coordinator-allocated disposable no-NIC
GENERIC_X64 VM can run the full configuration scripts with synthetic inputs.
No production profile, settings, installed account, emulator, proxy, or socket
listener is needed. Stage this small packet only, verify `SHA256SUMS`, then run
once from its directory as VM root under the coordinator's watched owner:

```sh
python3 -I -S -B fixtures/probe.py --output /run/pix584-route01
```

The path must be fresh; no retry/overwrite is automatic. This command is a
proposal, **not an allocation or an executed result**. Coordinator records the
VM plan/admission in #584, identity of this sealed packet, original command exit,
owner result, and finite process scope. Give the watched owner a75-second outer
wall limit covering60seconds of fixture work and bounded cleanup. On owner
interruption it must kill/reap the entire disposable scope and retain the
intervention as failure. The internal parent-death and cleanup mechanisms are
prepared, not runtime-qualified. No GNU `timeout`, `unshare`, `mount`, `chroot`
applet, `ldd`, or installed compiler is assumed by the command.

`fixtures/probe.py` refuses changed bindings/source, requires root and a fresh
`/run/pix584-*`, checks48MiB free including16MiB reserve, and copies at most24MiB
of actual guest Bash/cat and loader dependencies into a chroot. It parses ELF
headers statically and rejects non-x86-64/nonstandard search paths or missing
libraries. Invocation paths remain `/bin/bash` and `/bin/cat` even if the latter
resolves to BusyBox. It records requested/resolved/invocation paths and byte
hashes, plus the actual Python version. It never uses an installed profile.

Each child gets a new network namespace through the syscall, verified by
namespace identity before chroot; no interface is configured or listener opened.
After chroot it drops to UID/GID65534, drops supplementary groups, sets
no-new-privileges and re-arms/reads back parent-death KILL after the UID change.
This also makes the root-owned mode000 listener-table control truly unreadable.
Only the fixture profile, data, Bash/cat and libraries exist in the chroot.
Failure to establish containment is failure before the shell script, not a
configuration-test result.

Bounds:60-second internal work alarm,50CPU seconds/256MiB address space for the
owner;3-second wait,2CPU seconds,64KiB per output file and no cores for each
script. Runtime-file staging refuses a file larger than16MiB before reading it;
the owner also has a16MiB file-size limit. Scratch is checked against32MiB at
completion; this is an asserted aggregate bound, not a filesystem quota. Failures
retain receipts, and unexpected descendants cause failure even if killed/reaped.
The coordinator's finite scope supplies cleanup if the owner itself is killed.
Do not substitute a shared host or owner device for this VM boundary.

The fixture serializes63 cases for each exact before/after source (126 script
invocations, no retry). Old-source expected output reproduces the routing gap;
candidate expectations exercise the same settings. Per-case receipts retain
original shell exits, containment, complete generated INI/log/settings and
protected-file identities. Expected disabled/token exits are1; ordinary exits0.
A PASS result requires all cases and no descendants. Checks include:

| Cases per variant | Prepared assertion |
| --- | --- |
| 32 raw toggle/hardcore/customhost combinations | Exactly1/0 may route; unknown/empty/disabled settings retain customhost |
| 22 address/state/table/customhost cases | IPv4/wildcard/mapped IPv6 route; pure IPv6/wrong address/port/established/empty/missing/unreadable fall back |
| 6 disabled/empty-enabled/missing-token cases | Original refusal/log and prior INI preserved; no routing after refusal |
| 3 encore/new/legacy unofficial cases | Unrelated flags and compatibility unchanged |
| Every case | Entire INI oracle; source settings/profile/table/runtime and synthetic pending-award SQLite bytes/modes unchanged |

The queue is an inert synthetic tripwire, not an RAOfflineProxy schema or award
API test. The final chroot is reused serially, but each case regenerates its
synthetic inputs and compares immutable inputs before/after. No pass-by-retry.
Original failures and their first stopping case must be returned before a new
allocation. Do not re-run completed #583/Steam controls as part of this command.

## Acceptance mapping and remaining limits

| #584 criterion | Evidence now / remaining work |
| --- | --- |
| Source/upstream/raw/listener/contribution contract | Source complete: research, bindings, exact excerpts and this packet |
| Minimal routing and fallback | Candidate source prepared; static comparison only; VM behavior UNRUN |
| Full-script matrix and unchanged settings | Fixture prepared as above; all126 invocations UNRUN |
| Installed dependency/service and HostUrl interpretation | Pinned source contract established; actual image Bash/cat/procfs/unit/binary source identity and emulator interpretation remain unverified |
| Canonical flow and combined #574/#583 qualification | Coordinator-owned integration pending tested receipts; no shared documents edited |

The candidate introduces no new external CLI dependency. Existing Bash, `cat`,
procfs and profile `get_setting` still need installed-image verification.
The fixture stages actual guest Bash/cat but substitutes only its synthetic
profile/table boundary; it cannot prove installed profile behavior, systemd
startup ordering, another emulator's behavior, or the native Dolphin build.
A subsequent separately allocated source-matched emulator/proxy contract would
need synthetic local login/cache/award/reconnect responses and a proven offline
boundary. No provider or owner credential is authorized. Physical GameCube
compatibility, RVZ decoding, cache eligibility, award upload and next-game
readiness remain separate from this routing proof.

Proposed coordinator flow text, after VM proof: with offline achievements on,
known casual mode and the local listener available, Dolphin targets the local
service; otherwise it retains the configured host. Explicitly keep that listener
check separate from cached-game/offline eligibility. EN/FR menus/PO files need
no change in this script-only candidate; the two added English diagnostics go
only to the existing technical log, carry no credential/host value, and preserve
its current nonlocalized convention. Any player-facing explanation follows the
coordinator's #567/#574 flow and bilingual review.

`static-result.json` records actual syntax/AST/hash/diff check exits. No new
runtime result is claimed. Product integration/pin/build/push and GitHub/shared
record edits remain the coordinator's work.
