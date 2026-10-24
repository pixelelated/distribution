# Retrospective Audit — M6.P2 T6, upstream's helper tools and the other distributions

**Date:** 2026-10-24. **Read at:** `reviewed-at: b96e1ca761`, the slice's bytes `8ebaf8daad`'s. Findings are `02`'s `F-NN`.

## 3.1 Architectural coherence

The 135 paths are LibreELEC's developer tooling, carried whole into ROCKNIX and then the fork, and two distributions' identities the build can select but never does. They have no architecture of their own to keep coherent. What matters is the edge between them and the engine T5 read:
- **Three tools are on it:** `adjust_kernel_config` and `check_kernel_config` from the `Makefile`'s `kconfig-*` targets, and `mtstats.py` from every multithread build.
- **One sits beside it:** `pkgcheck`, run by hand after every recipe edit.
- **The rest stand off it.**

The table's shape, mostly kept, is the coherent outcome for upstream's tooling (futro addendum A3).

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed:** `tools/pkgcheck` fails it for an unmatched name (F-02).
- **`engineering-practices.md` § Before deleting a duplicate:** asked of every *unreached* row. What the file guarded, stamped or documented that nothing else does is its `Already written:` line, and none found a trace. No row is deleted (brief § 2).
- **`engineering-practices.md` § Consider contributing every applicable fix upstream** (D-WORKFLOW-164/165): finding 24's class, F-02 and F-03 are #585 lines; nothing is submitted.
- **`packaging-and-patches.md`:** the late-binding rule `pkgcheck` enforces is enforced for the names its list carries, and not for every name the build sets after a recipe loads. This line named `TOOLCHAIN`, `SYSROOT_PREFIX` and `INSTALL` until stage E. S2's derivation (`02` P14) found only `INSTALL` late of the three, plus 17 more, and `44f64842b6` adds them.
- **`instruction-files.md` § The fork's own tools:** `pkgcheck` *(upstream's)* is incomplete (F-01).
- **`fork-workflow.md` § Personal paths:** none of the 135 is on it. Correctly: the fork-only tools are other slices'.
- **`bugs-are-agent-first.md` rule 6:** F-02 is contained (a count and a status) and ours to close. F-03 is in a file no fork build reads, so it is upstream's to close.
- **`upgrade-and-install.md`:** nothing here is on an image, so no device carries anything written by these tools. Each `Already written:` line answers for the trees and caches instead.
- **`vm-first.md`:** asked and answered, no. The bench is the tree and the record.

## 3.3 Spec fidelity

The brief's figures reproduced exactly at stage A: 135 paths and 7,369 lines; tiers 134 and 1; reach 108 and 27; languages; the Q4 count of 1. Its first caller counts (`refresh-patches` 1, `pkgcheck` 1, `adjust_kernel_config` 2, `mtstats.py` 1) were a count by one pattern over fewer roots. The table's two-way search gives `pkgcheck` 14 by path, all documents.

The brief's question "`scripts/build` calls `tools/pkgcheck`?" is answered no, by T5's coverage row and the path search. The brief's class *reached by a tool nobody runs* fits the 62 helpers and the `find_build_warnings` configuration.

## 3.4 Platform conformance

`n/a`: nothing in the slice runs on a device or a guest (brief § 2, § 5).

## 3.5 Cross-system interaction audit

### Interaction: `tools/update-*` x `scripts/update_packages` (T5's E6) x D-WORKFLOW-193

`update_packages` (`make update`) and `update-pkg` both bump recipes. Since T5's E6, `update_packages` keeps every archive's `PKG_SHA256` and refreshes one from a verified fetch.

`update-pkg` writes a `PKG_SHA256` from one `curl` fetch (`:61-64`), which agrees with D-WORKFLOW-193's checksum rule. Its `curl` verifies TLS by default, but it lacks `--fail`, so an error page would be hashed (a lead, unreached).

No seam fault: neither is run on the fork. And `update_packages` does not call `update-pkg` or its helpers, as the brief corrected.

### Interaction: `tools/mtstats.py` x `config/multithread` (T5's E8)

`config/multithread:64` pipes a finished build's history into `mtstats.py`. T5's `7abea6eb86` puts the step in an `if` and says a failure instead of returning it. At `8ebaf8daad`, a failing `mtstats.py` still fails `scripts/build_mt`, the upstream CI route that calls the function bare. The seam's fix is T5's and lands with its merge.

### Interaction: `tools/pkgcheck` x `packages/README.md` x `packaging-and-patches.md`

The README (274 to 285, the issue table) and the rule (34, 46) say what `pkgcheck` checks and that it runs after every recipe edit. The tool checks the late-binding list it carries, unknown and duplicate functions, a missing brace and intertwined variables. Since `81221658b3` it exits non-zero on a FAIL.

What the documents promise and the tool does not do:
- it says nothing, and exits 0, for a name it does not find (F-02);
- its list does not hold every late-bound name (PL-06; S2, `44f64842b6`, adds 18).

### Interaction: `tools/docker/*` x the root `Dockerfile` x the `Makefile`'s pinned digest

The fork's container is upstream's image, copied to the fork's mirror by `fork-mirror-build-container.yml` (`skopeo copy`, 44) and pinned by digest in the `Makefile`. The root `Dockerfile` is identical to upstream's (T5); the pin's age is T5's PL-16, deferred to #652. `tools/docker/` holds six other Debian and Ubuntu containers and a README that describes them. No path in the tree names `tools/docker`, so the README can mislead a reader looking for the fork's container (F-06's class; listed in the #585 proposal).

## The futro's predictions, checked

The T6 addendum's simulation (`docs/futros/2026-10-24-m6-build-engine.md`, 370 on), point by point:

| Prediction | What happened |
| --- | --- |
| (1) running a tool to learn its reach | not done; only `pkgcheck`, a reader, was run, over a fixture tree |
| (2) a zero filed on one pattern | not done; every zero was searched a second way, and that search found `adjust_kernel_config:38`'s call |
| (3) a documented tool filed as unreached | not done; *reached by a document only* has 8 rows |
| (4) the two distributions deleted | not done; kept |
| (5) the 62 helpers read line by line | not done; one row, with its file count and `bash -n` |
| (6) the plan file without the two keys | not done; `review-plan.json` carries `tier_exception` and `reason` |

The pre-mortem's outcome is the table's: mostly *kept*, its value the #585 proposal and the one fork-own row.
