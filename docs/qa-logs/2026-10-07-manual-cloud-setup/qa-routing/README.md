# QA routing after migration retirement (#508)

Nine local controls in results.json prove current-source migration runners
refuse before creating test fixtures when the engine is absent, the sourced
protocol performs only its availability probe before refusing, and an explicit
historical --ref reconstructs deleted helper bytes exactly. They also verify
that --source-root stages actual working source bytes, --archives-only selects
all thirteen ordinary archive cases, and a mixed T24 selector still refuses
migration cases. No VM or provider
operation ran in these controls. Bash/Python syntax and diff checks pass.

check.py is the executable receipt driver for this workspace; it uses the
manual-cloud-folders source checkout, whose engine is removed, and historical
source7cfdf9f73ae2a064ee4f281461e661301cb2dd65. Its temporary fixtures are removed.
The historical engine SHA256 is retained in results.json. Historical migration
receipts are unchanged; these new guards do not count as migration QA passes.

The layout helper's --ref and --source-root are mutually exclusive. The
archive-only selection uses explicit case membership: a substring such as
T24 also matches historical migration classification and actor cases, so it
cannot authorize the ordinary archive subset by itself. The broad script
suite uses --archives-only for current source and retains the full matrix
when testing a historical source that supplies the engine.

The ordinary cloud-round-trip structural check now asks cloud_setup
--folder-state to report the chosen sibling paths and verifies the configuration
hash is unchanged. Its full installed-image run remains part of later affected
firmware qualification. Current source proof is in the separate script packet.

last-good-scripts-test is maintained separately under broad-harness; do not
conflate these local refusal controls with that suite's terminal result.
