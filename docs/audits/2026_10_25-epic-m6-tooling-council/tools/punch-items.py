#!/usr/bin/env python3
"""05-punch-list.md from one list (#692): the items, the punch_index and the Phase 7 table.

    python3 -I punch-items.py > ../05-punch-list.md
"""
HOST = "Yes, on the host: the toolchain's own checks and a constructed input in the worktree or the clone at the hash; nothing needs a guest, a device or a provider (brief § 5)"
AWN = "nothing inherited on devices: these are host-side council tools; what they leave is run directories under `research/`, audit `second-opinions/` and seat provenance records, which the item reads, never a device or a person's cloud"
EXPORT = "the export's owner (scaffold, through the maintainer's agent that delivers the bundles) and the coordinator"

I = [
 dict(f="F-01", t="The lane's tree carries a local Facilitator fork (`council-facilitator@1.14.1-pixelelated.2`, #636/#638) that no register row records, while D-WORKFLOW-088 describes the toolchain as scaffold's, refreshed only by copying the next export", sev="Medium", cat="Renovation", q="Q7",
  area="`scripts/council-invoke.ts`, `verifier-pins.json`, the register", what="A decision row for the local fork: what changed (a terminal content filter, exit 8; the `gemini-argon` audit route), why, and the condition under which it is reconciled with scaffold's next export. The coordinator carries the D-WORKFLOW-088 question to #346; this lane writes no row.",
  where="`council-invoke.ts:855` on the branch (`:844` at the hash); `IMPORTED-FROM.md` § Local retry correction / § Local audit route", ev="`grep -c -E '#636|#638|1\\.14\\.1-pixelelated' docs/decision-register.md` prints 0; `02` § The branch's delta", vm=HOST, aw=AWN,
  acc="a decided register row names `1.14.1-pixelelated.2`, #636 and #638 and the reconciliation condition; `tools/register-check` passes with it."),
 dict(f="F-02", t="A completed run under the then-current contract becomes unlintable on the current tree after any re-pin, and the local version bump left `council-facilitator@1.14.0` runs neither installed nor historical", sev="Low", cat="Renovation", q="Q3",
  area="`scripts/lib/council-verification.ts` (`HISTORICAL_CONTRACTS`, `assertGenesis`), `scripts/lib/council-roster.ts` (`assertRunRoster`)", what=f"For {EXPORT}: a way to retire a contract to the historical path when the Facilitator moves, or the written expectation that a completed run is linted at the commit that sealed it.",
  where="`council-verification.ts:343-356`, `:370-395`; `council-roster.ts:312-322`", ev="`02` § The runs: the 09-30 runs `genesis_binding_mismatch` at the hash (pins `4088e315…` against `4818febe…`), `council_roster_invalid` on the branch, and rc 0 at their own commit `4fa6e04948`", vm=HOST, aw=AWN,
  acc="either the next export lists the retired contract (the 09-30 runs read as historical inventory on the current tree, quoted), or the procedure says where a completed run is linted and the coordinator's record carries it."),
 dict(f="F-03", t="Two council-run HMAC seal keys are committed and on `next` in a public repository (outside the 52)", sev="Medium", cat="Security", q="Q2",
  area="`research/council-runs/2026-09-0{5,11}-*/verification/seal-key.local` (not members); `.githooks/` (the guard gap)", what="The coordinator's #1043: the files removed on its branch at `0fa5a20c5f`; the history question put to the maintainer; the guard gap for a bare-hex key file.",
  where="`df316365e6`, `bfbbc31772`; `.gitignore:81` (arrived 2026-09-30)", ev="`git ls-files`, `git ls-tree -r next` (the files unread)", vm=HOST, aw="what was written: two keys in history and on `next` since 2026-09-05/11; the coordinator's #1043 decides removal and history",
  acc="#1043's own criteria."),
 dict(f="F-04", t="`IMPORTED-FROM.md` item 3 says ten fixture key literals in *the two test files* are built at run time; the bytes show 7, in the routing test and the toolchain test, and none in the seat-efforts test (whose difference is item 2's)", sev="Low", cat="Documentation", q="Q7",
  area="`.claude/skills/council/IMPORTED-FROM.md` (not a member)", what="The item names the files the bytes show, or the next refresh records the count against the export's bytes; the lane edits no skill file.",
  where="`IMPORTED-FROM.md` item 3; `__tests__/council-invoke-routing.node-test.ts:98`, `:241`, `:284` and three more; `council-toolchain.node-test.mjs:81`", ev="`02` § Reconciliation (the marker counts)", vm=HOST, aw=AWN,
  acc="item 3 names the two files and a count that a `grep` of the `[\"synthetic\", ...].join` pattern at the current tree reproduces, or says which literals another pattern builds."),
 dict(f="F-05", t="`council-substrate-integrity.md` rules 4 and 5 read as unconditional and name two council-research lints (`scripts/lint-council-research-provenance.ts`, `-digests.ts`) that exist in no commit here; the fallback that replaces them is only in the rule's adoption note", sev="Low", cat="Documentation", q="Q7",
  area="`.claude/rules/council-substrate-integrity.md`, `.claude/skills/council-research/SKILL.md` (not members)", what=f"For the coordinator and {EXPORT}: rules 4 and 5 carry the adoption note's manual check beside them, or the two lints come with the next export. The lane edits no rule.",
  where="`council-substrate-integrity.md:42-46` (the adoption note), `:72-82` (rule 4), `:85-90` (rule 5); `council-research/SKILL.md` (3 mentions)", ev="`git cat-file -e` at the hash and the branch fail; `git log --all -- <path>` is empty", vm=HOST, aw=AWN,
  acc="a session reading rule 4 or 5 alone is told what to run on this tree: either the scripts exist (`test -f`, quoted) or the rule names the manual check beside the mandate."),
 dict(f="F-06", t="No lockfile (by policy, `.gitignore:67`), and no seat provenance record names the `tsx` or Bedrock SDK version that ran", sev="Low", cat="Renovation", q="Q4",
  area="`tools/council/package.json`, `scripts/council-invoke.ts` (the provenance record)", what=f"For {EXPORT}: either a recorded resolution (a lockfile, or the versions written into each record), or the policy's reason written beside the `.gitignore` line.",
  where="`.gitignore:66-67`; `tools/council/package.json`", ev="`npm ls`: `tsx@4.23.15`, `@aws-sdk/client-bedrock-runtime@3.1156.0` on both trees; `grep -c -i 'tsx|npm|bedrock'` of a record prints 0", vm=HOST, aw=AWN,
  acc="a seat call's provenance, or a committed lockfile, names the resolved toolchain versions; or the ignore line carries its reason."),
 dict(f="F-07", t="The seat-efforts snapshot is 27 days old (`refreshed_at` 2026-09-28) and the branch added the Argon entry from a 2026-10-22 catalogue without moving the stamp; a fresh reading needs `OPENROUTER_API_KEY`", sev="Low", cat="Renovation", q="Q4",
  area="`council-seat-efforts.json`, `scripts/lint-council-seat-efforts.ts`", what="The next keyed refresh (`tools/council/run efforts --refresh`, the maintainer's or a session with the key) rewrites the snapshot and its stamp; an entry added by hand carries its own date.",
  where="`council-seat-efforts.json` header; the `google/gemini-4-argon` entry", ev="the file on both trees; `0ceb2994c5`'s README (catalogue read October 22)", vm=HOST + "; the refresh itself needs the key and is not this lane's", aw=AWN,
  acc="`refreshed_at` is no older than the newest entry's source date, quoted from the file."),
 dict(f="F-08", t="Dead ends the export carries: the Mistral counter chain and its requirements, the Bedrock dependency (a Mistral-only backup route), `forge-write-status.mjs`, `owner-queue-lint.mjs`, and the four `council-stage-*` CLIs with no wrapper route", sev="Low", cat="Renovation", q="Q6",
  area="`scripts/lib/council-mistral-*`, `scripts/council-count-mistral.mjs`, `scripts/setup-council-mistral-tokenizer.mjs`, `scripts/forge-write-status.mjs`, `scripts/owner-queue-lint.mjs`, `scripts/council-stage-*.mjs`, `tools/council/package.json`", what="Kept because the export carries it (D-WORKFLOW-088: nothing is deleted from an export). The Bedrock dependency in the fork's own `package.json` is the one part that is the fork's choice; it is a lead inside this design.",
  where="`council-invoke.ts:108-111`, `:2243`, `:1552-1563`; `stage-b/refs.txt`", ev="`04` § Q6", vm=HOST, aw=AWN,
  acc="a design: recorded with its sentence in the Phase 7 table."),
 dict(f="F-09", t="`invoke` accepts `--member grok|deepseek|mistral` and `--provider azure|bedrock|direct`; nothing in code refuses an inactive member, only the agents' prose and the rules say not to", sev="Low", cat="Renovation", q="Q6",
  area="`scripts/council-invoke.ts`", what=f"For {EXPORT}: a refusal of a member outside the installed profile on a single `invoke`, or the rules' statement that the agents' prose is the guard.",
  where="`council-invoke.ts:2877-2885` (usage), `:1552-1563` (the provider switch)", ev="by reading: no profile check on the argument path (no call made)", vm=HOST + " (the proof is a constructed `invoke --member grok` that refuses before any network, run with no key)", aw=AWN,
  acc="`COUNCIL_ENV_FILE=/nonexistent tools/council/run invoke --member grok ...` exits with a refusal before any request, quoted; or the rule names the prose as the guard."),
 dict(f="F-10", t="`tools/council/run`'s env guard is one-sided (an absent or unreadable file is skipped in silence, a readable one at another mode is refused), and `COUNCIL_ENV_FILE` is not in its header", sev="Low", cat="Renovation", q="Q2",
  area="`tools/council/run`", what="The header names `COUNCIL_ENV_FILE` and says what an absent file means; whether an absent file should refuse for `invoke` is the coordinator's call. The lane changes no member.",
  where="`run:2-17`, `:21-28`", ev="by reading; this slice's every run used the silent branch on purpose", vm=HOST, aw=AWN,
  acc="the header documents the variable and the absent-file behaviour, quoted."),
 dict(f="F-11", t="npm 11 skipped esbuild's postinstall under `allowScripts`; `tsx` worked regardless", sev="Low", cat="Renovation", q="Q2",
  area="`tools/council/package.json` (npm's behaviour)", what="Recorded so a later failure has its first clue; no change.",
  where="`stage-a/branch/npm-install.out`", ev="`test` rc 0 under `tsx` on both trees", vm=HOST, aw=AWN,
  acc="a design: recorded with its sentence in the Phase 7 table."),
 dict(f="F-12", t="`tools/council/package.json`'s description names the retired `pfi/pfi-collaboration` lineage", sev="Low", cat="Documentation", q="Q7",
  area="`tools/council/package.json`", what="The description names scaffold's export and `IMPORTED-FROM.md`. The lane changes no member.",
  where="`tools/council/package.json:5`", ev="the file; `IMPORTED-FROM.md` § Before 2026-09-30", vm=HOST, aw=AWN,
  acc="the description names the current source, quoted."),
 dict(f="F-13", t="`tools/council/run test` runs its three files under `set -e`, so the first failing file hides the other two verdicts", sev="Low", cat="Renovation", q="Q3",
  area="`tools/council/run`", what="Every file runs and the exit reports any failure. The lane changes no member.",
  where="`run:18`, `:44-48`", ev="by reading", vm=HOST, aw=AWN,
  acc="a constructed failing first file still lets the other two print their summaries, and `run test` exits non-zero, quoted."),
 dict(f="F-14", t="The refresh is prose (*a refresh re-applies these adaptations*), with no recorded procedure or tool, and the export's pristine bytes are kept nowhere, so the fork's adaptations cannot be diffed against them here", sev="Low", cat="Renovation", q="Q1",
  area="`.claude/skills/council/IMPORTED-FROM.md` (not a member); the refresh", what=f"For the coordinator and {EXPORT}: a written procedure or a check that re-applies the five adaptations and keeps the export's SUMS-verified bytes outside the tree for the next diff.",
  where="`IMPORTED-FROM.md` § the adaptations and *A refresh re-applies...*", ev="`02` § Reconciliation: no commit holds the export's bytes for the 9", vm=HOST, aw=AWN,
  acc="the next refresh's record shows the diff of the fork's adaptations against the export's own bytes."),
 dict(f="F-15", t="`council-substrate-integrity.md` names exit 3 alone as the halt; the Facilitator also stops on 6 and 7 (and 8 on the branch)", sev="Low", cat="Documentation", q="Q7",
  area="`.claude/rules/council-substrate-integrity.md` (not a member)", what="The rule names every no-retry stop. The lane edits no rule.",
  where="`council-substrate-integrity.md:67-68`, `:135`; `council-invoke.ts:75-94`", ev="the exit table", vm=HOST, aw=AWN,
  acc="the rule's halt list matches the Facilitator's no-retry exits, quoted."),
]

