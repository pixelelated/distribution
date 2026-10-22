# Per-seat verification (the orchestrator's checks, before the next seat)

Checks made against each `<member>.md.provenance.json` (no council-research
lint stack is installed in this estate, so `review-formats.md` step 4's
checks are performed and recorded here directly):

| Seat | Exit | Served model (`final.verification`) | Effort (`final.effort_verification`) | Provider | Output sha256 = file | Sources = manifest | Duration |
| --- | --- | --- | --- | --- | --- | --- | --- |
| claude | 0 | `anthropic/claude-fable-5.1`, PASS (semantic, from the provider response) | xhigh, PASS (57,179 reasoning tokens) | Anthropic (not pinned) | `46f4def547dc...` = `sha256sum claude.md` | the four paths and sha256 of `source-manifest.json`, witness `d2f631e801` | 20:09:46Z to 20:24:34Z |
| gemini | 0 | `google/gemini-3.8-flash`, PASS (semantic, from the provider response) | high, PASS (36,431 reasoning tokens) | Google AI Studio (not pinned) | `395c7e6eca0f...` = `sha256sum gemini.md` | the four paths and sha256 of `source-manifest.json`, witness `d2f631e801` | 20:24:55Z to 20:29:50Z |
| gpt | 0 | `openai/gpt-6-astra`, PASS (semantic, from the provider response) | max, PASS (21,857 reasoning tokens) | OpenAI, pinned, PASS | `bd36b290abcf...` = `sha256sum gpt.md` | the four paths and sha256 of `source-manifest.json`, witness `d2f631e801` | 20:30:02Z to 20:41:50Z |

All three seats verified; no exit 3, 6 or 7; the three served models are distinct (no cross-corpus collision).
