export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t41; S=/workspace/cache/rocknix-sources; U=/workspace/repos/pixelelated/distribution
P=.qa-scratch/t41/paths.txt   # the 107, from the P1 run of the block (saved under $T/stage-a-p1 too)
# the tool's own row (R1 C14 ran it from the clone: rc=0, 50 lines, `unassigned: 0`, `ambiguous: 0`, the T41 row) [unverified from the worktree]
git status --short --ignored | $G -c ''
./tools/renovation-inventory --order --no-write --distribution "$W" > "$T/tmp/order.out" 2>&1; rc=$?
echo "renovation-inventory --order rc=$rc lines=$($G -c '' "$T/tmp/order.out")"; $G -E '^(slices|rows|unassigned|ambiguous):|^ *41 patches-shipped-kernel ' "$T/tmp/order.out"
git status --short --ignored | $G -c ''                                      # the same count as before the run (R1 C14: 2 in the clone)
# the recipe's pins and patch directories as text, never sourced (R1 C06; v1 read): the case labels, PKG_VERSION, PKG_SHA256 and PKG_PATCH_DIRS lines
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | $G -n -E '^\s*(PKG_VERSION|PKG_SHA256|PKG_PATCH_DIRS)[+]?=|^\s*[A-Z0-9|]+\)\s*$' | cut -c1-120   # :16 PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"; :29-31 the 7.2 group with f9fef3d1...; :36-38 RK3326|AMD64|GENERIC_X64 7.1.2 with 37198c93...; :40 PKG_PATCH_DIRS+=" 7.0"
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | sed -n '33,34p'   # the recipe's own comment on the 7.2 directory (R2 § 0)
for d in H700 SM8550 GENERIC_X64; do git show "HEAD:projects/ROCKNIX/devices/$d/options" | $G -n -E 'LINUX=|KERNEL_TARGET|TARGET_KERNEL_PATCH_ARCH' | sed "s/^/$d:/"; done   # no LINUX= (R1 C08); KERNEL_TARGET Image, Image, bzImage (R1 C06); GENERIC_X64:10 TARGET_KERNEL_PATCH_ARCH="x86_64" (R3 C5)
git show HEAD:config/arch.arm | sed -n 80p                                   # TARGET_KERNEL_PATCH_ARCH="aarch64" (R3 C5)
git show HEAD:scripts/unpack | sed -n '127,159p'                             # the PATCH_ARCH rule and the globs' order (R1 C05; v1 read of :127-133)
# the nine directories' counts and the three plans' application order (v1 read at 2174265e9c: GENERIC_X64 4+4 total 8; H700 4+6+32 total 42; SM8550 4+6+55 total 65), files sorted under LC_ALL=C as the container's shell globs
order() { case "$1" in GENERIC_X64) dirs="projects/ROCKNIX/packages/linux/patches/mainline projects/ROCKNIX/packages/linux/patches/7.0";; H700|SM8550) dirs="projects/ROCKNIX/packages/linux/patches/mainline projects/ROCKNIX/packages/linux/patches/7.2 projects/ROCKNIX/devices/$1/patches/linux";; esac; for d in $dirs; do git ls-tree -r --name-only HEAD -- "$d" | $G -E '\.patch$' | sort; done; }
for dev in GENERIC_X64 H700 SM8550; do order "$dev" > "$T/order-$dev.txt"; echo "$dev total: $($G -c '' "$T/order-$dev.txt")"; done
for d in 7.0 7.2 mainline; do echo "$d: $(git ls-tree -r --name-only HEAD -- projects/ROCKNIX/packages/linux/patches/$d | $G -c -E '\.patch$')"; done   # 4, 6, 4 (R1 C13)
for d in H700 SM8550; do echo "$d: $(git ls-tree -r --name-only HEAD -- projects/ROCKNIX/devices/$d/patches/linux | $G -c -E '\.patch$') patches, $(git ls-tree -r --name-only HEAD -- projects/ROCKNIX/devices/$d/patches/linux | $G -c '\.disabled$') disabled"; done   # 32 and 1; 55 and 1 (R1 C13)
for d in H700 SM8550 GENERIC_X64 default aarch64 x86 7.1.2; do git cat-file -e "HEAD:projects/ROCKNIX/packages/linux/patches/$d" 2>/dev/null || echo "absent patches/$d"; done   # seven `absent` (R1 C13; R3 § 0): the words of PKG_PATCH_DIRS and the arch/version forms that select nothing
# the header census (R1 C13: From: 87, Subject: 89; R2 § 1: 17 hand-made)
n=0; f=0; s=0; while IFS= read -r p; do case "$p" in *.patch) n=$((n+1)); h=$(git show "HEAD:$p" | head -n 60); printf '%s\n' "$h" | $G -q -E '^From: ' && f=$((f+1)); printf '%s\n' "$h" | $G -q -E '^Subject: ' && s=$((s+1));; esac; done < "$P"; echo "patches $n with From: $f with Subject: $s"
while IFS= read -r p; do case "$p" in *.patch) git show "HEAD:$p" | $G -n -m1 -E '^(Link:|Upstream-Status:)' | sed "s#^#$p:#";; esac; done < "$P" | cut -c1-160   # 4 lines: H700 0160, SM8550 0006, 7.2/0011, 7.2/0016 (R2 § 1; v1 read)
# byte identity against the merge base and upstream (R1 C07: SAME 106, ADDED 1; R1 C11: SAME 101, CHANGED 4, GONE 2)
for B in c445081a59 651150fc88; do while IFS= read -r p; do if git -C "$U" cat-file -e "$B:$p" 2>/dev/null; then [ "$(git -C "$U" rev-parse "$B:$p")" = "$(git rev-parse "HEAD:$p")" ] && echo "vs $B SAME" || echo "vs $B CHANGED"; else echo "vs $B ABSENT"; fi; done < "$P" | sort | uniq -c; done
# upstream's changes under the shipped kernel directories since the base (R1 C11: 12 A, 1 D, 4 M) and the five files of the 107 it touched (R1 C11's name-status)
KD="projects/ROCKNIX/packages/linux/patches projects/ROCKNIX/devices/H700/patches/linux projects/ROCKNIX/devices/SM8550/patches/linux projects/ROCKNIX/devices/SM8550/linux"
git -C "$U" diff --name-status c445081a59 651150fc88 -- $KD | awk '{print $1}' | sort | uniq -c
git -C "$U" diff --name-status c445081a59 651150fc88 -- $KD | $G -E '^[DM]' | cut -c1-140
git -C "$U" diff --name-status c445081a59 651150fc88 -- $KD | $G -E '^A' | cut -c1-140
tr '\n' '\0' < "$P" | xargs -0 git -C "$U" diff --shortstat c445081a59 651150fc88 --   # ` 5 files changed, 36 insertions(+), 515 deletions(-)` (R1 C11)
tr '\n' '\0' < "$P" | xargs -0 git -C "$U" log --format='%h %cs %s' c445081a59..651150fc88 -- | cut -c1-120   # 8 lines, 7 non-merge (R1 C11)
git -C "$U" diff --stat 2174265e9c 651150fc88 -- projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch projects/ROCKNIX/packages/linux/patches/7.0/0010-msm-resource-cleanup.patch | tail -n 1   # ` 2 files changed, 28 insertions(+), 22 deletions(-)` [unverified]: v1 read of the 7.2 copy alone printed ` 1 file changed, 14 insertions(+), 11 deletions(-)`
git -C "$U" show 651150fc88:projects/ROCKNIX/packages/linux/package.mk | sed -n '16,20p;26,53p' | cut -c1-120   # upstream's :18 rocknix-joypad line with its quoted =~ (R2 L-02); the pins: 7.2 unchanged for the H700 group, 7.1.2 for RK3326|AMD64 (GENERIC_X64 absent), 7.2.11 with 7.2.6 for RK3566|RK3576|S922X, 6.18.54 for RK3399 (R1 C16; R2 § 4)
for n in RK3326 RK3399 S922X H700 SM8550; do [[ "$n" =~ "RK3326|RK3399|S922X|H700" ]] && echo "$n quoted-match" || echo "$n no-match"; done   # five `no-match` (R2 command 14): L-02
git -C "$U" ls-tree -r --name-only 651150fc88 | $G -c -F 'rocknix-joypad/'   # the group's directory anywhere at 651150fc88: 0 under the override's patches (R1 § 10); the whole-tree count [unverified]
# the fork's side: its commits on the 107 and on the recipes (R1 C10: 6, one non-merge; the two recipe hunks)
tr '\n' '\0' < "$P" | xargs -0 git log --format='%h %cs %an %s' c445081a59..HEAD -- | cut -c1-120   # 6 lines at 2174265e9c; the coordinator's branch may add merges [unverified]
tr '\n' '\0' < "$P" | xargs -0 git log --no-merges --format='%h %cs %an %s' c445081a59..HEAD -- | cut -c1-120   # 1 line: cbf75c0b06 2026-09-10
git log --no-merges --format='%h %cs %s' c445081a59..HEAD -- projects/ROCKNIX/packages/linux/package.mk packages/linux/package.mk | cut -c1-120   # dc948f59aa 2026-08-21 and 3d7c075f63 2026-10-02 (R1 C16)
git diff --shortstat c445081a59 HEAD -- projects/ROCKNIX/packages/linux/package.mk packages/linux/package.mk   # ` 2 files changed, 5 insertions(+), 5 deletions(-)` (R1 C10)
tr '\n' '\0' < "$P" | xargs -0 git log --oneline --since=2026-06-01 HEAD -- | $G -c ''   # 64 at 8ebaf8daad (R5 C15); the tip's line is the record
# the duplicate pairs (R2 command 10: all identical) and the duplicate detector's three strictnesses (the generator)
for f in 0010-msm-resource-cleanup.patch 9998-silence-initramfs-unpack-warn.patch 9999-fix-rust-build-error.patch; do cmp <(git show "HEAD:projects/ROCKNIX/packages/linux/patches/7.0/$f") <(git show "HEAD:projects/ROCKNIX/packages/linux/patches/7.2/$f") && echo "identical 7.0/7.2 $f"; done
for f in 0001-Update-dram_sun50i_h616.c.patch 0002-sunxi-axp717-charge-only-boot.patch; do cmp <(git show "HEAD:projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches/$f") <(git show "HEAD:projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches/$f") && echo "identical DDR3/DDR4 $f"; done
# the symlink question (R3 § 1.5; R5 § G (e); v1 read: 3 entries under the roofs at P1, all ALSA ucm .conf under RK3566's and SM8750's filesystem overlays, none a patches directory)
git ls-tree -r HEAD | awk '$1=="120000"{print $4}' | $G -E '^(projects/ROCKNIX/(devices|packages/linux)|packages/linux)'
# the ramoops patch (ruling (e); R1 C10, C11; R2 command 8)
R=projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch
git log --format='%h %cs %an %s' HEAD -- "$R" | cut -c1-120                 # cbf75c0b06 2026-09-10 Max Engel Handhelds keep their evidence ...
git show "HEAD:$R" | $G -c ''; git show "HEAD:$R" | sed -n '1,2p;29,35p'   # 38; the From:/Subject: and the node
git -C "$U" merge-base --is-ancestor cbf75c0b06 651150fc88 && echo in-upstream || echo not-in-upstream   # not-in-upstream
git -C "$U" ls-tree -r --name-only 651150fc88 projects/ROCKNIX/devices/H700/patches/linux | $G -c -i ramoops   # 0 (R1 C11)
git -C "$U" show 651150fc88:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf | $G -n -E 'CONFIG_PSTORE_RAM'   # `# CONFIG_PSTORE_RAM is not set` (R2 command 8)
git show HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf | $G -n -E '^CONFIG_(PSTORE_RAM|PSTORE_CONSOLE|WATCHDOG_SYSFS|SOFTLOCKUP_DETECTOR|DETECT_HUNG_TASK|DEFAULT_HUNG_TASK_TIMEOUT)='   # the six lines of cbf75c0b06 in T27's conf (R2 command 8: :7290, :7292 among them)
# the SM8550 configuration (rulings (d), (j)): the four conf-diff counts, each naming its side
C=projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf
git show "HEAD:$C" | sed -n 3p                                                # `# Linux/arm64 7.2.0 Kernel Configuration` (R2 § 0)
git diff --numstat c445081a59 HEAD -- "$C" | $G -c ''                        # 0: the fork never changed it (R2 command 9)
git -C "$U" diff --numstat 2174265e9c 651150fc88 -- "$C"                  # `7	7	...` (R2 command 9; T28 02:78-90)
git -C "$U" diff 2174265e9c 651150fc88 -- "$C" | $G -E '^[-+]CONFIG|^[-+]# CONFIG' | cut -c1-100   # the 14 lines (R2 command 11)
diff <(git show "HEAD:$C" | sort) <(git show HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf | sort) | $G -c '^[<>]'   # (a) against H700's conf, same 7.2 and arch [unverified]
tar -xJf "$S/linux/linux-7.2.tar.xz" -C "$T/src" linux-7.2/arch/arm64/configs/defconfig; rc=$?
echo "defconfig extract rc=$rc"
diff <(git show "HEAD:$C" | $G -v '^#' | sort) <($G -v '^#' "$T/src/linux-7.2/arch/arm64/configs/defconfig" | sort) | $G -c '^[<>]'   # (b) against the kernel's own arm64 defconfig [unverified]
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | sed -n '146,335p' | $G -o -E 'CONFIG_[A-Z0-9_]+' | sort -u > "$T/tmp/forced.txt"; $G -c '' "$T/tmp/forced.txt"   # (c) the symbols pre_make_target sets or disables (R3 § 1.1) [unverified count]
while IFS= read -r k; do printf '%s %s\n' "$k" "$(git show "HEAD:$C" | $G -c -E "^(# )?$k[= ]")"; done < "$T/tmp/forced.txt"   # whether the conf already names each
git -C "$U" show 651150fc88:$C | sed -n 3p                                # (d) upstream's header line, the same 7.2.0 [unverified]
# the tarballs (ruling (g)): each hash against its .sha256 and the recipe's PKG_SHA256 as text
for v in 7.2 7.1.2; do a=$(cut -c1-64 "$S/linux/linux-$v.tar.xz.sha256"); b=$(sha256sum "$S/linux/linux-$v.tar.xz" | cut -c1-64); [ "$a" = "$b" ] && echo "linux-$v.tar.xz = its .sha256 ($(printf '%.16s' "$a"))" || echo "linux-$v.tar.xz MISMATCH"; done   # f9fef3d14c0df538 and 37198c93727be247, the recipe's PKG_SHA256 prefixes (v1 read)
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | $G -n -E '^\s*PKG_SHA256=' | cut -c1-60   # :31 f9fef3d1..., :38 37198c93... among the five
ls "$S/u-boot-DDR3" "$S/u-boot-DDR4" "$S/kernel-firmware"                     # u-boot-DDR3-v2026.01.tar.gz, u-boot-DDR4-v2026.01.tar.gz, kernel-firmware-20260309.tar.gz with .sha256 and .url (v1 read); the non-kernel rows' sources, L-12
# the removal rule's own check (ruling (c); D-WORKFLOW-209): expect no line at any stage
git diff --stat d7dd766659 HEAD -- '*.patch' '*.conf' packages projects tools scripts | tail -n 1
git log --no-merges --format=%h d7dd766659..HEAD -- '*.patch' '*.conf' packages projects tools scripts | $G -c ''   # 0
# the registers take the procedure's appends only: expect 0 removed lines
git diff d7dd766659 HEAD -- docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | $G -c -E '^-([^-]|$)'
# the checkers' baseline at the dispatch tip (their lines move with the dispatch's own commits, so each line that prints is recorded beside the research's)
tools/rules-check > "$T/tmp/rules-check.out" 2>&1; rc=$?
echo "rules-check rc=$rc"; tail -n 1 "$T/tmp/rules-check.out"               # rc=0 (T39's R3 C13: 30 rule files) -- no evidence for the 107
tools/register-check > "$T/tmp/register-check.out" 2>&1; rc=$?
echo "register-check rc=$rc"; tail -n 1 "$T/tmp/register-check.out"         # rc=0; `register-check: 715 IDs, each once; ...` at 6a12ce2d73 (v1 read); the dispatch's own row moves the count
tools/work-log-index --check > "$T/tmp/index.out" 2>&1; rc=$?
echo "work-log-index rc=$rc"; tail -n 1 "$T/tmp/index.out"
tools/ceremony-check > "$T/tmp/ceremony-check.out" 2>&1; rc=$?
echo "ceremony-check rc=$rc"; tail -n 1 "$T/tmp/ceremony-check.out"         # `nothing overdue.` rc 0 at 6a12ce2d73 (R5 § I); the dispatch tip's line is the record
tools/box-check > "$T/tmp/box-check.out" 2>&1; rc=$?
echo "box-check rc=$rc"; tail -n 1 "$T/tmp/box-check.out"                   # R5 § I: `300 issue(s), 695 open checkbox(es), 0 fail` at the research's read [unverified at the tip]
.githooks/hooks-test > "$T/tmp/hooks-test.out" 2>&1; rc=$?
echo "hooks-test rc=$rc"; tail -n 1 "$T/tmp/hooks-test.out"                 # [unverified]: no research file for this brief ran it
# the issues read at stage A (states recorded; a quoted line through the mask)
gh --repo pixelelated/distribution issue view 688 --json title,state,body --jq '.title, .state, (.body | split("\n") | length)'   # the title, OPEN, and the body's line count after the coordinator's fill (27 before it, R5 C14)
for n in 328 369 104 44 1056 1049 1086 1084 563 559 585; do printf '#%s %s\n' "$n" "$(gh --repo pixelelated/distribution issue view "$n" --json state,title --jq '.state + " " + .title' | cut -c1-110)"; done
