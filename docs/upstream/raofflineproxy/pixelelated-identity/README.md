# pixelelated account discovery — #409/#408/#168

Prepared against upstream5866cd9ba784c13771a99c52dd6b6f2acc546842; not
submitted. The new distribution name retains the ROCKNIX /storage settings
layout. Recognize its exact OS_NAME record so automatic account discovery
continues to use system.cfg after upgrading. No paths or state formats change.
The patch contains only config.py and focused upstream-format unittests.
Configured paths still take precedence; other platforms and partial/commented
name records do not match. Qualification receipts: `docs/qa-logs/2026-10-04-pixelelated-source/proxy-identity.log`.

Rechecked on 2026-10-05 against the distribution's upstream pin
`7252fc781392d45b22f50d1a92f9febc4d1fa172`: all 15 package patches apply with
zero fuzz and all 16 `linux.tests.test_linux_rocknix` tests pass. Direct
fixture checks recognize ROCKNIX and pixelelated, find their settings file,
and reject the unshipped RASTERATOPS identity. See the 05:00 UTC entry in
`docs/work-logs/2026_10-work_logs/2026_10_05-work_log.md`. These are isolated
host checks; frozen replacement08 does not include this cleanup.

Suggested title: `linux: recognize pixelelated account settings`

Suggested description: pixelelated uses ROCKNIX's settings layout but a new
OS_NAME, so the automatic account lookup misses system.cfg after the rename.
Recognize only the complete ROCKNIX and pixelelated OS_NAME records. Rasteratops
never shipped as an OS identity and needs no compatibility branch. Tests cover
branded account lookup,
configured-path precedence, and rejection of commented/partial names.
