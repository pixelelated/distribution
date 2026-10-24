# Running Log — M6.P2 T8, the image's own packages (projects/ROCKNIX)

**Issue:** #655 (`M6.P2 E848/T8`), slice `image-packages` (`k: 8`); epic #848; renovation #339; milestone M6
**Brief:** `docs/reviews/briefs/image-packages.md` version 2 (`dede8effec`); its § 7 is the contract, identical to #655's eighteen criteria
**Executor:** Claude Code, `anthropic/claude-opus-5-5` (Opus 5.5) at high effort; the T5 session `c649553c-8086-4db7-ad9c-248c7e41ff95`, herdr agent `m6-t5-build-engine`, pane `wN:p7` (the dispatch, issuecomment-6384032445)
**Skill:** code-auditor at epic tier, the renovation face (plan § 6b); depth **Independent** (D-WORKFLOW-184): one GPT-6 Astra seat at `max` through the Facilitator, a probe then one refutation over one bounded packet; the dispatch authorizes the two calls; a failed seat is a hold
**Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-image-packages-655`, branch `feature/m6-image-packages-655`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; **`reviewed-at` = `caf1de3727`** (the branch `HEAD` at stage A; the commit carrying this log changes no slice path); `upstream/next` `e0f9deb899` at the fetch (12:10)
**The bench:** the recipes, scripts, units and configs at the hash (`.qa-scratch/t8/at-hash/`), `upstream/next`, the hosts `tools/fork-package-freshness` reads, the GitHub API's `compare`, one HEAD probe per effective URL, ROCKNIX's mirror, the shared source cache's stamps, and the five M7 roots' `build/` listings and GENERIC_X64 install tree, read only. A guest only for a stage-E behaviour claim
**Can this be done on the VM?** **Yes, for every behaviour claim** (a stream's unit, script or install step, on the GENERIC_X64 guest); **no guest for the reading or the tables** (brief § 5)
**Prose:** written through Python or a quoted heredoc only (plan § 6b E; T7's incident)

Every time below is a `date -u` reading taken in the command that wrote it.

---

### [Stage A] 12:10 to 12:12 — Scope

- **Read**, in the order the dispatch gave: the dispatch comment on #655 (12:09, with T6's 08:57 lead before it); the lane pointer; `docs/reviews/plan-for-the-plan.md` (read whole for T7; its one change since, the stage-E row's three new bullets, read word by word with `git diff --word-diff e7978a1ca5 HEAD`); the brief whole (version 2).
- **Rules:** `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists exactly the dispatch's eight paths (127 insertions, 11 deletions).
- **The first commands** (12:10:46 to 12:10:58):
  - `git fetch`: rc 0; `upstream/next` is `e0f9deb899`;
  - the branch is stacked on `2174265e9c`; `inventory.json` is present;
  - `df -i`: `/workspace` 20%, `/tmp` 41%;
  - the at-hash export of `projects/ROCKNIX/packages`: 2,614 files under `.qa-scratch/t8/at-hash` (gitignored), rc 0;
  - P1's tools are present;
  - `rules-check` rc 0; `register-check` rc 0 (664 IDs); `ceremony-check` rc 1 on `OVERDUE: 2026-W42 summary missing` (M7's week, not this lane's);
  - the push set the upstream;
  - the host file's tail read (the coordinator's 10:36 correction on `portaudio`; census qemu 0);
  - the API budget: 4,007/5,000;
  - `~/.config/council/env` is present (not read).
- **The scope, re-derived** with brief § 2's filter on `inventory.json` (`00ca350666`). **All equal to the brief's: no delta:**
  - **485 paths, 20,644 lines**: upstream-carried 450, fork-own 35; reach `shipped` 478, `test` 6, `n/a` 1;
  - **260 recipes** (27 fork-own) in the brief's 22 groups; 60 with patches;
  - **14 paths contain spaces, and none of them is a recipe.**

  The full listing is `.qa-scratch/t8/scope-out.txt`.
