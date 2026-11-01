# Preliminary review 2026-10-22-m6-p1-order

- **Format**: the three-model preliminary review
  (`.claude/skills/council/references/review-formats.md`), advisory: no vote,
  no approval, not a council, `formal_council_complete: false`.
- **Purpose**: readiness of the proposed renovation order
  (`docs/reviews/order.md`) before it is put to the maintainer at M6.P1's
  pass-7 gate (#641; #346's third criterion).
- **Authorization for provider use**: the dispatch of M6.P1 on #641
  (2026-10-22), which authorizes exactly one preliminary review of the order
  through the Facilitator on OpenRouter (D-WORKFLOW-049).
- **Contract**: `review-contract.json`, from `readPreliminaryReviewContract()`,
  validated with `assertPreliminaryReviewContract()` (no error). Seats: claude
  `anthropic/claude-fable-5.1` (xhigh), gemini `google/gemini-3.8-flash`
  (high), gpt `openai/gpt-6-astra` (max); `council-facilitator@1.14.0`.
- **Source revision**: `feature/m6-p1-survey-641` at `d2f631e801`; the
  four sources in `source-manifest.json` with their sha256, git blob and
  witness commit.
- **Brief**: `brief.md`, the same for all three seats.
- **Substrate checks before the first call**: `tools/council/run test` (39,
  109 and 19 tests, 0 failures), `tools/council/run verify-pins` (OK),
  `tools/council/run efforts` (OK). The runner's dependencies were installed
  in the fresh clone with `npm install --prefix tools/council`: `tsx`
  4.23.15, node v24.21.0.
- **Calls**: one per seat, in the order claude, gemini, gpt, each verified
  from its provenance (served model, effort, source hashes, output hash)
  before the next. The outputs are `<member>.md` with
  `<member>.md.provenance.json`.
- **Synthesis**: `synthesis.md`, and the answers by name in
  `docs/reviews/order.md` § The preliminary review of this order.
