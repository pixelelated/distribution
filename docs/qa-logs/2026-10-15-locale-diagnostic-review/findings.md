# Finite locale diagnostic review — source and completed evidence only

The SM05 diagnostic excerpt exactly matches established completed GENERIC and H700 build diagnostics. No new SM locale defect is demonstrated. This review does not claim that every current SM locale category has been read or validated; no active SM cache or output was opened.

## Exact diagnostic comparison

Root's retained active-console prefix observation is `sm-prefix/observation.json`: 1,595,299 observed bytes, prefix SHA256 `dd80f8e79ddf5ab44f3df177c9739274ed91283279b45f7602c6cab1f8419a4e`. Its selected excerpt SHA256 is `0952587447ab69e8037961a39380e84cd2b2f510de950b7978432ecc945407cc`; this is a prefix observation, not a final run result.

All 88 locale diagnostic rows match the two completed originals below after removing only the device/build path before `translit_emojis:`: 70 syntax-error rows at lines 18–87, followed by the same 18 verbose table rows, including the exact enormous unsigned values. `comparison-{0,1,2}.json` records zero differences. No warning text or numeric value was normalized away.

| Completed original | Full log SHA256 | Locale lines |
| --- | --- | --- |
| `/workspace/tmp/pix-m7-h700-refresh-20261015-02/console.log` | `e74790b0b795fb60bd6acb8c8811d7d0312bd851dd55d656d581f9e82a445889` | 20951–21039 (88 selected rows) |
| `/workspace/tmp/pix-m7-engineering-build-20261015-02/console.log` | `b3f510a58d6639ebcd963bd6ab3684967c69a3057712fc814cb3319de307c170` | 2709–2797 (88 selected rows) |
| GENERIC watcher `20261015T035405Z-403ed573/build.log` | `cb6110019de79bd1c27e00e531d0a65fbd2167cedf36a6143463783baf7fe84b` | 2708–2796 (88 selected rows) |

The H700 combined producer's later failure remains original1; independent H700 artifact acceptance `e8107b4bffac81fa72dd127a45ec1b6b7455518829f04c143690ec60687813db` qualified its outputs. The GENERIC producer's #597 launcher-reporting collision and unknown final launcher wait remain explicit; successful original build stages, separate artifact readback, and installed VM results qualified its output. This comparison does not relabel either historical producer as an unqualified success0.

## Resolved recipe and runtime consumer

`config/functions` prefers project/device package recipes to generic packages. The resolved recipe is `projects/ROCKNIX/packages/devel/glibc/package.mk`, `PKG_VERSION="2.41"`, source SHA256 `a5a26b22f545d6b7d7b3dd828e11e428f24f4fac43c934fb071b6a7d0828e901`. Generic `packages/devel/glibc` 2.44 is not the resolved recipe. Frozen f863 and 9aa7 use identical locale recipes and startup script; their only product difference is the separate ABL checksum correction.

The ES package invokes unqualified `localedef --force --verbose --inputfile=en_US --charmap=UTF-8` with `I18NPATH` pointing to the resolved target glibc locale sources and output `/usr/config/locale/en_US.UTF-8`; `|| true` discards that command's failure as a package-install result. `config/path` prepends toolchain bin/sbin to PATH. These records do not independently identify the exact executable resolved by that unqualified command, so compiler-version mismatch is a hypothesis, not a finding. The unchanged pregeneration block originated in commit `96d387fffd1ff90a450fdada2b2ac5d3026b5d93` to reduce first-boot work on lower-end devices.

The installed `es_settings` only checks whether `LC_NAME` exists before skipping generation. ES16dbac `LocaleES.cpp:36–37` assigns `setlocale(LC_CTYPE, "")` and then overwrites its result with `setlocale(LC_MESSAGES, "")`. Consequently install completion, existence of LC_NAME, and an English UI frame alone are not a complete LC_CTYPE validity oracle. This is a source limitation, not evidence of a newly failing locale.

## What #566 actually proved

