# T42 punch list

Reviewed-at: `9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1`. Local reader Codex / GPT-6-Astra / xhigh, OpenAI. One finding: 0 Critical, 0 High, 1 Medium. Stage D proposes a route; the coordinator owns stream disposition. No product edit is authorized.

## PL-01 — PPSSPP patch creates inert nested patch data

- **Source Finding:** F-T42-01 (primary Local reader).
- **Question / category / severity:** Q3 / Bug / Medium.
- **Owner:** standalone-emulator/PPSSPP implementation owner (#677 context); coordinator #689 assigns the future fix stream. Reactive bug: #1410; audit child: #1411. Both readbacks are in stage-d/.
- **Trace:** seed `projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/patches/007-disable-home-pause.patch:11–16` creates `package/batocera/emulators/ppsspp/007-disable-home-pause.patch`; lines 17–29 contain an SDLJoystick.cpp diff as added text. `scripts/unpack:191–196` applies the outer file once. The PPSSPP recipe's `post_unpack` only rewrites compiler flag files; it never applies that nested patch. The intended GUIDE-button source hunk is therefore not performed by this patch.
- **Proof:** `stage-b/nested-patch/receipt.json`, normal GNU patch 2.8 rc 0 in a constructed projection, sentinel SDLJoystick.cpp unchanged and nested file created. This is a format/mechanism proof, not application at PPSSPP pin `afbc66a318b86432642b532c575241f3716642ef` or a runtime report. Fixed upstream `651150fc88` contains a direct SDL diff returning NKCODE_GUIDE; seed's nested payload returns NKCODE_UNKNOWN. Preserve that distinction before choosing a replacement.
- **Already written:** builds carrying this outer patch can contain the inert nested file in their build source while retaining the preexisting SDL mapping. This patch writes no player settings or cloud data. A future correction must rebuild the affected binary and preserve `/storage`; existing installed behavior is not repaired by editing this audit.
- **Can this be done on the VM?** Source-target and normal-application regression can be established from source fixtures without a guest. Any later observable input-flow acceptance can run in GENERIC_X64 with injected controller input; no physical fact is required and no runtime is allocated here.
- **Enforcement ladder:** currently written intent (patch subject) and routed selection; the intended source result was not audited. Next mechanism: the owning fix should add a fixture that first fails for the nested wrapper, then asserts the intended SDL target change and absence of the nested file. A product-patch target-shape guard can catch siblings, with explicit exceptions for intentional patch payloads and historical audit product-diff records. This audit supplies a demonstrated failure and scoped proposal, not a global-tool edit.
- **Next mechanism / route proposed:** one source-changing fix brief owned by the PPSSPP lane after coordinator disposition. Decide NKCODE_GUIDE versus NKCODE_UNKNOWN from intended product behavior and pinned source; do not mechanically flatten/import a different mapping. Then qualify exact selected stack and guest behavior under a separate grant. No fix or runtime occurs in T42 A–D.

### Observable acceptance for the reactive bug

- [ ] A source regression fails on the reviewed outer wrapper, then passes on the chosen direct SDL diff: actual normal rc, before/after target hashes and absence of the nested patch file are retained at the selected pin/stack.
- [ ] The recorded intended GUIDE mapping is exercised in GENERIC_X64 with an agent-verifiable input trace/frame or equivalent deterministic event assertion; the installed binary identity is bound to the correction.
- [ ] The fix's Already written record and upgrade/clean-install evidence show existing `/storage` settings are preserved; no cloud action is required by the correction.

## Previously tracked scope and evidence limits

The 22 inherited unresolved questions and 173 native application open items are specific limitations of this comparison, with recipe/current-pin owner actions in 02 and tables.json. They are not 195 new bugs or duplicate punch items. T8 #655, T22 #669 and T27 #674 keep their recipe questions; #1104 keeps systemd design. Existing #1048/#346, #1056/#1071/#1072 and #559/#563 remain their owners. Draft contributions stay local to this packet for #585. No source removal, policy change or release waiver is proposed.

## Phase 7 resolution gate

| Item | Outcome | Evidence / next owner |
| --- | --- | --- |
| PL-01 | Open | Stage D packet for #689 coordinator stream disposition; reactive bug #1410 remains open. Audit child #1411. No source remediation or accepted deferral is claimed. |

```yaml
punch_index:
- id: PL-01
  title: PPSSPP outer patch creates a nested patch instead of changing SDL
  severity: Medium
  category: Bug
  question: Q3
  source_finding: F-T42-01
  ladder: written-and-routed to audited source-target regression
  next_mechanism: PPSSPP owning fix brief with exact-pin source regression and separately authorized VM evidence
  owner: 'coordinator #689 routes to standalone-emulator implementation owner'
  outcome: open
```
