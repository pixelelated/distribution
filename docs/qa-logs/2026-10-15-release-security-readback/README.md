# #344 security evidence readback — 2026-10-15

The bot's current effective repository permissions and expiry are recorded. The expiry-notice mechanism and remote self-hosted runner isolation/disabled fallback remain unverified under the existing #344 criterion. This is a bounded read-only evidence update, not a new security policy or complete security audit.

At 19:58–19:59 UTC, GitHub identified `blitterbot` (335883270). The authentication response metadata reports expiry **2027-10-01 05:27:47 UTC**. Effective repository permissions are:

| Repository | Pull / triage / push | Maintain | Admin |
| --- | --- | --- | --- |
| pixelelated/distribution | true / true / true | false | false |
| pixelelated/emulationstation | true / true / true | false | false |
| pixelelated/splash | true / true / true | false | false |
| pixelelated/website | true / true / true | true | false |

These are the four named release repositories, not an exhaustive token-grant or organization inventory. No token value or authentication file was inspected. `existing-evidence.json` identifies the October6 sanitized original: the same expiry was already observed, and that proof expressly did not configure or send a reminder. The bounded current public-tool/workflow/document search found no expiry-notice mechanism. A private mechanism may exist; none was inspected or proved.

Remote `next` matches `e51c029e659edd6365d6996b4fe9edfc9e711f21`. All22 repository YAML workflows at that commit declare GitHub-hosted runner labels; the inherited PR validation and called freeze checker use `ubuntu-24.04`. Two existing current-head jobs independently report the `GitHub Actions` runner group: wordlist run38783551906 succeeded, while record run38783551822 failed. Their outcomes are preserved; no workflow was launched. The source-only disabled candidate automation has a literal job `if: false`, while its API workflow state is `active`. This does not prove remote runners are disabled.

The repository Actions settings, default workflow permissions, repository runners and organization runners endpoints each returned **403 Resource not accessible by personal access token**. Their values remain unknown. The current branch endpoint reports `protected: false`; that is a bounded observation, not a new branch-protection requirement or a blanket security failure. The API also lists one dynamic Copilot workflow outside the22 repository YAML files; its behavior is not inferred from the tracked workflow review.

Concrete remaining evidence is limited to the existing criterion: (1) a sanitized existing enabled expiry-notice mechanism tied to the recorded date and intended recipient/channel, and (2) an authorized administrative readback of applicable remote runner registration/access plus either the explicitly disabled/unregistered fallback or the trusted-trigger/isolation evidence already required by D-WORKFLOW-119. Local absence, a403 response or an offline status alone does not supply that evidence. No broader bot token permissions are requested here.

`host-read/` holds allowlisted fields and endpoint/HTTP/original-exit receipts for15GETs:11HTTP200 and4HTTP403. The initial sandbox's13transport/CLI failures remain at the root and are not relabelled as403. Raw responses, raw stderr, secret endpoints/values and authentication material were not retained. `workflow-source-review.json` binds each reviewed Git blob, source digest and relevant runner/trigger lines. `assessment.json` provides the criterion mapping and precise limits. No service, VM, build, settings mutation, timer installation, reminder/contact, shared-record edit or commit was performed.