The original French generation returned1 with nine optional-field warnings in LC_NAME, LC_ADDRESS, and LC_IDENTIFICATION, plus absurd verbose LC_CTYPE sizes. It had **no** translit_emojis syntax error. Its sealed adapter permits only those exact warning lines and verbose LC_CTYPE lines, then requires all 12 nonempty category files and an actual `locale.setlocale(locale.LC_ALL, "")` readback. The retained French readback is `fr_FR.UTF-8`, original0. Thus the strange verbose sizes alone have already coexisted with a successfully loaded locale, but that warning allowance does not authorize ignoring arbitrary syntax errors.

There is also direct English evidence: `accepted-1280/guest-originals.tar.gz::guest/pix566/cases/en_US/locale-readback.{stdout,stderr,exit.json}` records `en_US.UTF-8`, empty stderr, original0. The exact sealed `source05/guest/guest-case.py` first copies installed `/usr/config/locale`, then generates a locale only if LC_NAME is absent. The complete English archive has no `localedef.*` execution records, so its English readback used the pregenerated image locale. Actual EN640 attempt04 independently has the same readback.

That locale came from the earlier replacement20 GENERIC image, **not** the later f863 image:

- Image locator: `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261011T194522Z.g1a0266484423-from-ROCKNIX.img.gz`.
- Original image SHA256: `1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490`, compressed bytes 2,073,682,425.
- Durable original locator: `docs/qa-logs/2026-10-14-screenscraper-ui-runtime/accepted-1280/original-records.tar.gz::owner/records/image-size.json`; member SHA256 `33419eb48e80d3b5f728711713c65ea9eb23d740879aac229f30429afcce0fb2`.
- Installed locale root for comparison: `/usr/config/locale/en_US.UTF-8/`. The fixture copied this into `/storage/.config/locale/en_US.UTF-8/`; its frontend locale symlink resolves there.
- The exact glibc recipe, full es_settings script, and pregeneration block are byte-identical from image source1a0266484423 to f863, recorded in `566-reference-source-comparison.json`. This source equality is not a fabricated category-byte equality.

The retained #566 records provide per-category hashes for the generated **French** locale, not the pregenerated **English** locale. No English per-category hash manifest was found in those selected accepted records; none is invented here. `input-image.json` refers to the separate 268 MiB fixture disk and must not be mistaken for the OS image identity above.

## Optional stopped-artifact comparison

No new build, VM probe, issue, audit gate, or runtime allocation follows from this review. If root wants to settle exact current-output equivalence alongside the already planned stopped-artifact extraction, the minimal additional data are type, size, and SHA256 for these 12 paths from the completed SM SYSTEM and the identified load-proven GENERIC image (and, optionally, the already accepted f863/H700 artifacts):

```text
/usr/config/locale/en_US.UTF-8/LC_CTYPE
/usr/config/locale/en_US.UTF-8/LC_NUMERIC
/usr/config/locale/en_US.UTF-8/LC_TIME
/usr/config/locale/en_US.UTF-8/LC_COLLATE
/usr/config/locale/en_US.UTF-8/LC_MONETARY
/usr/config/locale/en_US.UTF-8/LC_MESSAGES/SYS_LC_MESSAGES
/usr/config/locale/en_US.UTF-8/LC_PAPER
/usr/config/locale/en_US.UTF-8/LC_NAME
/usr/config/locale/en_US.UTF-8/LC_ADDRESS
/usr/config/locale/en_US.UTF-8/LC_TELEPHONE
/usr/config/locale/en_US.UTF-8/LC_MEASUREMENT
/usr/config/locale/en_US.UTF-8/LC_IDENTIFICATION
```

Exact equality would support a narrow unchanged-data statement tied to the earlier loading proof; it would not prove every transliteration mapping or native ARM runtime behavior. A mismatch is evidence to interpret, not an automatic failure: locale source/compiler/input identity must be compared before inferring regression. This note supplies no new executable reader or test framework and has not read those firmware payloads.
