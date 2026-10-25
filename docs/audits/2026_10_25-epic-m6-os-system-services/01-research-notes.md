# T22 research notes: the OS's system services and platform quirks (#669)

Research for M6.P2 T22 (`os-system-services`), from the brief at `cc8b6cf2a3`.
The 422 paths are read at `8ebaf8daad`'s bytes and compared with upstream
`next` at `651150fc88`. Each figure carries the command that produced it,
run in the worktree on 2026-10-25. The raw outputs are in
`.qa-scratch/t22/runs/`, which is gitignored and re-made by the commands.

## Scope

### The membership (the brief's § 2 block, at `2174265e9c`)

The brief's block, run as written. The run also printed the config files'
count and saved the rows to `.qa-scratch/t22/rows.json`:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
INC=[rx("projects/ROCKNIX/packages/sysutils/**"), rx("projects/ROCKNIX/packages/hardware/**")]; EXC=rx("projects/ROCKNIX/packages/hardware/quirks/devices/**")
t=[r for r in rows if r["area"]=="os-scripts-and-launch" and r["reach"]=="shipped" and any(p.match(r["path"]) for p in INC) and not EXC.match(r["path"])]
READ={"shell","recipe","systemd","udev","c"}   # the survey counts these five as read; the dictionary below has no python or make
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ),"fork-own read",sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ and r["tier"]=="fork-own"),"fork-own paths",sum(1 for r in t if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("language",dict(collections.Counter((r.get("language") or "none") for r in t)))
g=collections.Counter("/".join(r["path"].split("/")[3:5]) for r in t); print("groups",dict(g.most_common(6)))
import os; os.makedirs(".qa-scratch/t22", exist_ok=True)
open(".qa-scratch/t22/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t22/paths.txt")'
```

Output (rc 0, wall .507550636s):

```
paths 422 lines 16604
read 10898 fork-own read 3002 fork-own paths 24
tier {'upstream-carried': 398, 'fork-own': 24} reach {'shipped': 422}
language {'shell': 299, 'recipe': 28, 'other': 7, 'none': 21, 'symlink': 2, 'systemd': 29, 'config': 30, 'c': 1, 'udev': 5}
groups {'hardware/quirks': 275, 'sysutils/systemd': 41, 'sysutils/busybox': 36, 'sysutils/system-utils': 28, 'sysutils/autostart': 5, 'sysutils/sleep': 4}
config files 30 lines 4487
written 422 .qa-scratch/t22/paths.txt
```

Every figure matches § 2: **422 paths, 16,604 lines; read 10,898, fork-own read
3,002 over 24 paths; tier 398 upstream-carried / 24 fork-own; reach shipped
422; written 422.**

### The language dictionary, and what is read though not counted

| Language | Paths | Counted as read |
| --- | ---: | --- |
| shell | 299 | yes |
| recipe | 28 | yes |
| systemd | 29 | yes |
| udev | 5 | yes |
| c | 1 (`evtest.c`) | yes |
| config | 30 (4,487 lines) | **no, read anyway** (the security lens) |
| other | 7 | no |
| none | 21 | no (binary or empty) |
| symlink | 2 | no (the target is read) |

**The 30 `config` files are read though not counted:** the three busybox
configurations (`busybox-init.conf` 1,224, `busybox-target.conf` 1,224,
`busybox-host.conf` 1,200 = **3,648**), `udevil.conf` 331, `modprobe.d/aliases.conf` 172,
`umtprd.conf` 100, `httpd.conf` 46, the sysctls (`hang-policy.conf`,
`99-coredump.conf`, `memory.conf`, `cdrom.conf`, `sysctl.d/rocknix.conf`,
`99-rocknix-networking.conf`), the tmpfiles, and the systemd drop-ins
(`.qa-scratch/t22/runs/21-fork-own-and-config.out` lists all 30).

### The fork-own 24 (3,002 read lines), with each path's last fork commit

```
hardware/quirks/platforms/GENERIC_X64/090-ui_service 8 shell 73b20caf86
hardware/quirks/platforms/GENERIC_X64/091-ui_shader 8 shell 73b20caf86
hardware/quirks/platforms/GENERIC_X64/092-retroarch-surface 113 shell 0b451e6c8e
hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh 76 shell 4e0078cc44
hardware/quirks/platforms/GENERIC_X64/097-retired-rescue-masks 40 shell 518aeffca5
hardware/quirks/profile.d/999-export 73 shell 7d64713537
sysutils/busybox/scripts/init 1383 shell bed8e2bb1e
sysutils/busybox/sysctl.d/99-coredump.conf 4 config 20e04cc2b8
sysutils/busybox/sysctl.d/hang-policy.conf 17 config cbf75c0b06
sysutils/busybox/system.d/storage-log.service 12 systemd cbf75c0b06
sysutils/busybox/system.d/var-log.mount 23 systemd cbf75c0b06
sysutils/nvtop/package.mk 33 recipe 6675159628
sysutils/powerstate/sources/powerstate.sh 80 shell 8d2f384d1c
sysutils/powerstate/system.d/powerstate.service 21 systemd 79729ba204
sysutils/system-utils/sources/devices/GENERIC_X64/video_sense 20 shell 73b20caf86
sysutils/system-utils/sources/scripts/input_sense 539 shell f4c5e0c91d
sysutils/systemd/config/sysctl.d/rocknix.conf 3 config d0a8fd4203
sysutils/systemd/config/system.conf.d/20-watchdog.conf 13 config cbf75c0b06
sysutils/systemd/package.mk 333 recipe 754df5cfc1
sysutils/systemd/scripts/network-base-setup 129 shell 9d71a829fe
sysutils/systemd/scripts/userconfig-setup 90 shell efb8aec861
sysutils/systemd/system.d/network-base.service 21 systemd af9295025a
sysutils/systemd/system.d/systemd-pstore.service.d/rocknix.conf 8 config cbf75c0b06
sysutils/systemd/tmpfiles.d/z_01_rocknix.conf 12 config cbf75c0b06
```

### The two selection mechanisms

**Install time (`system-utils`):**

```bash
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/package.mk | sed -n '10,36p' | cat -n | sed -E 's/^ *([0-9]+)/\1+9/' | awk -F'\t' '{split($1,a,"+"); printf "%d: %s\n", a[1]+a[2], $2}'
```

Output (rc 0, wall .006015298s):

```
10: PKG_TOOLCHAIN="manual"
11: 
12: makeinstall_target() {
13: 
14:   mkdir -p ${INSTALL}/usr/lib/autostart/common
15:   cp ${PKG_DIR}/sources/autostart/common/* ${INSTALL}/usr/lib/autostart/common
16: 
17:   mkdir -p ${INSTALL}/usr/bin
18:   cp ${PKG_DIR}/sources/scripts/fancontrol ${INSTALL}/usr/bin
19:   cp ${PKG_DIR}/sources/scripts/headphone_sense ${INSTALL}/usr/bin
20:   cp ${PKG_DIR}/sources/scripts/output_monitor ${INSTALL}/usr/bin
21:   cp ${PKG_DIR}/sources/scripts/hdmi_sense ${INSTALL}/usr/bin
22:   cp ${PKG_DIR}/sources/scripts/input_sense ${INSTALL}/usr/bin
23:   cp ${PKG_DIR}/sources/scripts/ledcontrol ${INSTALL}/usr/bin
24:   cp ${PKG_DIR}/sources/scripts/analog_sticks_ledcontrol ${INSTALL}/usr/bin
25:   cp ${PKG_DIR}/sources/scripts/battery_led_status ${INSTALL}/usr/bin
26:   cp ${PKG_DIR}/sources/scripts/turbomode ${INSTALL}/usr/bin
27:   if [ -d "${PKG_DIR}/sources/devices/${DEVICE}" ]
28:   then
29:     cp ${PKG_DIR}/sources/devices/${DEVICE}/* ${INSTALL}/usr/bin
30:     if [ -d "${PKG_DIR}/sources/autostart/${DEVICE}" ]
31:     then
32:       mkdir -p ${INSTALL}/usr/lib/autostart/${DEVICE}
33:       cp ${PKG_DIR}/sources/autostart/${DEVICE}/* ${INSTALL}/usr/lib/autostart/${DEVICE}
34:       chmod 0755 ${INSTALL}/usr/lib/autostart/${DEVICE}/*
35:     fi
36:   fi
```

```bash
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/sysutils/system-utils/sources/devices projects/ROCKNIX/packages/sysutils/system-utils/sources/autostart | sed -E 's#.*/sources/(devices|autostart)/##' | cut -d/ -f1 | sort | uniq -c
```

Output (rc 0, wall .005688587s):

```
      3 AMD64
      1 common
      1 GENERIC_X64
      3 RK3399
      1 RK3566
      1 S922X
```

```bash
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/sysutils/system-utils/sources/devices | grep video_sense
```

Output (rc 0, wall .004392207s):

```
projects/ROCKNIX/packages/sysutils/system-utils/sources/devices/GENERIC_X64/video_sense
projects/ROCKNIX/packages/sysutils/system-utils/sources/devices/RK3399/video_sense
```

So `:14-15` installs `sources/autostart/common/*` on every build, and
`:27-36` installs only `sources/devices/${DEVICE}/*` and
`sources/autostart/${DEVICE}`. **8 rows are installed by no shipped image:**
AMD64's 3, RK3399's 3, RK3566's 1 and S922X's 1. GENERIC_X64 installs its
own `video_sense`; H700 and SM8550 have no device directory.

**Run time (the quirks):**

```bash
git show 8ebaf8daad:projects/ROCKNIX/packages/hardware/quirks/package.mk | grep -n -E 'cp |platforms|devices|DEVICE' | cut -c1-140
```

Output (rc 0, wall .004841908s):

```
14:  mkdir -p ${INSTALL}/usr/lib/autostart/quirks/{platforms,devices}
15:  cp -r ${PKG_DIR}/devices/* ${INSTALL}/usr/lib/autostart/quirks/devices
16:  if [ -d "${PKG_DIR}/platforms/${DEVICE}" ]
18:    cp -r ${PKG_DIR}/platforms/* ${INSTALL}/usr/lib/autostart/quirks/platforms
25:  if [ "${DEVICE}" = "RK3566" ]
```

```bash
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/hardware/quirks/platforms | cut -d/ -f7 | sort | uniq -c
```

Output (rc 0, wall .006696044s):

```
     18 AMD64
      5 GENERIC_X64
     22 H700
     12 RK3326
      8 RK3399
     16 RK3566
     13 RK3576
     12 RK3588
     10 S922X
     13 SM4450
     31 SM6115
     30 SM8250
     24 SM8550
     24 SM8650
     26 SM8750
```

264 platform files. The shipped three are **GENERIC_X64 5, H700 22 and
SM8550 24 = 51**, so **213 shipped files run on no shipped device.**

```bash
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart | grep -n -E 'HW_DEVICE|QUIRK_DEVICE|/storage/.config/autostart|-f |exec' | cut -c1-120; git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart | wc -l
```

Output (rc 0, wall .007214258s):

```
16:if [ -d "/usr/lib/autostart/quirks/platforms/${HW_DEVICE}" ]
18:  log "Run ${HW_DEVICE} quirks."
19:  tocon "Applying ${HW_DEVICE} quirks..."
20:  for script in "/usr/lib/autostart/quirks/platforms/${HW_DEVICE}"/*
23:    if [ -f "${script}" ]
31:if [ -d "/usr/lib/autostart/quirks/devices/${QUIRK_DEVICE}" ]
33:  log "Run ${QUIRK_DEVICE} quirks."
34:  tocon "Applying ${QUIRK_DEVICE} quirks..."
35:  for script in "/usr/lib/autostart/quirks/devices/${QUIRK_DEVICE}"/*
38:    if [ -f "${script}" ]
58:if [ -d "/usr/lib/autostart/${HW_DEVICE}" ]
60:  for script in "/usr/lib/autostart/${HW_DEVICE}"/*
63:    if [ -f "${script}" ]
71:if [ -d "/storage/.config/autostart" ]
73:  for script in /storage/.config/autostart/*
97
```

```bash
git grep -n QUIRK_DEVICE 8ebaf8daad -- projects/ROCKNIX/packages/sysutils | cut -c1-140
```

Output (rc 0, wall .008341134s):

```
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart:8:  export QUIRK_DEVICE="$(strings /sys/firmware/devicetree/
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart:10:  export QUIRK_DEVICE="$(strings /sys/class/dmi/id/sys_ve
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart:12:export QUIRK_DEVICE="$(echo ${QUIRK_DEVICE} | sed -e "s#[
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart:31:if [ -d "/usr/lib/autostart/quirks/devices/${QUIRK_DEVICE}" ]
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart:33:  log "Run ${QUIRK_DEVICE} quirks."
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart:34:  tocon "Applying ${QUIRK_DEVICE} quirks..."
8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart:35:  for script in "/usr/lib/autostart/quirks/devices/${QUIRK_DEVI
8ebaf8daad:projects/ROCKNIX/packages/sysutils/sleep/sources/sleep.sh:9:  QUIRK_DEVICE=$(tr -d '\0' </sys/firmware/devicetree/base/model 2>/d
8ebaf8daad:projects/ROCKNIX/packages/sysutils/sleep/sources/sleep.sh:11:QUIRK_DEVICE="$(echo ${QUIRK_DEVICE} | sed -e "s#[/]#-#g")"
8ebaf8daad:projects/ROCKNIX/packages/sysutils/sleep/sources/sleep.sh:45:                  /usr/lib/autostart/quirks/devices/"${QUIRK_DEVICE}
8ebaf8daad:projects/ROCKNIX/packages/sysutils/sleep/sources/sleep.sh:85:               /usr/lib/autostart/quirks/devices/"${QUIRK_DEVICE}"/s
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/analog_sticks_ledcontrol:10:if [ -z "${QUIRK_DEVICE}" ] || [ -z "
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/analog_sticks_ledcontrol:14:if [ -f "/usr/lib/autostart/quirks/de
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/analog_sticks_ledcontrol:15:  exec "/usr/lib/autostart/quirks/dev
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/battery_led_status:10:if [ -z "${QUIRK_DEVICE}" ] || [ -z "${HW_D
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/battery_led_status:14:if [ -f "/usr/lib/autostart/quirks/devices/
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/battery_led_status:15:  exec "/usr/lib/autostart/quirks/devices/$
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/fancontrol:10:if [ -z "${QUIRK_DEVICE}" ] || [ -z "${HW_DEVICE}" 
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/fancontrol:14:if [ -f "/usr/lib/autostart/quirks/devices/${QUIRK_
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/fancontrol:15:  exec "/usr/lib/autostart/quirks/devices/${QUIRK_D
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol:5:if [ -z "${QUIRK_DEVICE}" ] || [ -z "${HW_DEVICE}" ]
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol:14:if [ -f "/usr/lib/autostart/quirks/devices/${QUIRK_
8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol:15:  exec "/usr/lib/autostart/quirks/devices/${QUIRK_D
8ebaf8daad:projects/ROCKNIX/packages/sysutils/systemd/scripts/userconfig-setup:24:  if [ -d "/usr/lib/autostart/quirks/devices/${QUIRK_DEVIC
8ebaf8daad:projects/ROCKNIX/packages/sysutils/systemd/scripts/userconfig-setup:26:    rsync -a /usr/lib/autostart/quirks/devices/"${QUIRK_DE
```

### The units

```bash
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/sysutils projects/ROCKNIX/packages/hardware/quirks/system.d | grep -E '\.(service|timer|socket|target|mount|path)$' | tee "$TMPDIR/units.txt" | wc -l
```

Output (rc 0, wall .005117123s):

```
29
```

```bash
for u in $(cat "$TMPDIR/units.txt"); do printf '%s: User=%s Exec=%s\n' "$(basename "$u")" "$(git show "8ebaf8daad:$u" | grep -c '^User=')" "$(git show "8ebaf8daad:$u" | grep -m1 '^ExecStart' | cut -c1-70)"; done | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
```

Output (rc 0, wall .141961926s):

```
led-poweroff.service: User=*** Exec=ExecStart=/bin/true
volume-fixup.service: User=*** Exec=ExecStart=/usr/lib/autostart/quirks/platforms/RK3566/bin/volumealign
rocknix-autostart.service: User=*** Exec=ExecStart=/bin/bash -a -c 'source /etc/profile && exec /usr/bin/autost
cron-defaults.service: User=*** Exec=ExecStart=/bin/sh -c 'cp /usr/share/services/crond.conf /storage/.cach
cron.service: User=*** Exec=ExecStartPre=/bin/mkdir -p /storage/.cache/cron/crontabs
fs-resize.service: User=*** Exec=ExecStart=/usr/lib/rocknix/fs-resize
fs-resize.target: User=*** Exec=
proc-sys-fs-binfmt_misc.mount: User=*** Exec=
shell.service: User=*** Exec=ExecStartPre=/bin/sh -c 'echo -en "\033[?25h"'
show-version.service: User=*** Exec=ExecStart=/usr/bin/lsb_release
storage-log.service: User=*** Exec=ExecStart=/bin/mkdir -p /storage/.cache/log/journal /storage/.cache/lo
textmode.target: User=*** Exec=
var-log.mount: User=*** Exec=
var.mount: User=*** Exec=
powerstate.service: User=*** Exec=ExecStart=/usr/bin/powerstate
batteryledstatus.service: User=*** Exec=ExecStart=/usr/bin/battery_led_status
fancontrol.service: User=*** Exec=ExecStart=/usr/bin/fancontrol
headphones.service: User=*** Exec=ExecStart=/usr/bin/headphone_sense
input.service: User=*** Exec=ExecStart=/usr/bin/input_sense
video.service: User=*** Exec=ExecStart=/usr/bin/video_sense
debugconfig.service: User=*** Exec=ExecStart=/bin/sh -c 'cp /usr/share/debugconf/*.conf /run/rocknix/debu
machine-id.service: User=*** Exec=ExecStart=/usr/bin/systemd-machine-id-setup
network-base.service: User=*** Exec=ExecStart=/usr/sbin/network-base-setup
systemd-timesyncd-setup.service: User=*** Exec=ExecStart=/usr/sbin/systemd-timesyncd-setup
usercache.service: User=*** Exec=ExecStart=/usr/bin/usercache-setup
userconfig.service: User=*** Exec=ExecStart=/usr/bin/userconfig-setup
udevil-mount@.service: User=*** Exec=ExecStart=-/usr/bin/udevil --mount %I
fstrim.service: User=*** Exec=ExecStart=-/usr/sbin/fstrim --all --verbose --quiet-unsupported
fstrim.timer: User=*** Exec=
```

**Delta in the brief's command:** its mask (`user[=:]`, case-insensitive)
matches `User=` too, so every row reads `User=***` and the count is hidden.
Rerun with the mask on the `ExecStart` text only:

```bash
(the same loop; the mask applied to the ExecStart text only, since the brief's mask also matches "User=" and hid the count)
```

Output (rc 0, wall .236647201s):

```
led-poweroff.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/bin/true
volume-fixup.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/lib/autostart/quirks/platforms/RK3566/bin/volumealign
rocknix-autostart.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/bin/bash -a -c 'source /etc/profile && exec /usr/bin/autost
cron-defaults.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/bin/sh -c 'cp /usr/share/services/crond.conf /storage/.cach
cron.service: User/Group/DynamicUser lines=0 Exec=ExecStartPre=/bin/mkdir -p /storage/.cache/cron/crontabs
fs-resize.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/lib/rocknix/fs-resize
fs-resize.target: User/Group/DynamicUser lines=0 Exec=
proc-sys-fs-binfmt_misc.mount: User/Group/DynamicUser lines=0 Exec=
shell.service: User/Group/DynamicUser lines=0 Exec=ExecStartPre=/bin/sh -c 'echo -en "\033[?25h"'
show-version.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/lsb_release
storage-log.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/bin/mkdir -p /storage/.cache/log/journal /storage/.cache/lo
textmode.target: User/Group/DynamicUser lines=0 Exec=
var-log.mount: User/Group/DynamicUser lines=0 Exec=
var.mount: User/Group/DynamicUser lines=0 Exec=
powerstate.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/powerstate
batteryledstatus.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/battery_led_status
fancontrol.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/fancontrol
headphones.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/headphone_sense
input.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/input_sense
video.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/video_sense
debugconfig.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/bin/sh -c 'cp /usr/share/debugconf/*.conf /run/rocknix/debu
machine-id.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/systemd-machine-id-setup
network-base.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/sbin/network-base-setup
systemd-timesyncd-setup.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/sbin/systemd-timesyncd-setup
usercache.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/usercache-setup
userconfig.service: User/Group/DynamicUser lines=0 Exec=ExecStart=/usr/bin/userconfig-setup
udevil-mount@.service: User/Group/DynamicUser lines=0 Exec=ExecStart=-/usr/bin/udevil --mount %I
fstrim.service: User/Group/DynamicUser lines=0 Exec=ExecStart=-/usr/sbin/fstrim --all --verbose --quiet-unsupported
fstrim.timer: User/Group/DynamicUser lines=0 Exec=
units with any User=/Group=/DynamicUser=: 0 of 29
```

**0 of 29 units name a user or group: all run as root.** Who enables them:

```bash
git grep -n -E 'enable_service|preset' 8ebaf8daad -- projects packages config | grep -E 'video|headphones|input|fancontrol|batteryledstatus|rocknix-autostart|shell|cron|udevil|userconfig|powerstate'
```

Output (rc 0, wall .134693112s):

```
8ebaf8daad:packages/addons/service/nextpvr/source/resources/Language/resource.language.en_gb/strings.po:149:msgid "Choose video preset"
8ebaf8daad:packages/sysutils/busybox/package.mk:158:  enable_service shell.service
8ebaf8daad:packages/sysutils/busybox/package.mk:167:      enable_service cron.service
8ebaf8daad:packages/sysutils/busybox/package.mk:171:      enable_service cron-defaults.service
8ebaf8daad:packages/sysutils/lirc/package.mk:65:  enable_service lircd-uinput.service
8ebaf8daad:packages/sysutils/systemd/package.mk:315:  enable_service userconfig.service
8ebaf8daad:packages/sysutils/udevil/package.mk:40:  enable_service udevil-mount@.service
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/AMD64/retroarch.cfg:3485:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/GENERIC_X64/retroarch.cfg:819:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/H700/retroarch.cfg:783:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/RK3326/retroarch.cfg:788:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/RK3399/retroarch.cfg:792:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/RK3566/retroarch.cfg:788:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/RK3576/retroarch.cfg:788:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/RK3588/retroarch.cfg:788:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/emulators/libretro/retroarch/sources/S922X/retroarch.cfg:786:video_shader_preset_save_reference_enable = "true"
8ebaf8daad:projects/ROCKNIX/packages/rocknix/package.mk:85:  enable_service rocknix-autostart.service
8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/package.mk:187:  enable_service shell.service
8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/package.mk:196:      enable_service cron.service
8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/package.mk:200:      enable_service cron-defaults.service
8ebaf8daad:projects/ROCKNIX/packages/sysutils/powerstate/package.mk:20:  enable_service powerstate.service
8ebaf8daad:projects/ROCKNIX/packages/sysutils/systemd/package.mk:326:  enable_service userconfig.service
8ebaf8daad:projects/ROCKNIX/packages/sysutils/systemd/package.mk:332:  enable_service debug-shell.service
8ebaf8daad:projects/ROCKNIX/packages/tools/inputplumber/package.mk:48:  enable_service inputplumber.service
all enable_service|preset hits: 189
```

### busybox

```bash
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/package.mk | sed -n '5,12p'
```

Output (rc 0, wall .005724569s):

```

PKG_NAME="busybox"
PKG_VERSION="1.36.1"
PKG_SHA256="b8cc24c9574d809e7279c3be349795c5d5ceb6fdf19ca709f80cde50e47de314"
PKG_LICENSE="GPL"
PKG_SITE="http://www.busybox.net"
PKG_URL="http://busybox.net/downloads/${PKG_NAME}-${PKG_VERSION}.tar.bz2"
PKG_DEPENDS_HOST="gcc:host"
```

```bash
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/config/busybox-target.conf | grep -n -E '^CONFIG_(FEATURE_SUID|LOGIN|PASSWD|SU|HTTPD|FEATURE_HTTPD_CGI|NC|UDHCPD)=' | cut -c1-60
```

Output (rc 0, wall .004924458s):

```
30:CONFIG_FEATURE_SUID=y
549:CONFIG_LOGIN=y
554:CONFIG_PASSWD=y
556:CONFIG_SU=y
888:CONFIG_HTTPD=y
894:CONFIG_FEATURE_HTTPD_CGI=y
950:CONFIG_NC=y
1010:CONFIG_UDHCPD=y
```

### History since 2026-06-01 (the explicit midnight cutoff)

```bash
tr '\n' '\0' < .qa-scratch/t22/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- | tee "$TMPDIR/hist.txt" | wc -l; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"; echo "upstream: $(grep -v -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt")"; sort -u "$TMPDIR/hist.txt" | wc -l
```

Output (rc 0, wall .274971458s):

```
87
33
upstream: 54
87
```

**87** non-merge commits; **33** the fork's (`Max Engel|blitterbot|rasterabot`); **54** upstream's; 87 unique.

### The upstream delta, `8ebaf8daad` -> `651150fc88`

```bash
tr '\n' '\0' < .qa-scratch/t22/paths.txt | xargs -0 git diff --name-status 8ebaf8daad 651150fc88 -- | awk '{print $1}' | sort | uniq -c
```

Output (rc 0, wall .010825050s):

```
     20 D
     44 M
```

```bash
git diff --name-status 8ebaf8daad 651150fc88 -- projects/ROCKNIX/packages/sysutils projects/ROCKNIX/packages/hardware | grep -v 'quirks/devices/' | grep -E '^(A|R)' | cut -c1-130
```

Output (rc 0, wall .007791177s):

```
A	projects/ROCKNIX/packages/hardware/quirks/autostart/045-background-cpus
A	projects/ROCKNIX/packages/hardware/quirks/platforms/RK3576/021-sleep_mode
A	projects/ROCKNIX/packages/hardware/quirks/platforms/S922X/031-sleep_mode
A	projects/ROCKNIX/packages/hardware/quirks/platforms/SM4450/075-scanout-offload
A	projects/ROCKNIX/packages/hardware/quirks/platforms/SM6115/075-scanout-offload
A	projects/ROCKNIX/packages/hardware/quirks/platforms/SM8250/075-scanout-offload
A	projects/ROCKNIX/packages/hardware/quirks/platforms/SM8550/075-scanout-offload
A	projects/ROCKNIX/packages/hardware/quirks/platforms/SM8650/075-scanout-offload
A	projects/ROCKNIX/packages/hardware/quirks/platforms/SM8750/075-scanout-offload
A	projects/ROCKNIX/packages/hardware/quirks/system.d/duolite-bottom-screen.service
A	projects/ROCKNIX/packages/sysutils/busybox/patches/0001-halt-no-init.patch
A	projects/ROCKNIX/packages/sysutils/busybox/patches/0002-silence-crond-startup-logging.patch
A	projects/ROCKNIX/packages/sysutils/busybox/patches/0003-make-unicode-printable.patch
A	projects/ROCKNIX/packages/sysutils/busybox/patches/0004-revert-dd-fsync-change.patch
A	projects/ROCKNIX/packages/sysutils/busybox/patches/0005-update-shadow-or-passwd-not-both.patch
A	projects/ROCKNIX/packages/sysutils/busybox/patches/0006-prevent-root-weak-passwd.patch
R056	projects/ROCKNIX/packages/sysutils/busybox/patches/busybox-10-add-MS_BIND-option-when-remouting-bind-mount.patch	projects/ROC
A	projects/ROCKNIX/packages/sysutils/gptfdisk/patches/<gptfdisk's patch 0001; its name matches the commit scanner's key shape, so it is not written here: git diff --name-status 8ebaf8daad 651150fc88 -- projects/ROCKNIX/packages/sysutils/gptfdisk>
A	projects/ROCKNIX/packages/sysutils/ntfs-3g_ntfsprogs/package.mk
A	projects/ROCKNIX/packages/sysutils/systemd/config/system.conf.d/20-crash.conf
A	projects/ROCKNIX/packages/sysutils/systemd/oomd/rules.d/games-swap.oomrule
A	projects/ROCKNIX/packages/sysutils/systemd/scripts/hwdb-update-cached
A	projects/ROCKNIX/packages/sysutils/systemd/scripts/low-memory-tunables
A	projects/ROCKNIX/packages/sysutils/systemd/scripts/rtc-offset
A	projects/ROCKNIX/packages/sysutils/systemd/sysctl.d/60-rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/background.slice
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/debug-shell.service.d/rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/games.slice
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/rtc-offset-sync.path
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/rtc-offset-sync.service
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/rtc-offset.service
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/service.d/10-rocknix-thp.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/storage-timesync.service
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/system.slice.d/10-rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/systemd-hwdb-update.service.d/rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/systemd-rfkill.service.d/rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/systemd-timesyncd.service.d/rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/systemd-udev-trigger.service.d/rocknix.conf
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/udev-trigger-late.service
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/udev-trigger-late.timer
A	projects/ROCKNIX/packages/sysutils/systemd/system.d/var-lib-systemd-timesync.mount
A	projects/ROCKNIX/packages/sysutils/systemd/udev.d/61-rocknix-internal-emmc.rules
A	projects/ROCKNIX/packages/sysutils/util-linux/patches/0001-fix-pkgconf.patch
R073	projects/ROCKNIX/packages/sysutils/util-linux/patches/util-linux-02-enable-blkdiscard.patch	projects/ROCKNIX/packages/sysutil
```

**42 A and 2 R** under the globs, `quirks/devices/` excluded. The two R are
`busybox-10-add-MS_BIND-option-when-remouting-bind-mount.patch` (R056) and
`util-linux-02-enable-blkdiscard.patch` (R073).

```bash
the 20 D, each with its upstream history: in 8ebaf8daad, at the merge base c445081a59, and the commit that deleted it in c445081a59..651150fc88
```

Output (rc 0, wall .094597073s):

```
projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/090-ui_service | base-lacks | none
projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/091-ui_shader | base-lacks | none
projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/092-retroarch-surface | base-lacks | none
projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh | base-lacks | none
projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/097-retired-rescue-masks | base-lacks | none
projects/ROCKNIX/packages/hardware/quirks/platforms/RK3576/sleep.d/pre/99-idle-only | base-has | a98a3066f5 systemd: persist timesyncd clock and reboot on PI
projects/ROCKNIX/packages/hardware/quirks/platforms/SM6115/sleep.d/post/001-led | base-has | 6ac52e0c04 sm6115: add mangmi air y
projects/ROCKNIX/packages/hardware/quirks/platforms/SM6115/sleep.d/post/002-freq | base-has | 6ac52e0c04 sm6115: add mangmi air y
projects/ROCKNIX/packages/hardware/quirks/platforms/SM6115/sleep.d/pre/001-led | base-has | 6ac52e0c04 sm6115: add mangmi air y
projects/ROCKNIX/packages/hardware/quirks/platforms/SM6115/sleep.d/pre/002-freq | base-has | 6ac52e0c04 sm6115: add mangmi air y
projects/ROCKNIX/packages/sysutils/busybox/sysctl.d/99-coredump.conf | base-has | 8bce25b3b7 systemd: log crashes in the journal without writi
projects/ROCKNIX/packages/sysutils/busybox/sysctl.d/hang-policy.conf | base-lacks | none
projects/ROCKNIX/packages/sysutils/file/package.mk | base-has | 6103571f67 Merge pull request #3470 from sunshineinabox/WIP_
projects/ROCKNIX/packages/sysutils/i2c-tools/package.mk | base-has | 6103571f67 Merge pull request #3470 from sunshineinabox/WIP_
projects/ROCKNIX/packages/sysutils/system-utils/sources/devices/GENERIC_X64/video_sense | base-lacks | none
projects/ROCKNIX/packages/sysutils/systemd/config/sysctl.d/99-rocknix-networking.conf | base-has | 54acd9556f systemd: ship the distro sysctls in the image, dr
projects/ROCKNIX/packages/sysutils/systemd/config/sysctl.d/rocknix.conf | base-has | 54acd9556f systemd: ship the distro sysctls in the image, dr
projects/ROCKNIX/packages/sysutils/systemd/config/system.conf.d/20-watchdog.conf | base-lacks | none
projects/ROCKNIX/packages/sysutils/systemd/system.d/systemd-pstore.service.d/rocknix.conf | base-lacks | none
projects/ROCKNIX/packages/sysutils/systemd/udev.d/80-clock.rules | base-has | 899193e5af systemd: drop the hwclock udev rules, the kernel 
```

**The 20 D are 9 / 2 / 9:**
- **9 upstream never had:** absent at the merge base `c445081a59`. They are the five GENERIC_X64 quirks, `hang-policy.conf`, `GENERIC_X64/video_sense`, `20-watchdog.conf` and the `systemd-pstore` drop-in.
- **2 the fork carries and upstream removed:** `99-coredump.conf` (`8bce25b3b7`) and `sysctl.d/rocknix.conf` (`54acd9556f`).
- **9 upstream deleted:** RK3576 `99-idle-only`, the four SM6115 sleep hooks, the `file` and `i2c-tools` recipes, `99-rocknix-networking.conf` and `80-clock.rules`.

```bash
git log --oneline 8ebaf8daad..651150fc88 -- projects/ROCKNIX/packages/sysutils/busybox projects/ROCKNIX/packages/sysutils/systemd | head -12
```

Output (rc 0, wall .006450209s):

```
03204074ef Merge pull request #3475 from sunshineinabox/PR_ToolCompat
9883f84793 systemd: kill runaway games when swap is nearly full
f2379f83b7 systemd: only start the debug shell when debugging is on
75e2468cef systemd: never start the clock before the image build date
8bce25b3b7 systemd: log crashes in the journal without writing core files
401028b691 systemd: turn off LLMNR in resolved
83c72c6a47 systemd: keep the boot log with an 8 MB runtime journal
a5406be245 systemd: reboot 20 seconds after a kernel panic
e0bb050a07 systemd: raise the map count and inotify limits for Steam and Wine
f4e284524d systemd: stop forwarding IP traffic between interfaces
54acd9556f systemd: ship the distro sysctls in the image, drop dead keys
ed5aeaa34a systemd: keep the clock across reboots on RTCs that can't be set
```

### The routes and the removal rule

```bash
grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts
```

Output (rc 0, wall .003314121s):

```
scripts/council-invoke.ts:7
tools/lint-audit-artifacts:4
```

```bash
git diff --stat 4a48d388c4 HEAD -- packages projects tools | tail -1; echo "(empty above = nothing changed)"
```

Output (rc 0, wall .004306862s):

```
(empty above = nothing changed)
```

