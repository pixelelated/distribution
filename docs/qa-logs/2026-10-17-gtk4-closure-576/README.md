# GTK4/WebKit6 closure evidence (#576)

**Strict status: FAIL, original return code 1 retained.** Attempt 05 inventories
95 ELF nodes and resolves all 396 NEEDED/interpreter edges. Eleven critical
package/sysroot pairs match at the normalized loaded-byte level. The compiled
input fixture contributes one ELF and 18 resolved edges (17 NEEDED plus its
interpreter), has no RPATH/RUNPATH, and is bound by SHA256
`27908eb5badf203de53332c4e35ee96d8c7fbbb6afefd5d72d11c9d8068359f8`
(27,056 bytes). No ELF binaries are retained in this packet.

Six inherited accepted-image search paths remain strict findings: FreeType,
libgcrypt, libthai and libX11 contain the build-host sysroot path; libwoff2dec and
libwoff2common contain relative `lib`. They are unchanged between attempts 04
and 05. No new overlay library or fixture introduces one. These are not observed
loader failures: a nonexistent absolute search directory may be skipped by the
loader. Relative paths also require the working-directory context to assess.
Do not relabel the strict check PASS or call this a GTK4 regression.

## Original attempts and verifier history

- `attempts/01/`: original verifier stopped on multiline CMake-cache parsing.
- `attempts/02/`: corrected CMake parser stopped on an absent build-ID assumption.
- `attempts/03/`: strict loaded-byte identity passed all 11 critical pairs;
  sparse sysroot closure exposed missing runtime-only files and staging RPATH.
- `attempts/04/`: runtime-only model uses the six new package payloads over the
  accepted image/system tree; 94 ELFs, 378 edges, no missing dependencies,
  six inherited search-path findings, original return code 1.
- `attempts/05/`: same runtime model plus the compiled fixture; 95 ELFs,
  396 edges, same six findings, original return code 1.

`tools/v1/` through `tools/v4/` preserve exact source, available source checks
and diffs. Three verifier diffs are losslessly gzip-compressed to retain their
original context whitespace. The v1 packet also retains its original unrun fixture preparation.
Its historical README and the attempt-04 README describe the state at capture;
this README and attempt 05 describe the latest result. No old result is rewritten.
The v3 identity comparison normalizes only ELF section-table offset/count/name
index fields; program headers, LOAD geometry and all loaded bytes must match.
The v4 runtime model never satisfies runtime dependencies with sysroot artifacts.
All unsupported/build-host search paths remain hard errors while inventory continues.

The included `compile-only-qualification.json` explicitly allowed compilation
with these inherited findings acknowledged. It granted no runtime qualification.
The separate [input compile evidence](../2026-10-17-gtk4-input-compile-576/README.md)
records the actual compiler/owner success; target execution and fixture runtime
remain **UNRUN**. Initial spike preparation is in
[GTK4 spike](../2026-10-17-gtk4-spike/README.md).

## Minimal next investigation

1. Keep the six exact path strings and accepted-image ELF hashes in
   `analysis.json`; trace their corresponding recipe/linker/install flags and
   compare the same upstream package versions before choosing a portable fix.
2. In a separately admitted disposable guest, verify actual load resolution,
   working directory and mapped libraries. Do not select sysroot binaries as
   replacement runtime files or infer a launch failure from a path string.
3. If a packaging fix is warranted, remove inappropriate RPATH at its source,
   rebuild the affected package, repeat static closure, then verify the normal
   browser/native-input flow. Upstream candidates should remain narrow.

This is ELF NEEDED/interpreter inspection only. It does not prove symbol-version
ABI, dlopen modules, schemas, fonts/certificates, input behavior, rendering,
performance or sandbox isolation. Root-run success alone is not sandbox proof.

## Lossless verification

Run `python3 -I verify.py`. It verifies the complete local SHA256 manifest and
all copied-original byte counts/hashes. `--originals` also compares the retained
source paths if those temporary paths still exist. Neither mode launches target
code or reproduces a build. `original-files.json` maps every lossless copy to its
original absolute path. Original receipt files retain their historical paths.
