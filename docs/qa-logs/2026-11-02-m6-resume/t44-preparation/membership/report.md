# T44 membership/boundary preparation — wN:p2

Codex / OpenAI, session `01a19d11-dda5-72e3-86f9-416f36341c24`, m6-p1-survey wN:p3. Authority: complete #691 comment **6589185959**; full #691 thread and #700 body/comment read. This is survey-pin membership preparation only. T2 retains accepted later-history/catalogue/import-version reconciliation; root retains baseline, ownership, brief, criteria and dispatch.

Immutable inputs:

- Distribution P1: `2174265e9cc1b248c0fbe27fa101875984d46d6b`.
- Coordinator: `92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1`.
- ES survey: `16dbac5211eea7e70db7394372033be2be7df829`, read only through Git objects in `/home/max/Development/emulationstation-next`.
- Inventory-recorded ES merge base: `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd`; fixed upstream: `e282b05627c0d2193c19d7cc526176e047530c3d`. No moving upstream ref used.

**The generated 594 / 374,547 / 51 / 543 / 143,710 / 11,989 quantities reproduce.** Every inventory line/tier matches the pinned Git derivation; no interface partition ambiguity. Six governing files—areas, slices, inventory JSON/Markdown, order, inventory tool—are byte-identical between P1 and coordinator. Their complete SHA256 pairs are in `results.json`.

## Exact population and line semantics

T44 is `es-vendored-and-data`: area interface, positive `es:**`, exclusions `es:es-app/**` and `es:es-core/**`, `rest:true`. The canonical selector first considers **all non-rest selectors**, then rest selectors; this is not an earlier-slice-only subtraction. The naive non-app/non-core set is **603 paths**. Nine fork-own libcheevos rows / **2,556 lines** belong to T20, leaving exactly **594**. Their exact paths are in `results.json:excluded_by_nonrest`: libcheevos CMakeLists, LICENSE.rvz-padding, RVZ-NOTICES, cheevos.cpp/.h, libretro-common's md5.c, rcheevos's hash_disc.c and rvz_hash.cpp/.h.

| Quantity | Pinned result |
| --- | ---: |
| Regular blobs | 593: 583 mode100644 + 10 mode100755 |
| Gitlink | 1 mode160000; no symlinks |
| Git text-counted blobs / binary blobs | 543 / 50 |
| Inventory / Git-numstat lines | 374,547 |
| Actual text-blob logical lines | 374,546 |
| Text newline bytes | 374,530; 16 text files lack a final newline |
| All regular-blob bytes | 40,988,941: text12,714,669 + binary28,274,272 |
| Inventory tiers | 51 fork-own / 543 upstream-carried / 0 vendor-carried |

The one-line difference is **`external/pugixml`**, gitlink commit **`61c944895e071872370219cadade8423dc6e04dc`**. Git numstat counts its synthetic subproject line; this is not one source line or a blob. Its child tree is not part of these 594 keys and was not fetched/read. The empty `external/id3v2lib/test/extra/empty.mp3` has zero bytes and Git counts it as text; “543 text” is a Git counting class, not a semantic media classification. The ten executable modes include binary `resources/checksound.ogg`; no mode change is proposed.

The **143,710 read / 11,989 fork-own read** figures follow the tool's code-language/non-vendor/non-unreached formula. They are not completed reading evidence or a T44 line-by-line mandate: the canonical order displays a table slice as **594 rows**. All ES rows inherit package-level `shipped` reach; that does not prove every test fixture, catalogue or asset is installed or used at runtime.

## Groups and provenance boundaries

| Survey group | Paths | Inventory lines | Fork-own paths |
| --- | ---: | ---: | ---: |
| external | 334 | 135,991 | 1 |
| locale | 38 | 158,693 | 3 |
| resources | 147 | 70,536 | 2 |
| tests | 35 | 3,824 | 35 |
| CMake | 15 | 1,496 | 0 |
| root files | 17 | 3,408 | 4 |
| .githooks | 6 | 526 | 6 |
| .github templates | 2 | 73 | 0 |

The external subdivision is: libretro-common **199/86,913**, rcheevos **67/32,771**, id3v2lib **60/4,682** (four binary fixtures/assets), nanosvg **5/4,480**, doctest **1/7,134**, external/CMakeLists **1/10**, pugixml gitlink **1/1**. These are T44 rows after T20's exclusion, not complete vendor trees.

All 543 upstream-carried identities equal both fixed merge base and fixed upstream. The 51 fork-own rows divide into **46 added / 11,946 lines** and **five changed / 15,779 lines**. The five changed files are `.gitignore`, root `CMakeLists.txt`, `locale/emulationstation2.pot`, and the en_GB/fr `.po` files. Relative to that merge base, no changed preexisting external blob remains in T44; the nine libcheevos fork-own rows are T20's.

“Fork-own” is a net-difference tier, not authorship. The selector explicitly describes doctest as a fork-added import. Its 7,134 lines account for most of the 11,989 fork-own code-line statistic; the remaining **4,855** are root CMake **617**, hook code **414**, and root tests **3,824**. At this pin doctest is mode100644, blob `52b4a4aa305548c1d302c57bdecd3d42b8cc0f89`, SHA256 `94029a7d32da24a56249658147dbd2b33ff0b9ed665295cbbaf19aafff5b0ced`. Its comparison with the original imported release belongs to T2; this preparation proves presence/identity and added-since-base status, not “unchanged import” or current upstream currency.