- **Branch against the hash, over the 485** (`xargs -0`): empty.
- **Provenance by git:**
  - against the base: 11 A, 24 M (the fork's 35);
  - against `upstream/next`: 31 A, 87 M;
  - the absent recipes: **11 orphans, 7 fork-added**;
  - 40 upstream commits on these paths since the base; 66 recipes changed upstream;
  - `fork-package-freshness --list` under `projects/`: 34;
  - the conflict set (fork-changed ∩ upstream-changed since the base): **11**, as the brief has it.
- **A T7 erratum found here:**
  - **What T7 wrote:** `docs/audits/2026_10_24-epic-m6-generic-packages-reached/` (`05`'s PL-12, `tools/punch-items.py`) and its retro called six of the 47 sourcing overrides *orphans ROCKNIX deleted*.
  - **The fact:** three of the six (`harfbuzz-icu`, `gst-plugins-bad`, `gnutls`) are **fork-added**, absent at the base too; only `libfreeaptx`, `opus` and `libfmt` are orphans. T7's check read `upstream/next` alone, not the base.
  - **Where it is recorded:** `01` § T7 erratum here; reported on #655, since T7 is accepted and its folder is not this lane's to edit.

### [Stage B] 12:13 to 12:36 — Phases 1 to 4: the movers, the sweep, the record, the conflicts

- **Phase 1 reads:**
  - the rules the brief § 3 names, `packaging-and-patches.md` from this worktree (the rest loaded this session at `next`'s bytes, by the stage-A diff);
  - `tools/fork-package-freshness` (read whole for T7, unchanged since: `git diff --quiet 4ea87f17dd HEAD -- tools/fork-package-freshness`), `tools/viewplan`, `tools/pkgcheck`;
  - `scripts/update_packages` (`PKG_PATH` at `:16`; its checksum lines `:52`, `:61`, `:63`), never run;
  - T7's audit (accepted at `db6597356b`), whose loops this stage re-uses; T6's widened `pkgcheck` (`git show 44f64842b6`);
  - T30's `second-opinions/` on `origin/feature/m6-emulators-standalone-677` (the probe prompt, the brief's head, the probe's provenance, `review-plan.json`).
- **§ 5's checks**, each in `02` § Mechanical checks with its exit status:
  - (a): 12:13:04;
  - the expansion: 12:13:05 to 12:13:50;
  - `make update`'s set: 12:15:06;
  - the freshness tool: 12:15:17 to 12:15:29, rc 2;
  - the hash pins: 12:16:02 to 12:17:10;
  - the HEAD probe: 12:17:32 to 12:20:13;
  - both `pkgcheck` runs: 12:17:40 to 12:18:33;
  - `bash -n`: 12:19:09;
  - the units: 12:19:33;
  - the redirect fetch: 12:20:44 to 12:28:36;
  - the mirror for the three: 12:20:56 to 12:22:07;
  - the base merge simulated: 12:23:57;
  - `git ls-remote` ×10: 12:25:28 to 12:26:24;
  - `samba` again: 12:28:05.
- **API budget:** 4,007 at 12:10; 3,907 before the freshness tool; 3,843 to 3,703 over the hash pins.
- **Posts on #655:**
  - 12:12 (stage A);
  - 12:14 (`simple-http-server`). The coordinator filed it as **#890**, packeted (`fix/m6-890-shs-sha256`), with D-WORKFLOW-197.
  - The T7 erratum was answered by a note on #654.
- **Deltas from the brief** (`03` § 3.3):
  - the record block's regex prints `entware` for `arm`;
  - 50 sourcing recipes are 43 plus 7 `get_pkg_directory` users;
  - the overrides that reset a pin are 6, not 8;
  - `sway`'s gap is RK3588's only;
  - the third empty checksum is #890.
- **Written:**
  - `02`: 485 coverage rows, § Mechanical checks, § The fetch sweep, § The conflict set, § The #644 findings, P1 to P15;
  - `03`;
  - `04` (§ Second opinion pending), with the orphan table and the conflict list;
  - `q4-table.md`, `q4-pins.json` and `tools/t8-tables.py`, one generator asserting 485 and 260.
- **The proof counts:** P1 to P15 in `02`; their proof lines follow.

PROOF: 12:11 P1 the slice is the brief's 485 paths and 260 recipes; 14 paths with spaces -- `01` § Scope
PROOF: 12:12 P2 35 fork changes; 11 orphans, 7 fork-added; 66 recipes changed upstream -- `prov-*.txt`
PROOF: 12:13 P3 (a): 367 identical, 87 differs, 21 orphan, 10 fork-added over the 485 -- `q4a.txt`
PROOF: 12:24 P4 9 of the 11 conflict at a simulated base merge; `gamescope`'s wraps agree at both commits -- `base-merge.txt`
PROOF: 12:13 P5 three archive versions without a checksum on the shipped plans -- `effective.txt`
PROOF: 12:15 P6 `make update`'s set holds 13 of this slice's recipes -- `update-set-*.txt`
PROOF: 12:17 P7 (c): the tool's 34, `cairo` BEHIND, 44 GitHub hash pins compared, 6 short -- `q4c.txt`, `q4c-hash.txt`
PROOF: 12:20 P8 the HEAD histogram; the controls 404 and 200 -- `probe/head.txt`, `probe/controls.txt`
PROOF: 12:28 P9 140 of 143 redirected archives match; the mirror covers `libaio`, `rocknix-abl`, `samba` -- `probe/fetch.txt`
PROOF: 12:18 P10 `pkgcheck` 258 and 257 PASS; each FAIL read -- `pkgcheck-*.txt`
PROOF: 12:22 P11 `bash -n` 48 ok; the four shapes absent, each grep proved on a fixture -- `bashn.txt`, `grep-fixture.sh`
PROOF: 12:22 P12 sourcing `virtual/image` wrote `image/system/opt` in three build directories here (#852) -- the symlinks' mtimes
PROOF: 12:20 P13 the units: no directive warning; `xorg-configure`'s script in no image -- `units-verify.txt`, `units-exec.txt`
PROOF: 12:21 P14 every plan's reached recipes stamped; the unbuilt the 12 virtual and `qcom-abl` -- `stamps-*.txt`
PROOF: 12:30 P15 the orphans' pins after the base merge; `glslang` 16.6.0 to 16.5.0 -- `git show upstream/next:<generic>`

### [Stage C] 12:36 to 12:40:00 — Phase 4.6: the Facilitator, the probe, the packet, the refutation started

- **Setup (12:36:46 to 12:37:17):** `npm install --prefix tools/council` rc 0. `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` `tools/council/run test`: 39/39, 127/127, 19/19, 0 fail. `run` sources `~/.config/council/env` itself, and the env was not read.
- **The probe** (12:37:35 to 12:37:43): `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-probe-prompt.md --output second-opinions/gpt-probe.md`, rc 0.
  - attempt 1, http 200, `model_field` `openai/gpt-6-astra` (`model_identity_source: provider_response`), served by **OpenAI**, effort `max`, 252 reasoning tokens, `finish=stop`;
  - `final.verification`: **PASS** (semantic; observed `openai/gpt-6-astra`);
  - the seat's own line reads `READY unknown`; the provider's field is the authority.
- **The packet** (`tools/t8-packet.py`): `second-opinions/gpt-brief.md`, **398,152 bytes, sha256 `7e93a08906a8168fe86ecf6b24c9e2d6381d1f316c28ce1af63cd59e41d6dca5`**, 69 parts (`second-opinions/packet-manifest.json` names each with its sha256).
  - **What it carries:** `02` less its 485 generated rows, `03`, `04` less its 260 generated rows, `q4-table.md`, the 35 fork-own files whole, the 64 upstream-carried paths that differ from `upstream/next` as their diff, 14 line-numbered excerpts, 15 mechanical outputs, and the ask.
  - **Checks before sending:** redirect query strings cut; the hook's secret patterns 0 hits; `forbidden-terms-check --stdin` rc 0; under the 440,000-byte cap.
- **The refutation** started at 12:40:00: `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md`, in the background.
  - **Watching it:** the harness task delivers its end.
  - **Its silent mode:** a seat that hangs is ended only by the Facilitator's own per-attempt and total timeouts, and by the `timeout 5400` around it.

### [Stage C] 12:55 to 13:01 — the second opinion graded, the punch list drafted

- **The refutation ended at 12:55:20, rc 0.** One attempt, http 200, `model_field` `openai/gpt-6-astra` (`provider_response`), served by OpenAI, effort `max`, 40,720 reasoning tokens, 46,644 completion, `finish=stop`, 920 s. `final.verification`: PASS. The provenance's `user_prompt_sha256` equals the packet's `7e93a089...`. The output is `second-opinions/gpt-audit.md`, 26,313 bytes.
- **Graded in `04` § Second opinion, every item read at its site:**
  - **27 new items:**
    - G-01 and G-15 confirmed Medium → F-14 and F-13, both `bug`s;
    - G-20 confirmed → F-15, a lead for #844;
    - G-22 confirmed → F-16;
    - G-27 confirmed → F-11 widened to the `spirv-headers` triple;
    - G-16 folded into F-02's stream;
    - the eight small shapes → F-17;
    - G-07 refuted (`050-sway.conf:4-5` exports the session variables);
    - G-08, G-18, G-19 and G-25 withdrawn with reasons;
    - G-26 applied (17 table rows now say *first `PKG_VERSION` literal*).
  - **Its refutations of F-01 to F-12:** accepted, narrowing F-01, F-06, F-10, F-11 and F-12, and correcting eight conflict dispositions (`gcc`, `gstreamer`, `gamelist.xml`, `gst-plugins-base`, `spirv-tools`, `rocknix-abl`, `cairo`, `111-sway-init`).
- **Two of my statements corrected in the grading:**
  - `make update` would move four hash pins, not "three at HEAD" (five are at HEAD);
  - `cairo`'s listing read was not stamped.
- **D-WORKFLOW-198** (the coordinator's, `152c4ee3c3`) settles F-11: keep the fork's `glslang` override at the base merge. The coordinator's 12:42 answer: the conflict list is one Renovation item, F-11 its own Medium, and `libaio` and `rocknix-abl` two Low bugs.
- **Written:** `05` from `tools/punch-items.py` (seventeen items); `second-opinions/review-plan.json` complete.