# Phase 7: each item's outcome and its evidence, written once the coordinator
# has answered where the leads point (stage D).
P7 = {}

def main():
  out = ["# Punch List — M6.P2 T45, the council toolchain and runner", "",
         "**Local depth** (D-WORKFLOW-184): no reviewer seat; the lint and the counts are the check. Every `where` is at `8ebaf8daad` unless it names the branch. No defect was proven by a run, so this slice files no `bug` (brief § 6: a currency gap is a lead). Generated by `tools/punch-items.py` from one list.", ""]
  idx = ["```yaml", "punch_index:"]
  gate = ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
  for n, x in enumerate(I, 1):
      pl = f"PL-{n:02d}"
      out += [f"## {pl}: {x['t']}", "", f"- **Severity:** {x['sev']}", f"- **Category:** {x['cat']}", f"- **Question:** {x['q']}",
              f"- **Source:** {x['f']}", f"- **Owner area:** {x['area']}", f"- **What:** {x['what']}", f"- **Where:** {x['where']}",
              f"- **Evidence:** {x['ev']}", f"- **Can this be done on the VM?** {x['vm']}", f"- **Already written:** {x['aw']}",
              f"- **Acceptance:** {x['acc']}", ""]
      idx += [f"- id: {pl}", f"  severity: {x['sev']}", f"  category: {x['cat']}", f"  question: {x['q']}",
              f"  source_finding: \"{x['f']}\"", f"  owner_area: \"{x['area'].replace(chr(34), chr(39))}\""]
      p7 = P7.get(pl)
      if p7:
          idx.append(f"  outcome: \"{p7[0].lower()}\"")
          gate.append(f"| {pl} | **{p7[0]}** | {p7[1]} |")
      else:
          idx.append("  outcome: open")
          gate.append(f"| {pl} | Open | stage D files the audit issue; the coordinator's answer on #692 names where each lead points |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
  main()
