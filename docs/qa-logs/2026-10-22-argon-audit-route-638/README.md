# Argon audit-only route — #638 / #636

Owner selected Gemini 4 Argon as an alternative independent reviewer. The new
`gemini-argon` Facilitator route pins `google/gemini-4-argon`, high effort,
OpenRouter Vertex global routing (reported provider Google), and 65536 output
tokens. It is outside every council profile; the five-seat roster and its
Gemini 3.8 Flash model remain unchanged. Direct or unqualified SSE use is refused.

Public catalog and endpoint JSON were retrieved October22. The catalog advertises
943718 maximum output tokens, while Google's official synchronous documentation
states 65536 (long-decode uses a separate continuation mechanism). This route
uses the synchronous allowance and preserves unified-context headroom. The
catalog below-maximum lint emits an informative NOTE, not an unexplained downgrade.
https://ai.google.dev/gemini-api/docs/models/gemini-4-argon
https://openrouter.ai/api/v1/models/google/gemini-4-argon/endpoints

Generation IDs, native finish reasons and bounded separate refusal previews are
now retained for buffered responses and synthetic SSE captures. Refusal text is
never extracted as review content. Identity/provider hard stops and explicit
filter no-retry behavior remain. Refusal previews can contain provider quotations
of the prompt; treat them as diagnostic data and review before publication.

Final validation: toolchain 39/39 and routing 127/127 in tests-final03.log;
effort suite 19/19 in effort-tests-final.log; accountable pins and strict efforts
PASS. Tests use mocked provider data only. Earlier failures remain original:
whole-recipe and count tests assumed only definitive/shadow recipes, then the
separate effort suite had the same assumption. Both now explicitly include the
audit route without changing the five-seat assertions. One attempted edit matched
no literal and made no change; its shell still reran the old test, retained in
tests-final.log. The later commands use set -e.

The source patch is local `council-facilitator@1.14.1-pixelelated.2`, with
accountable pins. No newer source-estate export was available for comparison;
reconcile this small adaptation upstream separately. Live probe and audit results
are separate later evidence, not implied by these synthetic passes. No product
source, safety setting or prior failed audit record was changed.

The first commit was correctly refused by the credential-shaped-line check for
a literal synthetic API-key fixture. It now uses the repository's runtime-built
fixture convention; no actual credential was present. Routing reran 127/127 in
routing-final.log after that test-only change. The check was not bypassed.
