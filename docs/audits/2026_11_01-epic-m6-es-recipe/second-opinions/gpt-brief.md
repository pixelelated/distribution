# T37 (#684): independent review of the EmulationStation recipe slice -- the refutation

You are the independent reviewer (one seat, another lab's model) for a read-only audit of 15 files in
a Linux distribution's build system: `projects/ROCKNIX/packages/ui/**` of the pixelelated fork of
ROCKNIX (LibreELEC-style `package.mk` recipes). The files are the EmulationStation recipe with its
config seeds, scripts, systemd units and autostart step; the `lowerdeck` recipe; and the
`es-theme-art-book-next` theme recipe with two source files. No build is run in this audit; the
lane read the files at the commit `2174265e9c`, the EmulationStation source at the pin
`16dbac5211`, computed the build plan and effective values in a scratch export, and read one VM
guest booted from the M7 candidate image (`069fc2704421`), whose ES recipe differs from the tip's.

Everything you need is in the packet below: the slice's code files whole (one line of the ES
recipe, `:39`, is withheld by line number: it is a local holding a shared developer credential's
value; `:40` uses it by reference), the cited ranges of the neighbouring sources, the lane's drafts
`02-forward-audit.md`, `03-retrospective.md`, `04-analysis.md` and `05-punch-list.md`, and the
brief's seven questions. Every source block is headed `=== SOURCE <name> (lines ...)` and every
line carries its number.

## What to do

1. **Grade each punch item PL-01 to PL-16** in `05-punch-list.md` against the packet's lines: one of
   **confirmed**, **confirmed with narrowing** (say what narrows), **refuted** (say which lines show
   it is wrong), or **cannot tell from the packet** (say what would settle it). Say whether the
   severity holds; if not, the severity you would give and why. Check the cited line numbers.
2. **Add what the lane missed**, as **G-1, G-2, ...**: a defect, a wrong claim in `02`/`04`, a
   sibling call site the lane did not hunt, a fix shape that would break something (for example a
   proposed recipe line that is wrong on some architecture or device). Each with its lines in the
   packet, a severity (Critical, High, Medium, Low) and the evidence.
3. **Challenge the proposed fixes**: PL-01's device path, PL-02's
   `[ "${ARCH}" = "x86_64" ] && PKG_PATCH_DIRS="x86_64"` against renaming the patch directory,
   PL-03's `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"`, PL-05's restored ARMSX2 block, PL-06's
   two options for fribidi. Say which you would choose and what each could break.
4. **Do not guess past the packet.** Where the answer depends on a file not sent, name the file and
   the lines you would need under **Sections I need** at the end; no second packet will be sent, so
   say what each would settle.

## The reply

Plain Markdown, no preamble:

- `## Grades` -- one entry per item: `- **PL-NN** -- <grade>; severity <holds | X>: <one to three
  sentences with line numbers>`.
- `## Added findings` -- `### G-N (<severity>): <title>` then the lines and the evidence.
- `## The fixes` -- one paragraph per fix named in step 3.
- `## Sections I need` -- or `none`.

Never reproduce a credential value, and do not speculate about what `:39` holds. Be terse and exact;
cite `source:line` for every claim.

## The packet


