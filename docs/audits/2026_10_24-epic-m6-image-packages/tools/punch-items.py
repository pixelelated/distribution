#!/usr/bin/env python3
"""05-punch-list.md from one list (#655): the items, the punch_index and the Phase 7 table.
    python3 -I punch-items.py > 05-punch-list.md
"""
VMNO = "No: a fetch property of a recipe, proved on the host (brief § 5; nothing here runs on an image)"
VMT = "No: the tree, the record and the release sources (brief § 5)"
AWF = "nothing on devices or in clouds: a recipe's source is a build input; the shared cache's file and stamp, and ROCKNIX's mirror, are the retained copies (D-INFRA-022)"
AWN = "nothing: a recipe's text or a record; no device or cloud holds anything of it"
AWM = "nothing until the merge: the base merge decides what the next image builds; this item is its pre-read, and changes nothing on a device"
I = [
 dict(f="F-01", t="`simple-http-server`'s `x86_64` and `arm` branches carry no `PKG_SHA256`; T5's fetch refuses it on GENERIC_X64", sev="Medium", cat="Interaction Defect", q="Q3", area="an upstream-carried recipe: `projects/ROCKNIX/packages/network/simple-http-server`", tracked="#890",
  what="The coordinator filed #890 and fixed it in the packet `fix/m6-890-shs-sha256` (the T1 session), ordered ahead of T5's branch; D-WORKFLOW-197 records the seventh archive version. This slice touches nothing.",
  where="`projects/ROCKNIX/packages/network/simple-http-server/package.mk:12-23`", ev="P5, P9; `02` § The fetch sweep", vm=VMNO,
  aw="nothing on devices or in clouds: every GENERIC_X64 build fetched the x86_64 binary unverified; the cache's file and its stamp, and today's download, are `a16d73db...` (no mirror copy)",
  acc="#890's packet tip carries the x86_64 checksum `a16d73db...`; `config/options simple-http-server` for GENERIC_X64 prints it.", upstream=True),
 dict(f="F-02", t="`virtual/image` writes the Entware symlink under `${INSTALL}` at global scope, on every sourcing of the recipe", sev="Medium", cat="Code Quality", q="Q3", area="the image's recipe: `projects/ROCKNIX/packages/virtual/image`", tracked="#852",
  what="Move `mkdir -p ${INSTALL}; ln -sf /storage/.opt ${INSTALL}/opt` into a function the build runs at install time, keeping `PKG_DEPENDS_TARGET+=\" entware\"` at global scope; this slice's stream (brief § 7).",
  where="`projects/ROCKNIX/packages/virtual/image/package.mk:109-110`", ev="P10 (T6's `pkgcheck`), P12 (this worktree's three `image/system/opt` symlinks)", vm="Yes: the image's root carries `opt -> /storage/.opt` after the fix (`fix-pending-image`); the load-time write is proved gone on the host by sourcing a fresh export",
  aw="nothing on devices: the image's `/opt -> /storage/.opt` is the intended result and stays; what the load-time write left behind is `build.*/image/system/opt` in build roots and in any worktree that sourced the recipe, which the next image build overwrites with the same link",
  acc="a fresh export sourced through `config/options image` for GENERIC_X64 leaves no `build.*/image/system/opt`; `tools/pkgcheck image` with T6's copy exits 0; the first image built from the fix carries `/opt -> /storage/.opt`.", upstream=True),
 dict(f="F-03", tracked="#891", t="`libaio`'s `PKG_URL` is gone (pagure's archive answers 404); every fetch depends on ROCKNIX's mirror", sev="Low", cat="Code Quality", q="Q3", area="an upstream-carried recipe: `projects/ROCKNIX/packages/devel/libaio`",
  what="Record it; propose a live URL for 0.3.113 to #585 when one is found (upstream carries the same URL). The mirror and the cache are the retained copies.",
  where="`projects/ROCKNIX/packages/devel/libaio/package.mk:10`", ev="P8, P9", vm=VMNO, aw=AWF,
  acc="a fetch of `libaio` for GENERIC_X64 into an empty source directory exits 0 with `716c7059...` (from the mirror today).", bug=True, upstream=True),
 dict(f="F-04", tracked="#892", t="`rocknix-abl`'s `PKG_URL` is gone (`ROCKNIX/abl` answers 404); every fetch depends on ROCKNIX's mirror", sev="Low", cat="Code Quality", q="Q3", area="an orphan recipe: `projects/ROCKNIX/packages/tools/rocknix-abl` (SM8550)",
  what="The base merge removes the orphan and SM8550's payload comes from `openabl` (`71d8932b33`); until then the mirror and the cache are the copies.",
  where="`projects/ROCKNIX/packages/tools/rocknix-abl/package.mk:8`", ev="P8, P9, P15", vm=VMNO, aw=AWF,
  acc="a fetch of `rocknix-abl` for SM8550 into an empty source directory exits 0 with `64034fb0...` (from the mirror today); after the base merge the recipe is gone and SM8550 builds `openabl`.", bug=True),
 dict(f="F-05", t="`cairo` 1.18.4, the fork's own pin, is behind its project's 1.18.6", sev="Low", cat="Renovation", q="Q4", area="a fork-edited recipe: `projects/ROCKNIX/packages/graphics/cairo`",
  what="The fork's: a Backlog issue in #839's shape, filed by the coordinator, for the first build after the M7 candidate; no pin moves in M6. The base merge conflicts on this recipe (F-09), so the bump is read with the merge.",
  where="`projects/ROCKNIX/packages/graphics/cairo/package.mk` `PKG_VERSION`", ev="P7", vm=VMT, aw=AWN,
  acc="the Backlog issue exists in #839's shape, citing this item.", defer="a Backlog issue (#839's shape)"),
 dict(f="F-06", t="`tools/fork-package-freshness` cannot see 17 of the 19 recipes the fork edited, reads a command-substituted `PKG_VERSION` as LOCAL and a `case`-branch override as INHERITED", sev="Low", cat="Renovation", q="Q4", area="a fork tool: `tools/fork-package-freshness`",
  what="A lead for #657: the set is `git diff --diff-filter=A` plus `EXTRA_PACKAGES`, so a recipe the fork edited and upstream still carries (and the fork may have re-pinned: `cairo`, `spirv-tools`, `rocknix-splash`) is never checked; `var()` greps `^PKG_VERSION=` at column 0, so `libfmt`'s override in a `case` reads INHERITED; `var()` reads `$(get_pkg_version rust)` as a literal and the verdict falls to LOCAL (`cargo`, `cargo-snapshot`, `rust-std-snapshot`, `rustc-snapshot`).",
  where="`tools/fork-package-freshness` `packages()`, `var()`", ev="P7", vm=VMT, aw=AWN,
  acc="#657 carries the lead with this item's text.", defer="#657"),
 dict(f="F-07", t="six recipes pin a git source with a short hash", sev="Low", cat="Renovation", q="Q2", area="upstream-carried recipes: `SDL2_gfx`, `glfw`, `libsndfile`, `pyudev`, `six`, `soundfont-generaluser`",
  what="`packaging-and-patches.md`: pin a git source with the full commit hash; the six are upstream's (#585 candidates).",
  where="the six recipes' `PKG_VERSION` lines (`hashpins.txt`)", ev="P7", vm=VMT, aw=AWN,
  acc="#585's proposal names the six with their full hashes.", upstream=True),
 dict(f="F-08", t="`tools/pkgcheck`'s duplicate-function check fails a function defined in the two arms of an `if` (`moonlight`)", sev="Low", cat="Renovation", q="Q2", area="a tool: `tools/pkgcheck`",
  what="A lead for #657 beside its heredoc-parser case (`wireplumber`): the duplicate check greps the whole file, so `moonlight`'s two `post_makeinstall_target()` in `if`/`else` read as one recipe defining it twice.",
  where="`tools/pkgcheck:166-169`; `projects/ROCKNIX/packages/apps/moonlight/package.mk:12-45`", ev="P10", vm=VMT, aw=AWN,
  acc="#657 carries the lead with this item's text.", defer="#657"),
 dict(f="F-09", t="the base merge conflicts on 9 of this slice's paths; `gcc`'s 15.2.0 hold carries no reason in its recipe", sev="Low", cat="Renovation", q="Q7", area="the integration: the next merge of `upstream/next`",
  what="The conflict list (`02` § The conflict set, `04` § Q4) is the merge's pre-read: each path with `merge-tree`'s verdict and a disposition; read at integration, the coordinator's.",
  where="`02` § The conflict set", ev="P4", vm=VMT, aw=AWM,
  acc="the coordinator records the list as read at the base merge (its resolution commit names the eleven).", defer="the integration (the coordinator's)"),
 dict(f="F-10", t="`xorg-configure@.service` and `97-xorg.rules` ship in every image; the script the unit runs is in none", sev="Low", cat="Renovation", q="Q6", area="an upstream-carried recipe: `projects/ROCKNIX/packages/x11/xserver/xwayland`",
  what="The unit's `ExecStart=/usr/lib/xorg/xorg-configure` comes from the generic `xorg-server` recipe, which these images do not build; the rule wants the unit on a PCI VGA-class display (`i915`, `amdgpu`, `radeon`, `vmwgfx`, `virtio-pci`). The QA guest's `virtio-gpu-pci` is `0x038000` and never matches; GENERIC_X64 installed on x86 hardware with an Intel or AMD display does (narrowed by the second opinion). A #585 candidate: install the script, or drop the unit and the rule.",
  where="`x11/xserver/xwayland/system.d/xorg-configure@.service:8`; `udev.d/97-xorg.rules:13-17`", ev="P13", vm="Yes, partly: a guest with a `virtio-vga` display (class `0x030000`) would pull the unit in and show it failed in `systemctl --failed`; not run here", aw=AWN,
  acc="#585's proposal names the unit, the rule and the absent script.", upstream=True),
 dict(f="F-11", t="the base merge's `glslang` modify/delete would downgrade it to 16.5.0 under a `spirv-tools` pinned to 16.6.0", sev="Medium", cat="Interaction Defect", q="Q4", area="the integration: `graphics/glslang` and `graphics/spirv-tools`",
  what="Settled by D-WORKFLOW-198 (the coordinator's, `152c4ee3c3` on `feature/m6-renovation-plan-346`): at the base merge the fork's `glslang` override is kept (16.6.0, coupled to `spirv-tools`' `known_good.json`), and the set later moves together in a Backlog bump the coordinator files. `merge-tree` leaves ours in the tree; the second opinion found `spirv-headers`' override a third modify/delete in the same set (outside this slice's 485, and `unreached` in the inventory although `spirv-tools` unpacks it), so the set is a triple; reported for the row.",
  where="`projects/ROCKNIX/packages/graphics/glslang/package.mk`; `graphics/spirv-tools/package.mk`; `upstream/next:packages/graphics/vulkan/glslang/package.mk`", ev="P4, P15", vm=VMT, aw=AWM,
  acc="the base merge's resolution commit keeps the fork's `glslang` override (D-WORKFLOW-198), so `glslang`'s effective pin and `spirv-tools`' `known_good.json` name the same release; the pair's bump is a Backlog issue in #839's shape.", defer="the integration, by D-WORKFLOW-198 (the coordinator's)"),
 dict(f="F-12", t="11 orphans: nine the base merge drops and two left as modify/delete conflicts, with five pin changes and `rocknix-abl` to `openabl`", sev="Low", cat="Renovation", q="Q1", area="the integration: the 11 orphan overrides",
  what="The orphan table (`04` § Q4) is the merge's pre-read: `opus` 1.5.2 → 1.6.1, `libfmt` 9.1.0 → 12.2.0 on GENERIC_X64 and H700, `vulkan-headers` 1.4.347 → 1.4.359, `mtdev` and `swaybg` a patch each, `glslang` (F-11), `rocknix-abl` → `openabl`; no dependant breaks by name.",
  where="`04` § Q4's orphan table", ev="P2, P15", vm=VMT, aw=AWM,
  acc="the coordinator records the table as read at the base merge.", defer="the integration (the coordinator's)"),
 dict(f="F-13", tracked="#893", t="`mangohud` downloads ImGui, ImPlot and spdlog at configure with `curl -L` and no checksum", sev="Medium", cat="Code Quality", q="Q3", area="an upstream-carried recipe: `projects/ROCKNIX/packages/apps/mangohud` (SM8550)",
  what="Bring the three in as sources the build verifies (the fork's own shape for the two Vulkan subprojects: a source package each, hash-checked at download, `50f3eeb726`), or as `PKG_URL`-fetched archives; until then an empty-cache or offline build of SM8550 depends on three unverified downloads that neither `get_archive`, ROCKNIX's mirror nor T5's guard covers (`device-builds.md` § A build that fetches its own dependency). ROCKNIX's lines (`01520aff68`): rule 6, and a #585 candidate.",
  where="`projects/ROCKNIX/packages/apps/mangohud/package.mk:66-91`", ev="the second opinion's G-15, read at its site; `git log -S`", vm="Yes, in part: a build with the network cut fails at `pre_configure_target`; the fixture for the fix is a grep of the recipe for `curl` and a hash check of each source; no build runs in M6",
  aw="nothing on devices: every SM8550 image built mangohud from whatever the three URLs served at that build; none is recorded, so nothing built is known to differ from the tags",
  acc="`grep -c 'curl ' projects/ROCKNIX/packages/apps/mangohud/package.mk` prints 0, and each of the three sources is fetched with a `PKG_SHA256`.", bug=True, upstream=True),
 dict(f="F-14", tracked="#894", t="the installer runs `dd`, `parted`, `mkfs.vfat` and `mount` unchecked and reports Install Complete whatever happened", sev="Medium", cat="Code Quality", q="Q3", area="an upstream-carried script (fork-own by its identity edits): `projects/ROCKNIX/packages/tools/installer/scripts/installer` (GENERIC_X64)",
  what="Check each destructive step and end on failure with what did not happen (`engineering-practices.md` § Fail gracefully; § Guards must fail closed); the second opinion's G-02 to G-06 (the text match on mount sources, `PARTID` never reset, 512-byte sectors, the boot-config order, the helper's cleanup) are leads for the same stream, read before it. Upstream's logic: rule 6, and a #585 candidate.",
  where="`installer:207`, `:280`, `:303`, `:374`", ev="the second opinion's G-01, read at its sites", vm="Yes: a GENERIC_X64 guest with a second virtual disk, the target made to fail (a read-only or detached disk), and the screen read for the message",
  aw="nothing on devices that kept their install: a past install that failed and said it completed left a half-written disk its owner has since reinstalled or noticed; nothing the fix reads",
  acc="on a GENERIC_X64 guest, an install whose `mkfs.vfat` or `mount` fails ends on a failure message, not Install Complete (a frame or the serial log); `bash -n` passes.", bug=True, upstream=True),
 dict(f="F-15", t="`get_archive`'s cache hit trusts the stamp without hashing the file", sev="Low", cat="Renovation", q="Q3", area="the build engine: `scripts/get_archive` (T5's slice)",
  what="A lead for #844 (the fetch check): a scheduled check hashes the cached file against its stamp and its recipe; `get_archive` itself is T5's, accepted, and upstream's logic (a #585 candidate).",
  where="`scripts/get_archive:4-11` at the hash; `52e6794ba7:scripts/get_archive:11-18`", ev="the second opinion's G-20, read at its site", vm=VMT, aw=AWN,
  acc="#844 carries the lead with this item's text.", defer="#844"),
 dict(f="F-16", t="`simple-http-server.service` passes the root password unquoted, and in the process's arguments", sev="Low", cat="Security", q="Q3", area="an upstream-carried unit: `projects/ROCKNIX/packages/network/simple-http-server`",
  what="Quote the substitution, and pass the credential some way other than the command line (a file the server reads, if it supports one); upstream's unit (a #585 candidate). The service runs only when its user turns it on.",
  where="`network/simple-http-server/system.d/simple-http-server.service:7`", ev="the second opinion's G-22, read at its site", vm="Yes: on a GENERIC_X64 guest with the service on, `ps -o args` shows the password (read through the filter's masking `sed`)",
  aw="nothing written: a password with a space never authenticated; the argument is not stored",
  acc="#585's proposal names the line.", upstream=True),
 dict(f="F-17", t="eight small shapes the second opinion found: card digit, topology branches, `After=` without `Wants=`, a shared cache name, a flag rewrite, a parser, a doubled scancode", sev="Low", cat="Renovation", q="Q2", area="scripts, a unit, recipes and a config (`04` § Second opinion G-09 to G-14, G-17, G-21, G-23, G-24)",
  what="Upstream's (`111-sway-init`'s lines, `glibc`, `wlr-randr`, the H700 `m8c` config): #585 candidates or the base merge. The fork's three (`avahi-daemon.service`'s ordering, `tailscale`'s cache name, the GENERIC_X64 `m8c` copy): the coordinator's call for a stream.",
  where="`04` § Second opinion", ev="each read at its site in § Second opinion", vm=VMT, aw=AWN,
  acc="each of the eight is named in #585's proposal or in a stream brief, with its verdict.", upstream=True),
 dict(f="F-18", tracked="#899", t="without a game controller the installer starts copies of itself without end, and a copy's Close runs `poweroff -f`", sev="Medium", cat="Interaction Defect", q="Q3", area="an upstream-carried script (fork-own by its identity edits): `projects/ROCKNIX/packages/tools/installer/scripts/installer` (GENERIC_X64)",
  what="Found on S3's guest cycle and added to S3 by the coordinator (13:51 UTC on #655). `control-gen` prints nothing without a pad, so `control.ini` is empty, `GPTOKEYB` is unset, and the gptokeyb line runs `installer -c ...` in the background. Guard the line on `GPTOKEYB` being set. Upstream carries the same lines (`09810c3ece`): rule 6, and a #585 row, the coordinator's.",
  where="`installer:43-47`", ev="P18: 153 to 381 copies in a minute on the guest; one with the guard", vm="Yes: the GENERIC_X64 guest has no game controller, so a plain run reproduces it; a stub `poweroff` keeps the failing control's guest up",
  aw="nothing inherited: each start rewrites `control.ini` and `installer.gptk`, and the guard reads them as before; no format changes",
  acc="on the guest with no pad, one installer process at MAIN MENU; with a pad-shaped `control.ini`, `gptokeyb` is run once with `installer -c .../installer.gptk`; `bash -n` and busybox `sh -n` pass.", bug=True, upstream=True),
 dict(f="F-19", tracked="#901", t="the installer copies the media's `syslinux.cfg` over the one it generated, so an installed GENERIC_X64 boots on the live media's cmdline", sev="Low", cat="Interaction Defect", q="Q3", area="an upstream-carried script (fork-own by its identity edits): `projects/ROCKNIX/packages/tools/installer/scripts/installer` (GENERIC_X64)",
  what="The second opinion's G-05, confirmed from the installed bytes in S3 and filed by the coordinator as #901 (S4). Write the `x86_64` boot configuration after `cp -r /flash/*`. Graded Low: the installed disk boots either way, on the same two labels, because `portable` only sets `SYSLINUX_DEFAULT=run` (`busybox/scripts/init:1245-1246`), which `:777-785` uses to keep `DEFAULT run` in a `syslinux.cfg` that has that label; the file and the cmdline are wrong, not the boot (both disks boot to the carousel on the guest). The reorder exposes the recipe's dead `@EXTRA_CMDLINE@` substitution: the script reads a run-time `${EXTRA_CMDLINE}` nothing sets, so the reorder alone would have cost `quiet` and the serial console (the first S4 install's disk booted with no answer on serial); S4 also turns the moved line's `${EXTRA_CMDLINE}` into `@EXTRA_CMDLINE@`, at the coordinator's yes (14:35 UTC on #655). Upstream's lines (`09810c3ece`): rule 6, and a #585 row, the coordinator's.",
  where="`installer:321-339` at `8ebaf8daad`; `tools/installer/package.mk` `post_install`", ev="P20: S3's installed `syslinux.cfg` and the control boot's `/proc/cmdline` (`portable`); S4's installs and boots", vm="Yes: a quick install on the GENERIC_X64 guest to a blank SATA disk, the target's `syslinux.cfg` read, and the installed disk booted alone through an overlay",
  aw="every GENERIC_X64 disk installed so far carries the media's `syslinux.cfg` and boots with `portable`; the fix changes the next install, and a reinstall rewrites the file; nothing under `/storage` or in a cloud",
  acc="after a quick install on the guest, the target's `syslinux.cfg` is the generated one (`DEFAULT linux`, the two labels, no `portable`), and the media's `/flash/syslinux.cfg` is unchanged; `bash -n` and busybox `sh -n` pass.", bug=True, upstream=True),
]

