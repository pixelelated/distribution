# Explicit audit filtering — #636

The local Facilitator now records `content_filtered_no_retry` (exit8) and stops
after one explicit OpenRouter `content_filter` response. Empty or partial text
does not become a successful review or a resend. Buffered Fable and supported
SSE routes retain the finish reason, identity and usage; a later stop frame or
stream interruption cannot erase filtering. Model/provider mismatch retains
precedence, and original transport diagnostics are retained. No model, effort,
route or content changed, and no provider request ran during this repair.

The local substrate is `council-facilitator@1.14.1-pixelelated.1`, with accountable
pins. Staged reconciliation passes the finish reason to the same classifier;
capture/readings reject a filtered receipt disguised as success. The original
imported bundle, hashes and failed audit provenance are unchanged.

## Evidence

- Original buffered controls reproduce four automatic empty-output attempts and
  acceptance of partial filtered text. The initial SSE fixture wrongly selected
  Fable, whose installed route does not support SSE, so those initial refusals
  prove nothing about stream classification. They remain in the original log.
- The corrected fixture uses the installed Mistral SSE recipe with fully mocked
  fetch; no historical/inactive seat was invoked externally. Its first follow-up
  overclaimed a response_body phase that the original SSE catch does not emit;
  the final assertion verifies the retained interruption message instead.
- Final routing:119/119; toolchain:39/39; effort tests:19/19. All exit0. Strict
  effort and final accountable-pin verification exit0. The toolchain reran after
  the final diagnostic-preservation change. These are local synthetic tests,
  not provider access or an independent audit.
- Offline replay of the four saved provider attempt records: the three explicit
  filters classify terminal without budget increases; the final unfiltered body
  failure retains its bounded transient classification. Original SHA256 remains
  `15380d5099110b9dcf583ceba3bb282b6ce7c56413f76dcbfa7863008354bfd6`.
- The staged controller/readings modules also load in the replay. Full staged
  reservation/capture runtime was not rerun; that boundary is not claimed from
  module loading. The current corrective audit uses the ordinary dispatcher.

## Upstream and continuation

The available source-estate export is scaffold main7be6721b (September30),
Facilitator1.14.0, with the recorded fork adaptations. Its classifier lacks the
finish-reason input. No newer delivered export or callable source-estate tracker
was available here; this is not a claim that current upstream lacks a fix.
OpenRouter's official schema confirms normalized content_filter is distinct
from stop/length/error:
https://openrouter.ai/docs/api_reference/overview#finish-reason .
Keep this small repair in the upstream queue and recheck the source estate before
submission/import reconciliation. No upstream submission has occurred.

Can this be done on the VM? No guest is needed: the defect is host response
classification, exercised with synthetic envelopes and offline original metadata.
No handset, cloud credentials or personal account data is consumed.

This fixes retry handling only. The frozen0bcbbb7f corrective audit still has no
verified independent answer. Do not automatically resend the filtered packet,
repackage it to evade filtering, or claim this test suite satisfies that audit.
The code-auditor Phase4.6 remains pending; product source stays frozen.

Original log bytes are stored losslessly as `.log.gz`; `log-identities.json`
records raw and compressed hashes. The first staged whitespace check rejected
Node assertion-output blank lines. Compression preserves those originals rather
than editing the evidence to satisfy a source whitespace check.
