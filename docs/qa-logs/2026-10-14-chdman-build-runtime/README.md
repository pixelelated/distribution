# CHD converter build preparation — #574

Three original failed families remain preserved; no converter accepted yet.

- Attempt01/export: exact archive has two Zstd CLI test symlinks absent from the assumed special-member category. Export refused before writing source. Additive26a527 omits only those exact two non-build aliases.
- Attempt02/configure: export/native GENie bootstrap pass; configure rejects XInput option. Exact source review2608923 finds libretro assignments overwriting selected SDL OSD; a two-line conditional preserves the intended options/graph.
- Attempt03/link: corrected export/bootstrap/configure pass. Actual target compile reaches final link, then make2 because forced static libgcc conflicts with shared libstdc++ unwind dependencies. A coherent shared-GCC-runtime correction is being prepared.

Original child/container/attach/launcher failures, source/graph inventories, watchdog0, cleanup PASS without force and host exit proofs are retained losslessly. Every admission consumed and failed private work tree retired after source inspection. Current source patches apply only to this standalone QA converter preparation, not the distro package or product pin. All later loader/CHD/Saturn/CUE checks remain unrun.

## Owner04 — BUILD PASS

Additive1015ccf0 explicitly shared GCC/C++ runtimes passes all four original stages. Final build run20261014T170255Z-dd6afbdc and admissionf787f597 consumed; actual host owners exited, no forced cleanup. Original records under attempt04-build-pass. Work retained only for immediate readelf closure and native formats. Compilation alone does not qualify loader compatibility, codecs, proxy native provenance or final firmware.