P7 = {   # (outcome, evidence, proved) by F; filled at Phase 7
 "F-01": ("Resolved", "#890, filed by the coordinator (D-WORKFLOW-197); fixed in the packet `fix/m6-890-shs-sha256` ahead of T5's branch", "fix-tree"),
 "F-14": ("Resolved", "`467f19fc14`: each step in the gauge ends it on failure, and the dialog names the step; G-03 fixed with it; G-02, G-04 to G-06 are #585 rows (`02` § S3's leads)", "fix-guest"),
 "F-18": ("Resolved", "`0602f598e9`: the gptokeyb line runs only when `GPTOKEYB` is set (#899, added to S3 by the coordinator)", "fix-guest"),
 "F-02": ('Resolved', "`43f6a81070`, T8's S1: the link is made in `post_install()` with `ln -sfn`; sourcing a fresh export leaves no `image/system/opt` (P16); `pkgcheck image` rc 0 at `d797678ede`. The image's `/opt -> /storage/.opt` is #852's `fix-pending-image` criterion", 'fix-tree'),
 "F-03": ('Deferred', "deferred:#585, item 4 of #585's T8 proposal ([issuecomment-6384909664](https://github.com/pixelelated/distribution/issues/585#issuecomment-6384909664), 13:40 UTC; the installer addendum [issuecomment-6385022026](https://github.com/pixelelated/distribution/issues/585#issuecomment-6385022026), 13:51); #891 stays open, Low, mirror-covered, with #844 the guard", ''),
 "F-04": ('Deferred', "deferred:#585, item 4 of #585's T8 proposal ([issuecomment-6384909664](https://github.com/pixelelated/distribution/issues/585#issuecomment-6384909664), 13:40 UTC; the installer addendum [issuecomment-6385022026](https://github.com/pixelelated/distribution/issues/585#issuecomment-6385022026), 13:51); #892 stays open, Low, mirror-covered; `openabl` is read at the integration (conflict row 10) before any deletion", ''),
 "F-05": ('Deferred', "deferred:#896 (the coordinator's Backlog); no pin moves in M6; read with the merge's conflict row 2", ''),
 "F-06": ('Deferred', "deferred:#657, the coordinator's T10 rows ([issuecomment-6384909901](https://github.com/pixelelated/distribution/issues/657#issuecomment-6384909901), 13:40 UTC)", ''),
 "F-07": ('Deferred', "deferred:#585, item 5 of #585's T8 proposal ([issuecomment-6384909664](https://github.com/pixelelated/distribution/issues/585#issuecomment-6384909664), 13:40 UTC; the installer addendum [issuecomment-6385022026](https://github.com/pixelelated/distribution/issues/585#issuecomment-6385022026), 13:51), with the six full hashes resolved through the GitHub API", ''),
 "F-08": ('Deferred', "deferred:#657, the same comment's second row, with `moonlight` as the failing control", ''),
 "F-09": ('Deferred', "deferred:the integration's pre-read, the coordinator's at #655's merge (the disposition in `t8-streams.md` at `7c4867330b`): `02` § The conflict set, 11 rows; nothing on this branch", ''),
 "F-10": ('Deferred', "deferred:#585, item 6 of #585's T8 proposal ([issuecomment-6384909664](https://github.com/pixelelated/distribution/issues/585#issuecomment-6384909664), 13:40 UTC; the installer addendum [issuecomment-6385022026](https://github.com/pixelelated/distribution/issues/585#issuecomment-6385022026), 13:51)", ''),
 "F-12": ('Deferred', "deferred:the integration's pre-read, the coordinator's at #655's merge (the disposition in `t8-streams.md` at `7c4867330b`): `04`'s orphan table, 11 rows; nothing on this branch", ''),
 "F-13": ('Resolved', "`4db09f6e2e` (the three source recipes, each `PKG_SHA256` its wrap's `source_hash`) and `1904e29d54` (`mangohud` unpacks them from `${SOURCES}`), T8's S2: `scripts/get` fetches them and refuses a one-digit change; the real hook unpacks them and stops on a missing one (P17); `pkgcheck` rc 0 on all four at `d797678ede`; no `curl` left", 'fix-tree'),
 "F-15": ('Deferred', "deferred:#844, the coordinator's lead ([issuecomment-6384910123](https://github.com/pixelelated/distribution/issues/844#issuecomment-6384910123), 13:40 UTC)", ''),
 "F-16": ('Deferred', "deferred:#585, item 7 of #585's T8 proposal ([issuecomment-6384909664](https://github.com/pixelelated/distribution/issues/585#issuecomment-6384909664), 13:40 UTC; the installer addendum [issuecomment-6385022026](https://github.com/pixelelated/distribution/issues/585#issuecomment-6385022026), 13:51)", ''),
 "F-17": ('Deferred', "deferred:#585, items 8 to 11 and the tailscale shape of #585's T8 proposal ([issuecomment-6384909664](https://github.com/pixelelated/distribution/issues/585#issuecomment-6384909664), 13:40 UTC; the installer addendum [issuecomment-6385022026](https://github.com/pixelelated/distribution/issues/585#issuecomment-6385022026), 13:51). The fork's three: G-14 withdrawn (`network-base.service` is enabled by `systemd/package.mk:328`, so `After=` alone orders it); G-17 a #585 row, its one-line `PKG_SOURCE_NAME` free to ride the integration; G-24 a #585 row, the fork's GENERIC_X64 copy following upstream's fix", ''),
 "F-19": ("Resolved", "`b58489297c`, T8's S4: the `x86_64` boot configuration is written after `cp -r /flash/*`, and the `APPEND` line carries `@EXTRA_CMDLINE@` for `post_install`'s `sed`; the installed disk booted alone reads `/proc/cmdline` `... disk=LABEL=STORAGE quiet console=ttyS0,115200 console=tty0` without `portable` (P20); the token mismatch is a #585 row, the coordinator's", "fix-guest"),
 "F-11": ("Deferred", "deferred:the integration, settled by D-WORKFLOW-198 (`152c4ee3c3`): the fork's glslang override is kept at the base merge; the pair's bump is the coordinator's Backlog", ""),
}

