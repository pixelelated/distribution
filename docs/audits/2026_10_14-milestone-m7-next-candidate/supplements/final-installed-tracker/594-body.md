Fable refutation R-01, independently confirmed as #590 G-02 Medium: cheevos_dolphin.sh exits before writing its generated INI when achievements are disabled or the API token is absent. Both native launchers continue. A previously enabled INI can therefore retain active credentials and hardcore state after the player disables achievements or logs out. The new NoGUI lifecycle makes this pre-existing Qt behavior active on the default frontend too.

User direction: “Let's fix any gaps we discover before we generate a new build.”

Current upstream ROCKNIX next has the same early-exit behavior; scoped open-PR search returned no matching fix. Queue the focused contribution under #585 after initial build qualification; no upstream submission yet.

Can this be done on the VM? Yes: exact full configuration helper with synthetic settings/credentials, seeded prior enabled INI, and launcher refusal controls in a disposable no-network guest. No real account, provider, or device required.

- [x] Disabling achievements atomically publishes an explicit disabled INI with credentials, custom host and hardcore state cleared; original settings/queue/saves remain unchanged.
- [x] Enabled-but-logged-out follows the same clear-session path; enabled signed-in routing/flags remain correct.
- [x] Failed publication cannot launch Dolphin with the stale enabled INI; original error exits and player recovery presentation are verified.
- [x] Independent source review, focused VM transitions, canonical flow/frame evidence and affected installed qualification are complete before the next candidate.

Keep ordinary game-save and unrelated account/history evidence unchanged. The previous disabled startup case used an authored private INI and does not prove this launcher transition.

October15 source-control result: committed d9054efc463387df3f0211481c5ae8c793dfadc8 passes15/15 exact full-helper/launcher-block controls in the installed d4af guest; disabled/logout clearing, enabled routing, atomic publication refusal, symlink target protection and unchanged selected data are verified. Original first fixture failure remains recorded; corrected controls02 and cleanup/export are0, admission consumed. Compact originals at docs/qa-logs/2026-10-15-audit-followup-controls/ (published f13f9d98). Actual full Wii/API/runemu/ES publication refusal now passes in EN/FR at640x480 and1280x800, with exact helper log/mv oracle, original250, complete reviewed messages and return to the originating Wii carousel. Original configuration identities restored; large-panel lifecycle/export0. The640 combined suite retains its unrelated timing failure. Canonical frames and originals are published in docs/qa-logs/2026-10-15-audit-ui-results/ at030518cd82. Final assembled-image installed/retained qualification remains open.

## Final scoped verification — 2026-10-15

The actual final installed helper and exact launcher achievement block passed disabled GameCube, missing-token Wii, enabled proxy GameCube and enabled hardcore Wii on clean and retained-upgrade guests. Stale session fields cleared where required, unrelated fixture state preserved; all original wrapper outcomes0. This complements the separately published EN/FR actual refusal flow; the chroot cases use a synthetic engine marker and do not claim native login/awards.

Published [clean result and reviewed frames](https://github.com/pixelelated/distribution/blob/0ca9443280/docs/qa-logs/2026-10-15-final-engineering-result/clean/README.md) and [retained upgrade result and reviewed frames](https://github.com/pixelelated/distribution/blob/0ca9443280/docs/qa-logs/2026-10-15-final-engineering-result/retained/README.md) include complete compact originals, exact source/installed hashes, and consumed receipts. Independent review found no blocker; canonical menu/flow references were updated in the same checkpoint. Historical build reporting failure remains explicit. Native-state proof and overall audit/RC closure remain under #596/#590.