**Catalogue distinction:** the survey has **35 `.po` language catalogues plus one `.pot` template**, totaling 36 translation-class files / 158,631 lines. Locale's remaining two files are its CMakeLists and checkLocale.sh. The complete shared note6375264017 says “all 36 catalogues”; that is not the survey's `.po` count. This report leaves the accepted T2 rename/later-source explanation to T2. The exact 35 language names are in results, not inferred from the note.

Resources comprise 101 Git text-counted assets/helpers and 46 binaries, including eight font files. Root XML data contributes 63,262 lines; SVGs remain text blobs despite inventory language=image. `resources/` data is distinct from `es-core/src/resources/` implementation.

## Concrete seams; no ownership recut

Canonical intersections with T21/T34/T35/T36 are empty. Their selector populations at the survey are respectively **14/9,249**, **80/21,984**, **96/22,575**, **58/50,840** (paths/lines). Boundary ownership comes from the immutable selectors and #700's slice map, not later accepted-history claims.

- **T21 #668:** Settings/SystemConf/HttpReq/AtomicFileUtil and the bridge remain its code. T44 owns the root test doubles and `tests/app-unit/CMakeLists.txt`, which references AtomicFileUtil.cpp at line96; its SystemConf double explicitly names the T21 header. These dependencies do not move either path.
- **T34 #681:** `es-core/src/components/**` remains T34. T44's AsyncNotificationComponent fake explicitly identifies itself as a double for that component (lines1–3).
- **T35 #682:** the remaining es-core files include Window/AppWindow and es-core/CMakeLists. T44's AppWindowTests includes AppWindow.h (line5); its Window fake names the production header. T44 root CMake adds es-core/es-app at lines607–608, without owning their subdirectory build files.
- **T36 #683:** utils/resources/renderers remain T36, excluding AtomicFileUtil already reserved to T21. T44's app-unit CMake references StringUtil.cpp at lines55,77,97. Assets/fonts/shaders under root resources remain T44; their core resource/renderer consumers remain T36.
- **T20 #667 / T18 #665 / T37 #684:** fork-own libcheevos stays T20; `es-app/tests/**` stays T18 while root `tests/**` stays T44; distribution recipe/themes stay T37. No proxy rcheevos files from the distribution are T44 members.

Build/catalogue facts are static only: root CMake lines610–615 conditionally add es-app unit tests and locale; locale/CMakeLists lines9,25,31 runs xgettext over es-app/es-core, updates PO files and emits MO files. The root updater script fetches/writes catalogues. None was run. `.gitmodules` identifies the pugixml submodule; external/CMakeLists includes it only when `USE_SYSTEM_PUGIXML` is off. Coordinator recipe line24 explicitly passes **`-DUSE_SYSTEM_PUGIXML=1`**, with pugixml dependency on line13. Its line5 still names survey16dbac; this historical pin does not establish integration of later accepted owner changes.

## Commands, immutable manifests and limits

The independent reader reproduces selection and metadata without importing/executing the inventory producer:

```sh
taskset -c 8-23 python3 /tmp/m6-t44-membership.6KRT8E/derive.py
```

Exact Git command forms in the script:

```sh
git -C DISTRIBUTION show P1:docs/reviews/slices.json
git -C DISTRIBUTION show P1:docs/reviews/inventory.json
git -C DISTRIBUTION show COORDINATOR:PATH
git -C ES ls-tree -rz IMMUTABLE_REF
git -C ES diff-tree -r --numstat -z --no-renames 4b825dc642cb6eb9a060e54bf8d69288fbee4904 SURVEY -- PATHS
git -C ES show SURVEY:PATH
```

Full repository paths, refs, glob semantics, CODE set and exact path lists are literal in `derive.py`/manifests. Supplemental reads used `git show` on the named CMake/test files; their hashes are in results. Coordinator recipe SHA256: `1d91f4a72032c67b89c0d986d26b728cf501f11bb9de891c168eb4f3f37d2719`. Live reads were GitHub connector issue/body/all-comment calls for #691 and #700; captures are retained here.

| Private artifact | SHA256 |
| --- | --- |
| paths.txt — sorted ES-relative 594 keys | 1478e929343f7b2e82aaa3972573809ca8c0ad9e0eb4d5973fb1ec0542d9e345 |
| object-identities.tsv — mode/type/OID/path | 7d11ea3f6a06d5e00e4c7ddade1b5878391daeb6cdbcb2118bcd206add7be16e |
| manifest.json — per-path identity/lines/tier/groups | 16b1da3ad4a7e4b3c7a6aadbd901c2502c940d20da697136babc27474d767965 |
| results.json | 20dfb1e3e3209e69dd30f8598ae13697f6c4d6445fdbc7665be520a13b17f070 |
| derive.py | 8a78e3fb55d5bde069a0158016ca7227ca9d26a67a54525d100cbbcefdec0f38 |

Unresolved factual inputs for the eventual brief are T2's accepted later ES/catalogue/import-version handoff and root's chosen execution baseline. This report does not prove vendor currency, original-import equivalence, translation completeness, installed reach or runtime behavior. It does not fetch/expand the pugixml gitlink. All source/record subprocesses used CPUs8–23. Only small private metadata/text scratch was written; no source payload export, repository/ledger/tracker/kit edit, configuration execution, producer replay, runtime/provider/device/cloud/host-ledger action or permission answer. Historical worktrees are untouched. Return complete; no T44 execution dispatched or undertaken.