def main():
  out = ["# Punch List — M6.P2 T8, the image's own packages (projects/ROCKNIX)", "",
         "**Independent depth** (D-WORKFLOW-184): one GPT-6 Astra seat, graded in `04` § Second opinion. Every `where` is at `8ebaf8daad`. The audit issue is #895 (a sub-issue of #655). Generated by `tools/punch-items.py` from one list, so the items, the `punch_index` and the Phase 7 table agree.", "", "---", ""]
  idx = ["```yaml", "punch_index:"]
  gate = ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
  for n, x in enumerate(I, 1):
      pl = f"PL-{n:02d}"
      out += [f"## {pl}: {x['t']}", "", f"- **Severity:** {x['sev']}", f"- **Category:** {x['cat']}", f"- **Question:** {x['q']}", f"- **Source Finding:** {x['f']}", f"- **Owner area:** {x['area']}", f"- **What:** {x['what']}", f"- **Where:** {x['where']}", f"- **Evidence:** {x['ev']}", f"- **Can this be done on the VM?** {x['vm']}", f"- **Already written:** {x['aw']}", f"- **Acceptance:** {x['acc']}"]
      if x.get("bug") or x.get("tracked"): out.append(f"- **Bug issue:** {x.get('tracked', 'filed at stage D')}")
      if x.get("upstream"): out.append("- **Upstream:** a #585 candidate (D-WORKFLOW-164; submission deferred, D-WORKFLOW-165); the coordinator posts it")
      if x.get("defer"): out.append(f"- **Disposition note:** deferred to {x['defer']} at Phase 7")
      out.append("")
      idx += [f"- id: {pl}", f"  severity: {x['sev']}", f"  category: {x['cat']}", f"  question: {x['q']}", f"  source_finding: \"{x['f']}\"", f"  owner_area: \"{x['area'].replace(chr(34), chr(39))}\""]
      if x.get("bug") or x.get("tracked"): idx.append(f"  tracked: \"{x.get('tracked', 'bug issue filed at stage D')}\"")
      p7 = P7.get(x["f"])
      if p7:
          idx.append(f"  outcome: \"{p7[0].lower()}\"")
          if p7[2]: idx.append(f"  proved: \"{p7[2]}\"")
          gate.append(f"| {pl} | **{p7[0]}** | {p7[1]}{'; ' + p7[2] if p7[2] else ''} |")
      else:
          idx.append("  outcome: open")
          gate.append(f"| {pl} | Open | stage D files the issue; a stage-E stream brief or the named issue resolves |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
    main()
