### Offline achievements → Dolphin routing (#584)

The existing offline-achievements control and game-launch navigation are unchanged.
The launcher routes a Dolphin launch to127.0.0.1:8080 only when the saved toggle
is exactly1, raw hardcore is exactly0 and an IPv4-capable listener is present.
Otherwise it keeps the configured custom host. The #594 correction atomically
publishes an inactive, credential-free Dolphin session when achievements are
disabled or the account has no token, then retains the existing early exit status.
Global account settings are unchanged. A failed publication refuses the game
launch so an older active session cannot be reused.
[Configuration proof](qa-logs/2026-10-14-rvz-proxy-components/README.md) contains126
before/after full-script cases. Installed proxy hashing, service lifecycle and
startup reconnect now have their own completed evidence; those do not prove
that the default Dolphin process uses the generated HostUrl.

The [NoGUI lifecycle repair](qa-logs/2026-10-15-dolphin-nogui-lifecycle/README.md)
adds the missing AchievementManager initialization/shutdown. The
[compiled candidate and actual-process proof](qa-logs/2026-10-15-dolphin-startup-result/README.md)
reproduces the installed baseline defect and verifies enabled, disabled and early
boot-failure lifecycle branches. One synthetic failed-login request reaches the
configured loopback endpoint. No ES copy/layout changes; the exercised nonvisual
flow is NoGUI startup/configuration and shutdown. Existing settings and game-launch
frames remain the presentation baseline. The subsequent actual installed enabled,
disabled and boot-error startup controls passed; ordinary Wii gameplay/cold-save
proof retains its earlier d4af source identity. The final f863
[native-state flow](audits/2026_10_14-milestone-m7-next-candidate/native-state02-readback.md)
and [reviewed frame index](audits/2026_10_14-milestone-m7-next-candidate/supplements/native-state02-result/frame-index.json)
verify manual restoration and normal frontend return. Listener presence alone
does not establish proxy identity/readiness, and synthetic login is not successful
authentication or an award. Physical-device behavior remains separately scoped.

