# Nova state provenance: October 13 continuation

Refs #565. Read-only retained records; no device/provider operations, credential
values, or secret-derived hashes. These are historical bounds, not proof that a
fresh image is clean. Coordinator independently confirmed the field-presence
counts in `nova-field-presence.json` without emitting their contents.

| Boundary | Evidence | Supported conclusion and limit |
| --- | --- | --- |
| September 29 first fork install | September29 work log lines275–285; private `/workspace/artifacts/rocknix-device-actions.log` lines578–593 | In-place update from stock20260901/1ebff24f36 to5b5005879e preserved storage. Recorded staging/verify/reboot/read chain contains no config or gamelist copy; this cannot exclude UI or unrecorded actions. |
| September29 incomplete account | #329 comment5899228308; worklog285; exact5b5005879e raofflineproxy-ctl `have_account` and scan guard | Device-clock16:50:24 scan refused because on-disk settings lacked username plus token OR password. This does not mean all fields were empty. #329 documents unsaved UI state; credentials could have been entered but not yet saved. Contemporaneous quoted journal only; separate raw journal not recovered. |
| September30 cloud operation stamps | Private `/workspace/tmp/pixelelated-nova-cloud-20261012/log-readback.json`, events131:154, original cloud_sync.log154–220 and retained stamps | Empty restore completed23:43:06UTC, then backup0B completed23:43:12UTC, code0. Log216 says settings backup skipped, saves only. This explains activity dates without games/settings copied by those operations. Initiator unknown. |
| October9 account upper bound | Private `/tmp/pixelelated-device-deploy-20261009/nova-config-semantics-private.json` original/live/fallback; collector check-config-semantics.py5–6 | Username/password/token fields nonempty in pre-update archive as well as live/fallback. Archive created15:31:37–15:31:48UTC; receipt16:00:17UTC verifies preservation. Field presence does not prove provider authentication or initial author. |
| Recent-list dates | Committed nova-feedback packet; #565 comment6138176065 | Playcounts5/1 and lastplayed20260908T031024 /20260906T014729 predate first fork install. These are imported/preserved metadata values, not evidence of local gameplay on those dates. Arrival method/date remain unknown. |

The defensible account interval is incomplete effective on-disk combination on
September29, complete fields before October9 update. No reviewed record identifies
the first entry or an intervening config copy. D-INFRA-006/007 allowed local build
credentials; September5 worklog257 says then-current options were commented
placeholders. Neither proves later seeding or delivery to Nova. The exact accepted
SYSTEM selected-file checks found no populated player fields, but are not a
whole-image contamination gate.

Next #565 qualification remains executable final-payload + fresh-boot checks for
player accounts, remote connection/activity stamps, play history and QA residue;
retained upgrades must preserve legitimate state. Synthetic positive and negative
cases must fail closed for required unreadable/malformed inputs, with value-free
reports. The parallel pix-nova implementation is separate from this historical
review and must not turn uncertain history into a passed clean-install claim.
