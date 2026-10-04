# Current upstream proxy before assembly — #419

Upstream ea9aba6c2b8b2f27e254d696ac8738c9e5c8793e arrived17:46:34UTC while
preparing the corrected build. The live freshness check found it before any
assembly. Archive9931790bb3f5d93f0d14afb7347af58badd0560413f85486d534071fefda2d62
is compared with the verified ec60 archive, including file modes. Both contain
586 files; only11 Android app/src/main/java files differ. All217 Linux and53
native-source files are identical. Parent gitlinks remain1433173(rcheevos)
and8e7b8bd(libchdr), matching their coupled recipes.

All15 fork patches apply at fuzz0 to both old and new trees. All270 resulting
Linux/native file hashes agree. Storage schema and version strings are
unchanged. Package pin, archive hash and schema-review annotation advance
together; no helper behavior changes. The initial test launcher lacked the
source root on PYTHONPATH and failed imports; original failure is retained.
Corrected fresh run20261004T180538Z-85aeb1a0 verifies imports from its actual
working directory before executing199 upstream tests and8 fork controls:
all PASS. Package lint/schema guard pass; live freshness says pin is HEAD.
Actual tool68167 and outer/watcher results0.

The first corrected98d0 tree was frozen but never built. Its independent
cache copy from1600 finished18:03:18UTC:104,071,325,281 bytes, zero checksum
comparison differences,2,525,215 regular files with independent inodes. The
actual tool27389, copy.rc, outer and watcher return0. This unbuilt independent
cache can be relocated to a new explicit frozen source tree after all copy
processes exit. Preserve the98d0 source/manifest, completed copy receipts and
both previously built trees/images. New source and packaged VM evidence must
name the refreshed freeze; no previous-artifact verdict is transferred.