=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/package.mk (lines 1-141 of 141; the ES recipe, whole, :39 withheld)
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="emulationstation"
    5  PKG_VERSION="16dbac5211eea7e70db7394372033be2be7df829"
    6  PKG_GIT_CLONE_BRANCH="test/qa-integration"
    7  PKG_LICENSE="MIT AND BSD-3-Clause"
    8  PKG_SITE="https://github.com/pixelelated/emulationstation"
    9  PKG_URL="${PKG_SITE}.git"
   10  # noto-sans-cjk came from upstream 2026-09, and poppler with the PDF support
   11  # upstream's EmulationStation gained (e0e8b7ac33); the fork builds its own ES
   12  # from its own branch, so the clone form stays.
   13  PKG_DEPENDS_TARGET="boost toolchain SDL2 freetype curl freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool poppler pugixml noto-sans-cjk zstd ${OPENGLES}"
   14  PKG_NEED_UNPACK="busybox"
   15  PKG_LONGDESC="Emulationstation emulator frontend"
   16  PKG_BUILD_FLAGS="-gold"
   17  GET_HANDLER_SUPPORT="git"
   18  
   19  PKG_CMAKE_OPTS_TARGET+=" -DROCKNIX=1 \
   20                           -DDISABLE_KODI=1 \
   21                           -DENABLE_FILEMANAGER=0 \
   22                           -DCEC=0 \
   23                           -DENABLE_PULSE=1 \
   24                           -DUSE_SYSTEM_PUGIXML=1 \
   25                           -DGLES3=1"
   26  
   27  # #566 / D-WORKFLOW-166: provision the shared JELOS developer identity below.
   28  # Keep runtime support for alternate builds; a compiled pair hides developer
   29  # entry rows while the player's own ScreenScraper account stays separate.
   30  PKG_CMAKE_OPTS_TARGET+=" -DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1"
   31  
   32  # Upstream replaced the S922X test with a build option (2026-09).
   33  [ "${BATTERYPLUS_SUPPORT}" = "yes" ] && PKG_CMAKE_OPTS_TARGET+=" -DBATTERYPLUS=1"
   34  
   35  pre_configure_target() {
   36    # This public shared developer account is the explicit interim choice. An
   37    # intentional build override remains supported, but does not gain the shared
   38    # identity exception in the image's selected-state gate (#565/#566).
   39  [:39 withheld by line number]
   40    export SCREENSCRAPER_DEV_LOGIN="${SCREENSCRAPER_DEV_LOGIN:-devid=${screenscraper_shared_dev}&devpassword=${screenscraper_shared_dev}}"
   41  
   42    for key in SCREENSCRAPER_DEV_LOGIN \
   43               GAMESDB_APIKEY \
   44               CHEEVOS_DEV_LOGIN; do
   45      if [ -z "${!key}" ]; then
   46        echo "WARNING: ${key} not declared, will not build support."
   47      else
   48        # The name, never the value: a developer password or an API key does
   49        # not belong in a build log that gets pasted into an issue.
   50        echo "USING: ${key} (set)"
   51      fi
   52    done
   53  
   54    export DEVICE=$(echo ${DEVICE^^} | sed "s#-#_##g")
   55  }
   56  
   57  makeinstall_target() {
   58    # The bounded RVZ reader carries a BSD padding adaptation. Older ES pins
   59    # have no such reader; preserve their existing installation path.
   60    if [ -f "${PKG_BUILD}/external/libcheevos/LICENSE.rvz-padding" ]; then
   61      mkdir -p ${INSTALL}/usr/share/licenses/emulationstation
   62      cp -a ${PKG_BUILD}/external/libcheevos/LICENSE.rvz-padding \
   63            ${PKG_BUILD}/external/libcheevos/RVZ-NOTICES.md \
   64            ${INSTALL}/usr/share/licenses/emulationstation/
   65    fi
   66  
   67    mkdir -p ${INSTALL}/usr/config/locale
   68      cp -a ${PKG_BUILD}/locale/lang/* ${INSTALL}/usr/config/locale
   69  
   70      # Pre-generate default (en_US.UTF-8) locale for lower-end devices to speed up first boot
   71      # This saves a minute or two on RK3326 in a cost of about 1 MB of SYSTEM size
   72      # Copy-paste of a locale generating part of es_settings script
   73      I18NPATH=$(get_install_dir glibc)/usr/share/i18n/locales/ \
   74        localedef --force --verbose --inputfile=en_US --charmap=UTF-8 \
   75        ${INSTALL}/usr/config/locale/en_US.UTF-8 || true
   76  
   77    mkdir -p ${INSTALL}/usr/config/emulationstation
   78      cp -a ${PKG_DIR}/config/common/*.cfg ${INSTALL}/usr/config/emulationstation
   79      rm -f ${INSTALL}/usr/config/emulationstation/resources/logo.png
   80  
   81    mkdir -p ${INSTALL}/usr/config/emulationstation/resources
   82      cp -a ${PKG_BUILD}/resources/* ${INSTALL}/usr/config/emulationstation/resources
   83      rm -f ${INSTALL}/usr/config/emulationstation/resources/DroidSansFallbackFull.ttf
   84      ln -sf /usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf \
   85        ${INSTALL}/usr/config/emulationstation/resources/DroidSansFallbackFull.ttf
   86  
   87    mkdir -p ${INSTALL}/usr/bin
   88      cp -a ${PKG_BUILD}/es_settings ${INSTALL}/usr/bin
   89      cp -a ${PKG_BUILD}/start_es.sh ${INSTALL}/usr/bin
   90      cp -a ${PKG_BUILD}/serial_number_check ${INSTALL}/usr/bin
   91  
   92    mkdir -p ${INSTALL}/usr/bin
   93      #ln -sf /storage/.config/emulationstation/resources ${INSTALL}/usr/bin/resources
   94      cp -a ${PKG_BUILD}/emulationstation ${INSTALL}/usr/bin
   95  
   96    mkdir -p ${INSTALL}/etc
   97      ln -sf /storage/.cache/system_timezone ${INSTALL}/etc/timezone
   98  
   99    mkdir -p ${INSTALL}/etc/emulationstation
  100      ln -sf /storage/.config/emulationstation/themes ${INSTALL}/etc/emulationstation/themes
  101      ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/emulationstation/es_systems.cfg
  102  
  103  
  104    # If we're not an emulation device, ES may still be installed so we need a default config.
  105    if [[ "${EMULATION_DEVICE}" == "no" || "${BASE_ONLY}" == "true" ]]; then
  106      cat <<EOF >${INSTALL}/usr/config/emulationstation/es_systems.cfg
  107  <?xml version="1.0" encoding="UTF-8"?>
  108  <systemList>
  109          <system>
  110                  <name>tools</name>
  111                  <fullname>Tools</fullname>
  112                  <manufacturer>ROCKNIX</manufacturer>
  113                  <release>2024</release>
  114                  <hardware>system</hardware>
  115                  <path>/storage/.config/modules</path>
  116                  <extension>.sh</extension>
  117                  <command>%ROM%</command>
  118                  <platform>tools</platform>
  119                  <theme>tools</theme>
  120          </system>
  121  </systemList>
  122  EOF
  123    fi
  124  
  125    #Delete all vulkan options from es_features when vulkan is not present
  126    if [ ! "${VULKAN_SUPPORT}" = "yes" ]; then
  127      xmlstarlet ed --inplace -d '//choice[contains(@name, "vulkan")]' ${INSTALL}/usr/config/emulationstation/es_features.cfg
  128    fi
  129  }
  130  
  131  
  132  post_install() {
  133    mkdir -p ${INSTALL}/usr/share
  134      ln -sf /storage/.config/locale ${INSTALL}/usr/share/locale
  135  
  136    mkdir -p ${INSTALL}/usr/lib
  137      ln -sf /usr/share/locale ${INSTALL}/usr/lib/locale
  138  
  139    mkdir -p ${INSTALL}/usr/config/emulationstation
  140      ln -sf /usr/share/locale  ${INSTALL}/usr/config/emulationstation/locale
  141  }

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/autostart/001-emulationstation (lines 1-13 of 13; whole)
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  # Minimal OS variable loading for performance
    6  . /etc/profile.d/001-functions
    7  
    8  if [ ! -L "/storage/.emulationstation" ] && \
    9     [ -d /storage/.config/emulationstation ]
   10  then
   11    ln -sf /storage/.config/emulationstation /storage/.emulationstation
   12  fi
   13  

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/sources/es_settings (lines 1-52 of 52; whole)
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2019-present Shanti Gilbert (https://github.com/shantigilbert)
    4  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    5  
    6  # Source predefined functions and variables
    7  . /etc/profile
    8  
    9  export SDL_AUDIODRIVER=pulseaudio
   10  
   11  TZ=$(get_setting system.timezone)
   12  echo -n "TIMEZONE=${TZ}" > /storage/.cache/timezone
   13  echo -n "${TZ}" >/storage/.cache/system_timezone
   14  systemctl restart tz-data.service
   15  
   16  MYLOCALE=$(get_setting system.language)
   17  if [[ -n "${MYLOCALE}" ]]
   18  then
   19  
   20    unset I18NPATH LANG LANGUAGE LOCPATH
   21  
   22    MYCHARMAP="UTF-8"
   23    MYLANG="${MYLOCALE}.${MYCHARMAP}"
   24    MYLOCPATH="/storage/.config/emulationstation"
   25  
   26    if [ ! -e "${MYLOCPATH}/locale/${MYLANG}/LC_NAME" ]; then
   27      performance
   28   I18NPATH="/usr/share/i18n"
   29   localedef -i ${MYLOCALE} \
   30             -c \
   31             -v \
   32             -f ${MYCHARMAP} \
   33             ${MYLOCPATH}/locale/${MYLANG} >/var/log/start_es.log 2>&1
   34      ${DEVICE_CPU_GOVERNOR}
   35    fi
   36  
   37    export LOCPATH="${MYLOCPATH}/locale"
   38    export LANG=${MYLANG}
   39    export LANGUAGE=${MYLANG}
   40    systemctl import-environment LANG
   41    systemctl import-environment LOCPATH
   42    systemctl import-environment I18NPATH
   43    systemctl import-environment LANGUAGE
   44  fi
   45  
   46  ### Import quirk variables.
   47  for VARIABLE in $(cat /etc/profile.d/999-export | grep _ | sed 's/export//g; s/^\W//g; s/\\//g')
   48  do
   49    systemctl import-environment ${VARIABLE}
   50  done
   51  
   52  set_kill set "emulationstation"

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/sources/serial_number_check (lines 1-27 of 27; whole)
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
    5  
    6  . /etc/profile
    7  
    8  if [ -z "${DEVICE_SERIAL_NUMBER_PATH}" ]; then
    9    log $0 "SERIAL NUMBER CHECK: This device has no unique serial number to check, skipping and continue to Emulation Station"
   10    exit 0
   11  else
   12    DEVICE_SERIAL_NUMBER="$(cat ${DEVICE_SERIAL_NUMBER_PATH})"
   13    log $0 "SERIAL NUMBER CHECK: DEVICE SERIAL NUMBER: ${DEVICE_SERIAL_NUMBER}"
   14  fi
   15  
   16  STORED_SERIAL_NUMBER=$(get_setting "device.serial.number")
   17  if [ ! -n "${STORED_SERIAL_NUMBER}" ]; then
   18    set_setting "device.serial.number" "${DEVICE_SERIAL_NUMBER}"
   19    echo 1 > "/storage/serial_number_check_status"
   20    log $0 "SERIAL NUMBER CHECK: No storted serial number found, saving SOC serial number to system.cfg and show warning."
   21  elif [ ! "${STORED_SERIAL_NUMBER}" == "${DEVICE_SERIAL_NUMBER}" ]; then
   22    set_setting "device.serial.number" "${DEVICE_SERIAL_NUMBER}"
   23    echo 1 > "/storage/serial_number_check_status"
   24    log $0 "SERIAL NUMBER CHECK: Device and stored serial numbers do not match, show warning."
   25  else
   26    log $0 "SERIAL NUMBER CHECK: Device and stored serial numbers match, continue to Emulation Station."
   27  fi

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/sources/start_es.sh (lines 1-8 of 8; whole)
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ### setup is the same
    6  . $(dirname $0)/es_settings
    7  
    8  emulationstation --log-path /var/log --no-splash

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/system.d/emustation.service (lines 1-20 of 20; whole)
    1  [Unit]
    2  Description=EmulationStation emulator frontend
    3  ConditionPathExists=/var/lock/start.games
    4  After=rocknix-automount.service
    5  
    6  [Service]
    7  Environment=XDG_RUNTIME_DIR=/var/run/0-runtime-dir
    8  Environment=HOME=/storage
    9  Environment=SDL_AUDIODRIVER=pulseaudio
   10  EnvironmentFile=/etc/profile
   11  ExecStartPre=/usr/bin/es_settings
   12  ExecStart=/usr/bin/emulationstation --log-path /var/log --no-splash
   13  KillMode=process
   14  TimeoutStopSec=3
   15  Restart=always
   16  RestartSec=2
   17  StartLimitInterval=0
   18  
   19  [Install]
   20  WantedBy=rocknix.target

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/system.d/essway.service (lines 1-21 of 21; whole)
    1  [Unit]
    2  Description=EmulationStation-with-Sway
    3  # This path never exist on rk3566
    4  #ConditionPathExists=/var/lock/start.games
    5  Requires=sway.service
    6  After=sway.service
    7  
    8  [Service]
    9  Type=simple
   10  Environment=HOME=/storage
   11  EnvironmentFile=/etc/profile
   12  # Wait for usable Wayland; keep failure/retry owned by this frontend unit.
   13  ExecStartPre=/usr/bin/sway-ready
   14  TimeoutStartSec=20
   15  ExecStart=/usr/bin/start_es.sh
   16  WorkingDirectory=/storage
   17  Restart=always
   18  RestartSec=2
   19  
   20  [Install]
   21  WantedBy=rocknix.target

=== SOURCE projects/ROCKNIX/packages/ui/lowerdeck/package.mk (lines 1-17 of 17; whole)
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="lowerdeck"
    5  PKG_VERSION="ab735114ab318a84e4d28c9c5f1b154e450a579a"
    6  PKG_SHA256="2677d3ce675b9704487f9f09f82728b56009f9fa7c36403086e9c655af108f42"
    7  PKG_LICENSE="GPL-2.0-or-later"
    8  PKG_SITE="https://github.com/bulzipke/lowerdeck"
    9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_TARGET="toolchain Python3 SDL2 SDL2_image SDL2_ttf"
   11  PKG_LONGDESC="Touch UI for the second screen of dual-screen handhelds."
   12  PKG_TOOLCHAIN="manual"
   13  
   14  makeinstall_target() {
   15    mkdir -p ${INSTALL}/usr/share/lowerdeck
   16      cp -a ${PKG_BUILD}/* ${INSTALL}/usr/share/lowerdeck
   17  }

=== SOURCE projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/package.mk (lines 1-28 of 28; whole)
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="es-theme-art-book-next"
    5  PKG_VERSION="9a50ef366e750aabfab29e6915a2867607212971"
    6  PKG_SHA256="7ee1e93f2c4e4f7385b78680ecfa3828acf12bc616e2111d23cc66a524231125"
    7  PKG_LICENSE="CUSTOM"
    8  PKG_SITE="https://github.com/anthonycaccese/art-book-next-es"
    9  PKG_URL="https://github.com/anthonycaccese/art-book-next-es/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_TARGET="toolchain noto-sans-cjk"
   11  PKG_LONGDESC="Art Book Next"
   12  PKG_TOOLCHAIN="manual"
   13  
   14  makeinstall_target() {
   15    mkdir -p ${INSTALL}/usr/share/themes/${PKG_NAME}
   16      cp -rf * ${INSTALL}/usr/share/themes/${PKG_NAME}
   17      cp ${PKG_DIR}/sources/pixelelated-wordmark.svg ${INSTALL}/usr/share/themes/${PKG_NAME}/
   18      cp ${PKG_DIR}/sources/Tiny5-OFL.txt ${INSTALL}/usr/share/themes/${PKG_NAME}/
   19      rm -rf ${INSTALL}/usr/share/themes/${PKG_NAME}/_inc/systems/{artwork-circuit,artwork-classic,artwork-nintendont,artwork-noir,artwork-outline}
   20      sed -i '/<include name="\(noir\|nintendont\|circuit\|outline\)"/d' ${INSTALL}/usr/share/themes/${PKG_NAME}/theme.xml
   21      sed -i '/<\/theme>/i\
   22     <variables lang="zh" ifSubset="fonts:default|custom">\
   23        <fontBold>/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf</fontBold>\
   24        <fontRegular>/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf</fontRegular>\
   25        <fontLight>/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf</fontLight>\
   26        <fontLogo>/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf</fontLogo>\
   27     </variables>' ${INSTALL}/usr/share/themes/${PKG_NAME}/fonts.xml
   28  }

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/config/common/es_savestates.cfg (lines 1-26 of 26; whole)
    1  <?xml version="1.0"?>
    2  <!--
    3    Save state layout for EmulationStation's save state manager (es-app/src/SaveStateConfigFile.cpp).
    4  
    5    Batocera's libretro entry (package/batocera/emulationstation/batocera-emulationstation/
    6    es_savestates.cfg), under the emulator name ROCKNIX's es_systems.cfg gives RetroArch:
    7    "retroarch", where Batocera's systems say "libretro" (SaveStateRepository::isEnabled tests
    8    the same name). Every other attribute is Batocera's, verbatim.
    9  
   10    With this file present the interface hands the launcher "-state_slot N -state_file <file>"
   11    and parks nothing; runemu.sh and setsettings.sh turn a .auto file into RetroArch's
   12    savestate_auto_load and any other into its entry slot, "-e N", so the slot you launch is
   13    the one RetroArch loads and the exit auto save is RetroArch's own, kept whatever tile the
   14    game was started from (fork #196, D-UI-057). Without it the interface falls back to its
   15    built-in layout, whose "racommands" path restores the pre-launch auto save at exit and
   16    loses the quit state.
   17  
   18    Managed with the OS, like es_systems.cfg: userconfig-setup leaves it out of the
   19    first-boot copy and links it into /storage/.config/emulationstation; post-update
   20    moves any copy aside (last_es_savestates.cfg) and links it after every update. Both
   21    paths end on the link (audit #258 PL-001: the first-boot exclusion was missing, so a
   22    fresh device held a copy until its first update).
   23  -->
   24  <savestates>
   25    <emulator name="retroarch"   directory="{{system}}" file="{{romfilename}}.state{{slot}}" image="{{romfilename}}.state{{slot}}.png" nofileextension="true" firstslot="0" autosave="true" autosave_file="{{romfilename}}.state.auto" autosave_image="{{romfilename}}.state.auto.png" incremental="true" />
   26  </savestates>

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/config/common/es_settings.cfg (lines 1-3 of 3; whole)
    1  <?xml version="1.0"?>
    2  <config>
    3  </config>

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/config/common/es_features.cfg (lines 1320-1400 of 2039; cited range: the armsx2 cores (PL-05))
 1320          <choice name="off" value="0"/>
 1321          <choice name="on" value="1"/>
 1322        </feature>
 1323        <feature name="vsync">
 1324          <choice name="on" value="1"/>
 1325          <choice name="off" value="0"/>
 1326        </feature>
 1327       </features>
 1328      </core>
 1329     </cores>
 1330    </emulator>
 1331    <emulator name="armsx2">
 1332     <cores>
 1333      <core name="armsx2-sa">
 1334       <features>
 1335        <feature name="aspect ratio">
 1336          <choice name="4/3" value="0"/>
 1337          <choice name="16/9" value="1"/>
 1338          <choice name="stretch" value="2"/>
 1339        </feature>
 1340        <feature name="bilinear filtering">
 1341          <choice name="nearest" value="0"/>
 1342          <choice name="forced" value="1"/>
 1343          <choice name="ps2" value="2"/>
 1344          <choice name="forced exc. srpite" value="3"/>
 1345        </feature>
 1346        <feature name="ee cycle rate">
 1347          <choice name="50% speed" value="0"/>
 1348          <choice name="60% speed" value="1"/>
 1349          <choice name="75% speed" value="2"/>
 1350          <choice name="100% speed (normal)" value="3"/>
 1351          <choice name="130% speed" value="4"/>
 1352          <choice name="180% speed" value="5"/>
 1353          <choice name="300% speed" value="6"/>
 1354        </feature>
 1355        <feature name="ee cycle skip">
 1356          <choice name="normal" value="0"/>
 1357          <choice name="mild underclock" value="1"/>
 1358          <choice name="moderate underclock" value="2"/>
 1359          <choice name="maximum underclock" value="3"/>
 1360        </feature>
 1361        <feature name="hw download mode">
 1362          <choice name="accurate (recommended)" value="0"/>
 1363          <choice name="disable readbacks (synchronize gs thread)" value="1"/>
 1364          <choice name="unsynchronized (non-deterministic)" value="2"/>
 1365          <choice name="disable (ignore transfers)" value="3"/>
 1366        </feature>
 1367        <feature name="graphics backend">
 1368          <choice name="automatic" value="0"/>
 1369          <choice name="opengl" value="1"/>
 1370          <choice name="vulkan" value="2"/>
 1371          <choice name="software" value="3"/>
 1372        </feature>
 1373        <feature name="internal resolution">
 1374          <choice name="1x (480p)" value="1"/>
 1375          <choice name="1.25x" value="1.25"/>
 1376          <choice name="1.5x" value="1.5"/>
 1377          <choice name="1.75x" value="1.75"/>
 1378          <choice name="2x (720p)" value="2"/>
 1379          <choice name="2.25x" value="2.25"/>
 1380          <choice name="2.5x" value="2.5"/>
 1381          <choice name="2.75x" value="2.75"/>
 1382          <choice name="3x (1080p)" value="3"/>
 1383        </feature>
 1384        <feature name="show fps">
 1385          <choice name="yes" value="true"/>
 1386          <choice name="no" value="false"/>
 1387        </feature>
 1388        <feature name="enable widescreen patches">
 1389          <choice name="yes" value="true"/>
 1390          <choice name="no" value="false"/>
 1391        </feature>
 1392        <feature name="vulkan driver">
 1393          <choice name="armsx2 turnip (default)" value="armsx2"/>
 1394          <choice name="system mesa" value="system"/>
 1395        </feature>
 1396      </features>
 1397      </core>
 1398     </cores>
 1399    </emulator>
 1400    <emulator name="aethersx2">

=== SOURCE projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch (T40's) (lines 1-27 of 27; PL-02 reaches it; T40's text)
    1  diff --git a/es-app/src/ApiSystem.cpp b/es-app/src/ApiSystem.cpp
    2  index 19acd7ded..721347be9 100644
    3  --- a/es-app/src/ApiSystem.cpp
    4  +++ b/es-app/src/ApiSystem.cpp
    5  @@ -745,12 +745,20 @@ std::vector<std::string> ApiSystem::getAvailableChannels()
    6   
    7   std::vector<std::string> ApiSystem::getAvailableCpuGovernors()
    8   {
    9  -	return executeEnumerationScript("/usr/bin/sh -lc \"echo \\\"default\\\"; tr \\\" \\\" \\\"\\n\\\" < /sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors\" | grep \[a-z\]");
   10  +#ifdef __x86_64__
   11  +        return executeEnumerationScript("/usr/bin/sh -lc \". /etc/profile.d/100-amd64-freqfunctions; get_available_cpu_governors\"");
   12  +#else
   13  +        return executeEnumerationScript("/usr/bin/sh -lc \". /etc/profile.d/099-freqfunctions; get_available_cpu_governors\"");
   14  +#endif
   15   }
   16   
   17   std::vector<std::string> ApiSystem::getAvailableGpuGovernors()
   18   {
   19  -	return executeEnumerationScript("/usr/bin/sh -lc \". /etc/profile.d/099-freqfunctions; get_available_gpu_governors\"");
   20  +#ifdef __x86_64__
   21  +        return executeEnumerationScript("/usr/bin/sh -lc \". /etc/profile.d/100-amd64-freqfunctions; get_available_cpu_governors\"");
   22  +#else
   23  +        return executeEnumerationScript("/usr/bin/sh -lc \". /etc/profile.d/099-freqfunctions; get_available_cpu_governors\"");
   24  +#endif
   25   }
   26   
   27   std::vector<std::string> ApiSystem::getAvailableDisplayModes()

=== SOURCE 651150fc88:projects/ROCKNIX/packages/ui/emulationstation/package.mk (ROCKNIX's recipe now) (lines 1-121 of 121; PL-05, PL-14)
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="emulationstation"
    5  PKG_VERSION="f6c542872e3850c5f432929ead219547a897cd4a"
    6  PKG_SHA256="605f548474b887401b46250ad8791a9e1d6d12d8afe798fcd20ce19e758578fa"
    7  PKG_LICENSE="GPL"
    8  PKG_SITE="https://github.com/ROCKNIX/emulationstation-next"
    9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_TARGET="boost toolchain SDL2 freetype curl freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool poppler pugixml noto-sans-cjk ${OPENGLES}"
   11  PKG_NEED_UNPACK="busybox"
   12  PKG_LONGDESC="Emulationstation emulator frontend"
   13  PKG_BUILD_FLAGS="-gold"
   14  PKG_PATCH_DIRS+=" ${DEVICE}"
   15  
   16  PKG_CMAKE_OPTS_TARGET+=" -DROCKNIX=1 \
   17                           -DDISABLE_KODI=1 \
   18                           -DENABLE_FILEMANAGER=0 \
   19                           -DCEC=0 \
   20                           -DENABLE_PULSE=1 \
   21                           -DUSE_SYSTEM_PUGIXML=1 \
   22                           -DGLES3=1"
   23  
   24  [ "${BATTERYPLUS_SUPPORT}" = "yes" ] && PKG_CMAKE_OPTS_TARGET+=" -DBATTERYPLUS=1"
   25  
   26  pre_configure_target() {
   27    for key in SCREENSCRAPER_DEV_LOGIN \
   28               GAMESDB_APIKEY \
   29               CHEEVOS_DEV_LOGIN; do
   30      if [ -z "${!key}" ]; then
   31        echo "WARNING: ${key} not declared, will not build support."
   32      else
   33        echo "USING: ${key} = ${!key}"
   34      fi
   35    done
   36  
   37    export DEVICE=$(echo ${DEVICE^^} | sed "s#-#_##g")
   38  }
   39  
   40  makeinstall_target() {
   41    mkdir -p ${INSTALL}/usr/config/locale
   42      cp -a ${PKG_BUILD}/locale/lang/* ${INSTALL}/usr/config/locale
   43  
   44      # Pre-generate default (en_US.UTF-8) locale for lower-end devices to speed up first boot
   45      # This saves a minute or two on RK3326 in a cost of about 1 MB of SYSTEM size
   46      # Copy-paste of a locale generating part of es_settings script
   47      I18NPATH=$(get_install_dir glibc)/usr/share/i18n/locales/ \
   48        localedef --force --verbose --inputfile=en_US --charmap=UTF-8 \
   49        ${INSTALL}/usr/config/locale/en_US.UTF-8 || true
   50  
   51    mkdir -p ${INSTALL}/usr/config/emulationstation
   52      cp -a ${PKG_DIR}/config/common/*.cfg ${INSTALL}/usr/config/emulationstation
   53      rm -f ${INSTALL}/usr/config/emulationstation/resources/logo.png
   54  
   55    mkdir -p ${INSTALL}/usr/config/emulationstation/resources
   56      cp -a ${PKG_BUILD}/resources/* ${INSTALL}/usr/config/emulationstation/resources
   57      rm -f ${INSTALL}/usr/config/emulationstation/resources/DroidSansFallbackFull.ttf
   58      ln -sf /usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf \
   59        ${INSTALL}/usr/config/emulationstation/resources/DroidSansFallbackFull.ttf
   60  
   61    mkdir -p ${INSTALL}/usr/bin
   62      cp -a ${PKG_BUILD}/es_settings ${INSTALL}/usr/bin
   63      cp -a ${PKG_BUILD}/start_es.sh ${INSTALL}/usr/bin
   64      cp -a ${PKG_BUILD}/serial_number_check ${INSTALL}/usr/bin
   65  
   66    mkdir -p ${INSTALL}/usr/bin
   67      #ln -sf /storage/.config/emulationstation/resources ${INSTALL}/usr/bin/resources
   68      cp -a ${PKG_BUILD}/emulationstation ${INSTALL}/usr/bin
   69  
   70    mkdir -p ${INSTALL}/etc
   71      ln -sf /storage/.cache/system_timezone ${INSTALL}/etc/timezone
   72  
   73    mkdir -p ${INSTALL}/etc/emulationstation
   74      ln -sf /storage/.config/emulationstation/themes ${INSTALL}/etc/emulationstation/themes
   75      ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/emulationstation/es_systems.cfg
   76  
   77  
   78    # If we're not an emulation device, ES may still be installed so we need a default config.
   79    if [[ "${EMULATION_DEVICE}" == "no" || "${BASE_ONLY}" == "true" ]]; then
   80      cat <<EOF >${INSTALL}/usr/config/emulationstation/es_systems.cfg
   81  <?xml version="1.0" encoding="UTF-8"?>
   82  <systemList>
   83          <system>
   84                  <name>tools</name>
   85                  <fullname>Tools</fullname>
   86                  <manufacturer>ROCKNIX</manufacturer>
   87                  <release>2024</release>
   88                  <hardware>system</hardware>
   89                  <path>/storage/.config/modules</path>
   90                  <extension>.sh</extension>
   91                  <command>%ROM%</command>
   92                  <platform>tools</platform>
   93                  <theme>tools</theme>
   94          </system>
   95  </systemList>
   96  EOF
   97    fi
   98  
   99    #Delete all vulkan options from es_features when vulkan is not present
  100    if [ ! "${VULKAN_SUPPORT}" = "yes" ]; then
  101      xmlstarlet ed --inplace -d '//choice[contains(@name, "vulkan")]' ${INSTALL}/usr/config/emulationstation/es_features.cfg
  102    fi
  103  
  104    #ARMSX2's own Turnip ships only on these devices (see armsx2-sa)
  105    case ${DEVICE} in
  106      SM4450|SM6115|SM8250|SM8550|SM8650) ;;
  107      *) xmlstarlet ed --inplace -d '//core[@name="armsx2-sa"]//feature[@name="vulkan driver"]' ${INSTALL}/usr/config/emulationstation/es_features.cfg ;;
  108    esac
  109  }
  110  
  111  
  112  post_install() {
  113    mkdir -p ${INSTALL}/usr/share
  114      ln -sf /storage/.config/locale ${INSTALL}/usr/share/locale
  115  
  116    mkdir -p ${INSTALL}/usr/lib
  117      ln -sf /usr/share/locale ${INSTALL}/usr/lib/locale
  118  
  119    mkdir -p ${INSTALL}/usr/config/emulationstation
  120      ln -sf /usr/share/locale  ${INSTALL}/usr/config/emulationstation/locale
  121  }

=== SOURCE ES 16dbac5211:CMakeLists.txt (lines 1-40, 110-170, 200-262, 296-335, 345-400, 455-470, 560-580 of 617; the options, the GL system, the finds, the definitions, the link list, i18n)
    1  cmake_minimum_required(VERSION 3.10)
    2  
    3  option(GLES "Set to ON if targeting Embedded OpenGL" ${GLES})
    4  option(GLES2 "Set to ON if targeting OpenGL ES 2.0" ${GLES2})
    5  option(GLES3 "Set to ON if targeting OpenGL ES 3.0" ${GLES3})
    6  option(GL "Set to ON if targeting Desktop OpenGL" ${GL})
    7  
    8  set(OPENGL_OPTION_COUNT 0)
    9  foreach(OPENGL_OPTION GLES GLES2 GLES3 GL)
   10      if(${OPENGL_OPTION})
   11          math(EXPR OPENGL_OPTION_COUNT "${OPENGL_OPTION_COUNT} + 1")
   12      endif()
   13  endforeach()
   14  if(OPENGL_OPTION_COUNT GREATER 1)
   15      message(FATAL_ERROR "GLES, GLES2, GLES3, and GL are mutually exclusive; enable only one graphics API")
   16  endif()
   17  option(RPI "Set to ON to enable the Raspberry PI video player (omxplayer)" ${RPI})
   18  option(CEC "CEC" ON)
   19  option(BCM "BCM host" OFF)
   20  
   21  option(BATOCERA "Set to ON to enable BATOCERA specific code" OFF)
   22  option(RETROBAT "Set to ON to enable RETROBAT specific code" OFF)
   23  option(ROCKNIX "Set to ON to enable ROCKNIX specific code" OFF)
   24  
   25  option(ENABLE_FILEMANAGER "Set to ON to enable f1 shortcut for filesystem" OFF)
   26  option(DISABLE_KODI "Set to ON to disable kodi in menu" OFF)
   27  option(ENABLE_PULSE "Set to ON to enable pulse audio (versus alsa)" OFF)
   28  option(ENABLE_TTS "Set to ON to enable text to speech" OFF)
   29  option(USE_SYSTEM_PUGIXML "Set to ON to use system-wide pugixml library" OFF)
   30  
   31  # The unit tests for the pure code (es-app/tests/unit, #120). Off by default,
   32  # so an image build never builds or links them; they need no SDL, no fonts
   33  # and no device, and es-app/tests/unit/CMakeLists.txt also stands on its own
   34  # for a run with the host compiler.
   35  option(ES_BUILD_TESTS "Set to ON to build the es-unit-tests binary" OFF)
   36  
   37  add_definitions(-w)
   38  
   39  # Win32 default platform & directory detection
   40  if(WIN32)
  110      ${CMAKE_CURRENT_SOURCE_DIR}/CMake/Utils
  111      ${CMAKE_CURRENT_SOURCE_DIR}/CMake/Packages
  112  )
  113  
  114  # Pull the hardware device out of the build environment
  115  if(DEFINED ENV{DEVICE})
  116      add_definitions(-DHW_DEVICE="$ENV{DEVICE}")
  117      add_definitions(-D$ENV{DEVICE})
  118  endif()
  119  
  120  if(BATOCERA)
  121    MESSAGE("Batocera build")
  122    add_definitions(-DBATOCERA)
  123  endif()
  124  
  125  if(RETROBAT)
  126    MESSAGE("Retrobat build")
  127    add_definitions(-DRETROBAT)
  128  endif()
  129  
  130  if(ROCKNIX)
  131    MESSAGE("ROCKNIX build")
  132    add_definitions(-DROCKNIX)
  133  endif()
  134  
  135  if(BATTERYPLUS)
  136    MESSAGE("batteryplus build")
  137    add_definitions(-DBATTERYPLUS)
  138  endif()
  139  
  140  # disable kodi menu
  141  if(DISABLE_KODI)
  142    MESSAGE("Kodi disabled")
  143  else()
  144    add_definitions(-D_ENABLE_KODI_)
  145  endif()
  146  
  147  # batocera / file manager f1 button
  148  # disable file manager
  149  if(ENABLE_FILEMANAGER)
  150    MESSAGE("file manager enabled")
  151    add_definitions(-D_ENABLE_FILEMANAGER_)
  152  endif()
  153  
  154  if(BCM)
  155      set(BCMHOST found)
  156  endif()
  157  
  158  #-------------------------------------------------------------------------------
  159  #set up OpenGL system variable
  160  if(GLES)
  161      set(GLSystem "Embedded OpenGL" CACHE STRING "The OpenGL system to be used" FORCE)
  162  elseif(GLES2)
  163      set(GLSystem "OpenGL ES 2.0" CACHE STRING "The OpenGL system to be used" FORCE)
  164  elseif(GLES3)
  165      set(GLSystem "OpenGL ES 3.0" CACHE STRING "The OpenGL system to be used" FORCE)
  166  elseif(GL)
  167      set(GLSystem "Desktop OpenGL" CACHE STRING "The OpenGL system to be used" FORCE)
  168  #-------------------------------------------------------------------------------
  169  #check if we're running on Raspberry Pi
  170  elseif(EXISTS "${CMAKE_FIND_ROOT_PATH}/opt/vc/include/bcm_host.h")
  200  endif()
  201  
  202  set_property(CACHE GLSystem PROPERTY STRINGS "Desktop OpenGL" "Embedded OpenGL" "OpenGL ES 2.0" "OpenGL ES 3.0")
  203  
  204  MESSAGE("-- Graphics API: ${GLSystem}")
  205  if(NOT GLES AND NOT GLES2 AND NOT GLES3 AND NOT GL)
  206      MESSAGE("-- No graphics API selected; using ${GLSystem}. Pass -DGLES3=ON for the OpenGL ES 3.0 renderer.")
  207  endif()
  208  
  209  #finding necessary packages
  210  #-------------------------------------------------------------------------------
  211  if(${GLSystem} MATCHES "Desktop OpenGL")
  212      find_package(OpenGL REQUIRED)
  213  elseif(${GLSystem} MATCHES "OpenGL ES 3.0")
  214      find_package(OpenGLES3 REQUIRED)
  215  elseif(${GLSystem} MATCHES "OpenGL ES 2.0")
  216      find_package(OpenGLES2 REQUIRED)
  217  else()
  218      find_package(OpenGLES REQUIRED)
  219  endif()
  220  find_package(Freetype REQUIRED)
  221  find_package(FreeImage REQUIRED)
  222  # batocera / background musics
  223  find_package(SDL2MIXER REQUIRED)
  224  # batocera / customisations
  225  find_package(SDL2 REQUIRED)
  226  find_package(CURL REQUIRED)
  227  find_package(VLC REQUIRED)
  228  find_package(RapidJSON REQUIRED)
  229  
  230  # FriBidi is only used to reorder right-to-left scripts (Arabic, Hebrew) at render time.
  231  # It is optional on purpose: when it is missing, Font.cpp falls back on tryFastBidi(), which
  232  # is what every build used before RTL support was added. pkg-config is a Unix mechanism and
  233  # the Windows dependency package does not ship FriBidi, so this must never be REQUIRED.
  234  find_package(PkgConfig QUIET)
  235  if(PKG_CONFIG_FOUND)
  236  	pkg_check_modules(FRIBIDI QUIET fribidi)
  237  endif()
  238  
  239  if(FRIBIDI_FOUND)
  240  	MESSAGE("-- FriBidi found, using it for right-to-left text reordering")
  241  	add_definitions(-DHAVE_FRIBIDI)
  242  else()
  243  	MESSAGE("-- FriBidi not found, falling back on the built-in right-to-left reordering")
  244  endif()
  245  
  246  if(NOT WIN32)
  247  	if(ENABLE_PULSE)
  248  	  MESSAGE("pulse audio enabled")
  249  	  find_package(PulseAudio REQUIRED)
  250  	  add_definitions(-D_ENABLE_PULSE_)
  251  	else()
  252  	  MESSAGE("pulse audio disabled")
  253  	endif()
  254  
  255  	find_package(udev)
  256  	if(UDEV_FOUND)
  257  	  MESSAGE("udev found. guns enabled")
  258  	  add_definitions(-DHAVE_UDEV)
  259  	else()
  260  	  MESSAGE("udev not found. guns will be disabled")
  261  	endif()
  262  	
  296  
  297  if(CEC)
  298    if(DEFINED libCEC_FOUND)
  299      add_definitions(-DHAVE_LIBCEC)
  300    endif()
  301  endif()
  302  
  303  if(DEFINED ENV{SCREENSCRAPER_SOFTNAME})
  304      add_definitions(-DSCREENSCRAPER_SOFTNAME="$ENV{SCREENSCRAPER_SOFTNAME}")
  305  endif()
  306  
  307  if(DEFINED ENV{SCREENSCRAPER_DEV_LOGIN})
  308      add_definitions(-DSCREENSCRAPER_DEV_LOGIN="$ENV{SCREENSCRAPER_DEV_LOGIN}")
  309  endif()
  310  
  311  # Enable runtime developer credentials for builds without a compiled pair.
  312  # Those builds show DEVELOPER ID and DEVELOPER PASSWORD under SCRAPER > ACCOUNTS.
  313  # Set from the package recipe (-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1) or environment.
  314  # A compiled-in SCREENSCRAPER_DEV_LOGIN takes precedence and hides the rows;
  315  # normal distribution builds supply that pair at build time (#566).
  316  if(SCREENSCRAPER_RUNTIME_DEV_LOGIN OR DEFINED ENV{SCREENSCRAPER_RUNTIME_DEV_LOGIN})
  317      add_definitions(-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1)
  318  endif()
  319  
  320  if(DEFINED ENV{GAMESDB_APIKEY})
  321      add_definitions(-DGAMESDB_APIKEY="$ENV{GAMESDB_APIKEY}")
  322  endif()
  323  
  324  if(DEFINED ENV{CHEEVOS_DEV_LOGIN})
  325      add_definitions(-DCHEEVOS_DEV_LOGIN="$ENV{CHEEVOS_DEV_LOGIN}")
  326  endif()
  327  
  328  if(DEFINED ENV{HFS_DEV_LOGIN})
  329      add_definitions(-DHFS_DEV_LOGIN="$ENV{HFS_DEV_LOGIN}")
  330  endif()
  331  
  332  #-------------------------------------------------------------------------------
  333  
  334  if(MSVC)
  335      set(CMAKE_DEBUG_POSTFIX "d")
  345      execute_process(COMMAND ${CMAKE_CXX_COMPILER} -dumpversion OUTPUT_VARIABLE G++_VERSION)
  346      if (G++_VERSION VERSION_LESS 4.7)
  347              message(SEND_ERROR "You need at least G++ 4.7 to compile EmulationStation!")
  348      endif()
  349  
  350      #set up compiler flags for GCC
  351  if (CMAKE_BUILD_TYPE MATCHES Debug)
  352      set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wno-attributes -O0") #support C++17 for std::, optimize
  353      set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -O0")
  354  else()
  355      set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wno-attributes -O3") #support C++17 for std::, optimize
  356      set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -O3")  #-s = strip binary
  357  endif()
  358  endif()
  359  
  360  if(${GLSystem} MATCHES "Desktop OpenGL")
  361      add_definitions(-DUSE_OPENGL_21)
  362  elseif(${GLSystem} MATCHES "OpenGL ES 3.0")
  363      add_definitions(-DUSE_OPENGLES_30)
  364  elseif(${GLSystem} MATCHES "OpenGL ES 2.0")
  365      add_definitions(-DUSE_OPENGLES_20)
  366  else()
  367      add_definitions(-DUSE_OPENGLES_10)
  368  endif()
  369  
  370  #-------------------------------------------------------------------------------
  371  #add include directories
  372  set(COMMON_INCLUDE_DIRS
  373      ${FREETYPE_INCLUDE_DIRS}
  374      ${FreeImage_INCLUDE_DIRS}
  375      ${FRIBIDI_INCLUDE_DIRS}
  376      # batocera / background musics
  377      ${SDLMIXER_INCLUDE_DIR}
  378      # batocera / customisations    
  379      ${SDL2_INCLUDE_DIR}
  380      ${CURL_INCLUDE_DIR}
  381      ${VLC_INCLUDE_DIR}
  382      ${RAPIDJSON_INCLUDE_DIRS}
  383      ${CMAKE_CURRENT_SOURCE_DIR}/external
  384      ${CMAKE_CURRENT_SOURCE_DIR}/es-core/src
  385  )
  386  
  387  if(ENABLE_PULSE)
  388   LIST(APPEND COMMON_INCLUDE_DIRS
  389      ${PULSEAUDIO_INCLUDE_DIR}
  390        )
  391  endif()
  392  
  393  if(USE_SYSTEM_PUGIXML)
  394    MESSAGE("Use system pugixml")
  395    find_package(pugixml REQUIRED)
  396  endif()
  397  
  398  #add libCEC_INCLUDE_DIR
  399  if(CEC)
  400    if(DEFINED libCEC_FOUND)
  455          "${CMAKE_FIND_ROOT_PATH}/opt/vero3/lib"
  456      )
  457  endif()
  458  
  459  set(COMMON_LIBRARIES
  460      ${FREETYPE_LIBRARIES}
  461      ${FreeImage_LIBRARIES}
  462      ${FRIBIDI_LIBRARIES}
  463      ${SDL2_LIBRARY}
  464      # batocera / background musics
  465      ${SDLMIXER_LIBRARY}
  466      # batocera / customisations    
  467      ${CURL_LIBRARIES}
  468      ${VLC_LIBRARIES}
  469      pugixml
  470      nanosvg 
  560              ${OPENGLES_LIBRARIES}
  561          )
  562      endif()
  563  endif()
  564  
  565  if(NOT WIN32)
  566  	# batocera / i18n
  567  	# i18n
  568  	find_program (MSGFMT_EXECUTABLE msgfmt)
  569  	find_program (MSGMERGE_EXECUTABLE msgmerge)
  570  	find_program (XGETTEXT_EXECUTABLE xgettext)
  571  	find_package(Intl)
  572  
  573  	if(MSGFMT_EXECUTABLE AND MSGMERGE_EXECUTABLE AND XGETTEXT_EXECUTABLE AND Intl_FOUND)
  574  	  message (STATUS "Native language support enabled.")
  575  	  add_definitions(-DHAVE_INTL)
  576  	else()
  577  	  message (STATUS "Native language support disabled.")
  578  	endif()
  579  endif()
  580  

=== SOURCE ES 16dbac5211:es-core/CMakeLists.txt (lines 240-246, 276-284 of 303; the renderer list)
  240  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector4f.cpp
  241  
  242  	# Renderer
  243  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer.cpp
  244  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GL21.cpp
  245  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES10.cpp
  246  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/GlExtensions.cpp	
  276  )
  277  
  278  if(${GLSystem} MATCHES "OpenGL ES 3.0")
  279  	LIST(APPEND CORE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES30.h)
  280  	LIST(APPEND CORE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES30.cpp)
  281  else()
  282  	LIST(APPEND CORE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES20.h)
  283  	LIST(APPEND CORE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES20.cpp)
  284  endif()

=== SOURCE ES 16dbac5211:es-core/src/Paths.cpp (lines 70-85 of 363; the ROCKNIX log path (PL-09))
   70  	mSystemConfFilePath = "/userdata/system/batocera.conf";
   71  	mUserManualPath = "/usr/share/batocera/doc/notice.pdf";
   72  	mVersionInfoPath = "/usr/share/batocera/batocera.version";
   73  	mKodiPath = "/usr/bin/kodi";
   74  #endif
   75  
   76  #if defined(ROCKNIX)
   77  	mRootPath = "/storage";
   78  	mEmulationStationPath = getExePath();
   79  	mUserEmulationStationPath = "/storage/.config/emulationstation";
   80  
   81  	mLogPath = "/var/log";
   82  	mScreenShotsPath = "/storage/roms/screenshots";
   83  	mSaveStatesPath = "/storage/roms/savestates";
   84  	mMusicPath = mUserEmulationStationPath + "/music";
   85  	mUserMusicPath = "/storage/roms/music";

=== SOURCE ES 16dbac5211:es-core/src/Log.cpp (lines 255-290 of 322; the log file (PL-09))
  255          lvl = (LogLevel) LogPolicy::parseLogLevel(Settings::getInstance()->getString("LogLevel"));
  256      }
  257  
  258      auto base = Paths::getLogPath() + "/es_log";
  259      auto logPath = base + ".txt";
  260  
  261      if ((int)lvl < 0)
  262      {
  263          Utils::FileSystem::removeFile(logPath);
  264          mEnabled = false;
  265          return;
  266      }
  267  
  268      static constexpr int kMaxArchives = 4; // Keep 5 logs ( current + 4 latest )
  269  
  270      Utils::FileSystem::removeFile(base + "." + std::to_string(kMaxArchives - 1) + ".txt");
  271  
  272      for (int i = kMaxArchives - 2; i >= 0; --i)
  273      {
  274          Utils::FileSystem::renameFile(
  275              base + "." + std::to_string(i) + ".txt",
  276              base + "." + std::to_string(i + 1) + ".txt", true);
  277      }
  278  
  279      Utils::FileSystem::renameFile(logPath, base + ".0.txt", true);
  280  
  281      // signal(SIGSEGV, crashHandler); // It's already managed by main()
  282      signal(SIGABRT, crashHandler);
  283  
  284  #ifndef WIN32
  285      signal(SIGTERM, crashHandler);
  286  #endif
  287  
  288      bool debugToStderr = (lvl >= LogDebug);
  289      AsyncLogger::instance().open(logPath, lvl, debugToStderr);
  290  

=== SOURCE ES 16dbac5211:es-core/src/Splash.h (lines 1-25 of 44; the default splash (PL-04))
    1  #pragma once
    2  
    3  #include <string>
    4  #include "components/ImageComponent.h"
    5  #include "components/TextComponent.h"
    6  
    7  class Window;
    8  class TextureResource;
    9  
   10  #if defined(ROCKNIX)
   11  #define DEFAULT_SPLASH_IMAGE ":/pixelelated-wordmark.svg"
   12  #define OLD_SPLASH_LAYOUT true
   13  #elif WIN32
   14  #define DEFAULT_SPLASH_IMAGE ":/splash.svg"
   15  #define OLD_SPLASH_LAYOUT true
   16  #else
   17  #define DEFAULT_SPLASH_IMAGE ":/logo.png"
   18  #define OLD_SPLASH_LAYOUT false
   19  #endif
   20  
   21  class Splash
   22  {
   23  public:
   24  	Splash(Window* window, const std::string image, bool fullScreenBackGround = true, IBindable* bindable = nullptr);
   25  	~Splash();

=== SOURCE ES 16dbac5211:es-app/src/main.cpp (lines 75-100, 255-298 of 1368; parseArgs (PL-09))
   75  bool parseArgs(int argc, char* argv[])
   76  {
   77  	Paths::setExePath(argv[0]);
   78  
   79  	// We need to process --home before any call to Settings::getInstance(), because settings are loaded from homepath
   80  	for (int i = 1; i < argc; i++)
   81  	{
   82  		if (strcmp(argv[i], "--home") == 0)
   83  		{
   84  			if (i == argc - 1)
   85  				continue;
   86  
   87  			std::string arg = argv[i + 1];
   88  			if (arg.find("-") == 0)
   89  				continue;
   90  
   91  			Paths::setHomePath(argv[i + 1]);
   92  			break;
   93  		}
   94  	}
   95  
   96  	for(int i = 1; i < argc; i++)
   97  	{
   98  		if (strcmp(argv[i], "--videoduration") == 0)
   99  		{
  100  			gPlayVideoDuration = atoi(argv[i + 1]);
  255  		}
  256  		else if (strcmp(argv[i], "--force-disable-filters") == 0)
  257  		{
  258  			Settings::getInstance()->setBool("ForceDisableFilters", true);
  259  		}
  260  		else if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0)
  261  		{
  262  #ifdef WIN32
  263  			// This is a bit of a hack, but otherwise output will go to nowhere
  264  			// when the application is compiled with the "WINDOWS" subsystem (which we usually are).
  265  			// If you're an experienced Windows programmer and know how to do this
  266  			// the right way, please submit a pull request!
  267  			AttachConsole(ATTACH_PARENT_PROCESS);
  268  			freopen("CONOUT$", "wb", stdout);
  269  #endif
  270  			std::cout <<
  271  				"EmulationStation, a graphical front-end for ROM browsing.\n"
  272  				"Written by Alec \"Aloshi\" Lofquist.\n"
  273  				"Version " << PROGRAM_VERSION_STRING << ", built " << PROGRAM_BUILT_STRING << "\n\n"
  274  				"Command line arguments:\n"
  275  				"--resolution [width] [height]	try and force a particular resolution\n"
  276  				"--gamelist-only			skip automatic game search, only read from gamelist.xml\n"
  277  				"--ignore-gamelist		ignore the gamelist (useful for troubleshooting)\n"
  278  				"--draw-framerate		display the framerate\n"
  279  				"--no-exit			don't show the exit option in the menu\n"
  280  				"--no-splash			don't show the splash screen\n"
  281  				"--debug				more logging, show console on Windows\n"				
  282  				"--windowed			not fullscreen, should be used with --resolution\n"
  283  				"--vsync [1/on or 0/off]		turn vsync on or off (default is on)\n"
  284  				"--max-vram [size]		Max VRAM to use in Mb before swapping. 0 for unlimited\n"
  285  				"--anti-aliasing [0, 2 or 4]	set MSAA anti-aliasing to disabled, 2x or 4x\n"
  286  				"--force-kid		Force the UI mode to be Kid\n"
  287  				"--force-kiosk		Force the UI mode to be Kiosk\n"
  288  				"--force-disable-filters		Force the UI to ignore applied filters in gamelist\n"
  289  				"--home [path]		Directory to use as home path\n"
  290  				"--help, -h			summon a sentient, angry tuba\n\n"
  291  				"--monitor [index]			monitor index\n\n"				
  292  				"More information available in README.md.\n";
  293  			return false; //exit after printing help
  294  		}
  295  	}
  296  
  297  	return true;
  298  }

=== SOURCE ES 16dbac5211:locale/CMakeLists.txt (lines 1-35 of 52; the catalog build (PL-07))
    1  add_custom_target (i18n ALL COMMENT "Building i18n messages.")
    2  file (GLOB es_PO_FILES ${dir}/locale/lang/*)
    3  set(es_POT ${dir}/locale/emulationstation2.pot)
    4  # update the pot
    5  MESSAGE("Building the pot file")
    6  add_custom_command (
    7      TARGET i18n
    8      POST_BUILD
    9      COMMAND find "${dir}/es-app" "${dir}/es-core" -name "*.cpp" -o -name "*.h" | ${XGETTEXT_EXECUTABLE} --add-comments=TRANSLATION -f - -o ${es_POT} --no-location --keyword=_
   10  )
   11  add_custom_command (
   12      TARGET i18n
   13      POST_BUILD
   14      COMMAND sed -i '/^\"POT-Creation-Date:/d' ${es_POT}
   15  )
   16  
   17  foreach (es_PO_INPUT ${es_PO_FILES})
   18          get_filename_component (es_PO_LANG ${es_PO_INPUT} NAME_WE)
   19          MESSAGE("LANG = ${es_PO_LANG}")
   20          set (es_MO_OUTPUT ${es_PO_INPUT}/LC_MESSAGES/emulationstation2.mo)
   21          # update the po from the pot
   22          add_custom_command (
   23              TARGET i18n
   24              POST_BUILD
   25              COMMAND ${MSGMERGE_EXECUTABLE} -U --no-fuzzy-matching ${es_PO_INPUT}/LC_MESSAGES/emulationstation2.po ${es_POT}
   26          )
   27          # compile the po to mo
   28          add_custom_command (
   29              TARGET i18n
   30              POST_BUILD
   31              COMMAND basename ${es_PO_INPUT} && ${MSGFMT_EXECUTABLE} -o ${es_MO_OUTPUT} ${es_PO_INPUT}/LC_MESSAGES/emulationstation2.po
   32          )
   33          install (FILES ${es_MO_OUTPUT} DESTINATION share/locale/${es_PO_LANG}/LC_MESSAGES RENAME emulationstation2.mo)
   34  endforeach (es_PO_INPUT ${es_PO_FILES})
   35  

=== SOURCE 2174265e9c:scripts/unpack (lines 120-165 of 228; the patch globs (PL-02))
  120    rm -rf "${PKG_UNPACK_DIR}"
  121  
  122    pkg_call_exists_opt post_unpack && pkg_call
  123  
  124    if [ "${PKG_SKIP_PATCHES}" != "yes" ]; then
  125      pkg_call_exists_opt pre_patch && pkg_call
  126  
  127      if [ "${TARGET_ARCH}" = "x86_64" ]; then
  128        PATCH_ARCH="x86"
  129      elif [ "${PKG_IS_KERNEL_PKG}" = "yes" ]; then
  130        PATCH_ARCH="${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}"
  131      else
  132        PATCH_ARCH="${TARGET_PATCH_ARCH:-${TARGET_ARCH}}"
  133      fi
  134  
  135      PATCH_DIRS_PKG=""
  136      PATCH_DIRS_PRJ=""
  137      if [ -n "${PKG_PATCH_DIRS}" ]; then
  138        for patch_dir in ${PKG_PATCH_DIRS}; do
  139          if [[ ${patch_dir} =~ ^/ ]]; then
  140            [ -f ${patch_dir} ] && PATCH_DIRS_PKG+=" ${patch_dir}"
  141            [ -d ${patch_dir} ] && PATCH_DIRS_PKG+=" ${patch_dir}/*.patch"
  142          else
  143            [ -d ${PKG_DIR}/patches/${patch_dir} ] && PATCH_DIRS_PKG+=" ${PKG_DIR}/patches/${patch_dir}/*.patch"
  144            [ -d ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${patch_dir} ] && PATCH_DIRS_PRJ+=" ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${patch_dir}/*.patch"
  145            [ -d ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/${patch_dir} ] && PATCH_DIRS_PRJ+=" ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/${patch_dir}/*.patch"
  146          fi
  147        done
  148      fi
  149  
  150      for i in ${PKG_DIR}/patches/*.patch \
  151        ${PKG_DIR}/patches/${PATCH_ARCH}/*.patch \
  152        ${PATCH_DIRS_PKG} \
  153        ${PKG_DIR}/patches/${PKG_VERSION}/*.patch \
  154        ${PKG_DIR}/patches/${PKG_VERSION}/${PATCH_ARCH}/*.patch \
  155        ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/*.patch \
  156        ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PATCH_ARCH}/*.patch \
  157        ${PATCH_DIRS_PRJ} \
  158        ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION}/*.patch \
  159        ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/*.patch; do
  160  
  161        thisdir="${i%/*}"
  162  
  163        if [ "${thisdir}" = "${PKG_DIR}/patches" ]; then
  164          PATCH_DESC="(common)"
  165        elif [ "${thisdir}" = "${PKG_DIR}/patches/${PATCH_ARCH}" ]; then

=== SOURCE 2174265e9c:scripts/install (lines 79-110, 160-190 of 196; the install copy (PL-01))
   79  if [ "${TARGET}" = "target" ]; then
   80    for PKG_TMP_DIR in ${PKG_DIR} \
   81      ${PROJECT_DIR}/${PROJECT}/packages/${PKG_NAME} \
   82      ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/packages/${PKG_NAME}; do
   83  
   84      [ -d ${PKG_TMP_DIR} ] || continue
   85  
   86      if [ -d ${PKG_TMP_DIR}/profile.d ]; then
   87        mkdir -p ${INSTALL}/etc/profile.d
   88        cp ${PKG_TMP_DIR}/profile.d/* ${INSTALL}/etc/profile.d
   89      fi
   90  
   91      if [ -d ${PKG_TMP_DIR}/tmpfiles.d ]; then
   92        mkdir -p ${INSTALL}/usr/lib/tmpfiles.d
   93        cp ${PKG_TMP_DIR}/tmpfiles.d/*.conf ${INSTALL}/usr/lib/tmpfiles.d
   94      fi
   95  
   96      if [ -d ${PKG_TMP_DIR}/autostart ]; then
   97        mkdir -p ${INSTALL}/usr/lib/autostart/common
   98        cp ${PKG_TMP_DIR}/autostart/* ${INSTALL}/usr/lib/autostart/common
   99        chmod 0755 ${INSTALL}/usr/lib/autostart/common/*
  100      fi
  101  
  102      if [ -d ${PKG_TMP_DIR}/daemons ]; then
  103        mkdir -p ${INSTALL}/usr/lib/autostart/daemons
  104        cp ${PKG_TMP_DIR}/daemons/* ${INSTALL}/usr/lib/autostart/daemons
  105      fi
  106  
  107      if [ -d ${PKG_TMP_DIR}/system.d ]; then
  108        mkdir -p ${INSTALL}/usr/lib/systemd/system
  109        cp -Pr ${PKG_TMP_DIR}/system.d/*.* ${INSTALL}/usr/lib/systemd/system
  110      fi
  160  if [ "${TARGET}" = "target" ]; then
  161    pkg_call_exists_opt pre_install && pkg_call
  162  fi
  163  
  164  if [ -n "${PKG_INSTALL}" -a -d "${PKG_INSTALL}" ]; then
  165    tar \
  166      -C "${PKG_INSTALL}" \
  167      --exclude=./usr/local/include \
  168      --exclude=./usr/local/lib/cmake \
  169      --exclude=./usr/local/lib/pkgconfig \
  170      --exclude=./usr/local/share/aclocal \
  171      --exclude=./usr/local/share/pkgconfig \
  172      --exclude=./usr/include \
  173      --exclude=./usr/lib/cmake \
  174      --exclude=./usr/lib/pkgconfig \
  175      --exclude=./usr/share/aclocal \
  176      --exclude=./usr/share/pkgconfig \
  177      --exclude=./include \
  178      --exclude=./lib/cmake \
  179      --exclude=./lib/pkgconfig \
  180      --exclude=./share/aclocal \
  181      --exclude=./share/pkgconfig \
  182      --exclude=./.* \
  183      --exclude='*.a' \
  184      --exclude='*.la' \
  185      -cf - . | tar -C "${INSTALL}" -xf -
  186  fi
  187  
  188  if [ "${TARGET}" = "target" ]; then
  189    pkg_call_exists_opt post_install && pkg_call
  190  fi

=== SOURCE 2174265e9c:scripts/build (lines 135-175 of 646; INSTALL and the build type)
  135  
  136  # setup toolchain
  137  setup_toolchain ${TARGET} ${PKG_TOOLCHAIN}
  138  
  139  # configure install directory
  140  [ -n "${PKG_INSTALL}" ] && INSTALL="${PKG_INSTALL}" || unset INSTALL
  141  
  142  # remove previous install files
  143  if [ -n "${INSTALL}" -a -d "${INSTALL}" ]; then
  144    rm -rf "${INSTALL}"
  145  fi
  146  
  147  # configure debug build defaults
  148  if [ "${BUILD_WITH_DEBUG}" = "yes" ]; then
  149    CMAKE_BUILD_TYPE="Debug"
  150    MESON_BUILD_TYPE="debug"
  151  else
  152    CMAKE_BUILD_TYPE="Release"
  153    MESON_BUILD_TYPE="release"
  154  fi
  155  
  156  CMAKE_GENERATOR_NINJA="-GNinja"
  157  
  158  # configure TARGET build defaults
  159  TARGET_CONFIGURE_OPTS="--host=${TARGET_NAME} \
  160                         --build=${HOST_NAME} \
  161                         --prefix=/usr \
  162                         --bindir=/usr/bin \
  163                         --sbindir=/usr/sbin \
  164                         --sysconfdir=/etc \
  165                         --libdir=/usr/lib \
  166                         --libexecdir=/usr/lib \
  167                         --localstatedir=/var"
  168  if flag_enabled "cfg-libs" "yes"; then
  169    TARGET_CONFIGURE_OPTS+=" --disable-static --enable-shared"
  170  fi
  171  
  172  TARGET_CMAKE_OPTS="-DCMAKE_TOOLCHAIN_FILE=${CMAKE_CONF} \
  173                     -DCMAKE_INSTALL_PREFIX=/usr \
  174                     -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}"
  175  

=== SOURCE 2174265e9c:config/functions (lines 380-392, 795-805, 1105-1135, 1315-1340 of 1936; NDEBUG, the caches, calculate_stamp, PKG_NEED_UNPACK's framework uses)
  380      NINJA_OPTS+=" -v"
  381      MAKEFLAGS+=" V=1 VERBOSE=1"
  382    fi
  383  
  384    # NDEBUG flag
  385    if [ "${BUILD_WITH_DEBUG}" != "yes" ] && flag_enabled "ndebug" "yes"; then
  386      TARGET_CFLAGS+=" -DNDEBUG"
  387      TARGET_CXXFLAGS+=" -DNDEBUG"
  388    fi
  389  
  390    # average load limit
  391    if [ "${CONCURRENCY_LOAD}" != "0" ]; then
  392      NINJA_OPTS+=" -l${CONCURRENCY_LOAD}"
  795      # cache project folder for packages
  796      find "${ROOT}/projects/${PROJECT}/packages" -type f -name package.mk 2>/dev/null | sed "s#/package\.mk\$#${_ANCHOR}#" >> "${temp_local}"
  797  
  798      # cache packages folder
  799      find "${ROOT}/${PACKAGES}" -type f -name package.mk 2>/dev/null | sed "s#/package\.mk\$#${_ANCHOR}#" >> "${temp_global}"
  800  
  801      _CACHE_PACKAGE_LOCAL="${BUILD}/.cache_package_local"
  802      _CACHE_PACKAGE_GLOBAL="${BUILD}/.cache_package_global"
  803      export _CACHE_PACKAGE_LOCAL _CACHE_PACKAGE_GLOBAL
  804  
  805      # overwrite existing cache files only when they are invalid, or not yet created
 1105      return
 1106    done
 1107  }
 1108  
 1109  calculate_stamp() {
 1110    local stamp data global_dir
 1111  
 1112    stamp="$PKG_DIR $PROJECT_DIR/$PROJECT/patches/$PKG_NAME $PROJECT_DIR/$PROJECT/packages/$PKG_NAME"
 1113    [ -n "$DEVICE" ] && stamp+=" $PROJECT_DIR/$PROJECT/devices/$DEVICE/patches/$PKG_NAME"
 1114    [ -n "$PKG_NEED_UNPACK" ] && stamp+=" $PKG_NEED_UNPACK"
 1115  
 1116    # A project package.mk routinely sources the global one to inherit
 1117    # PKG_VERSION, PKG_URL and PKG_SHA256, adding only project-specific hooks.
 1118    # $PKG_DIR resolves to the project copy in that case, so without this the
 1119    # global recipe is never hashed and a version bump there does not invalidate
 1120    # the stamp - the previous version stays built and installed, silently. For
 1121    # a package with no project override this adds a path already in the list,
 1122    # which the sort -u below discards, so existing stamps do not change.
 1123    global_dir="$(get_global_pkg_directory "${PKG_NAME}")"
 1124    [ -n "${global_dir}" ] && stamp+=" ${global_dir}"
 1125  
 1126    data="$(find -L ${stamp} -type f -not -name '.*' -print0 2>/dev/null | sed -z "s|^${ROOT}/||" | LC_ALL=C sort -zu | xargs -0 sha256sum)"
 1127    [ -n "${PKG_STAMP}" ] && data+=$'\n'"$(echo "${PKG_STAMP}" | sha256sum)"
 1128  
 1129    echo "${data}" | sha256sum | cut -d" " -f1
 1130  }
 1131  
 1132  target_has_feature() {
 1133    listcontains "$TARGET_FEATURES" "$1"
 1134  }
 1135  
 1315      cd "${opwd}"
 1316  
 1317      PKG_SHORTDESC="${PKG_SHORTDESC:-${PKG_NAME} (autogenerated)}"
 1318      PKG_LONGDESC="${PKG_LONGDESC:-${PKG_NAME} (autogenerated)}"
 1319  
 1320      if [ "$PKG_IS_ADDON" = "yes" -o "$PKG_IS_ADDON" = "embedded" ] ; then
 1321        [ -z $PKG_SECTION ] && PKG_ADDON_ID="$PKG_NAME" || PKG_ADDON_ID="${PKG_SECTION//\//.}.$PKG_NAME"
 1322        [ "$PKG_ADDON_IS_STANDALONE" != "yes" ] && PKG_NEED_UNPACK="${PKG_NEED_UNPACK} $(get_pkg_directory $MEDIACENTER)"
 1323      fi
 1324  
 1325      if [ -n "${PKG_IS_KERNEL_PKG}" -a "${PKG_NAME}" != "linux" ]; then
 1326        PKG_DEPENDS_TARGET="toolchain linux ${PKG_DEPENDS_TARGET}"
 1327        PKG_DEPENDS_UNPACK="linux ${PKG_DEPENDS_UNPACK}"
 1328        PKG_NEED_UNPACK="${LINUX_DEPENDS} ${PKG_NEED_UNPACK}"
 1329      fi
 1330  
 1331      if [ -n "${PKG_DEPENDS_UNPACK}" ]; then
 1332        for _p in ${PKG_DEPENDS_UNPACK}; do
 1333          PKG_NEED_UNPACK+=" $(get_pkg_directory ${_p})"
 1334        done
 1335      fi
 1336  
 1337      # Automatically set PKG_SOURCE_NAME unless it is already defined.
 1338      # PKG_SOURCE_NAME will be automatically set to a name based on
 1339      # the $PKG_NAME-$PKG_VERSION convention.
 1340      #

=== SOURCE 2174265e9c:scripts/get_env (lines 1-22 of 22; the four names kept (PL-08))
    1  #!/usr/bin/env bash
    2  # Forward the environment into the build container -- minus anything that looks
    3  # like a secret.
    4  #
    5  # The whole exported environment used to go through. On a developer's machine
    6  # that is also their shell: API keys and access tokens for unrelated tools
    7  # landed in a world-readable .env in the worktree and inside every build
    8  # container. The four scraper and achievement credentials EmulationStation
    9  # compiles in are the exception -- they are the reason a build needs a secret
   10  # at all -- so they pass by name; everything else that looks like one is
   11  # dropped. Names, not values, are matched, so a variable holding a secret under
   12  # an innocent name still leaks: keep such things out of the shell that runs
   13  # make, or in ~/.ROCKNIX/options where only the build sees them.
   14  KEEP='^(SCREENSCRAPER_DEV_LOGIN|GAMESDB_APIKEY|CHEEVOS_DEV_LOGIN|HFS_DEV_LOGIN)$'
   15  DROP='(^|_)(KEY|KEYS|TOKEN|TOKENS|SECRET|SECRETS|PASSWORD|PASSWD|CREDENTIAL|CREDENTIALS|AUTH|APIKEY|API_KEY|PRIVATE)($|_)|^(AWS|GH|GITHUB|NPM|OPENAI|ANTHROPIC)_'
   16  for var in $(compgen -e); do
   17    [[ "$var" == PATH ]] && continue
   18    if [[ ! "$var" =~ $KEEP ]] && [[ "$var" =~ $DROP ]]; then
   19      continue
   20    fi
   21    echo "$var=${!var}"
   22  done

=== SOURCE 2174265e9c:projects/ROCKNIX/packages/virtual/image/package.mk (lines 1-50 of 113; PKG_UI)
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
    3  
    4  PKG_NAME="image"
    5  PKG_LICENSE="GPL"
    6  PKG_SITE="https://libreelec.tv"
    7  
    8  PKG_SECTION="virtual"
    9  PKG_LONGDESC="Root package used to build and create complete image"
   10  
   11  PKG_DEPENDS_TARGET="toolchain squashfs-tools:host dosfstools:host fakeroot:host kmod:host \
   12                      mtools:host populatefs:host libc gcc linux linux-drivers linux-firmware \
   13                      ${BOOTLOADER} busybox lsof umtprd util-linux usb-modeswitch jq socat \
   14                      p7zip file grep util-linux btrfs-progs zstd lz4 empty lzo libzip \
   15                      bash coreutils system-utils autostart quirks powerstate sdl2notify \
   16                      gzip six xmlstarlet pyudev dialog network mako-osd rocknix"
   17  
   18  PKG_UI="emulationstation es-themes textviewer lowerdeck"
   19  
   20  PKG_UI_TOOLS="fbgrab grim"
   21  
   22  PKG_GRAPHICS="imagemagick"
   23  
   24  PKG_FONTS="corefonts noto-sans-cjk"
   25  
   26  PKG_MULTIMEDIA="ffmpeg vlc mpv gmu m8c"
   27  
   28  PKG_SOUND="espeak libao"
   29  
   30  PKG_SYNC="synctools"
   31  
   32  PKG_TOOLS="patchelf i2c-tools evtest"
   33  
   34  PKG_DEBUG="debug"
   35  
   36  if [ "${BASE_ONLY}" = "true" ]
   37  then
   38    EMULATION_DEVICE=no
   39    ENABLE_32BIT=no
   40    PKG_DEPENDS_TARGET+=" ${PKG_TOOLS} ${PKG_FONTS} misc-packages"
   41  else
   42    PKG_DEPENDS_TARGET+=" ${PKG_TOOLS} ${PKG_FONTS} ${PKG_SOUND} ${PKG_SYNC} ${PKG_GRAPHICS} ${PKG_UI} ${PKG_UI_TOOLS} ${PKG_MULTIMEDIA} misc-packages"
   43  
   44    # GL demos and tools
   45    [[ ! -z "${OPENGL_SUPPORT}" ]] && PKG_DEPENDS_TARGET+=" mesa-demos"
   46  
   47    # GLmark2
   48    [[ ! -z "${OPENGLES_SUPPORT}" ]] && PKG_DEPENDS_TARGET+=" glmark2"
   49  
   50    # Vulkan demos and tools

=== SOURCE 2174265e9c:projects/ROCKNIX/packages/virtual/emulators/package.mk (lines 40-110 of 1777; armsx2-sa's devices (PL-05))
   40  case "${DEVICE}" in
   41    H700|RK3326)
   42      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 desmume-lr gpsp-lr pcsx_rearmed-lr"
   43      PKG_DEPENDS_TARGET+=" common-shaders glsl-shaders"
   44      PKG_EMUS+=" drastic-sa mednafen"
   45      LIBRETRO_CORES+=" uae4arm-lr"
   46      ;;
   47    RK3399)
   48      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 desmume-lr gpsp-lr pcsx_rearmed-lr"
   49      PKG_EMUS+=" aethersx2-sa armsx2-sa dolphin-sa drastic-sa mednafen melonds-sa nanoboyadvance-sa"
   50      LIBRETRO_CORES+=" beetle-psx-lr bsnes-lr bsnes-hd-lr dolphin-lr uae4arm-lr"
   51      ;;
   52    RK3566|RK3576)
   53      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 desmume-lr gpsp-lr pcsx_rearmed-lr"
   54      PKG_DEPENDS_TARGET+=" common-shaders glsl-shaders"
   55      PKG_EMUS+=" aethersx2-sa armsx2-sa azahar-sa dolphin-sa drastic-sa mednafen melonds-sa vita3k-sa"
   56      LIBRETRO_CORES+=" dolphin-lr uae4arm-lr"
   57      ;;
   58    RK3588)
   59      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 desmume-lr gpsp-lr pcsx_rearmed-lr"
   60      PKG_EMUS+=" aethersx2-sa armsx2-sa azahar-sa dolphin-sa drastic-sa mednafen melonds-sa supermodel-sa vita3k-sa"
   61      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr uae4arm-lr"
   62      ;;
   63    SM6115)
   64      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 desmume-lr gpsp-lr pcsx_rearmed-lr"
   65      PKG_EMUS+=" aethersx2-sa azahar-sa dolphin-sa drastic-sa mednafen melonds-sa supermodel-sa vita3k-sa armsx2-sa"
   66      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr uae4arm-lr"
   67      ;;
   68    # TODO: cemu and xemu testing, drop if unplayable
   69    SM4450)
   70      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 daedalusx64-sa desmume-lr gpsp-lr pcsx_rearmed-lr"
   71      PKG_EMUS+=" aethersx2-sa azahar-sa bigpemu-sa cemu-sa dolphin-sa heroic mednafen melonds-sa nanoboyadvance-sa supermodel-sa xemu-sa \
   72                  skyemu-sa steam vita3k-sa armsx2-sa"
   73      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr kronos-lr uae4arm-lr"
   74      ;;
   75    SM8250)
   76      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 daedalusx64-sa desmume-lr gpsp-lr pcsx_rearmed-lr"
   77      PKG_EMUS+=" aethersx2-sa azahar-sa bigpemu-sa cemu-sa dolphin-sa heroic mednafen melonds-sa nanoboyadvance-sa rpcs3-sa supermodel-sa \
   78                  xemu-sa skyemu-sa steam vita3k-sa armsx2-sa"
   79      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr kronos-lr uae4arm-lr"
   80      ;;
   81    SM8550)
   82      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 daedalusx64-sa desmume-lr gpsp-lr pcsx_rearmed-lr"
   83      PKG_EMUS+=" aethersx2-sa ares-sa azahar-sa bigpemu-sa cemu-sa dolphin-sa drastic-sa gopher64-sa heroic mednafen melonds-sa nanoboyadvance-sa rpcs3-sa supermodel-sa \
   84                  xemu-sa skyemu-sa steam vita3k-sa armsx2-sa"
   85      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr kronos-lr uae4arm-lr"
   86      ;;
   87    SM8650|SM8750)
   88      PKG_EMUS+=" aethersx2-sa ares-sa azahar-sa bigpemu-sa cemu-sa dolphin-sa gopher64-sa heroic mednafen melonds-sa nanoboyadvance-sa rpcs3-sa supermodel-sa \
   89                  xemu-sa skyemu-sa steam vita3k-sa armsx2-sa"
   90      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr kronos-lr uae4arm-lr"
   91      ;;
   92    S922X)
   93      [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 pcsx_rearmed-lr"
   94      PKG_EMUS+=" aethersx2-sa azahar-sa bigpemu-sa dolphin-sa drastic-sa duckstation-sa melonds-sa vita3k-sa armsx2-sa"
   95      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr uae4arm-lr"
   96      ;;
   97    GENERIC_X64)
   98      # Native standalone Dolphin supports the developer VM qualification path.
   99      PKG_EMUS+=" dolphin-sa"
  100      ;;
  101    AMD64)
  102      PKG_EMUS+=" ares-sa azahar-sa cemu-sa dolphin-sa gopher64-sa mednafen melonds-sa nanoboyadvance-sa \
  103                  xemu-sa skyemu-sa vita3k-sa armsx2-sa"
  104      LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr"
  105  esac
  106  
  107  # GENERIC_X64 (x86_64): drop libretro cores that don't yet build for x86_64.
  108  # These are tracked in issue #16 to fix/re-enable per-core later (e.g. parallel-n64-lr's
  109  # x86 hacktarux dynarec defines fsqrt(), which collides with glibc's C23 fsqrt).
  110  if [ "${DEVICE}" = "GENERIC_X64" ]; then

=== SOURCE docs/audits/2026_11_01-epic-m6-es-recipe/02-forward-audit.md (lines 1-541 of 541; the lane's draft)
    1  # T37 (#684) forward audit -- the EmulationStation recipe and themes in the distribution
    2  
    3  Stage B, 2026-11-01, the T3 session (Opus 5.5, high), at the distribution tip `2ce981005e`
    4  (reviewed-at `9fa740a91b`; the slice's bytes are `2174265e9c`'s, `ui/` unchanged since:
    5  `stage-a/s5-runs.out` R03, R22). `reviewed-at-es: none -- no ES change`. Every count is a tool's
    6  own line in the file named beside it; `proved:` is one of `tree`, `history`, `tool-run`,
    7  `fixture`, `guest`, `fix-fixture`, `fix-image-pending`, `design`. Every read of
    8  `emulationstation/package.mk` went through the mask with `:39` withheld by line number (`W39`,
    9  the coordinator's answer 3 of 6551707733). The three generated tables (Coverage, The patches, The
   10  currency) are `tools/t37-tables.py`'s output, each seen to exit 1 on a constructed drift before it
   11  was trusted (`stage-b/tables-*-drift.out`: `ASSERT FAIL: coverage rows 14 != 15`, `ASSERT FAIL:
   12  rows 29 (es 14, theme 15) != 30 (15, 15)`, `ASSERT FAIL: currency rows 13 != 14`).
   13  
   14  ## Coverage
   15  
   16  The inventory's 15 (`01` § Scope), one row each; inventory tier beside git's class against the
   17  base `c445081a59` (`behind`: the blob equals the base's and not `upstream/next`'s; `overlap`: both
   18  sides moved it). `python3 -B -I tools/t37-tables.py --repo <worktree> --tiers
   19  stage-a/block-2.txt coverage`, `rc=0` (`stage-b/tables-coverage.out`):
   20  
   21  | File under `projects/ROCKNIX/packages/ui/` | Lines (`grep -c ''`) | Inventory tier | Git class against the base (`c445081a59`; behind: equal to the base and not to `upstream/next`) | Fork stat | What it is |
   22  | --- | ---: | --- | --- | ---: | --- |
   23  | `emulationstation/autostart/001-emulationstation` | 13 | upstream-carried | upstream-carried | -- | boot step: links /storage/.emulationstation to /storage/.config/emulationstation |
   24  | `emulationstation/config/common/es_features.cfg` | 2039 | upstream-carried | upstream-carried, behind | -- | per-emulator feature catalogue |
   25  | `emulationstation/config/common/es_input.cfg` | 1810 | upstream-carried | upstream-carried | -- | controller database |
   26  | `emulationstation/config/common/es_savestates.cfg` | 26 | fork-own | fork-added | 26 | save-state layout (retroarch) |
   27  | `emulationstation/config/common/es_settings.cfg` | 3 | upstream-carried | upstream-carried | -- | an empty <config> seed |
   28  | `emulationstation/package.mk` | 141 | fork-own | fork-modified, overlap | 47 | the ES recipe: clone of the fork's ES at the pin; depends, cmake options, credentials by name, install steps |
   29  | `emulationstation/sources/es_settings` | 52 | upstream-carried | upstream-carried | -- | ExecStartPre: timezone, locale, environment import |
   30  | `emulationstation/sources/serial_number_check` | 27 | upstream-carried | upstream-carried | -- | the serial number check |
   31  | `emulationstation/sources/start_es.sh` | 8 | upstream-carried | upstream-carried, behind | -- | sources es_settings and runs ES |
   32  | `emulationstation/system.d/emustation.service` | 20 | upstream-carried | upstream-carried, behind | -- | the non-sway unit |
   33  | `emulationstation/system.d/essway.service` | 21 | fork-own | fork-modified, overlap | 3 | the sway unit, with sway-ready before start |
   34  | `lowerdeck/package.mk` | 17 | upstream-carried | upstream-carried | -- | lowerdeck at its pin, copied to /usr/share/lowerdeck |
   35  | `themes/es-theme-art-book-next/package.mk` | 28 | fork-own | fork-modified | 2 | the theme at its pin, with the wordmark, the licence, five artwork sets removed, a zh font block |
   36  | `themes/es-theme-art-book-next/sources/Tiny5-OFL.txt` | 93 | fork-own | fork-added | 93 | the Tiny5 font licence |
   37  | `themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg` | 263 | fork-own | fork-added | 263 | the wordmark |
   38  
   39  generated, asserted: rows 15, lines 4561, inventory fork-own 6 upstream-carried 9, git classes {'fork-added': 3, 'fork-modified': 3, 'upstream-carried': 9}
   40  
   41  **The four patches under the glob are not rows** (ruling (a)): `emulationstation/patches/x86_64/cpugov.patch`
   42  (27 lines, inventory `vendor-carried`, git upstream-carried) is **T40's**; the theme's
   43  `patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch` (20, `vendor-carried`, git
   44  upstream-carried), `patches/001-pixelelated-splash.patch` (31, `vendor-carried`, git fork-added)
   45  and `patches/001-tools-always-show-image.patch` (11, `vendor-carried`, git fork-added) are
   46  **T42's** (`stage-a/block-2.txt` `CLAIMS`; 89 lines together, `stage-a/s5-runs.out` R02). They
   47  are read here only as the recipe reaches them (§ The patches).
   48  
   49  ## The leads
   50  
   51  L-01 to L-22 (L-14 and L-15 folded by R2, § 3); the FAIL-first five first. Lines at `2174265e9c`.
   52  **Family**: *fail-open* (a guard that fails open), *install* (an install step whose output is not
   53  what its line says), *build order* (a dependency taken by build order), *structure* (a structure or
   54  merge-debt fact), *currency* (a currency fact). **Disposition** at stage B is the lane's proposal;
   55  the pause decides (§ 9's rows: fribidi, the link, the patch directory, the freshness tool's reach,
   56  a loud catalog, the ARMSX2 block).
   57  
   58  | Lead | Lines | Family | Owner | Proved | What the read shows | Proposed disposition |
   59  | --- | --- | --- | --- | --- | --- | --- |
   60  | **L-02** | `emulationstation/patches/x86_64/`; `scripts/unpack:127-128`, `:137-160` | fail-open | T37 (`PKG_PATCH_DIRS`), T40 (the patch, #1072) | tool-run | `patches/x86_64/: NOT REACHED` on all 15 devices (§ The patches): `PATCH_ARCH` is `x86` for an `x86_64` target (`:127-128`), the recipe sets no `PKG_PATCH_DIRS`, and outside recipes only `scripts/unpack:137-138` read it (`stage-b/reads.out` B01). Intent: `git log --diff-filter=A` prints `40fce2a089 2026-08-20 amd64: wip am64 changes`; `-S cpugov` prints `0` commits (the word is the file's name). Its hunk header `@@ -745,12 +745,20 @@` | **take up as #1072** (not a new bug); T37's half at the pause: a recipe line `PKG_PATCH_DIRS="x86_64"` (reaches `patches/x86_64/` on every `x86_64` device, and the patch's text unchanged) against T40's rename to `patches/x86/`; only one of the two lands, and the build is the only proof the patch applies (#1072 `:29`). The checker's step 4 FAILs here at stage C |
   61  | **L-03** | `emulationstation/package.mk:101` | install | T37 (#613 if routed) | tree, history | `ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/...`: `INSTALL` is `$BUILD/install_pkg/emulationstation-<pin>` there (`scripts/build:140`, `config/functions:1380`), and neither `scripts/install` nor `scripts/image` rewrites a link (`01` open item 2), so the image carries a build-host target. Upstream's form at `c445081a59:74` and `651150fc88:75`; `-S` for the device-path form prints `0` commits (B02). The other six links of the two functions take device paths (`:84`, `:97`, `:100`, `:134`, `:137`, `:140`; s5-runs R17) | **take up as #613** -- the fix `ln -sf /usr/config/emulationstation/es_systems.cfg ...` in this slice's stream if the coordinator routes it; a #585 line (upstream's form); G-03 reads the candidate's corrected link (ruling (h)). The checker's step 5 FAILs here |
   62  | **L-07** | `emulationstation/package.mk:70-75`; `sources/es_settings:26-35` | fail-open | T37 | tree, history | the host's `localedef` pre-generates `en_US.UTF-8` and ends `\|\| true` (`:75`), so its failure is silent; `es_settings:26-35` regenerates a missing locale at first start, so the cost of a silent failure is first-boot time (*"a minute or two on RK3326"*, `:71`). Added by `96d387fffd 2025-12-22 emulationstation: pre-generate locale to spped up first boot on lower-end devices`, upstream's (`localedef` lines: `1` at both upstream hashes; B04) | **record as written** (a best-effort cache with a correct fallback), the checker's step 5 WARN quoting `:75`; a loud variant (warn in the build log on failure) is a stream question, not a defect. G-03 reads `/usr/config/locale/en_US.UTF-8` on the candidate |
   63  | **L-08** | `emulationstation/package.mk:67-68`; the pin's `CMakeLists.txt:565-578`, `locale/CMakeLists.txt:9`, `:25`, `:31` | fail-open | T37 (the install line); the integration (ES's CMake, ruling (f)) | tree, tool-run | with no `msgfmt`, `msgmerge`, `xgettext` or `Intl`, ES's CMake prints `Native language support disabled.` and builds no `.mo` (`:573-578`); the recipe then copies whatever `locale/lang/` holds (`:68`), so French (D-UI-051) would be absent with no error. The tools reach ES's build by build order: `gettext:host` is in ES's plan through `toolchain -> gcc:host -> autoconf:host -> gettext:host` (`01` open item 3). Whether ES's CMake found them in a given build is its configure log's (`CANNOT`) | **a stream question at the pause** ("a loud catalog"): a `makeinstall_target` line that fails when `${PKG_BUILD}/locale/lang/fr/LC_MESSAGES/emulationstation2.mo` is absent (fork-own lines; moves only ES's stamp). G-03 reads the candidate's `.mo` |
   64  | **L-04** | `emulationstation/package.mk:79` against `:81-82` | install | T37 | tree, history | `rm -f .../resources/logo.png` runs before `resources/` is made (`:81`) and filled (`:82`), so it removes nothing and the pin's `resources/logo.png` (a blob at the pin) ships; its reader is the pin's `es-core/src/Splash.h:17`, `#define DEFAULT_SPLASH_IMAGE ":/logo.png"`. Upstream's order too (`c445081a59:52` before `:54`; `651150fc88:53` before `:55`); `-S logo.png` prints `9f1fab30f6 2025-07-13 projects: add modifications for ROCKNIX`, upstream's first line (B03) | **a question at the pause, not a defect**: the line's effect is none; had it worked it would remove ES's default splash image. Proposed: drop the line (the shipped behaviour unchanged, the recipe says what it does) -- or record as written with a #585 note; G-05 reads `logo.png` on the candidate. The checker's step 5 FAILs here |
   65  | L-01 | `emulationstation/package.mk:125-129`; `es_features.cfg:1331`, `:1333`, `:1393`; `virtual/emulators/package.mk:49-103` | structure | T37 | history, fixture | upstream's block (`651150fc88:104-108`: `armsx2-sa`'s *vulkan driver* feature deleted except on `SM4450\|SM6115\|SM8250\|SM8550\|SM8650`) is absent at the tip: every one of the four merges `a06539d8ec`, `049765fba0`, `fa2990c1e7` (2026-09-29) and `f370dc8787` (2026-10-12) had an upstream parent with `2` ARMSX2 lines and a result with `0` (`stage-b/l01-merges.out`); the tip's catalogue holds `1` such feature (B13, `xml.etree`) and installs it on every `armsx2-sa` device (`virtual/emulators/package.mk:49`, `:55`, `:60`, `:65`, `:72`, `:78`, `:84`, `:89`, `:94`, `:103`) | **a bug candidate for the pause** ("the ARMSX2 block"): restore upstream's five lines after `:128` (fork-own lines; moves only ES's stamp; a device built from the tip offers a Turnip driver it does not have, RK3566 of the fork's devices). The fixture with upstream's two `xmlstarlet` edits reproduced in `xml.etree` is stage C's (upstream `0`, tip `1`) |
   66  | L-05 | `emulationstation/package.mk:42-44`; `scripts/get_env:14-15`; the pin's `CMakeLists.txt:303-305`, `:328-330` | fail-open | T37 | tree | the loop logs `SCREENSCRAPER_DEV_LOGIN`, `GAMESDB_APIKEY`, `CHEEVOS_DEV_LOGIN` (B09); `get_env:14` forwards those three and `HFS_DEV_LOGIN`, which builds the HFS scraper (`CMakeLists.txt:328-330`; read at the pin's `HfsDBScraper.cpp:1`, `:181`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33` -- `:181` beyond the brief's list, s5-runs R10) with no `USING:` line; `SCREENSCRAPER_SOFTNAME` (`:303-305`) is neither logged nor in `get_env`'s keep list, so it reaches ES only in a native build | **a stream candidate**: `HFS_DEV_LOGIN` added to `:42-44`'s list (names only; fork-own lines). The count of `USING:` lines with the four placeholders is stage C's sandbox fixture (4 loud, 3 at the tip) |
   67  | L-09 | `emulationstation/package.mk:13`; `SDL2/package.mk`, `swaywm-env`, `sway`, `pango` | build order | T37 (D-WORKFLOW-216) | tool-run | ES's plan reaches fribidi only by `emulationstation:target -> SDL2:target -> swaywm-env:target -> sway:target -> pango:target -> fribidi:target`, on GENERIC_X64 and H700 alike (`01`, trace.out); no `libass` in ES's plan; an `arm` plan builds no ES. **T36's G-01 on the candidate image reads `libfribidi` NOT linked** while the pin links `${FRIBIDI_LIBRARIES}` when the `QUIET` find succeeds (`CMakeLists.txt:236-241`, `:375`, `:462`), so that build's find failed | **the pause's** (D-WORKFLOW-216): declare `fribidi` in `:13` or record the chain as the recipe's decision with the `QUIET` branch named. Either way the candidate shipped the built-in reordering, and why its find failed is the integration's build's configure log (`CANNOT` here, inherited) |
   68  | L-19 | `emulationstation/package.mk:14`; `config/functions:1114`, `:1126` | fail-open | T37 | tree, history | `PKG_NEED_UNPACK="busybox"` is added to the stamp's path list as a bare word (`:1114`); `find -L busybox` from the root finds `0` files, while the package's directories are `packages/sysutils/busybox` and `projects/ROCKNIX/packages/sysutils/busybox`; no script reads the variable (`scripts/ readers: 0`); the framework's own uses pass directories (`config/functions:1322`, `:1328`, `:1333`). Upstream's line at both hashes (`:11`), from `9f1fab30f6` (B07) | **a rule-6 candidate for the pause**: `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"` (the form `:1333` uses), which makes busybox's recipe move ES's stamp -- or drop the line if no ES build reads busybox (intent not recorded upstream). A #585 line. The checker's step 5 FAILs here |
   69  | L-06 | `emulationstation/package.mk:54` | install | T37 | tool-run | `echo a-b-c \| sed "s#-#_##g"` printed `a_b-c`: `#g` is a comment and only the first hyphen goes; `0` device names have a hyphen (B08); upstream's at `c445081a59:36`, `651150fc88:37` | **record as written** with a #585 line (`s#-#_#g`); no device is affected today (rule 6 governs a defect, and this one has no effect) |
   70  | L-10 | `tools/fork-package-freshness:16-18`, `:42-44`, `:89-93` | currency | T6 (the tool); the coordinator (`EXTRA_PACKAGES`) | tool-run | `lines=48 ui=0` (s5-runs R21): the three recipes are not in its reach | **Backlog lead** for the coordinator; whether the three join `EXTRA_PACKAGES` is the pause's |
   71  | L-21 | `tools/pkgcheck:157`, `:169`; `tools/fork-package-freshness:42-43` | fail-open | T6 | tool-run | `pkgcheck es-theme-no-such-package` `rc=0 lines=0` (R12); freshness exits 0 with a missing ref (proof C8) | **Backlog lead** naming the three fail-opens (ruling (d)), for the coordinator to file |
   72  | L-20 | `config/common/es_settings.cfg:1-3`; the pin's `Settings.cpp:252`, `CollectionSystemManager.cpp:1360-1366` | structure | -- | tree | the seed is an empty `<config>`, so `ThemeSet` starts at ES's `"system-theme"` and, with no such set installed, the first available set is chosen and saved (B10) | **design, recorded**; G-02 reads the installed themes and the setting the image chose |
   73  | L-11 | `emulationstation/package.mk:30`, `:39-40`, `:46` | design | D-WORKFLOW-166 | design | `:30` always passes the runtime flag and `:40` always supplies a pair, so the runtime rows never show in a recipe-built image and `:46`'s warning is unreachable for that key | **design** (D-WORKFLOW-166), recorded so no stream "fixes" it |
   74  | L-12 | `sources/serial_number_check:12`, `:20` | -- | upstream's (D-UI-079) | tree | `cat ${DEVICE_SERIAL_NUMBER_PATH}` unquoted (`:12`); *"storted"* in a log line (`:20`); `bash -n` rc 0 | **note**, outside the lanes |
   75  | L-13 | `sources/es_settings:12-13`, `:47-50` | -- | upstream's (D-UI-079) | tree | two timezone files rewritten in place (`:12-13`); `:47` imports unquoted words from `999-export` | **note**, outside the lanes |
   76  | L-16 | `emulationstation/package.mk:7` | currency | #990 (the tool), #528 (custody) | history | `git log -L7,7` prints `9f1fab30f6` (`+PKG_LICENSE="GPL"`), `3d7c075f63` 2026-10-02 (`GPL` to `MIT`) and `84ff94fb3d` 2026-10-13 (`MIT` to `MIT AND BSD-3-Clause`) (B06) | **read**: the expression is the source's (`84ff94fb3d` added the RVZ reader's BSD file, `:58-65`); #990's fix reads it from there |
   77  | L-17 | `device-builds.md` § Iterating on EmulationStation; `:8` | structure | the coordinator's sweep | tree | the rule names `maxengel/emulationstation-next` and `~/Development/emulationstation-next`; `PKG_SITE` is `https://github.com/pixelelated/emulationstation` | **doc drift** for the coordinator |
   78  | L-18 | `CLAUDE.md` (*"scope per device with `patches/<DEVICE>/`"*); `scripts/unpack:137-159` | structure | the coordinator's sweep | tree | a `patches/<DEVICE>/` directory under a package is reached only through `PKG_PATCH_DIRS` (`:137-145`); `:159` globs a device directory outside the package (`devices/<DEVICE>/patches/<pkg>/`), present for none of the three on any device (`stage-b/reach-15.out`: `0` project-side lines) | **doc drift** for the coordinator, or upstream's `PKG_PATCH_DIRS+=" ${DEVICE}"` (`651150fc88:14`) adopted with the merge (§ The currency) |
   79  | L-22 | the theme's XML at its pin; `themes/.../package.mk:21-27` | structure | -- | tree | read by hash (`01` § L-22): 25 `fontPath` elements, each with a `fontSize`, naming the four bundled fonts, each in the tarball; the one absolute path is the recipe's `zh` block, `/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` (`noto-sans-cjk`'s, T8's) | **sound**; the image half is a G-02 line (`candidate`) |
   80  
   81  **Found at stage B, beside the leads:**
   82  
   83  | Item | Lines | Family | Proved | What the read shows | Proposed disposition |
   84  | --- | --- | --- | --- | --- | --- |
   85  | PL-029's sibling | `system.d/emustation.service:12` | structure | tree | `ExecStart=/usr/bin/emulationstation --log-path /var/log --no-splash` carries the same flag as `start_es.sh:8` (B12) | with PL-029 (§ The recipe) |
   86  
   87  ### The take-up (§ 2), one row each
   88  
   89  | Found by | Lines | Disposition at stage B |
   90  | --- | --- | --- |
   91  | D-WORKFLOW-216 (`decision-register.md:777` at HEAD): fribidi | `:13` | L-09: **the pause's**, with T36's G-01 `libfribidi` NOT linked cited (`775d0893fe`'s `00:54`) |
   92  | D-WORKFLOW-216: the `:25` define | `:25` | **read** (§ The recipe: the define's chain); the three empty pairs named for T35 (the list) and T36 (the bodies) |
   93  | T2 PL-029 (`deferred:#684`) | `sources/start_es.sh:8` | **the pause's** (§ The recipe, PL-029): proposed *kept with the reason*; G-04 reads `/var/log/es_log.txt` |
   94  | #1072 | `patches/x86_64/`, the recipe | L-02: **the pause's**, T37's `PKG_PATCH_DIRS` against T40's rename |
   95  | #613 | `:101` | L-03: **fix if routed** |
   96  | #1193 | `config/common/*.cfg`, `:77-78` | **read** (§ The recipe, the seeds' modes) |
   97  | #990 | `:7` | L-16: **read** |
   98  | T20's RVZ notices | `:58-65` | **read** (§ The recipe, install row 1) |
   99  | The credentials (#566 CLOSED, #586, #64) | `:30`, `:39-44` | **read** (§ The recipe, credentials); #64's `:54` recorded |
  100  | The build options the neighbours read | `:13`, `:19-25` | **read** (§ The recipe, the `-D` table); udev and pugixml in § The dependencies |
  101  | NDEBUG; `CPPHTTPLIB_OPENSSL_SUPPORT` | the build type; `:19-25` | **read** (§ The recipe, derived rows) |
  102  | pugixml | `:13`, `:24` | **read** (§ The dependencies) |
  103  | The theme (D-UI-090) | `themes/.../package.mk:5`, `:7` | **read** (§ The themes) |
  104  | #69 | T42's Tools patch | **read**: its `:52` checkbox open, nothing sent (§ The themes) |
  105  | The splash wordmark | `themes/.../package.mk:17-18` | **read** (§ The themes) |
  106  | `lowerdeck` | `lowerdeck/package.mk` | **read** (§ The themes) |
  107  | Currency against ROCKNIX's recipe | the 14 files | **read** (§ The currency, generated) |
  108  | ES PRs through the distribution (D-WORKFLOW-012) | the recipe | **read** (§ The currency, the series) |
  109  | The lanes that name the recipe; iterating on ES | `:5`, `:6` | **read** (§ The recipe, the pin table) |
  110  | T36's § 5 item 3 and its stage-B lines | `:25` | **open until T36 hands back** (T36 at `775d0893fe`, in stage E) |
  111  | The pin bump's inputs | `:5`, `:6` | **integration** (§ What the integration inherits) |
  112  | #716; rapidjson; the earlier inherit lists; #1231; T35's `05` | -- | **none**, recorded |
  113  
  114  ## The recipe
  115  
  116  ### Q1 The pin and its bump
  117  
  118  | Item | Value | Source | Proved |
  119  | --- | --- | --- | --- |
  120  | The pin (`:5`) | `16dbac5211eea7e70db7394372033be2be7df829` | s5-runs R07, R14 | tree |
  121  | Its branch (`:6`) | `test/qa-integration`; local and `origin` both `16dbac5211` | R07, R08 | tree |
  122  | Its site (`:8-9`) | `https://github.com/pixelelated/emulationstation`, cloned (`PKG_URL=...git`, `GET_HANDLER_SUPPORT="git"` `:17`, `PKG_SHA256` empty) | R07, R14 | tree |
  123  | ROCKNIX's pin at the base | `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (site `ROCKNIX/emulationstation-next`) -- the pin's merge base with `rocknix/master` | R07, R08 | tree |
  124  | ROCKNIX's pin at `upstream/next` | `f6c542872e3850c5f432929ead219547a897cd4a`, `rocknix/master` itself | R07, R08 | tree |
  125  | The distance | the pin lacks `14` of `rocknix/master`'s commits (`7` first-parent merges) and is `724` ahead | R08 | tree |
  126  | The M7 candidate's ES | the same `PKG_VERSION` plus nine ES patches and a corrected link, recipe blob `35e5f45e79` (R3 § 2.2 C1, C2, § 2.3, cmd 21; ruling (h)); its `BUILD_ID` `069fc270442134fe771258418adf4e666e0473fb` (T36's G-01) and, at the window, G-01's own read | R3; G-01 | -- (cited) |
  127  | The identity sidecar | carries no ES pin (#1013) | #1013 | -- |
  128  | The bump's steps | the ES branches merged into `test/qa-integration`; `:5` moved to that tip in the same integration commit; the stamp cleared; the compiler sees every touched `.cpp` and the ES package is built before the pin lands on `next` (`device-builds.md` § Iterating on EmulationStation, `es-native-ui.md` § Before the pin moves); `tools/pkgcheck emulationstation` by name. **This slice moves nothing** (ruling (b)) | the rules | design |
  129  | The ES branches' tips at stage A | T34 `52f0ff5128` (local and `origin`); T35 `b7fdb3a24c` (9 ahead of the pin); T36 local at the pin (`0` ahead), no `origin` ref; the others per § 8 item 1, read at the integration's turn | `stage-a/open-items.out` | tree |
  130  | L-17 | the rule's repository names drift from `:8` | L-17 | tree |
  131  
  132  ### Q2 The build options, one row per `-D`
  133  
  134  The pin's `CMakeLists.txt` read by hash (`stage-a/s5-runs.out` R09, R10; the option lines read at
  135  stage B).
  136  
  137  | `-D` | Recipe line | CMake test at the pin | Branch it selects |
  138  | --- | --- | --- | --- |
  139  | `-DROCKNIX=1` | `:19` | `option(ROCKNIX ...)` `:23`; `if(ROCKNIX)` `:130-133` | `add_definitions(-DROCKNIX)`; e.g. `es-core/src/Paths.cpp:76-81` (`/storage`, `/var/log`) |
  140  | `-DDISABLE_KODI=1` | `:20` | `:26`; `:141-145` | no `-D_ENABLE_KODI_` |
  141  | `-DENABLE_FILEMANAGER=0` | `:21` | `:25`; `:149-152` | no `-D_ENABLE_FILEMANAGER_` |
  142  | `-DCEC=0` | `:22` | `option(CEC "CEC" ON)` `:18`; `:274-279`, `:297-300`, `:399`, `:494` | `CEC disabled`: no `find_package(libCEC)`, no `-DHAVE_LIBCEC` |
  143  | `-DENABLE_PULSE=1` | `:23` | `:27`; `:247-250`, `:387-391`, `:481-484` | `find_package(PulseAudio REQUIRED)`, `-D_ENABLE_PULSE_`, its include and library |
  144  | `-DUSE_SYSTEM_PUGIXML=1` | `:24` | `:29`; `:393-396`; the library at `:469` | `find_package(pugixml REQUIRED)`: the system `pugixml` (in `:13`) |
  145  | `-DGLES3=1` | `:25` | `option(GLES3 ...)` `:5`; the four exclusive `:9-16`; `:164-165`; `:213-214`; `:362-363` | `GLSystem "OpenGL ES 3.0"`, `find_package(OpenGLES3 REQUIRED)`, `-DUSE_OPENGLES_30`; and in `es-core/CMakeLists.txt:278-280` the `Renderer_GLES30` listing |
  146  | `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1` | `:30` | `:311-318` | `add_definitions(-DSCREENSCRAPER_RUNTIME_DEV_LOGIN...)`; a compiled pair hides the rows (`:313-315`, L-11) |
  147  | `-DBATTERYPLUS=1` | `:33`, when `BATTERYPLUS_SUPPORT=yes` (H700 `options:49`, S922X `:53`; empty on GENERIC_X64, R14) | `:135-138` | `-DBATTERYPLUS` |
  148  
  149  **Derived, not passed:** `DEVICE` upper-cased by `:54` (L-06) feeds `:115-117`
  150  (`-DHW_DEVICE="<DEVICE>"`, `-D<DEVICE>`); `HAVE_UDEV` from `find_package(udev)` (`:255-261`);
  151  `_ENABLE_TTS_` not defined (`ENABLE_TTS` defaults `OFF`, `:28`, `:263-272`); `HAVE_LIBCEC` not
  152  defined (`CEC=0`); `HAVE_INTL` from the gettext tools and `Intl` (`:568-578`, L-08); `HAVE_FRIBIDI`
  153  from the `QUIET` find (`:236-241`, L-09); `ES_BUILD_TESTS` `OFF` (`:35`); the build type `Release`
  154  (`scripts/build:152`, passed at `:174`) and `-DNDEBUG` in `TARGET_CFLAGS`/`TARGET_CXXFLAGS` when not
  155  a debug build (`config/functions:385-388`) -- NDEBUG is the build system's, not a recipe line;
  156  `CPPHTTPLIB_OPENSSL_SUPPORT` is defined nowhere (`es-app-views-scrapers.md:882-887`, cited), so the
  157  HTTP server is plain HTTP. `proved: tree`.
  158  
  159  **The define's chain** (D-WORKFLOW-216's `:25`): `GLES3` selects `GLSystem "OpenGL ES 3.0"`
  160  (`:164-165`), and that one value both adds `-DUSE_OPENGLES_30` (`:362-363`) and lists
  161  `Renderer_GLES30.{h,cpp}` (`es-core/CMakeLists.txt:278-280`, `if(${GLSystem} MATCHES "OpenGL ES
  162  3.0")`); the define compiles no source. `Renderer_GLES20` is the `else` (`:281-283`) and never
  163  compiled here; `Renderer_GL21` and `Renderer_GLES10` are listed unconditionally (`:244-245`). No
  164  device `case` surrounds `:25`, so every device builds the GLES 3.0 renderer, and every device's
  165  `${OPENGLES}` is `mesa` with `-Dgles2=enabled` (`01` open item 9). **The list is T35's, the
  166  bodies T36's, the define T37's**; a change to any is reconciled with the other two at the
  167  integration (§ What the integration inherits item 4). `proved: tree`.
  168  
  169  ### Q2 The install steps, one row each
  170  
  171  | Lines | What it installs | How it fails | Lead |
  172  | --- | --- | --- | --- |
  173  | `:58-65` | `LICENSE.rvz-padding` and `RVZ-NOTICES.md` to `/usr/share/licenses/emulationstation/` when the pin's `external/libcheevos/LICENSE.rvz-padding` exists (it does, R2 cmd 28) | silently skipped on an older pin, by design (`:58-59`); T20's records, #528's custody | -- |
  174  | `:67-68` | `${PKG_BUILD}/locale/lang/*` to `/usr/config/locale` | copies whatever the ES build left; no `.mo` without the gettext tools, and no error | L-08 |
  175  | `:70-75` | the pre-generated `en_US.UTF-8` | `\|\| true`: silent; first boot regenerates | L-07 |
  176  | `:77-78` | the four `.cfg` seeds to `/usr/config/emulationstation`, by `cp -a` (git modes `100644` for all four, B11) | -- | #1193 |
  177  | `:79` | nothing (the `rm` precedes the directory) | the pin's `logo.png` ships | L-04 |
  178  | `:81-85` | the pin's `resources/*`; `DroidSansFallbackFull.ttf` replaced by a link to `/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` | a missing `noto-sans-cjk` file leaves a dangling link (G-05) | L-22 |
  179  | `:87-90` | `es_settings`, `start_es.sh`, `serial_number_check` from `${PKG_BUILD}` (`scripts/unpack` copies `sources/*` into the unpack) | -- | -- |
  180  | `:92-94` | the binary to `/usr/bin` (`:93` a commented link) | -- | -- |
  181  | `:96-97` | `/etc/timezone` -> `/storage/.cache/system_timezone` | -- | -- |
  182  | `:99-101` | `/etc/emulationstation/themes` -> `/storage/.config/emulationstation/themes`; **`/etc/emulationstation/es_systems.cfg` -> a build-host path** | the second dangles on a device | L-03, #613 |
  183  | `:104-123` | a tools-only `es_systems.cfg`, only when `EMULATION_DEVICE=no` or `BASE_ONLY=true` (neither on GENERIC_X64, R14) | -- | -- |
  184  | `:125-128` | the vulkan choices deleted when `VULKAN_SUPPORT` is not `yes` (`yes` on GENERIC_X64, so the catalogue ships whole there) | -- | L-01 (the block it lost) |
  185  | `:132-140` | `/usr/share/locale` -> `/storage/.config/locale`, `/usr/lib/locale` -> `/usr/share/locale`, the ES `locale` -> `/usr/share/locale` | -- | -- |
  186  | `scripts/install:96-99`, `:107-109` | `autostart/*` to `/usr/lib/autostart/common` (mode 0755) and `system.d/*.*` to `/usr/lib/systemd/system` -- the build system's conventions, not the recipe's lines | -- | -- |
  187  
  188  `proved: tree`. **#1193, this recipe's half:** the ES recipe installs its four seeds by `cp -a`
  189  from files git records `100644` (B11); the `/usr/config/system/configs/system.cfg` seed #1193 names
  190  at 0645 is not installed by any of the 15 -- the issue's own checkbox for its build step is the
  191  coordinator's (`#1193` `:20`), named here, not traced further in this slice.
  192  
  193  **PL-029** (`start_es.sh:8`, `deferred:#684`): `--log-path` is parsed nowhere at the pin
  194  (`es-app/src/main.cpp`: `0` lines naming it; `parseArgs` `:75-298`), and under `-DROCKNIX`
  195  `es-core/src/Paths.cpp:76-81` sets `mLogPath = "/var/log"`, which `es-core/src/Log.cpp:258-259`
  196  makes `/var/log/es_log.txt` -- so the flag is inert and the path holds. Its sibling is
  197  `emustation.service:12`. Both are upstream's lines (`c445081a59` `start_es.sh:8`, `651150fc88`
  198  `:14`). **Proposed: kept with the reason** -- inert, and editing either makes an upstream-carried
  199  file fork-modified, one of them (`start_es.sh`) already behind upstream; a #585 line instead. G-04
  200  reads `/var/log/es_log.txt` on the candidate. `proved: tree`.
  201  
  202  ### Q4 The build credentials, by name
  203  
  204  | Name | Recipe line | ES's CMake | `get_env` | Logged |
  205  | --- | --- | --- | --- | --- |
  206  | `SCREENSCRAPER_RUNTIME_DEV_LOGIN` | `:30` (the option, value `1`) | `:311-318` | -- (an option, not an environment name) | -- |
  207  | `SCREENSCRAPER_DEV_LOGIN` | `:40` (exported, defaulting to the shared identity built from `:39`'s local; value never printed), `:42` | `:307-309` | `:14` keep | yes |
  208  | `GAMESDB_APIKEY` | `:43` | `:320-322` | `:14` keep | yes |
  209  | `CHEEVOS_DEV_LOGIN` | `:44` | `:324-326` | `:14` keep | yes |
  210  | `HFS_DEV_LOGIN` | none | `:328-330` | `:14` keep | **no** (L-05) |
  211  | `SCREENSCRAPER_SOFTNAME` | none | `:303-305` | not kept | no |
  212  
  213  `count lines: 5` (`:30`, `:40`, `:42`, `:43`, `:44`; s5-runs R18), names and line numbers only. The
  214  recipe passes no credential to cmake: ES's CMake reads the environment (R10). D-WORKFLOW-166's
  215  route holds: a recipe-built image compiles the shared pair (`:40`) and the runtime option (`:30`),
  216  so its developer rows are hidden (L-11). **#64's open checkbox `:54`** (*"An upstream-style build
  217  (no runtime flag, `SCREENSCRAPER_DEV_LOGIN` set) shows no new rows and behaves as before."*) is
  218  **not answerable from this recipe**: it always passes the runtime flag; the CMake read says the
  219  runtime define comes only from that option or the environment (`:316`), so an upstream-style build
  220  defines none, but the observation is a build's -- recorded for #64, `CANNOT` here. #586
  221  (replacement credentials) is not a current gate. G-05 counts names in the binary (`0` expected; the
  222  macro names do not survive compilation) and the state check runs on the host (§ The guest cycle).
  223  `proved: tree`.
  224  
  225  ## The dependencies
  226  
  227  **Effective `PKG_DEPENDS_TARGET`**, sourced in the export (ruling (k)): GENERIC_X64 `boost
  228  toolchain SDL2 freetype curl freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool
  229  poppler pugixml noto-sans-cjk zstd mesa` (s5-runs R14); H700 the same 19 wants
  230  (`stage-a/trace.out`: `emulationstation:target build wants (19)`, identical lists on both). The
  231  theme `toolchain noto-sans-cjk`; `lowerdeck` `toolchain Python3 SDL2 SDL2_image SDL2_ttf` (R14).
  232  
  233  **L-09's chain, each link's effective value** (`stage-a/trace.out`, from pkgjson in the export):
  234  `SDL2` (local) `toolchain alsa-lib systemd dbus pulseaudio libdrm mesa glu mesa vulkan-loader
  235  vulkan-headers wayland swaywm-env`; `swaywm-env` (local) `sway wlr-randr swayimg rocknix-screenshot`;
  236  `sway` (local) `... cairo pango libjpeg-turbo ...`; `pango` (global) `toolchain cairo freetype
  237  fontconfig fribidi glib json-glib harfbuzz`; `fribidi` (global) `toolchain`. The chain holds on
  238  GENERIC_X64 and H700; it breaks if SDL2's `arm` branch or a device's `WINDOWMANAGER` changes, and
  239  an `arm` plan builds no ES (`01` open item 5). `vlc` (local) declares no `libass` and no fribidi.
  240  **The candidate shipped without fribidi** (T36's G-01) -- the pause's question, with the decision
  241  D-WORKFLOW-216 hands here. `proved: tool-run`.
  242  
  243  **udev**: `:13` names none; ES's plan reaches `systemd:target` through `SDL2` (trace.out), and
  244  `HAVE_UDEV` comes from `find_package(udev)` -- build order, as fribidi. **pugixml**:
  245  `-DUSE_SYSTEM_PUGIXML=1` and `pugixml:target` in ES's plan (trace.out), so the image links the
  246  system library where the lanes' host harnesses used the ES gitlink's copy (R4 item 23). **mesa**:
  247  `${OPENGLES}` is `mesa` on all 15 devices with `-Dgles2=enabled` (`01`). **L-19** above. The
  248  dependencies' recipes are T7's, T8's, T22's and T23's (`stage-a/block-2.txt` `DEPS`). `proved:
  249  tool-run`.
  250  
  251  ## The themes and `lowerdeck`
  252  
  253  | Package | Pin | `PKG_SHA256` | Licence | Install (`makeinstall_target`) | At its author's `HEAD` (R1 C20, 2026-10-31) |
  254  | --- | --- | --- | --- | --- | --- |
  255  | `es-theme-art-book-next` | `9a50ef366e750aabfab29e6915a2867607212971` (`upstream/next`'s too, R07) | `7ee1e93f2c4e4f7385b78680ecfa3828acf12bc616e2111d23cc66a524231125` (the cached tarball's sha256 equal, `01` § L-22) | `CUSTOM` (`:7`) | `:15-16` the tarball to `/usr/share/themes/es-theme-art-book-next`; `:17-18` the wordmark and `Tiny5-OFL.txt` (the fork's); `:19` five artwork sets removed; `:20` four of their includes deleted (`classic` has none); `:21-27` the `zh` font block appended to `fonts.xml` | yes: the pin is its author's `HEAD` |
  256  | `lowerdeck` | `ab735114ab318a84e4d28c9c5f1b154e450a579a` (ROCKNIX's too) | `2677d3ce675b9704487f9f09f82728b56009f9fa7c36403086e9c655af108f42` | `GPL-2.0-or-later` (`:7`) | `:14-17` the tarball to `/usr/share/lowerdeck` | **no**: its author's `HEAD` was `8fefe16e9c`, by a count nobody made (no fetch, ruling (e)) |
  257  
  258  - **The three theme patches** (T42's text): applied in name order by `scripts/unpack:150`'s
  259    `patches/*.patch` glob, which REACHES the theme's `patches/` on all 15 devices (§ The patches):
  260    `0001-system-style-...` before `001-pixelelated-splash` before `001-tools-always-show-image`
  261    (R2 § 3: they apply at the pin). Two share the `001-` prefix.
  262  - **#69's upstream offer**: its `:52` checkbox (*"Patch offered upstream to the theme repository"*)
  263    is open; nothing is sent (D-UI-090, D-WORKFLOW-165, #585).
  264  - **The wordmark** (D-WORKFLOW-144 to -146, `decision-register.md:604`, `:608`, `:610`): the SVG and
  265    the Tiny5 licence are installed beside each other (`:17-18`); the SVG carries no `font` or
  266    `<text>` line (`0`, `01` § L-22), so the licence ships for letterforms drawn as paths and no font
  267    file is needed at run time. The splash patch is T42's.
  268  - **The default theme**: L-20 (ES's `"system-theme"`, else the first set); G-02 reads which.
  269  - **The theme draws its own picture** (`es-code-traps.md` § The picture beside a game list):
  270    recorded; nothing in the recipe touches it.
  271  - **`lowerdeck` is installed by `PKG_UI`** (`virtual/image/package.mk:18`, consumed at `:42` unless
  272    `BASE_ONLY` is `true`; `BASE_ONLY=` empty on GENERIC_X64, R14), and used at run time by
  273    `runemu.sh:337-338`, `vertical-check:6-7`, `:143`, `:175`, `:180` and `111-sway-init:163-164`,
  274    owned by `os-launch-control-state` (T1) and `image-packages` (T8) (`01`, the extended run). Why
  275    it lives under `ui/`: it is a touch interface for a second screen (`:11`).
  276  - **A bump of either is a finding, never a change** (ruling (b)): `lowerdeck` behind its author's
  277    `HEAD` is a currency finding for the pause; a bump needs a new `PKG_SHA256`, which needs the
  278    tarball, which needs a fetch. `proved: tree`.
  279  
  280  ## The patches and their directories
  281  
  282  Every `patches/` subdirectory of the three packages on every device, reached or not by
  283  `scripts/unpack:150-160`'s globs with `PATCH_ARCH` by `:127-133` and the recipe's
  284  `PKG_PATCH_DIRS` (`stage-b/reach-15.sh`, sourced in the export, `reach rc=0`;
  285  `tools/t37-tables.py patches`, `rc=0`):
  286  
  287  | Device / arch | Package | `PATCH_ARCH` | `PKG_PATCH_DIRS` | Directory | Verdict |
  288  | --- | --- | --- | --- | --- | --- |
  289  | AMD64/x86_64 | `emulationstation` | `x86` | `[]` | `patches/x86_64/` | NOT REACHED |
  290  | AMD64/x86_64 | `es-theme-art-book-next` | `x86` | `[]` | `patches/` | REACHED |
  291  | GENERIC_X64/x86_64 | `emulationstation` | `x86` | `[]` | `patches/x86_64/` | NOT REACHED |
  292  | GENERIC_X64/x86_64 | `es-theme-art-book-next` | `x86` | `[]` | `patches/` | REACHED |
  293  | H700/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  294  | H700/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  295  | RK3326/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  296  | RK3326/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  297  | RK3399/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  298  | RK3399/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  299  | RK3566/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  300  | RK3566/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  301  | RK3576/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  302  | RK3576/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  303  | RK3588/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  304  | RK3588/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  305  | S922X/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  306  | S922X/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  307  | SM4450/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  308  | SM4450/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  309  | SM6115/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  310  | SM6115/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  311  | SM8250/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  312  | SM8250/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  313  | SM8550/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  314  | SM8550/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  315  | SM8650/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  316  | SM8650/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  317  | SM8750/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
  318  | SM8750/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
  319  
  320  generated, asserted: rows 30 over 15 devices; emulationstation patches/x86_64/ REACHED on 0 of 15; the theme's patches/ REACHED on 15 of 15; lowerdeck has no patches/ directory
  321  
  322  **L-02** is the 15 `NOT REACHED` rows: no device reaches `emulationstation/patches/x86_64/`,
  323  because `PATCH_ARCH` is `x86` on the two `x86_64` devices and the arch name on the 13 others, and
  324  the recipe sets no `PKG_PATCH_DIRS`. **T37's line is the recipe's `PKG_PATCH_DIRS`; the patch's
  325  content and place are T40's** (ruling (a), #1072). **L-18:** the device directory `:159` globs
  326  (`devices/<DEVICE>/patches/<pkg>/`) exists for none of the three on any device (`0`
  327  `project-side` lines), and a package's own `patches/<DEVICE>/` is reached only through
  328  `PKG_PATCH_DIRS` (`:137-145`), which upstream's recipe sets (`PKG_PATCH_DIRS+=" ${DEVICE}"`,
  329  `651150fc88:14`) for its `patches/RK3566/fix_multistateinput.patch` (§ The currency). The theme's
  330  three patches apply in name order; the GLES 3.0 context patch the fork added and reverted
  331  (`6afeaa2681`, `5da39f7adf`) is history only. `proved: tool-run`.
  332  
  333  ## The currency
  334  
  335  One row per file of the tip-to-`upstream/next` difference over `ui/` (`git diff --shortstat
  336  2174265e9c 651150fc88 -- projects/ROCKNIX/packages/ui/` printed ` 14 files changed, 83
  337  insertions(+), 536 deletions(-)`, s5-runs R05). Upstream's 16 commits since the base printed ` 8
  338  files changed, 72 insertions(+), 75 deletions(-)`; the fork's change against the base ` 8 files
  339  changed, 463 insertions(+), 13 deletions(-)` (R04); by side `upstream-only 6 fork-only 6 both 2`
  340  (R06). `tools/t37-tables.py currency`, `rc=0` (`stage-b/tables-currency.out`):
  341  
  342  | File under `projects/ROCKNIX/packages/ui/` | Side | Upstream commits `c445081a59..651150fc88` | Fork non-merge commits `c445081a59..2174265e9c` | Tip to `upstream/next` | What it is |
  343  | --- | --- | ---: | ---: | --- | --- |
  344  | `emulationstation/config/common/es_features.cfg` | upstream moved | 4 | 0 | +36 -71 | upstream's change the fork lacks |
  345  | `emulationstation/config/common/es_savestates.cfg` | fork moved | 0 | 2 | +0 -26 | the fork's own (absent upstream) |
  346  | `emulationstation/package.mk` | both | 8 | 241 | +14 -34 | both moved: a merge pending |
  347  | `emulationstation/patches/RK3566/fix_multistateinput.patch` | upstream moved | 1 | 0 | +21 -0 | upstream's change the fork lacks (absent at the tip) |
  348  | `emulationstation/sources/start_es.sh` | upstream moved | 1 | 0 | +6 -0 | upstream's change the fork lacks |
  349  | `emulationstation/system.d/emustation.service` | upstream moved | 1 | 0 | +1 -1 | upstream's change the fork lacks |
  350  | `emulationstation/system.d/emustation.service.d/20-thp.conf` | upstream moved | 1 | 0 | +2 -0 | upstream's change the fork lacks (absent at the tip) |
  351  | `emulationstation/system.d/essway.service` | both | 1 | 1 | +1 -4 | both moved: a merge pending |
  352  | `emulationstation/system.d/essway.service.d/20-thp.conf` | upstream moved | 1 | 0 | +2 -0 | upstream's change the fork lacks (absent at the tip) |
  353  | `themes/es-theme-art-book-next/package.mk` | fork moved | 0 | 2 | +0 -2 | the fork's own |
  354  | `themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch` | fork moved | 0 | 2 | +0 -31 | the fork's own (absent upstream) |
  355  | `themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch` | fork moved | 0 | 1 | +0 -11 | the fork's own (absent upstream) |
  356  | `themes/es-theme-art-book-next/sources/Tiny5-OFL.txt` | fork moved | 0 | 1 | +0 -93 | the fork's own (absent upstream) |
  357  | `themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg` | fork moved | 0 | 2 | +0 -263 | the fork's own (absent upstream) |
  358  
  359  generated, asserted: rows 14; upstream-only 6 fork-only 6 both 2
  360  
  361  Each row is **a finding with its reason, never a merge here** (the distribution merge on `ui/` is
  362  `release-candidates.md` step 0's, R3 § 1.8):
  363  
  364  - **Upstream's changes the fork lacks** (the six `upstream moved` rows): `es_features.cfg`'s 107
  365    lines (`+36 -71`); the RK3566 patch with the recipe's `PKG_PATCH_DIRS+=" ${DEVICE}"` (its context
  366    matches the pin, R2 cmd 21); `start_es.sh`'s `prerotate_env` and `scanout_reset_stale` (`+6`);
  367    `start.games` moving to `/run/rocknix/` in `emustation.service`; the two `20-thp.conf` drop-ins
  368    (`MemoryTHP=system`). Their ES half is the ES merge's (the 14 below).
  369  - **Both moved, a merge pending** (the two `overlap` files): `emulationstation/package.mk` --
  370    upstream's ROCKNIX pin `cada856d86` to `f6c542872e`, its `PKG_PATCH_DIRS` line and its ARMSX2
  371    block (L-01) against the fork's source, credentials, logging and RVZ hunks (§ 2); and
  372    `essway.service` -- upstream's comment at `:4` (`@@ -4 +4 @@`) against the fork's `sway-ready`
  373    wait (`@@ -11,0 +12,3 @@`).
  374  - **The fork's own** (the six `fork moved` rows): `es_savestates.cfg` (#196), the theme recipe's two
  375    lines, the wordmark and the licence (D-WORKFLOW-144 to -146), and T42's two theme patches.
  376  - **The ES 14**: the pin lacks `14` of `rocknix/master`'s commits (`7` first-parent merges) and is
  377    `724` ahead (R08) -- **#791's input**; this recipe's currency moves with that merge, not
  378    separately.
  379  - **The tools that would measure currency and do not:** L-10 (`lines=48 ui=0`) and L-21; both
  380    Backlog leads. **The licence**: L-16 (#990). **The upstream series**: an ES change reaches upstream
  381    as the package bump plus patches in the distribution (D-WORKFLOW-012, `decision-register.md:240`),
  382    so this recipe is the ES bucket's carrier in #256's and #322's series; nothing is cut here.
  383  - **The cost to the player** is boot to interface (`essway.service`'s `sway-ready` wait,
  384    `TimeoutStartSec=20`; `start_es.sh`; `es_settings`' locale generation, which L-07's silent
  385    failure would move onto first boot), priced from G-04. `proved: tool-run`.
  386  
  387  ## The structure
  388  
  389  - **The 15 against the 19:** the inventory's 15 are the glob's 19 less the four patches, at the
  390    inventory's head and at the P1 hash (`01` § Scope, the two `diff`s); 14 of the 19 are in the
  391    merge base, the 19 less the five fork additions (`14`, the block's last count but one).
  392  - **The doc drifts for the coordinator's sweep:** L-17 (`device-builds.md` § Iterating on
  393    EmulationStation names `maxengel/emulationstation-next`; `:8` names `pixelelated/emulationstation`)
  394    and L-18 (`CLAUDE.md`'s *"scope per device with `patches/<DEVICE>/`"*, true only with
  395    `PKG_PATCH_DIRS`). Also the brief's *"through the mask"*, which leaves `:39` unchanged: the
  396    coordinator recorded it as an erratum (6551707733 answer 3).
  397  - **The candidate's provenance** (ruling (h)): the M7 candidate `069fc2704421` built the pin plus
  398    nine ES patches the tip's recipe lacks and a corrected `es_systems.cfg` link (R3 § 2.2 C1, C2,
  399    § 2.3, cmd 21); `069fc2704421` is not in this repository (open item 16), and nothing under
  400    `/workspace/repos/rocknix` was read. Its `SYSTEM` (sha256
  401    `ade55e79f85d8896610a7ffecb228193c8ce651f65640c67479d64ca4c6e6982`, from M6's artifact copy at
  402    stage B) carries `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`
  403    (`stage-b/state-check-root.out`).
  404  
  405  ### The rulings, one row each
  406  
  407  | Ruling | Brief | How this slice keeps it |
  408  | --- | --- | --- |
  409  | (a) the inventory's 15; the four patches T40's and T42's; L-02's `PKG_PATCH_DIRS` T37's | `:150-157` | Coverage has 15 rows and names the four after it; L-02 splits the line from the patch |
  410  | (b) only the 15, never `:5` or `:6`; a bump a finding | `:158-169` | no edit under `packages/`, `projects/` or `tools/` at stages A and B (s5-runs R22); `lowerdeck` behind its author's `HEAD` is a finding |
  411  | (c) no ES worktree; `-es` fields `none -- no ES change` | `:170-177` | every ES read by `git -C qa-integration` (`show`, `grep`, `rev-parse`); `00`'s `reviewed-at-es` |
  412  | (d) `pkgcheck` by name, each after its `find` positive, with the control | `:178-190` | s5-runs R12; the fail-opens as L-21's Backlog lead |
  413  | (e) the upstream read from the refs already here; the authors' `HEAD`s R1 C20's | `:191-207` | no fetch, `ls-remote` or `gh api`; freshness `--list` only (R21); § The themes cites R1 C20 |
  414  | (f) ES's top-level CMake the integration's; es-core's T35's; the virtual packages T8's; the dependencies T7/T8/T22/T23 | `:208-214` | read by hash only; owners named in § The recipe and § The dependencies |
  415  | (g) PL-029, #1072 and D-WORKFLOW-216's two are the take-up table | `:215-217` | § The take-up |
  416  | (h) the candidate's provenance the integration's | `:218-222` | § The structure; every G-row labelled by side |
  417  | (i) the French catalog, the themes' content and every ES file outside the slice | `:223-225` | L-08 is the recipe's install line only; L-22 reads the theme by hash without a change |
  418  | (j) D-WORKFLOW-217 the ownership row; D-WORKFLOW-215 governs any hold | `:226-230` | D-WORKFLOW-217 at `decision-register.md:778`; no hold met at stages A and B |
  419  | (k) never `config/options` in the worktree | `:231-246` | every sourced call in `/workspace/tmp/m6-t37/export/`; `0` build roots in the worktree at each check |
  420  
  421  ## The runs
  422  
  423  Every run with its exit, wall time, figure and what a FAIL would mean. Stage A's § 5 runs are
  424  `stage-a/s5-runs.out` R01-R22 (each `rc=0`, walls 0-5 s; figures in `01` § The § 5 runs at stage
  425  A); stage A's open-item runs and stage B's are below.
  426  
  427  | Run | Exit | Wall | Figure | A FAIL would mean |
  428  | --- | --- | --- | --- | --- |
  429  | § 1 first commands (`stage-a/s1-first-commands.sh`) | 0 | 2 s | every line as expected; T36's ES `origin` ref `fatal:` | a stale base, a missing pin or a moved ref under the read |
  430  | § 2 block (`stage-a/block.sh`) | 0 | 6 s | output equal to the brief's `:531-560` | the slice is not the inventory's 15, or a count drifted |
  431  | § 2 extended run | 0 | not timed | 8 lines | a neighbour's owner misnamed |
  432  | R01-R22 (`stage-a/s5-runs.sh`) | 0 each | 0-5 s | `01` § The § 5 runs | an expectation the read was built on is false |
  433  | plans (`stage-a/plans.sh`) | 0 | 2 s | ES's plan 254 steps (GENERIC_X64), 247 (H700); the `arm` plan 271 with no ES | the dependency answers (open items 3, 5, fribidi's path) unfounded |
  434  | trace (`stage-a/trace.py`) | 0 | not timed | the chains to fribidi and gettext | as above |
  435  | mesa per device (`stage-a/mesa-gles.sh`) | 0 | not timed | `-Dgles2=enabled` on 15 of 15 | a device whose mesa ships no GLES 3 path |
  436  | open items (`stage-a/open-items.sh`) | 0 | 5 s | open items 2, 13, 15; L-22; the lanes' tips | the stage-A answers unfounded |
  437  | reach on 15 devices (`stage-b/reach-15.sh`) | 0 | not timed | 15 `NOT REACHED`, 15 `REACHED`, 15 `no patches/` | a patch directory reached somewhere, or a theme patch never applied |
  438  | tables, drift (`tools/t37-tables.py --drift`) | 1 each | not timed | `ASSERT FAIL` per table | the generator cannot fail |
  439  | tables (`tools/t37-tables.py`) | 0 each | not timed | 15 rows, 30 rows, 14 rows | a count drifted from the scope |
  440  | reads (`stage-b/reads.sh`) | 0 | not timed | B01-B14 | a lead's intent or a line misread |
  441  | L-01 merges (`stage-b/l01-merges.sh`) | 0 | not timed | four merges `2 -> 0` | the block was never upstream's, or the fork has it |
  442  | state check, payload (`stage-b/state-check-host.sh`) | script 1 (its last `grep -c` of leftover temp directories printed `0`); the check `rc=2` | sha 4 s, the check 5 s | `status error`, `input-invalid`: `mcopy` absent on the host (`command -v` printed `sfdisk` and `unsquashfs` only) | -- (it could not run: not a pass) |
  443  | state check, root (`stage-b/state-check-root.sh`) | 0; the check `rc=0` | gunzip 7 s, unsquashfs 3 s, the check 0 s; the rest not timed | `status pass`, 279 checks: 278 `clear`, 1 `allowed` (`/usr/bin/emulationstation approved-shared-developer-identity`); `developer-service-identity clear count 0` | a compiled pair other than D-WORKFLOW-166's |
  444  | window plan's bounds | 0 | not timed | `780` | the bound is not the plan's |
  445  
  446  **The `CANNOT`s:** a stamp, the `USING:` lines, the gettext pass, the CMake cache (`HAVE_FRIBIDI`,
  447  `HAVE_INTL`, `HAVE_UDEV`), the tip's recipe output, the H700 and SM8550 branches and upstream's
  448  RK3566 patch need a build, which this slice never runs (§ 5 item 1); they are the integration's.
  449  
  450  ## The guest cycle
  451  
  452  **The window:** granted as slot 1 at 01:40 UTC (comment 6551886156 and the host-file block); **START
  453  01:42:09 UTC** (comment 6551903971 and the host-file line), **RETURN inside the bound** (the
  454  guest stopped 01:44:35, bound 01:57:09, grace 02:02:09). One GENERIC_X64 guest from M6's
  455  `069fc2704421` copy (`ls -l` on the host: 2,122,289,964 bytes) on the fresh
  456  `/workspace/tmp/m6-t37/guest/disk.qcow2` (16 GiB), one boot at 640x480, isolated by T36's
  457  `qemu-wrap` (`guest-cycle/helpers/qemu-wrap`, sha256 `39a8bc357e84cfb281bd149875af2effc0c28aadb3c74cedfb5f13391b7b0a3b`,
  458  equal to `7978463093`'s blob; the running `-netdev` `user,id=net0,restrict=on,...`, `guestfwd`
  459  `0`). The detached stop timer, pid `426713`, set for 02:02:09, was stopped by its PID unfired
  460  (and its orphaned `sleep`, pid `426715`, by its own). Every row over `tools/vm-serial sh` through
  461  the device read filter; the guest's own first boot wrote what an image writes (the `system-theme`
  462  link below is one); this lane wrote nothing there. Records under `guest-cycle/` (terminal colour
  463  codes stripped after capture).
  464  
  465  | G | Side | Read | Proved |
  466  | --- | --- | --- | --- |
  467  | G-01 | candidate | `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`, `BUILD_VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`; `/usr/bin/emulationstation` `25155163fd7970f7da54b3f36d003b8c006111c894d4fe6f0c92d24d51831226` (R3 G2's). The `ldd` is T36's G-01 on this image, cited: `libfribidi` NOT linked (`g01-identity.txt`) | guest |
  468  | G-02 | ui-equal (the font file candidate) | ES themes `es-theme-art-book-next` (beside two non-ES directories, `Default`, `Emacs`); the wordmark and `Tiny5-OFL.txt` present; only `_inc/systems/artwork-default` left (the five removed, `:19`); removed includes `0` (`:20`); `zh` blocks `1` (`:21-27`); T42's lines present (`logoText` `2`, the `pixelelated` include `1`, the splash wordmark `1`, the Tools path `1`); the four bundled fonts; **`/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` present, 16,437,364 bytes** (L-22's one image read); `/etc/emulationstation/themes` -> `/storage/.config/emulationstation/themes` (`:100`); the seed the empty `<config>`; **the default (L-20):** the user `es_settings.cfg` (41 bytes) carries no `ThemeSet` line (`0`), and `/storage/.config/emulationstation/themes/system-theme` is a link, made at first boot, to `/usr/share/themes/es-theme-art-book-next` -- so ES's default `"system-theme"` resolves to the shipped theme (`g02-themes.txt`, `g02b-g04b-followup.txt`, `g02c-themes-dir.txt`) | guest |
  469  | G-03 | the cfgs ui-equal; the link candidate | the four cfg digests **equal to the tree's at `2174265e9c`** (es_features `588958bd...`, es_input `8e6033b5...`, es_savestates `93644274...`, es_settings `c93d8b29...`); vulkan lines `15`; **the candidate's link `/usr/config/emulationstation/es_systems.cfg`, `resolves rc=0`** (L-03's corrected form); modes `644` for the four seeds and `es_systems.cfg` (#1193's ES half); the French `.mo` present, 176,095 bytes (L-08); `/usr/share/locale` -> `/storage/.config/locale`, `/usr/lib/locale` -> `/usr/share/locale`; `/usr/config/locale/en_US.UTF-8` present (L-07); 36 locale entries (`g03-configs.txt`) | guest |
  470  | G-04 | ui-equal | `essway.service` `ActiveState=active` with the fork's three lines (`sway-ready`, `TimeoutStartSec=20`); `emustation.service` `inactive`; both `is-enabled` `disabled` and named in no `.wants` directory (a starter, `Starting[1502]: sway.service essway.service...` at 4.97 s, starts them); the three scripts' digests **equal to the tree's**; **PL-029: the running ES's argv is `emulationstation --log-path /var/log --no-splash` and `/var/log/es_log.txt` is written** (14,802 bytes, this boot) -- the flag inert, the path held by `Paths.cpp:81`; **boot to interface:** `essway.service` started at **5.37 s** (kernel monotonic), ES logging at **5.82 s**; `vm-serial wait` found ES running at 01:42:48, 39 s after START, firmware included (`g04-services.txt`, `g02b-g04b-followup.txt`) | guest |
  471  | G-05 | candidate | the two sources' heads read, not run; names in the binary `0`; the patch's string `0` (L-02: `cpugov.patch` not in the binary); `resources/logo.png` present, 283,835 bytes (L-04); `DroidSansFallbackFull.ttf` -> the noto-cjk file, resolving; **the state check: `CANNOT -- the tool is not on the image and the window writes nothing`**, its host half `status pass` (§ The runs) (`g05-sources.txt`) | guest |
  472  | G-06 | ui-equal | `/usr/share/lowerdeck` present, 12 entries (`main.py`, `ra_proxy.py` among them) (`g06-lowerdeck.txt`) | guest |
  473  | G-07 | -- | `tools/vm-stop` on the pidfile: `down: owned QEMU exited (pid 426693)`, `rc=0`; the timer stopped by PID, its log empty (unfired); the disk retired: `disk.qcow2` 2,308,440,064 bytes, sha256 `f334cde02be3802e3e994b5d6deb15645164f4cd47b686bc04f7118660fc392b`, with `disk.ovmf-vars.fd` and the logs (2,308,981,090 bytes in all), `disk.img` (4,333,764,608) removed before the boot; leftover census **`qemu 0, compilers 0`** (`g07-close.txt`, `retired.txt`) | guest |
  474  
  475  **Time to play:** boot to interface on this guest is `essway.service` at 5.37 s and ES at 5.82 s
  476  of kernel time; the slice changes nothing on that path at stage B (no fix yet), and the recipe's
  477  cost there is `sway-ready`'s bounded wait and `es_settings`' locale step, which L-07's
  478  pre-generated `en_US.UTF-8` (present) keeps off first boot.
  479  
  480  ## The streams
  481  
  482  Written by the coordinator after stage D, as for T21 to T36; the lane leaves this heading and the
  483  pause's dispositions.
  484  
  485  ## Positives
  486  
  487  - The three recipes keep global scope to option variables, and `tools/pkgcheck` agrees by name
  488    (`rc=0`, no `FAIL` or `WARN` line; R12); `bash -n` passes on all seven scripts and recipes (R11).
  489  - The theme and `lowerdeck` are pinned by full hash with `PKG_SHA256`; the theme's cached tarball
  490    hashes to it (`01` § L-22); the theme is at its author's `HEAD` (R1 C20).
  491  - The credential path keeps names out of the log (`:48-50` print `USING: <key> (set)`, never the
  492    value) and `get_env:14-15` forwards exactly four names; the image's state check passes with the
  493    one allowed shared identity (D-WORKFLOW-166).
  494  - The text checks over the 15 and the four patches are clean after their planted positives
  495    (non-ASCII `0`, secret patterns `0`, forbidden terms `0`, the four `.cfg` well-formed; R20).
  496  - The theme's 25 `fontPath` elements all carry a `fontSize` and name bundled fonts (L-22), and
  497    T42's three patches are reached on every device.
  498  - Six of the seven links in `makeinstall_target` and `post_install` take device paths (R17).
  499  - `essway.service`'s `sway-ready` wait is bounded (`TimeoutStartSec=20`) and owned by the unit
  500    (`:12-14`).
  501  
  502  ## The #585 lines owed
  503  
  504  One per upstream-carried defect the lane proves, in the lane's shape, never sent (D-WORKFLOW-164,
  505  -165). At stage B, proposed pending the checker's FAIL at stage C:
  506  
  507  - **L-03** (ROCKNIX, `projects/ROCKNIX/packages/ui/emulationstation/package.mk`): the
  508    `es_systems.cfg` fallback link interpolates `${INSTALL}` into its target, so the image carries a
  509    build-host path; the device path is `/usr/config/emulationstation/es_systems.cfg` (#613).
  510  - **L-06** (ROCKNIX, the same recipe): `sed "s#-#_##g"` replaces only the first hyphen of `DEVICE`
  511    (`#g` is a comment); `s#-#_#g` is meant. No current device name has a hyphen.
  512  - **L-19** (ROCKNIX, the same recipe): `PKG_NEED_UNPACK="busybox"` is a bare word where
  513    `calculate_stamp` expects a path, so busybox's recipe never moves the stamp; `$(get_pkg_directory
  514    busybox)` is the framework's own form.
  515  - **PL-029** (ROCKNIX, `start_es.sh` and `emustation.service`): `--log-path /var/log` is parsed by
  516    no ES argument branch; under `ROCKNIX` the path is `/var/log` by `Paths.cpp`. Offered as a tidy-up,
  517    not a defect.
  518  
  519  ## What the integration inherits
  520  
  521  1. **The pin bump**, with the ES branches' merged tip (none yet; § The recipe, Q1) and its steps;
  522     T34's eight ES commits (`52f0ff5128`, `ahead=8`) and its three patches
  523     `stage-e/s2-holders.patch`, `stage-e/s2-window.patch`, `stage-e/s3-msgbox.patch` in T34's audit
  524     folder, named by path and applied by no one here; T35 at `b7fdb3a24c` (9 ahead); T36's ES branch
  525     local at the pin.
  526  2. **The French catalog merges**, counted at the integration's turn; `tools/es-untranslated` after
  527     them (L-08's loud line, if the pause takes it, then guards the image).
  528  3. **The define's three owners** (`:25` T37's, `es-core/CMakeLists.txt:278-283` T35's, the bodies
  529     T36's).
  530  4. **Fribidi** -- the pause's decision; and **why the candidate's `QUIET` find failed** although
  531     ES's plan builds fribidi first, which only that build's configure log shows (L-09).
  532  5. **The candidate's provenance** (ruling (h)): nine ES patches and the corrected link the tip's
  533     recipe lacks.
  534  6. **The identity sidecar** carries no ES pin (#1013).
  535  7. **The distribution merge on `ui/`** (upstream's 16 commits on 8 files) is
  536     `release-candidates.md` step 0's; **the ES 14** are #791's.
  537  8. **The fixes this slice proves**, each `fix-image-pending` until the first image built from the
  538     fixed recipe shows it.
  539  9. **The state check's payload route on this host** needs `mcopy`, absent here; the `--root` route
  540     over an extracted `SYSTEM` ran instead (stage B). A tool note for the coordinator, not a slice
  541     fix.

=== SOURCE docs/audits/2026_11_01-epic-m6-es-recipe/03-retrospective.md (lines 1-62 of 62; the lane's draft)
    1  # Retrospective: M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)
    2  
    3  The audit's look back over the slice's history: what these 15 files are for, what the fork changed
    4  against ROCKNIX's base, what drifted, and what nobody's earlier fix noticed. The lane's own retro
    5  is stage G's (`docs/retros/<date>-m6-es-recipe.md`).
    6  
    7  ## 3.1 What the files are for
    8  
    9  They are how the distribution builds and installs the interface: the ES recipe clones the fork's
   10  EmulationStation at its pin and installs the binary, its seeds, its catalog and its boot pieces
   11  (the two units, the autostart link, the three scripts); the theme recipe installs ROCKNIX's shipped
   12  theme with the fork's wordmark; `lowerdeck` is a second-screen touch interface that `PKG_UI`
   13  installs on every image. None of them holds a menu or a player string; their effect on the player
   14  is what the image carries and how quickly it reaches the interface.
   15  
   16  ## 3.2 What the fork changed, and what drifted
   17  
   18  - **The source moved to the fork's own clone** (`:5-13`, `cb50b45f6e` 2026-08-19 first in the
   19    range's log, `84ff94fb3d` adding `zstd`), so the recipe's history is the pin's: 241 of the 246
   20    non-merge commits on `ui/` since the base touch the ES recipe (`stage-a/s5-runs.out` R04).
   21  - **The credentials** (`:27-50`, #566, D-WORKFLOW-166), **the RVZ licence files** (`:58-65`), the
   22    **log loop that prints names only** (`144b3eccb6`), the **sway-ready wait** (`essway.service:12-14`,
   23    `c6afa31db1`), the **save-state layout** (`es_savestates.cfg`, #196), and the **wordmark and its
   24    licence** (D-WORKFLOW-144 to -146) are the fork's.
   25  - **The licence expression** moved twice (`GPL` -> `MIT` -> `MIT AND BSD-3-Clause`), which a
   26    consuming check (#990) did not follow.
   27  - **Drift by merge:** four merges of `upstream/next` resolved the ES recipe as the fork's file and
   28    dropped upstream's ARMSX2 block each time (PL-05); since the base upstream moved six more files the
   29    fork lacks and changed the two the fork also changed (PL-14).
   30  
   31  ## 3.3 What none of the fixes noticed
   32  
   33  - **The link** at `:101` is upstream's form and dangled on every image built from this recipe; M7
   34    corrected it in its candidate's own recipe (#613) and the fork's tip still carries the old form
   35    (PL-01).
   36  - **The patch directory**: `cpugov.patch` was added under a directory no device reaches
   37    (`40fce2a089`, "wip"), and nothing reported that it never applied (PL-02, #1072).
   38  - **The stamp**: `PKG_NEED_UNPACK="busybox"` has never named a path (PL-03); upstream's line.
   39  - **The no-op `rm`** has been upstream's order since the first ROCKNIX recipe (PL-04).
   40  - **fribidi**: a dependency the plan supplies and the shipped binary did not take (PL-06), found only
   41    by an `ldd` on an image.
   42  
   43  ## 3.4 What the record says about catches
   44  
   45  Each of the five was visible in the recipe's text and none tripped a check: `tools/pkgcheck` reads
   46  late binding only, `fork-package-freshness` reaches none of the three recipes, and the image build
   47  reports success over a dangling link, an unapplied patch and a missing library alike. This slice's
   48  `tools/t37-checks.sh` FAILs on four of them at the tip and passes a fixture with them fixed
   49  (`stage-c/failfirst.out`).
   50  
   51  ## 3.5 The seams
   52  
   53  The ES pin is the integration's (D-WORKFLOW-191); the renderer source list T35's and the bodies
   54  T36's beside `:25`'s define; T40's patch and T42's theme patches; T8's `virtual/image`. A fix here
   55  moves only the ES recipe's stamp (the fixture's step 7: `moved=1 touched=1` for
   56  `emulationstation`, `moved=0 touched=0` for the other two, on both devices).
   57  
   58  ## 3.6 Time to play
   59  
   60  The recipe sits on boot to interface. On the candidate guest `essway.service` started at 5.37 s
   61  and ES was logging at 5.82 s of kernel time (G-04), with the pre-generated `en_US.UTF-8` present
   62  (PL-12's step worked there). Nothing in this slice's proposals adds work to that path.

=== SOURCE docs/audits/2026_11_01-epic-m6-es-recipe/04-analysis.md (lines 1-204 of 204; the lane's draft)
    1  # Analysis: M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)
    2  
    3  Stage C, 2026-11-01, the T3 session (Opus 5.5, high), at `reviewed-at` `9fa740a91b` (the slice's
    4  bytes `2174265e9c`'s); `reviewed-at-es: none -- no ES change`. The evidence is `02` and its records;
    5  this file answers the brief's Q1 to Q7 at their lines and states what the slice found.
    6  
    7  ## Executive summary
    8  
    9  The 15 files build and install the interface correctly in the ways an image shows -- on the
   10  candidate guest the four seeds and the three scripts are byte-identical to the tip's, the French
   11  catalog and the pre-generated locale are present, the theme resolves as ES's default, and the state
   12  check passes with only D-WORKFLOW-166's shared identity -- and they carry **four defects a check now
   13  catches and nothing caught before**: the `es_systems.cfg` link to a build-host path (PL-01, #613),
   14  `cpugov.patch` reached on no device (PL-02, #1072), `PKG_NEED_UNPACK`'s bare word (PL-03) and a
   15  no-op `rm` (PL-04). Beside them: **upstream's ARMSX2 block lost in four merges** (PL-05), **fribidi
   16  not linked in the candidate though the plan supplies it** (PL-06), two quiet guards (PL-07, PL-08),
   17  an inert flag (PL-09), the checkers that do not reach these recipes (PL-10), and the currency and
   18  doc findings (PL-11 to PL-16). Sixteen items, none above Medium; every disposition is proposed for
   19  the stage-D pause.
   20  
   21  ## Acceptance-criteria scorecard
   22  
   23  The 21 checkboxes of the brief's § 7 (#684's body), at stage C.
   24  
   25  | # | Checkbox (short) | State at stage C | Artifact |
   26  | --- | --- | --- | --- |
   27  | 1 | the folder's files | partly: `00`-`05`, `second-opinions/`, `stage-a/` to `stage-c/`, `tools/`, `guest-cycle/` present; `stage-d/`, `stage-e/` to come | `ls` of the folder |
   28  | 2 | the lint `PASS` both phases and with `--issue` | the pre-issue phase at stage C; the rest after stage D | `tools/lint-audit-artifacts` |
   29  | 3 | the review plan, the probe and refutation receipts, the manifest | at stage C's end | `second-opinions/` |
   30  | 4 | the punch-list issue at Phase 7 | stage D onward | the audit issue |
   31  | 5 | the header fields and no `PKG_VERSION`/`PKG_GIT_CLONE_BRANCH` change | `reviewed-at` written in `00`; no lane commit touches `ui/` | `git diff --stat 94d8ef8e7e HEAD -- packages projects tools` (no line) |
   32  | 6 | `01` § Scope with the block and its sha | met | `01` § Scope |
   33  | 7 | `02` § Coverage 15 rows | met | the checkbox's `awk`: `15` |
   34  | 8 | `02` § The runs | met for stages A to C | `02` § The runs |
   35  | 9 | `tools/t37-checks.sh` FAIL-first and at the tip | met | `stage-c/failfirst.out`, `stage-c/checks-at-tip.out` |
   36  | 10 | `02` § The recipe | met | `02` § The recipe |
   37  | 11 | `02` § The dependencies | met | `02` § The dependencies |
   38  | 12 | `02` § The themes and `lowerdeck` | met | `02` § The themes |
   39  | 13 | `02` § The patches | met | `02` § The patches |
   40  | 14 | `02` § The currency | met | `02` § The currency |
   41  | 15 | `02` § The guest cycle | met | `02` § The guest cycle |
   42  | 16 | `00` shows what never ran | met to stage C | `00` |
   43  | 17 | `04` answers, bugs with their traces | the answers here; the bugs at stage D | this file; the bugs |
   44  | 18 | `proved:` cells; `question:` per item | met | `02`, `05` |
   45  | 19 | the retro | stage G | -- |
   46  | 20 | the five checkers before the hand-back | stage H | -- |
   47  | 21 | the collisions named in the hand-back | stage H | -- |
   48  
   49  ## Risk assessment
   50  
   51  - **On the image a player has today, the risks are small**: the candidate the M7 line shipped
   52    corrects the link itself, carries the catalog and the locale, and its binary carries no stray
   53    credential pair. The tip's recipe, built as it is, would ship the dangling link (PL-01) -- the
   54    fallback ES uses when the player's own `es_systems.cfg` is missing.
   55  - **The silent ones are the risk to the next image**: a patch that never applies (PL-02), a stamp
   56    that never moves (PL-03), a dependency taken by order (PL-06), a catalog that can vanish (PL-07).
   57    Each fails without a message; the checker now catches four of them before a build.
   58  - **The merge debt** (PL-05, PL-14) is the largest change waiting: the ES recipe and `essway.service`
   59    conflict with upstream on the next merge.
   60  
   61  ## Coverage boundary
   62  
   63  - **Read:** the 15 files whole (the ES recipe with `:39` withheld by number); the pin's CMake, the
   64    sources the questions reached, by hash; the build engine's scripts the recipes depend on; the
   65    build's own plan computed in a scratch export; the candidate image on one guest and its `SYSTEM`
   66    on the host.
   67  - **Not read, and why:** the four patches' text beyond what the recipe reaches (T40's, T42's); ES's
   68    sources beyond the cited lines (the `es-*` slices'); `/workspace/repos/rocknix` (M7's), so the
   69    candidate's nine ES patches are cited from R3, not read; the authors' current repositories (no
   70    fetch, ruling (e)).
   71  - **`CANNOT` here, the integration's:** a stamp after a real build, the `USING:` lines, the gettext
   72    pass, the CMake cache (`HAVE_FRIBIDI`, `HAVE_INTL`, `HAVE_UDEV`), the tip's recipe output, the H700
   73    and SM8550 branches on an image, upstream's RK3566 patch applied.
   74  
   75  ## The questions
   76  
   77  ### Q1 The pin and its bump
   78  
   79  The pin is `16dbac5211eea7e70db7394372033be2be7df829` on `test/qa-integration` (`:5`, `:6`), cloned
   80  from `https://github.com/pixelelated/emulationstation` (`:8-9`, `:17`); ROCKNIX's recipe pinned
   81  `cada856d86` at the base and `f6c542872e` now; the pin lacks 14 of `rocknix/master`'s commits and
   82  is 724 ahead (`02` § The recipe, Q1). No merged ES tip exists; the bump's steps are stated and none
   83  is taken here (ruling (b)). The candidate is the same pin plus nine patches (ruling (h)); the
   84  sidecar carries no pin (#1013). L-17's rule drift is PL-15.
   85  
   86  ### Q2 The build options, the renderers and the install steps
   87  
   88  One row per `-D` (`:19-25`, `:30`, `:33`) with its CMake test and branch, and the derived defines
   89  (`02` § The recipe). `:25`'s `-DGLES3=1` selects `GLSystem "OpenGL ES 3.0"`, which both adds
   90  `-DUSE_OPENGLES_30` and lists `Renderer_GLES30`; the define compiles nothing; the list is T35's and
   91  the bodies T36's. Every device's mesa enables GLES 2. NDEBUG is the build system's
   92  (`config/functions:385-388`). One row per install step; the defects are PL-01 (`:101`), PL-04
   93  (`:79`), PL-07 (`:67-68`), PL-11 (`:54`), PL-12 (`:73-75`); PL-09 is T2's PL-029 with its sibling
   94  at `emustation.service:12`; #1193's half is the seeds' `cp -a` from `100644` (`644` on the guest).
   95  
   96  ### Q3 The dependencies
   97  
   98  The effective `PKG_DEPENDS_TARGET` is the same 19 wants on GENERIC_X64 and H700, ending `zstd mesa`
   99  (`02` § The dependencies). fribidi, udev (through `systemd`) and the gettext tools all arrive by
  100  build order; pugixml is the system library; `busybox`'s word in `PKG_NEED_UNPACK` names nothing
  101  (PL-03). fribidi's question is D-WORKFLOW-216's and the pause's (PL-06).
  102  
  103  ### Q4 The build credentials, by name
  104  
  105  Five lines name the build's credential variables (`:30`, `:40`, `:42`, `:43`, `:44`), each a
  106  *build-variable name*; `:39`'s value is never printed or sent, and `:40` carries only names and
  107  references. The recipe passes no credential to cmake; `get_env` forwards four names and the loop
  108  logs three (PL-08). The candidate's binary passes the state check with the one allowed shared
  109  identity. #64's `:54` cannot be answered from this recipe (it always passes the runtime flag);
  110  #586 is not a current gate. PL-16 is the state check's host route.
  111  
  112  ### Q5 The themes and `lowerdeck`
  113  
  114  The theme is at its author's `HEAD` and `upstream/next`'s pin, by hash (`PKG_SHA256` equal to the
  115  cached tarball's); its install steps, T42's patches (all reached), the wordmark and its licence,
  116  and the default theme (`system-theme` -> the shipped theme) are stated at their lines; all 25
  117  `fontPath` elements carry a `fontSize` and name bundled fonts (L-22). `lowerdeck` is behind its
  118  author's `HEAD` (PL-13), installed by `PKG_UI`, used by three run-time scripts outside the slice.
  119  
  120  ### Q6 The patches and their directories
  121  
  122  30 rows over 15 devices: the ES recipe's `patches/x86_64/` reached on none (PL-02), the theme's
  123  `patches/` on all; T37's line is `PKG_PATCH_DIRS`, the patch T40's. L-18's doc drift is PL-15.
  124  
  125  ### Q7 Package currency, the structure and the #585 lines
  126  
  127  14 rows: six upstream changes the fork lacks, six of the fork's own, two that both moved (PL-14);
  128  the ES 14 are #791's; the ARMSX2 block (PL-05); the checkers' reach (PL-10); the licence (L-16,
  129  #990); four #585 lines (L-03, L-06, L-19, PL-029), written in `02`, never sent.
  130  
  131  ## The take-up table (brief § 2), each row disposed
  132  
  133  `02` § The leads, *The take-up (§ 2), one row each*: 22 rows, each with its disposition; the items
  134  it raises are PL-01 (#613), PL-02 (#1072), PL-06 (D-WORKFLOW-216), PL-09 (PL-029).
  135  
  136  ## Renovation face
  137  
  138  The plan's seven questions, answered from the brief's.
  139  
  140  ### Q1 Modernize
  141  
  142  The recipes use the build system's current forms except `PKG_NEED_UNPACK` (PL-03) and the patch
  143  directory (PL-02), whose framework forms exist (`get_pkg_directory`, `PKG_PATCH_DIRS`).
  144  
  145  ### Q2 Standards
  146  
  147  `tools/pkgcheck` passes all three by name; `bash -n` passes the seven; the install link (PL-01) and
  148  the no-op `rm` (PL-04) are the standard lapses, each now asserted by the checker.
  149  
  150  ### Q3 Bugs
  151  
  152  PL-01, PL-02 and PL-05 are the defects with an effect on an image; PL-06 is the build-order
  153  decision; PL-03 the stamp; the rest are guards and notes.
  154  
  155  ### Q4 Package currency
  156  
  157  The theme is current; `lowerdeck` is behind (PL-13); the ES recipe's currency moves with the ES
  158  merge (#791); upstream's six `ui/` changes wait for the distribution merge (PL-14); no tool
  159  measures these three (PL-10).
  160  
  161  ### Q5 Efficiency
  162  
  163  Boot to interface: `essway.service` at 5.37 s, ES at 5.82 s (G-04); the pre-generated locale keeps
  164  `localedef` off first boot. PL-03's fix would rebuild ES when busybox changes, which is its point.
  165  
  166  ### Q6 Dead ends
  167  
  168  The inert `--log-path` (PL-09); the commented link at `:93`; the no-op `rm` (PL-04); a patch that
  169  never applies (PL-02).
  170  
  171  ### Q7 Clarity and structure
  172  
  173  The recipe says what it does except at `:79`, `:101` and `:14`; the two rules that describe it
  174  otherwise are PL-15.
  175  
  176  ## Instruction File Recommendations
  177  
  178  Proposals for the coordinator (the lane edits no rule):
  179  
  180  - `device-builds.md` § Iterating on EmulationStation: the fork's repository name (`:8`) in place of
  181    `maxengel/emulationstation-next` (PL-15).
  182  - `CLAUDE.md`'s package rules: *"scope per device with `patches/<DEVICE>/` -- reached only where the
  183    recipe sets `PKG_PATCH_DIRS`"* (PL-15).
  184  - `engineering-practices.md` § The form: a census by process name counts the kernel's 15-character
  185    name (`qemu-system-x86`), never `qemu-system-x86_64`, which matches nothing (this slice's stage-A
  186    and B censuses; corrected in `00`).
  187  - The brief kit's read mask: *"through the mask, and `:39` withheld by line number"* (the
  188    coordinator's answer 3).
  189  
  190  ## Second opinion
  191  
  192  Pending at the time of writing: the probe and the refutation run at stage C's end; their outcome is
  193  written here before the pre-issue lint.
  194  
  195  ## Quality self-check
  196  
  197  - Every count in `02`, `04` and `05` is a tool's line in a named file; the three generated tables
  198    and the punch list's generator each failed on a constructed drift first.
  199  - The checker failed on the tip, passed the fixed fixture and caught all 15 mutations before its
  200    verdict at the tip was trusted (`stage-c/failfirst.out`).
  201  - No value of a credential is in any artifact: the hooks' patterns count `0` over the folder after a
  202    planted positive matched `1`; `:39` and `:40`'s value parts occur `0` times.
  203  - What the lane did not check is said: the `CANNOT`s above, the candidate's nine patches (R3's),
  204    the authors' current `HEAD`s (R1 C20's, dated).

=== SOURCE docs/audits/2026_11_01-epic-m6-es-recipe/05-punch-list.md (lines 1-289 of 289; the lane's draft)
    1  # Punch list (Phases 5 and 6) — M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)
    2  
    3  Written by `tools/t37-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 the pin, Q2 the build options and install steps, Q3 the dependencies, Q4 the credentials, Q5 the themes and `lowerdeck`, Q6 the patches, Q7 currency and structure); `04` § Renovation face maps them to the plan's seven. Every disposition is proposed; the stage-D pause rules them. At Phase 7 (stage E) every item has its outcome below.
    4  
    5  reviewed-at: 9fa740a91ba9fcaa21a26cc72f0b50fac10f32df
    6  reviewed-at-es: none -- no ES change
    7  
    8  ## PL-01: The `es_systems.cfg` fallback link points at a build-host path
    9  
   10  - **Severity:** Medium; **category:** Install step; **question:** Q2
   11  - **Source finding:** L-03; #613
   12  - **Lines at the tip:** `emulationstation/package.mk:101`; `scripts/build:140`; `config/functions:1380`
   13  - **Owner:** T37 (the recipe's line, if the coordinator routes #613 here); upstream's form
   14  - **What is wrong:** `ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/...`: in `makeinstall_target` `INSTALL` is `$BUILD/install_pkg/emulationstation-<pin>`, and neither `scripts/install` nor `scripts/image` rewrites a link, so an image built from the tip carries `/etc/emulationstation/es_systems.cfg` pointing into the build host. The candidate image's link is the corrected `/usr/config/...` and resolves (G-03), because its own recipe differs (ruling (h)).
   15  - **Proposed disposition:** take up as #613: the device path in this slice's stream if routed (`fix-fixture` by the checker's L-03 assertion, `fix-image-pending`); a #585 line
   16  - **proved:** tool-run
   17  
   18  ## PL-02: `emulationstation/patches/x86_64/` is reached on no device
   19  
   20  - **Severity:** Medium; **category:** Patch directories; **question:** Q6
   21  - **Source finding:** L-02; #1072
   22  - **Lines at the tip:** `emulationstation/patches/x86_64/`; `scripts/unpack:127-128`, `:137-160`
   23  - **Owner:** T37 (the recipe's `PKG_PATCH_DIRS`); T40 (the patch's content and place, #1072)
   24  - **What is wrong:** `PATCH_ARCH` is `x86` for an `x86_64` target and the recipe sets no `PKG_PATCH_DIRS`, so `cpugov.patch` applies on none of the 15 devices (`stage-b/reach-15.out`); its string is absent from the candidate's binary (G-05). Added by `40fce2a089 2026-08-20 amd64: wip am64 changes`.
   25  - **Proposed disposition:** take up as #1072: the pause chooses T37's `[ "${ARCH}" = "x86_64" ] && PKG_PATCH_DIRS="x86_64"` (the fixture form, which reaches it on the two `x86_64` devices only) or T40's rename to `patches/x86/`; only a build proves the patch applies
   26  - **proved:** tool-run
   27  
   28  ## PL-03: `PKG_NEED_UNPACK="busybox"` is a bare word, so busybox never moves the ES stamp
   29  
   30  - **Severity:** Low; **category:** Build order; **question:** Q3
   31  - **Source finding:** L-19
   32  - **Lines at the tip:** `emulationstation/package.mk:14`; `config/functions:1114`, `:1126`
   33  - **Owner:** T37; upstream's line (`9f1fab30f6`)
   34  - **What is wrong:** `calculate_stamp` adds the word to its `find -L` paths relative to the root, where `busybox` names nothing (`0` files); the framework and upstream recipes pass a directory (`$(get_pkg_directory vdr)` in the vdr plugins' recipes, `config/functions:1322-1333`).
   35  - **Proposed disposition:** rule 6: `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"` (the fixture passes `pkgcheck` and the checker with it), or the line dropped if no ES build needs busybox; a #585 line
   36  - **proved:** tool-run
   37  
   38  ## PL-04: The `rm` of `resources/logo.png` runs before the directory exists
   39  
   40  - **Severity:** Low; **category:** Install step; **question:** Q2
   41  - **Source finding:** L-04
   42  - **Lines at the tip:** `emulationstation/package.mk:79`, `:81-82`; the pin's `es-core/src/Splash.h:17`
   43  - **Owner:** T37; upstream's order (`9f1fab30f6`)
   44  - **What is wrong:** The line removes nothing, so the pin's `logo.png` ships (G-05) -- ES's `DEFAULT_SPLASH_IMAGE`. Had it worked, it would remove the default splash.
   45  - **Proposed disposition:** a question at the pause: drop the line (the shipped behaviour unchanged) or record it as written with a #585 note
   46  - **proved:** tree
   47  
   48  ## PL-05: Upstream's ARMSX2 *vulkan driver* block was dropped by four merges
   49  
   50  - **Severity:** Medium; **category:** Merge debt; **question:** Q7
   51  - **Source finding:** L-01
   52  - **Lines at the tip:** `emulationstation/package.mk:125-129` (`651150fc88:104-108`); `es_features.cfg:1331`, `:1333`, `:1393`
   53  - **Owner:** T37
   54  - **What is wrong:** `a06539d8ec`, `049765fba0`, `fa2990c1e7` and `f370dc8787` each had an upstream parent with the two ARMSX2 lines and a result without them (`stage-b/l01-merges.out`); the tip's catalogue keeps `armsx2-sa`'s *vulkan driver* feature on every device that ships `armsx2-sa`, so devices without ARMSX2's own Turnip offer it (RK3566 of the fork's).
   55  - **Proposed disposition:** a bug candidate for the pause: upstream's five lines restored after `:128` (moves only ES's stamp); the fixture with upstream's two edits reproduced in `xml.etree` at stage E
   56  - **proved:** history
   57  
   58  ## PL-06: The candidate's ES does not link fribidi; the recipe declares it nowhere
   59  
   60  - **Severity:** Medium; **category:** Build order; **question:** Q3
   61  - **Source finding:** L-09; D-WORKFLOW-216; T36's G-01
   62  - **Lines at the tip:** `emulationstation/package.mk:13`; the pin's `CMakeLists.txt:236-241`, `:462`
   63  - **Owner:** T37 (the declaration, D-WORKFLOW-216); the integration (why the find failed)
   64  - **What is wrong:** ES's plan reaches fribidi only by `SDL2 -> swaywm-env -> sway -> pango -> fribidi`; T36's G-01 on the candidate reads `libfribidi` NOT linked, so its `QUIET` find failed and the built-in reordering shipped.
   65  - **Proposed disposition:** the pause's ruling under D-WORKFLOW-216 (declare `fribidi` at `:13`, or record the chain as the recipe's decision); the find's failure is the integration's configure log (`CANNOT` here)
   66  - **proved:** tool-run
   67  
   68  ## PL-07: A missing French catalog would install silently
   69  
   70  - **Severity:** Low; **category:** Guard that fails open; **question:** Q2
   71  - **Source finding:** L-08
   72  - **Lines at the tip:** `emulationstation/package.mk:67-68`; the pin's `CMakeLists.txt:565-578`
   73  - **Owner:** T37 (the install line); ES's CMake the integration's
   74  - **What is wrong:** Without the gettext tools ES builds no `.mo` and says only `Native language support disabled.`; the recipe copies what is there. The tools reach the build by `toolchain -> gcc:host -> autoconf:host -> gettext:host`, and the candidate carries the French `.mo` (G-03).
   75  - **Proposed disposition:** a stream question at the pause ("a loud catalog"): a line that fails when `fr/LC_MESSAGES/emulationstation2.mo` is absent; the checker WARNs at the tip
   76  - **proved:** tree
   77  
   78  ## PL-08: `HFS_DEV_LOGIN` builds a scraper with no `USING:` line
   79  
   80  - **Severity:** Low; **category:** Guard that fails open; **question:** Q4
   81  - **Source finding:** L-05
   82  - **Lines at the tip:** `emulationstation/package.mk:42-44`; `scripts/get_env:14`; the pin's `CMakeLists.txt:328-330`
   83  - **Owner:** T37
   84  - **What is wrong:** The log loop names three of the four names `get_env` forwards; `HFS_DEV_LOGIN` (read at the pin's `HfsDBScraper.cpp:1`, `:181`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33`) is the fourth.
   85  - **Proposed disposition:** a stream candidate: `HFS_DEV_LOGIN` added to the loop's list (names only)
   86  - **proved:** tree
   87  
   88  ## PL-09: `--log-path /var/log` is passed to ES and parsed by nothing
   89  
   90  - **Severity:** Low; **category:** Install step; **question:** Q2
   91  - **Source finding:** T2 PL-029 (`deferred:#684`)
   92  - **Lines at the tip:** `sources/start_es.sh:8`; `system.d/emustation.service:12`; the pin's `Paths.cpp:76-81`
   93  - **Owner:** T37 (upstream's two lines)
   94  - **What is wrong:** `parseArgs` has no such branch; under `-DROCKNIX` the log path is `/var/log`, and the candidate writes `/var/log/es_log.txt` with the flag in its argv (G-04).
   95  - **Proposed disposition:** kept with the reason (inert; editing either file makes an upstream-carried file fork-modified, `start_es.sh` already behind upstream); a #585 line
   96  - **proved:** guest
   97  
   98  ## PL-10: The two checkers that would measure these recipes pass over nothing
   99  
  100  - **Severity:** Low; **category:** Guard that fails open; **question:** Q7
  101  - **Source finding:** L-10, L-21
  102  - **Lines at the tip:** `tools/pkgcheck:157`, `:169`; `tools/fork-package-freshness:16-18`, `:42-44`
  103  - **Owner:** T6 (the tools); the coordinator (`EXTRA_PACKAGES`)
  104  - **What is wrong:** `pkgcheck` with a name that matches nothing prints nothing and exits 0; freshness prints its header for an unknown name and exits 0 with a missing ref, and its `--list` reaches none of the three (`lines=48 ui=0`).
  105  - **Proposed disposition:** a Backlog lead for the coordinator to file, naming the three fail-opens and the three recipes' reach
  106  - **proved:** tool-run
  107  
  108  ## PL-11: `sed "s#-#_##g"` replaces only the first hyphen of `DEVICE`
  109  
  110  - **Severity:** Low; **category:** Install step; **question:** Q2
  111  - **Source finding:** L-06
  112  - **Lines at the tip:** `emulationstation/package.mk:54`
  113  - **Owner:** T37; upstream's line
  114  - **What is wrong:** `echo a-b-c | sed "s#-#_##g"` prints `a_b-c`; no device name has a hyphen today.
  115  - **Proposed disposition:** recorded as written, with a #585 line (`s#-#_#g`)
  116  - **proved:** tool-run
  117  
  118  ## PL-12: The pre-generated locale's failure is silent
  119  
  120  - **Severity:** Low; **category:** Guard that fails open; **question:** Q2
  121  - **Source finding:** L-07
  122  - **Lines at the tip:** `emulationstation/package.mk:70-75`; `sources/es_settings:26-35`
  123  - **Owner:** T37; upstream's (`96d387fffd`)
  124  - **What is wrong:** `|| true` ends the `localedef` step; `es_settings` regenerates a missing locale at first start, so a failure costs first-boot time only. The candidate has the pre-generated locale (G-03).
  125  - **Proposed disposition:** recorded as written (a best-effort cache with a correct fallback); the checker's WARN
  126  - **proved:** tree
  127  
  128  ## PL-13: `lowerdeck` is behind its author's `HEAD`
  129  
  130  - **Severity:** Low; **category:** Package currency; **question:** Q5
  131  - **Source finding:** R1 C20 (2026-10-31)
  132  - **Lines at the tip:** `lowerdeck/package.mk:5-6`
  133  - **Owner:** T37 (a finding); a bump needs a fetch
  134  - **What is wrong:** Pinned at `ab735114ab` (ROCKNIX's pin too); its author's `HEAD` was `8fefe16e9c` at R1's dated read, by a count nobody made.
  135  - **Proposed disposition:** a currency finding, never a bump here (ruling (b)): the bump, with its new `PKG_SHA256`, at the integration or with ROCKNIX's
  136  - **proved:** tree
  137  
  138  ## PL-14: Upstream's six `ui/` changes and two overlaps wait for the distribution merge
  139  
  140  - **Severity:** Low; **category:** Merge debt; **question:** Q7
  141  - **Source finding:** § The currency (14 rows)
  142  - **Lines at the tip:** the 14 files of `2174265e9c..651150fc88` over `ui/`
  143  - **Owner:** `release-candidates.md` step 0 (the merge); #791 (the ES 14)
  144  - **What is wrong:** `upstream-only 6 fork-only 6 both 2`: the RK3566 patch and `PKG_PATCH_DIRS+=" ${DEVICE}"`, the two THP drop-ins, `start_es.sh`'s two functions, `emustation.service`'s `start.games` path and 107 lines of `es_features.cfg` the fork lacks; the ES recipe and `essway.service` changed on both sides.
  145  - **Proposed disposition:** deferred to the distribution merge and #791 (a finding per row in `02` § The currency, never a merge here)
  146  - **proved:** tool-run
  147  
  148  ## PL-15: Two rules describe the recipe as it is not
  149  
  150  - **Severity:** Low; **category:** Documentation; **question:** Q1
  151  - **Source finding:** L-17, L-18
  152  - **Lines at the tip:** `device-builds.md` § Iterating on EmulationStation; `CLAUDE.md` (patches per device)
  153  - **Owner:** the coordinator's sweep
  154  - **What is wrong:** The rule names `maxengel/emulationstation-next` where `:8` is `pixelelated/emulationstation`; `CLAUDE.md`'s `patches/<DEVICE>/` holds only where a recipe sets `PKG_PATCH_DIRS`.
  155  - **Proposed disposition:** the coordinator's doc sweep
  156  - **proved:** tree
  157  
  158  ## PL-16: `tools/pixelelated-state-check --payload` cannot run on this host
  159  
  160  - **Severity:** Low; **category:** Tooling; **question:** Q4
  161  - **Source finding:** stage B (G-05's host half)
  162  - **Lines at the tip:** `tools/pixelelated-state-check:767-792`
  163  - **Owner:** the coordinator (a tool note; the tool fails closed, as it should)
  164  - **What is wrong:** The `.img.gz` route needs `mcopy`, absent here: `rc=2`, `input-invalid`. The `--root` route over an extracted `SYSTEM` ran instead and passed.
  165  - **Proposed disposition:** a tool note for the integration (§ What the integration inherits item 9); no slice fix
  166  - **proved:** tool-run
  167  
  168  ## Phase 7 resolution gate
  169  
  170  | Item | Outcome | Evidence |
  171  | --- | --- | --- |
  172  | PL-01 | Open | before stage D's audit issue |
  173  | PL-02 | Open | before stage D's audit issue |
  174  | PL-03 | Open | before stage D's audit issue |
  175  | PL-04 | Open | before stage D's audit issue |
  176  | PL-05 | Open | before stage D's audit issue |
  177  | PL-06 | Open | before stage D's audit issue |
  178  | PL-07 | Open | before stage D's audit issue |
  179  | PL-08 | Open | before stage D's audit issue |
  180  | PL-09 | Open | before stage D's audit issue |
  181  | PL-10 | Open | before stage D's audit issue |
  182  | PL-11 | Open | before stage D's audit issue |
  183  | PL-12 | Open | before stage D's audit issue |
  184  | PL-13 | Open | before stage D's audit issue |
  185  | PL-14 | Open | before stage D's audit issue |
  186  | PL-15 | Open | before stage D's audit issue |
  187  | PL-16 | Open | before stage D's audit issue |
  188  
  189  ## punch_index
  190  
  191  ```yaml
  192  punch_index:
  193  - id: PL-01
  194    severity: "Medium"
  195    category: "Install step"
  196    question: Q2
  197    source_finding: "L-03; #613"
  198    outcome: "open"
  199  - id: PL-02
  200    severity: "Medium"
  201    category: "Patch directories"
  202    question: Q6
  203    source_finding: "L-02; #1072"
  204    outcome: "open"
  205  - id: PL-03
  206    severity: "Low"
  207    category: "Build order"
  208    question: Q3
  209    source_finding: "L-19"
  210    outcome: "open"
  211  - id: PL-04
  212    severity: "Low"
  213    category: "Install step"
  214    question: Q2
  215    source_finding: "L-04"
  216    outcome: "open"
  217  - id: PL-05
  218    severity: "Medium"
  219    category: "Merge debt"
  220    question: Q7
  221    source_finding: "L-01"
  222    outcome: "open"
  223  - id: PL-06
  224    severity: "Medium"
  225    category: "Build order"
  226    question: Q3
  227    source_finding: "L-09; D-WORKFLOW-216; T36's G-01"
  228    outcome: "open"
  229  - id: PL-07
  230    severity: "Low"
  231    category: "Guard that fails open"
  232    question: Q2
  233    source_finding: "L-08"
  234    outcome: "open"
  235  - id: PL-08
  236    severity: "Low"
  237    category: "Guard that fails open"
  238    question: Q4
  239    source_finding: "L-05"
  240    outcome: "open"
  241  - id: PL-09
  242    severity: "Low"
  243    category: "Install step"
  244    question: Q2
  245    source_finding: "T2 PL-029 (`deferred:#684`)"
  246    outcome: "open"
  247  - id: PL-10
  248    severity: "Low"
  249    category: "Guard that fails open"
  250    question: Q7
  251    source_finding: "L-10, L-21"
  252    outcome: "open"
  253  - id: PL-11
  254    severity: "Low"
  255    category: "Install step"
  256    question: Q2
  257    source_finding: "L-06"
  258    outcome: "open"
  259  - id: PL-12
  260    severity: "Low"
  261    category: "Guard that fails open"
  262    question: Q2
  263    source_finding: "L-07"
  264    outcome: "open"
  265  - id: PL-13
  266    severity: "Low"
  267    category: "Package currency"
  268    question: Q5
  269    source_finding: "R1 C20 (2026-10-31)"
  270    outcome: "open"
  271  - id: PL-14
  272    severity: "Low"
  273    category: "Merge debt"
  274    question: Q7
  275    source_finding: "§ The currency (14 rows)"
  276    outcome: "open"
  277  - id: PL-15
  278    severity: "Low"
  279    category: "Documentation"
  280    question: Q1
  281    source_finding: "L-17, L-18"
  282    outcome: "open"
  283  - id: PL-16
  284    severity: "Low"
  285    category: "Tooling"
  286    question: Q4
  287    source_finding: "stage B (G-05's host half)"
  288    outcome: "open"
  289  ```

=== SOURCE docs/reviews/briefs/es-recipe.md § 4 (lines 904-1082 of 1887; the seven questions)
  904  ## 4. The questions
  905  
  906  Each answered in `04-analysis.md` with the evidence at its lines; a defect
  907  proved becomes a `bug` with its trace, its `Already written:` line and its VM
  908  line (D-WORKFLOW-187), in one of the families the earlier briefs used --
  909  **a guard that fails open**, **an install step whose output is not what its
  910  line says**, **a dependency taken by build order**, **a structure or
  911  merge-debt fact**, **a currency fact** -- with the lens, **package currency**,
  912  asked of every recipe: is it at its author's current release or pinned with a
  913  stated reason, and is what it builds what the image carries. The leads are §
  914  3's, cited by number; the FAIL-first ones get their `git log -S` first. The
  915  seven questions are R4 § 1's proposal in the coordinator's order for a recipe
  916  slice (Q1 to Q6 by subject, Q7 the lens's).
  917  
  918  - **Q1 The pin and its bump** (`emulationstation/package.mk:5`, `:6`, `:8`,
  919    `:9`, `:17`; `device-builds.md` § Iterating on EmulationStation;
  920    `release-candidates.md:29`; D-WORKFLOW-191). State the pin and where it
  921    sits: `16dbac5211` is the tip of `test/qa-integration`, local and
  922    `origin`, the same at `2174265e9c` and `next` (blob `98cbc055d83f` at both,
  923    R1 C08, C15); ROCKNIX's `f6c542872e` is 14 commits the pin lacks, and the
  924    pin is 724 ahead (R1 C15). **No merged ES tip exists yet**
  925    (`test/qa-integration` is the pin; R4 item 6), so the lane states the bump's
  926    inputs (§ 8) and its steps -- the branches merged into the branch `:6`
  927    names, `:5` moved to that tip, the stamp cleared -- and moves nothing
  928    (ruling (b)). The pin each kept image carries is read from its
  929    `os-release` or its binary, never from a sidecar: the image's
  930    `.identity.json` does not carry the ES pin (#1013, R4 item 10), and the M7
  931    candidate is the pin plus nine patches (ruling (h); R3 § 2.2 C2). L-17's
  932    rule drift is recorded for the coordinator's sweep.
  933  - **Q2 The build options, the renderers and the install steps**
  934    (`:19-25`, `:30`, `:33`, `:54`; `makeinstall_target:57-129`;
  935    `post_install:132-141`). **One table of every `-D` the recipe passes, the
  936    CMake test it feeds and the branch it selects at the pin** (R4 item 20):
  937    `-DROCKNIX=1`, `-DDISABLE_KODI=1`, `-DENABLE_FILEMANAGER=0`, `-DCEC=0`,
  938    `-DENABLE_PULSE=1`, `-DUSE_SYSTEM_PUGIXML=1`, `-DGLES3=1` (`:19-25`),
  939    `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1` (`:30`), and `-DBATTERYPLUS=1` when
  940    `BATTERYPLUS_SUPPORT=yes` (`:33`; `H700/options:49` sets it, the CMake test
  941    `:135-137`) (R2 § 1). **The define D-WORKFLOW-216 hands here:** `:25` is
  942    `-DGLES3=1"`, and **the recipe carries no `-DUSE_OPENGLES_30`** -- ES's
  943    CMake derives it: the four graphics options are mutually exclusive
  944    (`CMakeLists.txt:3-16`), `GLES3` gives `GLSystem "OpenGL ES 3.0"`
  945    (`:164-165`) and `find_package(OpenGLES3 REQUIRED)` (`:213-214`), and that
  946    one `GLSystem` value both adds `-DUSE_OPENGLES_30` (`:362-363`) and lists
  947    `Renderer_GLES30.{h,cpp}` (`es-core/CMakeLists.txt:278-280`, whose `:278`
  948    is `if(${GLSystem} MATCHES "OpenGL ES 3.0")`): the define does not compile
  949    the source, `GLSystem` selects both (proof C4, Correction 8);
  950    `Renderer_GLES20` is never compiled
  951    (`:281-283`, the else); `Renderer_GL21` and `Renderer_GLES10` are listed
  952    unconditionally (`:110-111`, `:244-245`) (R2 § 1, cmds 8-9). No device
  953    `case` surrounds `:25`, so every device builds the GLES 3.0 renderer (R2 §
  954    1); `${OPENGLES}` is `mesa` wherever `projects/ROCKNIX/` sets it
  955    (`options:19`, `devices/AMD64/options:32`, proof C14), and which devices'
  956    `mesa` builds provide GLES 3 headers was not read `[unverified]` (R4 item
  957    2) -- mesa's effective options per device in the export, or an image
  958    build, settle it. The bodies are T36's and the source list T35's
  959    (D-WORKFLOW-216); the lane names them for their owners. The effective
  960    options on GENERIC_X64: `BATTERYPLUS_SUPPORT` empty, `VULKAN_SUPPORT=yes`
  961    (so `:126-128` keeps the vulkan choices; `no` on H700),
  962    `EMULATION_DEVICE=yes` (no stub `es_systems.cfg`, `:105-123`) (R3 § 1.5;
  963    proof C8). `:54` exports `DEVICE`
  964    upper-cased for `CMakeLists.txt:115-117` (L-06). Where NDEBUG comes from is
  965    the build type's, not a line of this recipe (R4 item 21). **The install
  966    steps, one row each** (R2 § 1's table): the RVZ licence files `:60-65`; the
  967    locale tree `:67-68`; the pre-generated locale `:73-75` (L-07); the
  968    `.cfg` seeds `:77-78`, with their modes (#1193); the no-op `rm` `:79`
  969    (L-04); the resources and the CJK fallback link `:81-85`; the three sources
  970    `:87-90`, which reach `${PKG_BUILD}` because `scripts/unpack:65`,
  971    `:107-108` copies `${PKG_DIR}/sources/*` into the unpack; the binary `:94`;
  972    the timezone link `:96-97`; the themes link and **the `es_systems.cfg`
  973    link** `:99-101` (L-03, #613); the tools-only `es_systems.cfg`
  974    `:105-123`; the vulkan deletion `:126-128` and the lost ARMSX2 block
  975    (L-01); the locale links `:132-141`; with PL-029's `start_es.sh:8` flag and
  976    L-08's silent catalog beside them. The units and `autostart/` are installed
  977    by the build system's directory conventions, not by the recipe:
  978    `scripts/install:96-99` copies `autostart/*` to `/usr/lib/autostart/common`
  979    and `:107-109` `system.d/*.*` to `/usr/lib/systemd/system`
  980    (`git show 2174265e9c:scripts/install | sed -n '96,99p;107,109p'`, proof
  981    C7; R2 § 1).
  982  - **Q3 The dependencies** (`:13`; L-09, L-19). The effective
  983    `PKG_DEPENDS_TARGET` on GENERIC_X64 is `boost toolchain SDL2 freetype curl
  984    freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool poppler
  985    pugixml noto-sans-cjk zstd mesa` (`${OPENGLES}` = `mesa`, R3 § 1.5), and
  986    the same on H700 (proof C8);
  987    **fribidi** is L-09's chain and D-WORKFLOW-216's question: declare it in
  988    `:13`, or record the transitive chain as the recipe's decision with the
  989    `QUIET` branch named -- a ruling put to the pause, never made by the lane,
  990    and an image build is the only proof of either (§ 8). **udev**: `:13`
  991    names no udev package, and T35's G-01 found libudev linked (R4 item 20);
  992    recorded as build order like fribidi. **pugixml**: the image links the
  993    system package (`-DUSE_SYSTEM_PUGIXML=1`, `:24`, with `pugixml` in `:13`),
  994    where the lanes' harnesses used the ES gitlink's copy (R4 item 23). The
  995    owners of every dependency's recipe are § 2's neighbours, and `${OPENGLES}`
  996    under `projects/ROCKNIX/` is set only at `options:19` and
  997    `devices/AMD64/options:32`, both `"mesa"` (§ 2; proof C14).
  998  - **Q4 The build credentials, by name** (`pre_configure_target:35-55`;
  999    `device-builds.md:528-578`; D-INFRA-006, D-INFRA-007, D-WORKFLOW-166).
 1000    The recipe passes nothing to cmake explicitly: ES's CMake reads each name
 1001    from the environment -- `SCREENSCRAPER_DEV_LOGIN` (`CMakeLists.txt:307-309`),
 1002    `GAMESDB_APIKEY` (`:320-322`), `CHEEVOS_DEV_LOGIN` (`:324-326`),
 1003    `HFS_DEV_LOGIN` (`:328-330`, consumed by the HFS scraper; L-05), plus
 1004    `SCREENSCRAPER_SOFTNAME` (`:303-305`) and `SCREENSCRAPER_RUNTIME_DEV_LOGIN`
 1005    (`:311-318`) (R2 § 1); `scripts/get_env:14` keeps exactly four names and
 1006    `:15` drops the rest secret-shaped (R2 § 1; R3 § 2.2 C7, cmd 18); the log
 1007    loop `:42-52` names three; `:40` always supplies a pair, so the warning at
 1008    `:46` is unreachable for that key (L-11, the design). **The answer is
 1009    names, lines and routes only:** the recipe is read through the mask, `:39`'s
 1010    value is never printed, and the binary cannot show the names, because the
 1011    macro names do not survive compilation (R3 G5); whether #64's open
 1012    checkbox (`:54`) is answerable from the recipe is stated; replacement
 1013    credentials are #586's, not a current gate.
 1014  - **Q5 The themes and `lowerdeck`** (the theme's `package.mk`; D-UI-090;
 1015    D-WORKFLOW-144, -145, -146). The theme is pinned at
 1016    `9a50ef366e750aabfab29e6915a2867607212971`, the same commit `upstream/next`
 1017    pins and its author's `HEAD` at R1 C20's read, with `PKG_SHA256`
 1018    `7ee1e93f2c4e4f7385b78680ecfa3828acf12bc616e2111d23cc66a524231125` (R1 C08,
 1019    C14, C20; R3 § 1.5); **no pin reason is stated, and none is required**,
 1020    because D-WORKFLOW-024's tool does not reach it (L-10). Its install steps
 1021    (`:14-28`), its three patches (T42's text; they apply, R2 § 3), the
 1022    upstream offer of the Tools-icon patch (#69's open checkbox, D-UI-090,
 1023    nothing sent), the wordmark and the font licence copied beside the font's
 1024    use, the default theme (L-20), and the theme drawing its own picture
 1025    (R4 item 28) are each stated at their lines. **`lowerdeck`** is pinned at
 1026    `ab735114ab318a84e4d28c9c5f1b154e450a579a` with `PKG_SHA256`
 1027    `2677d3ce675b9704487f9f09f82728b56009f9fa7c36403086e9c655af108f42`,
 1028    `GPL-2.0-or-later`, ROCKNIX's pin too (R1 C08, C14; R3 § 1.5; R4 § 0),
 1029    and **behind its author's `HEAD` `8fefe16e9c`** at R1 C20's read, by a
 1030    number of commits nobody counted (no fetch, ruling (e)). **`PKG_UI`
 1031    installs it**: `virtual/image/package.mk:18` assigns `PKG_UI` with no
 1032    device test and `:42` consumes it in the `else` of `:36`'s
 1033    `if [ "${BASE_ONLY}" = "true" ]`, and the effective `BASE_ONLY` is empty on
 1034    GENERIC_X64
 1035    (`git show 2174265e9c:projects/ROCKNIX/packages/virtual/image/package.mk | /usr/bin/grep -n -E 'PKG_UI|BASE_ONLY'`,
 1036    proof C7, C8; R1 C09). **Three scripts outside the slice use it at run
 1037    time** -- `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh:337-338`
 1038    (`python3 /usr/share/lowerdeck/ra_proxy.py`), the same directory's
 1039    `vertical-check:6-7`, `:143`, `:175`, `:180`, and
 1040    `projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init:163-164`
 1041    (`git grep -n lowerdeck 2174265e9c -- projects packages`, proof C6,
 1042    Correction 11) -- each owned by the slice § 2's extended `named` run
 1043    gives its path. **A bump of either is a finding with its reason** (ruling
 1044    (b)).
 1045  - **Q6 The patches and their directories** (`scripts/unpack:124-160`;
 1046    `packaging-and-patches.md:76-97`; L-02, L-18). The reach of every
 1047    `patches/` subdirectory of the three packages, computed per device from
 1048    the sourced recipe: the glob list at `scripts/unpack:150-160` (R3 § 8,
 1049    quoted there whole), `PATCH_ARCH` `x86` for an `x86_64` target
 1050    (`:127-128`), and the recipe's `PKG_PATCH_DIRS`, unset (R3 § 8: NOT
 1051    REACHED for `patches/x86_64/` on GENERIC_X64 and on H700; the lane extends
 1052    it to every device in the plan; `:159`'s device directory outside the
 1053    package, L-18). **T37's line is the recipe's patch
 1054    directories; the patch's text and place are T40's** (ruling (a), #1072).
 1055    Upstream's `PKG_PATCH_DIRS+=" ${DEVICE}"` with the RK3566 patch is the
 1056    shape a recipe uses for device patches (§ 2's merge debt; L-18). The theme
 1057    patches apply in name order, `0001-` before `001-p` before `001-t` (R2 § 3),
 1058    and two share the `001-` prefix (R4 item 27); the GLES 3.0 context patch
 1059    the fork added and reverted is history only (R1 C13).
 1060  - **Q7 Package currency against upstream's recipe, the structure and the
 1061    #585 lines** (D-WORKFLOW-024, -162, -164, -165, -012; `time-to-play.md`).
 1062    **One row per file of the tip-to-`upstream/next` difference over `ui/`**
 1063    (` 14 files changed, 83 insertions(+), 536 deletions(-)`, § 2; proof
 1064    Correction 6), each saying whether upstream moved it (one of the 8 of § 2's
 1065    merge debt), the fork moved it (one of the fork's 8), or both (the two
 1066    `overlap` files; `upstream-only 6 fork-only 6 both 2`, § 5): upstream's
 1067    change the fork lacks (the RK3566 patch and
 1068    `PKG_PATCH_DIRS`, the THP drop-ins, `start_es.sh`'s two functions, the units'
 1069    `start.games` path, `es_features.cfg`'s 107 lines, L-01's ARMSX2 block), the
 1070    fork's own (§ 2's hunks), or a merge pending (the ES 14, #791's input) --
 1071    **each a finding with its reason, never a merge here** (the distribution
 1072    merge is `release-candidates.md` step 0's, R3 § 1.8). The tools that would
 1073    measure currency and do not: L-10, L-21. The licence expression (L-16,
 1074    #990). The recipe's part of the upstream PR series (D-WORKFLOW-012: an ES
 1075    change reaches upstream as the package bump plus patches in the
 1076    distribution). **The #585 lines owed**: one for each upstream-carried
 1077    defect the lane proves -- L-03's link is upstream's form (R3 cmd 23), L-06's
 1078    `sed` upstream's line, L-19's bare `PKG_NEED_UNPACK` upstream's line
 1079    (proof C6) -- in the shape the lane writes, never sent
 1080    (D-WORKFLOW-164, -165). The cost of a recipe's choice to the player is
 1081    boot to interface (§ 3 item 10).
 1082  
