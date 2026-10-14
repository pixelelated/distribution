# Independent GameCube RVZ format qualification — #574 / #583 / #584

Can this be done on the VM? Yes: self-created, nonbootable PX5740 data, no account/game/provider, an actual target DolphinTool and target hash executable on accepted no-NIC VM20. Source packets are retained beside this directory: `2026-10-14-independent-format-guest` and `2026-10-14-rvz-empty-partition-source`. Source-only controls remain UNRUN unless a receipt explicitly says otherwise.

## Original failure and minimal fixture correction

Attempt01 is original FAIL1. Both installed/private loaders and help succeeded, then the first independent decode returned1: input file could not be opened. No later conversion/hash ran. Pinned/current official Dolphin requires SHA1(empty) for an empty partition table; the historical generator left zero bytes there. Prior hashing-reader agreement did not establish container validity.

Worker052b36080fe8c9f0f8c9ef6307175bc6786cf9ff supplies an additive generator copy with one assignment/comment and explicit oracle/input rebinding. Raw ISO/expected MD5, d92e127fa5 runtime driver, independent oracle code, actual Dolphin/hash ELF bytes and all timeouts remain unchanged. Historical source and failed results stay immutable. No product-reader bypass or pin change.

## Attempt02 accepted within scope

Original guest worker0, driver0, lifecycle/launcher/runner0 and monitor0;3.100484838 seconds. Five synthetic inputs decode to the same393216-byte ISO; actual Dolphin independently encodes NONE and Zstandard, and both full roundtrips exactly reproduce the raw SHA256. Both target candidate hash invocations return the unchanged GameCube MD5. All11 original native commands exit0 with no timeout or stderr. Sanitizer settings are recorded.

- Raw ISO SHA256:83c6dacc46797bc7d4bdcb4aa2dd253c290316c07c4cda8f6ca1afb889c44121.
- GameCube MD5:118545082f24fc195a446d1ee7bbf816.
- DolphinTool SHA256:f36a2c5f2f31e961ce605cc1c762f1e839f1880a0b1feeba4e09a1fccaa90d5b.
- Candidate hash ELF SHA256:5e00ed65dc6ae8031c54c4309d3f1876be4b380e438a15b8281104402e9375b2.
- Independent NONE RVZ:159504bytes,4526c1597cf8f2c00a236796fcf5433ce56a81d7d4a157f4ae75f58a307bc48f.
- Independent Zstd RVZ:33268bytes,bb3c40134d089fdcf97502f2cff30db9f3b7073ddd61c39adb993a2d24b4d2b9.

Actual original results, argv, source/native hashes, output hashes, samples, admissions and cleanup are retained in each attempt. No forced guest cleanup or surviving descendant. Actual host namespace4026531836 confirms QEMU/launcher/runner/command/watcher exited. Output flushed/unmounted; both admissions consumed; disposable disk/media/UEFI retired: attempt01 2362396672bytes, attempt02 2366124032bytes. Synthetic outputs remain only for the immediate native-proxy input proof; do not keep VM history.

Scope: synthetic GameCube NONE/Zstandard and packed input decoding. No Wii/CHD, commercial-disc integrity, gameplay, actual Sys resource lookup, native-proxy/service lifecycle, new installed firmware or physical-memory claim. The separate native-proxy experiment consumes the independent outputs; it must retain its own results.

`coordinator/` preserves the preparer/exporter and Steam acceptance helper used in this turn. These are recorded test procedures, not permission to replay consumed owners. Fresh allocations and exact input hashes are required. Lossless host record archives carry their original scripts; source-only helper retention itself is not an executed test result.
