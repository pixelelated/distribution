# Retrospective (Phase 3) — M6.P2 T45, the council toolchain and runner (#692)

The audit's Phase 3: how the 52 members came to be what they are, and where they meet the rest of the fork. This is not the slice's mini-retro (stage G, `docs/retros/`).

## 3.1 How the toolchain arrived

- **2026-09-05, the first import** (`b3e5c92559`, #70; `4796a78983`). It came from the `pfi/pfi-collaboration` lineage and was relocated under `tools/council/` with path patches. `IMPORTED-FROM.md` § Before 2026-09-30 says that relocation *"made every refresh a patch job"*. It was 12 Facilitator versions behind when it was replaced. Eleven members still carry that lineage's *Adopted/Adapted from pfi-collaboration@5344750886…* header line (`stage-b/refs.txt`'s role reading).
- **2026-09-30, scaffold's export at its own paths** (`5f1b343d25`, D-WORKFLOW-088/089/090). Scaffold `main` at `7be6721b`, corpus 4.29.1 plus #976, 94 files byte-identical, with five adaptations applied in the same commit. The export's pristine bytes therefore never entered this repository (`02` § Reconciliation).
- **2026-10-02, #372** (`4bf31083c7`): the instructions kept on the installed five seats; agent re-pins only, no member script.
- **2026-10-04, the identity re-pin** (`a9af618398`, D-WORKFLOW-144, #409): the organization name in two URLs and the remote scope.
- **2026-10-22, the local Facilitator fork** (`033eb7ed23` #636, `0ceb2994c5` #638). It exists on the coordinator's branch and every M6 lane branch, not on `next`. Explicit `content_filter` responses stop rather than retry (exit 8), and an owner-selected audit route, `gemini-argon`, is added outside the five. Every Independent slice since has run on it.

## 3.2 What the record says the toolchain caught

- **The Facilitator's per-call identity, effort and provider checks pass on every recorded seat call this week** (10 of 10; `stage-b/seat-records.md`). The record holds no refusal, so it shows the checks running but not one of them firing. Their firing is the routing tests' job: 109 cases at the hash, 127 on the branch, all mocked.
- **The genesis binding fired, correctly,** on both 2026-09-30 runs once the fork re-pinned on 10-02 and 10-04. Nothing in the fork's record noticed until this slice ran the lint (F-02).
- **#636 is the toolchain catching itself:** a filtered response had been retried as if transient (`docs/qa-logs/2026-10-22-review-filter-636/README.md`).

## 3.3 What was hard

- **A provenance table without the export's bytes.** The SUMS gives each file's hash, but none of the 9 differing members' export bytes exist in any commit here. Each of the 9 is accounted for by the adaptation list, by reading, and the list's own attribution drifts once (F-04).
- **The lint's two modes.** The same run passes as *historical inventory* under default discovery and fails under explicit naming. Reading that took the code's own comment (`lint-council-run.ts:47-49`), and this slice first got it wrong on #692 (corrected at 03:05 UTC).

## 3.5 The seams

| Seam | What crosses it | What the read found |
| --- | --- | --- |
| the export × the fork's adaptations | five items in `IMPORTED-FROM.md`, applied at import | all 9 differing members are accounted for; item 3's file attribution drifts (F-04); the export's bytes are not recoverable here, so a future refresh cannot diff *our* adaptations against *their* bytes from this repository alone (F-14) |
| the adaptations × the pins | `repin_reason` on each adapted pinned file (D-WORKFLOW-089) | 4 fork reasons at the hash, each true of its diff; 2 more fork reasons on the branch (#636, #638), true of theirs. 5 differing members are unpinned by design: three tests, the manifest, and the pins file itself |
| the pins × the recorded runs | a run's `genesis.json` binds `verifier_pins_hash` | any later re-pin leaves every completed current-contract run unlintable on the current tree; the fork re-pinned twice after the 09-30 runs (F-02) |
| the Facilitator version × `HISTORICAL_CONTRACTS` | a run is historical only by a listed contract | the branch's `1.14.1-pixelelated.2` left `1.14.0` neither installed nor historical (F-02) |
| the export × the push guard's personal paths | `fork-workflow.md`'s list and `PERSONAL_PATTERNS` in `.githooks/pre-push` enumerate the council paths (18 pattern hits by `grep`) | the enumeration is a second copy of the export's path set; a refresh that adds a path must add it there too (Q1) |
| the export × `.gitignore` | the export's ignore lines merged at 2026-09-30 | the seal-key line arrived after two keys were already committed, and it untracked nothing (F-03, #1043) |
| the toolchain × the four slices' runs | `tools/council/run invoke` in each slice's Phase 4.6 | every record names `1.14.1-pixelelated.2` (the branch's), the served model and provider, and PASS; none names the npm versions that ran (F-06) |
| the toolchain × the rules | `adversarial-council.md` (the floor), `council-substrate-integrity.md` (Facilitator only) | the floor holds on both trees. The integrity rule's rules 4 and 5 name two council-research lints this tree lacks; its adoption note (`:42-46`) says they are carried by the source estate only and gives a manual fallback (F-05). It names exit 3 alone as the halt (F-15) |

## 3.6 What the time-to-play numbers have to do with it

Nothing. No member reaches an image (`reach: n/a` for all 52), and nothing here runs on a device or a guest.
