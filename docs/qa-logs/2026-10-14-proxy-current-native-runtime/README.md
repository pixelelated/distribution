# Current proxy native source build — #583 / #584

Attempt02 built the current native bridge successfully from exact recipe archives: RAOfflineProxy c7ebd1b6e777f3751ff0ecdf8aba54045844e00d, rcheevos1433173220a7eaede6a9ed7a18e94117be1821e0, and libchdr607694ca0812edfc9cc2030c64634fc2393668de. All857 original files match; the recipe make_target body is unchanged. No native patch or unpinned source was selected.

Pinned offline builder and readonly accepted SDK produced447272-byte libraproxy_rchash.so, SHA6349b150899f7c32971b8d9ee882934e41f2f8fc9d6a129045e15ea62096d52c. GCC/export/readelf/container/runner/launcher original exits0; monitor0; no OOM, forced cleanup or surviving owners. ELF64 x86-64 shared object has the required four exports, libc as its only DT_NEEDED and no RPATH/RUNPATH. Both stages' original receipts were consumed; compact lossless export retained and16,711,680bytes of compiler work retired. The small library remains solely for current dependent qualification.

Original attempt01 failed in source export because the pinned builder's Python3.10 does not implement hashlib.file_digest. The additive py310 packet streams the same open descriptor, retaining fstat checks and all archive/recipe/source identities; failed receipts remain unchanged.

Source provenance is now established for the new ELF. Subsequent #588 actual-service runtime in ../2026-10-14-proxy-startup-runtime verifies its guest loader and source-bound overlay. Current-library hash/codec matrix and final installed/default-boot/clean/retained image acceptance remain due; older ELF receipts are not relabelled. Qualification provenance files intentionally retain their creation-time VM_UNRUN label; later runtime receipts establish only their stated scope.
