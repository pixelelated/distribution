# Final five-profile inventory runtime — #528

The root-owned inventory completed with original result **`PASS_INVENTORY_WITH_PUBLICATION_GAPS`**. This is successful inventory execution with publication gaps, not a completed publication bundle or corresponding-source/legal clearance. `publication_bundle_complete` remains false and `common_rc_identity` remains null.

Run `20261015T093346Z-ed162eab` returned command/monitor/runner 0/0/0 and launcher/inner/outer/wrapper 0 at 09:34:11 UTC. All ten collector children have original returncode0, observed waits, no timeout/interruption or cleanup signals. The original cleanup receipt records all ten child identities absent, no survivors and no cleanup/receipt errors. Ordinary admission `e73b73b3325f41c392a8eb6e7ddeb105` was consumed at 09:39:31 UTC with outputs held and zero deletion credit. This custody task did not repeat collectors or inspect live process state.

The actual profile results are:

| Profile | Mapped component rows | Unpacked roots | Image install stamps | Archive-reconstructed packages |
| --- | ---: | ---: | ---: | ---: |
| generic-x64-x86_64 | 594 | 579 | 536 | 0 |
| h700-arm | 238 | 234 | 188 | 0 |
| h700-aarch64 | 616 | 600 | 554 | 0 |
| sm8550-arm | 241 | 237 | 195 | 0 |
| sm8550-aarch64 | 677 | 659 | 620 | 1 |

Counts are per-profile entries, not deduplicated unique components; historical counts are not reused. Original `source-inventory.json`, `components.json`, `publication-worklist.json`, input manifests, stdout/stderr, original child/process results and per-profile results are retained for every profile. All original worklists remain `publication_bundle_complete:false`. The SM8550 AArch64 collector reports one reconstructed package; the raw output preserves its exact provenance. The shared publication-holds input retains 17 existing notice rows plus the separate Doom-data disposition. No notice or source hold is closed by execution success.

GENERIC_X64 and H700 remain source `f8636de1d105275dbf9420bbabbbc26f79abb10f`; SM8550 remains `9aa7affee9d4ad5e69725cab20b6d7ad84d93dea`. The exact one-path ABL checksum product delta is retained in the binding receipt. This is explicitly a mixed engineering source family, not a common RC identity. The original VM #597 reporting failure/null launcher status, H700 failed producer/reader history and SM8550 failed producer followed by fresh independent acceptance remain preserved in the bound originals. No producer failure is relabeled by this inventory.

`originals.tar.gz` holds the exact complete small owner tree and original watch-run records: executed collector/lifecycle source, preparation/bindings and copied acceptance originals, resources/retention/admission, original channels, profile outputs, cleanup, completion evidence and consumed receipt. `member-manifest.json` records original paths, bytes, hashes, modes, UID/GID, user/group names and exact nanosecond mtimes; all members were read back against original bytes and metadata. `outcomes.json` gives the compact result/digest index. Large source archives, caches and firmware are not included, and originals are not deleted. Existing owner copies of prerequisite manifests are retained to keep the exact execution bindings reviewable.

The source/review proposal is separately durable at `../final-inventory-source/`; its preparation seal is `6b2c7bf6e9d953d054ab666df6f5ab25b8bc184660c267c12bcce218059a99a3`. Original `PREPARED_UNRUN` preparation receipts describe preparation time and are not rewritten after execution. Later actual results and consumption are retained separately here. The corrected collectors' known coverage limits and prior source-review failures remain in that source custody.

This packet establishes execution and custody of the named current inventory outputs only. It does not collect the source archives, prove independent/off-host retrieval, resolve notices/vendor/static provenance, clear #528 or #601 publication holds, or establish physical device behavior, native FEX execution or RC readiness. No runtime, collector, network transfer, tracker or canonical record was changed during this retention task.
