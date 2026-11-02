## Ramoops, all 38 lines

1: From: ROCKNIX fork <noreply@rocknix.org>
2: Subject: [PATCH] arm64: dts: allwinner: h616: reserve 1 MiB for ramoops on every H700 board
3:
4: A panic or a detected hang on a handheld currently leaves nothing behind:
5: the kernel log is in RAM and the reset that follows erases it. This adds
6: a pstore/ramoops region at 0x4F000000, which every H700 board has as RAM
7: and which nothing in the U-Boot boot chain touches (fork #104).
8:
9: ---
10: --- a/arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi
11: +++ b/arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi
12: @@ -117,6 +117,26 @@
13:                     reg = <0x0 0x40000000 0x0 0x40000>;
14:                     no-map;
15:             };
16: +
17: +           /*
18: +            * ROCKNIX (fork #104): 1 MiB for pstore/ramoops, so the kernel
19: +            * log of a panic or a detected hang survives the reset that
20: +            * follows it and is read back at the next boot. 0x4F000000 is
21: +            * RAM on every H700 board (all carry at least 1 GiB from
22: +            * 0x40000000) and nothing in the boot chain writes there: the
23: +            * kernel is loaded at 0x40080000 (~32 MiB), U-Boot proper runs
24: +            * at 0x4A000000, and what U-Boot loads late sits above it -- the
25: +            * FDT at 0x4FA00000, the SPL's relocated stack at 0x4FE00000,
26: +            * the ramdisk slot at 0x4FF00000. 512 KiB of console log and
27: +            * four 128 KiB dumps, oopses and panics both.
28: +            */
29: +           ramoops@4f000000 {
30: +                   compatible = "ramoops";
31: +                   reg = <0x0 0x4f000000 0x0 0x100000>;
32: +                   record-size = <0x20000>;
33: +                   console-size = <0x80000>;
34: +                   max-reason = <2>;
35: +           };
36:     };
37:
38:     osc24M: osc24M-clk {

## H700 config evidence

3: # Linux/arm64 7.2.0 Kernel Configuration
3656: CONFIG_WATCHDOG_SYSFS=y
7290: CONFIG_PSTORE_CONSOLE=y
7292: CONFIG_PSTORE_RAM=y
7975: CONFIG_SOFTLOCKUP_DETECTOR=y
7978: CONFIG_DETECT_HUNG_TASK=y
7979: CONFIG_DEFAULT_HUNG_TASK_TIMEOUT=120

## H700 options

25:     KERNEL_TARGET="Image"

## SM8550 config evidence

3: # Linux/arm64 7.2.0 Kernel Configuration
4461: CONFIG_DRM_MSM=y
7765: CONFIG_PSTORE_RAM=m

## SM8550 options

25:     KERNEL_TARGET="Image"

## GENERIC_X64 config evidence

3: # Linux/x86 6.15.6 Kernel Configuration
3745: CONFIG_WATCHDOG_SYSFS=y
6805: CONFIG_PSTORE_CONSOLE=y
6806: CONFIG_PSTORE_RAM=y
7499: CONFIG_SOFTLOCKUP_DETECTOR=y
7510: CONFIG_DETECT_HUNG_TASK=y
7511: CONFIG_DEFAULT_HUNG_TASK_TIMEOUT=120

## GENERIC_X64 options

10:         TARGET_KERNEL_PATCH_ARCH="x86_64"
24:     KERNEL_TARGET="bzImage"

## Kernel override recipe, whole text

1: # SPDX-License-Identifier: GPL-2.0-or-later
2: # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
3: # Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
4:
5: PKG_NAME="linux"
6: PKG_LICENSE="GPL"
7: PKG_SITE="http://www.kernel.org"
8: PKG_DEPENDS_HOST="ccache:host openssl:host"
9: PKG_DEPENDS_TARGET="linux:host kmod:host xz:host keyutils ncurses openssl:host ${KERNEL_EXTRA_DEPENDS_TARGET}"
10: PKG_NEED_UNPACK="${LINUX_DEPENDS} $(get_pkg_directory initramfs) $(get_pkg_variable initramfs PKG_NEED_UNPACK)"
11: PKG_NEED_UNPACK+=" ${PROJECT_DIR}/${PROJECT}/bootloader ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader"
12: PKG_LONGDESC="This package contains a precompiled kernel image and the modules."
13: PKG_IS_KERNEL_PKG="yes"
14: PKG_STAMP="${KERNEL_TARGET} ${KERNEL_MAKE_EXTRACMD}"
15:
16: PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"
17:
18: [[ "${DEVICE}" == RK* ]] && PKG_PATCH_DIRS+=" mainline-rockchip"
19: [[ "${DEVICE}" == SM* ]] && PKG_DEPENDS_TARGET+=" mkbootimg:host"
20:
21: case ${DEVICE} in
22:   RK3588)
23:     PKG_VERSION="b8e62bed74766b6c8c423a767b35495e78b64caf"
24:     PKG_SHA256="0e0fe5a2f108d525a044e190c3f23a4603cdbf8d54bc1cc488d6ee04b9fc5b3a"
25:     PKG_URL="https://github.com/armbian/linux-rockchip/archive/${PKG_VERSION}.tar.gz"
26:     PKG_GIT_CLONE_BRANCH="rk-6.1-rkr3"
27:     PKG_PATCH_DIRS="${LINUX} ${DEVICE} default"
28:     ;;
29:   H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
30:     PKG_VERSION="7.2"
31:     PKG_SHA256="f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3"
32:     PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
33:     # Note that the patch dir 7.2 is automatically added as it matches the
34:     # version. When we move past 7.2, remember to add 7.2 to patch dirs.
35:     ;;
36:   RK3326|AMD64|GENERIC_X64)
37:     PKG_VERSION="7.1.2"
38:     PKG_SHA256="37198c93727be247c9fb5309bb86cd5e496c61e5322cd8c4eca9476bb0b5883f"
39:     PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
40:     PKG_PATCH_DIRS+=" 7.0"
41:     ;;
42:   RK3576|RK3566)
43:     PKG_VERSION="7.0.2"
44:     PKG_SHA256="53591a03294527a48ccb0b9e559e922df8a38554745a1206827ca751d2ca7662"
45:     PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
46:     PKG_PATCH_DIRS+=" 7.0"
47:     ;;
48:   S922X|RK3399)
49:     PKG_VERSION="6.18.49"
50:     PKG_SHA256="ae826f33111fea6f1d279dde7299d7463c8dfd204aeb75a8fb5432bc60a28191"
51:     PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
52:     ;;
53: esac
54:
55: PKG_KERNEL_CFG_FILE=$(kernel_config_path) || die
56:
57: if [ -n "${KERNEL_TOOLCHAIN}" ]; then
58:   PKG_DEPENDS_TARGET+=" gcc-${KERNEL_TOOLCHAIN}:host"
59:   HEADERS_ARCH=${TARGET_ARCH}
60: else
61:   PKG_DEPENDS_TARGET+=" toolchain"
62: fi
63:
64: if [ "${PKG_BUILD_PERF}" != "no" ] && grep -q ^CONFIG_PERF_EVENTS= ${PKG_KERNEL_CFG_FILE}; then
65:   PKG_BUILD_PERF="yes"
66:   PKG_DEPENDS_TARGET+=" binutils elfutils libunwind zlib openssl"
67: fi
68:
69: if [[ "${TARGET_ARCH}" =~ i*86|x86_64 ]]; then
70:   PKG_DEPENDS_TARGET+=" elfutils:host pciutils"
71:   PKG_DEPENDS_UNPACK+=" intel-ucode kernel-firmware"
72: fi
73:
74: # Ensure that the dependencies of initramfs:target are built correctly, but
75: # we don't want to add initramfs:target as a direct dependency as we install
76: # this "manually" from within linux:target
77: for pkg in $(get_pkg_variable initramfs PKG_DEPENDS_TARGET); do
78:   ! listcontains "${PKG_DEPENDS_TARGET}" "${pkg}" && PKG_DEPENDS_TARGET+=" ${pkg}" || true
79: done
80:
81: if [ "${DEVICE}" = "RK3326" -o "${DEVICE}" = "RK3566" ]; then
82:   PKG_DEPENDS_UNPACK+=" generic-dsi"
83: elif [ "${DEVICE}" = "SM8250" -o "${DEVICE}" = "H700" -o "${DEVICE}" = "SM8650" -o "${DEVICE}" = "SM8750" ]; then
84:   PKG_DEPENDS_UNPACK+=" kernel-firmware"
85: fi
86:
87: # SM8650/SM8750 build device-specific firmware blobs into the kernel, so the
88: # extra-firmware package must be unpacked before the kernel is built.
89: if [ "${DEVICE}" = "SM8650" -o "${DEVICE}" = "SM8750" ]; then
90:   PKG_DEPENDS_UNPACK+=" extra-firmware"
91: fi
92:
93: # A built-in cfg80211 needs regulatory.db inside the kernel image (see
94: # pre_make_target), so unpack wireless-regdb before the kernel is built.
95: if grep -q '^CONFIG_CFG80211=y' ${PKG_KERNEL_CFG_FILE}; then
96:   PKG_DEPENDS_UNPACK+=" wireless-regdb"
97: fi
98:
99: post_patch() {
100:   # linux was already built and its build dir autoremoved - prepare it again for kernel packages
101:   if [ -d ${PKG_INSTALL}/.image ]; then
102:     cp -p ${PKG_INSTALL}/.image/.config ${PKG_BUILD}
103:     kernel_make -C ${PKG_BUILD} prepare
104:
105:     # restore the required Module.symvers from an earlier build
106:     cp -p ${PKG_INSTALL}/.image/Module.symvers ${PKG_BUILD}
107:   fi
108:
109:   if [ "${DEVICE}" = "RK3326" -o "${DEVICE}" = "RK3566" -o "${DEVICE}" = "RK3576" ]; then
110:     cp -v $(get_pkg_directory generic-dsi)/sources/panel-generic-dsi.c ${PKG_BUILD}/drivers/gpu/drm/panel/
111:     echo "obj-y" += panel-generic-dsi.o >> ${PKG_BUILD}/drivers/gpu/drm/panel/Makefile
112:   fi
113:
114:   DTS_SOURCE_DIR="${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/linux/dts"
115:   if [ -d "${DTS_SOURCE_DIR}" ]; then
116:     rsync -av "${DTS_SOURCE_DIR}/" ${PKG_BUILD}/arch/arm64/boot/dts/
117:   fi
118: }
119:
120: make_init() {
121:  : # reuse make_target()
122: }
123:
124: makeinstall_init() {
125:   :
126: }
127:
128: make_host() {
129:   :
130: }
131:
132: makeinstall_host() {
133:   make \
134:     ARCH=${HEADERS_ARCH:-${TARGET_KERNEL_ARCH}} \
135:     HOSTCC="${TOOLCHAIN}/bin/host-gcc" \
136:     HOSTCXX="${TOOLCHAIN}/bin/host-g++" \
137:     HOSTCFLAGS="${HOST_CFLAGS}" \
138:     HOSTCXXFLAGS="${HOST_CXXFLAGS}" \
139:     HOSTLDFLAGS="${HOST_LDFLAGS}" \
140:     INSTALL_HDR_PATH=dest \
141:     headers_install
142:   mkdir -p ${SYSROOT_PREFIX}/usr/include
143:     cp -R dest/include/* ${SYSROOT_PREFIX}/usr/include
144: }
145:
146: pre_make_target() {
147:   ( cd ${ROOT}
148:     rm -rf ${BUILD}/initramfs
149:     rm -f ${STAMPS_INSTALL}/initramfs/install_target ${STAMPS_INSTALL}/*/install_init
150:     ${SCRIPTS}/install initramfs
151:   )
152:   pkg_lock_status "ACTIVE" "linux:target" "build"
153:
154:   cp ${PKG_KERNEL_CFG_FILE} ${PKG_BUILD}/.config
155:
156:   # set initramfs source
157:   ${PKG_BUILD}/scripts/config --set-str CONFIG_INITRAMFS_SOURCE "$(kernel_initramfs_confs) ${BUILD}/initramfs"
158:
159:   # Keep the RC2 network identity across the display rename (D-WORKFLOW-123).
160:   ${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "ROCKNIX"
161:
162:   # disable swap support if not enabled
163:   if [ ! "${SWAP_SUPPORT}" = yes ]; then
164:     ${PKG_BUILD}/scripts/config --disable CONFIG_SWAP
165:   fi
166:
167:   # disable nfs support if not enabled
168:   if [ "${NFS_SUPPORT}" = no ]; then
169:     ${PKG_BUILD}/scripts/config --disable CONFIG_NFS_FS
170:   fi
171:
172:   # disable cifs support if not enabled
173:   if [ ! "${SAMBA_SUPPORT}" = yes ]; then
174:     ${PKG_BUILD}/scripts/config --disable CONFIG_CIFS
175:   fi
176:
177:   # disable iscsi support if not enabled
178:   if [ ! "${ISCSI_SUPPORT}" = yes ]; then
179:     ${PKG_BUILD}/scripts/config --disable CONFIG_SCSI_ISCSI_ATTRS
180:     ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_TCP
181:     ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_BOOT_SYSFS
182:     ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_IBFT_FIND
183:     ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_IBFT
184:   fi
185:
186:   # disable lima/panfrost if libmali is configured
187:   if [ "${OPENGLES}" = "libmali" ]; then
188:     ${PKG_BUILD}/scripts/config --disable CONFIG_DRM_LIMA
189:     ${PKG_BUILD}/scripts/config --disable CONFIG_DRM_PANFROST
190:   fi
191:
192:   # disable wireguard support if not enabled
193:   if [ ! "${WIREGUARD_SUPPORT}" = yes ]; then
194:     ${PKG_BUILD}/scripts/config --disable CONFIG_WIREGUARD
195:   fi
196:
197:   if [[ "${TARGET_ARCH}" =~ i*86|x86_64 ]]; then
198:     # copy some extra firmware to linux tree
199:     mkdir -p ${PKG_BUILD}/external-firmware
200:       cp -a $(get_build_dir kernel-firmware)/.copied-firmware/{amdgpu,amd-ucode,i915,radeon,e100,rtl_nic} ${PKG_BUILD}/external-firmware
201:
202:     cp -a $(get_build_dir intel-ucode)/intel-ucode ${PKG_BUILD}/external-firmware
203:
204:     FW_LIST="$(find ${PKG_BUILD}/external-firmware \( -type f -o -type l \) \( -iname '*.bin' -o -iname '*.fw' -o -path '*/intel-ucode/*' \) | sed 's|.*external-firmware/||' | sort | xargs)"
205:
206:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
207:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
208:   elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "SM8250" ]; then
209:     mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8250
210:     mkdir -p ${PKG_BUILD}/external-firmware/qcom/vpu-1.0
211:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/a650_gmu.bin ${PKG_BUILD}/external-firmware/qcom
212:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/a650_sqe.fw ${PKG_BUILD}/external-firmware/qcom
213:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/a650_zap.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
214:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/adsp.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
215:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/cdsp.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
216:       cp $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/Thundercomm/RB5/* $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/
217:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/slpi.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
218:
219:     FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
220:
221:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
222:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
223:   elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "H700" ]; then
224:     mkdir -p ${PKG_BUILD}/external-firmware/rtl_bt
225:     mkdir -p ${PKG_BUILD}/external-firmware/rtw88
226:     mkdir -p ${PKG_BUILD}/external-firmware/panels
227:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/rtl_bt/rtl8821cs_config.bin ${PKG_BUILD}/external-firmware/rtl_bt
228:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/rtl_bt/rtl8821cs_fw.bin ${PKG_BUILD}/external-firmware/rtl_bt
229:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/rtw88/rtw8821c_fw.bin ${PKG_BUILD}/external-firmware/rtw88
230:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg28xx-panel.panel ${PKG_BUILD}/external-firmware/panels
231:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg34xx-panel.panel ${PKG_BUILD}/external-firmware/panels
232:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg34xx-sp-panel.panel ${PKG_BUILD}/external-firmware/panels
233:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg34xx-sp-v2-panel.panel ${PKG_BUILD}/external-firmware/panels
234:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg35xx-plus-panel.panel ${PKG_BUILD}/external-firmware/panels
235:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg35xx-plus-rev6-panel.panel ${PKG_BUILD}/external-firmware/panels
236:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg35xx-sp-v2-panel.panel ${PKG_BUILD}/external-firmware/panels
237:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg40xx-panel.panel ${PKG_BUILD}/external-firmware/panels
238:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg40xx-v2-panel.panel ${PKG_BUILD}/external-firmware/panels
239:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rgcubexx-panel.panel ${PKG_BUILD}/external-firmware/panels
240:
241:     FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
242:
243:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
244:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
245:   elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "SM8650" ]; then
246:     mkdir -p ${PKG_BUILD}/external-firmware/qcom
247:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen70900_aqe.fw ${PKG_BUILD}/external-firmware/qcom
248:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen70900_sqe.fw ${PKG_BUILD}/external-firmware/qcom
249:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gmu_gen70900.bin ${PKG_BUILD}/external-firmware/qcom
250:     mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8650/ayaneo/ps2
251:       cp -Lv $(get_build_dir extra-firmware)/SM8650/qcom/sm8650/ayaneo/ps2/gen70900_zap.mbn ${PKG_BUILD}/external-firmware/qcom/sm8650/ayaneo/ps2
252:
253:     FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
254:
255:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
256:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
257:   elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "SM8750" ]; then
258:     mkdir -p ${PKG_BUILD}/external-firmware/qcom
259:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen80000_aqe.fw ${PKG_BUILD}/external-firmware/qcom
260:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen80000_sqe.fw ${PKG_BUILD}/external-firmware/qcom
261:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen80000_gmu.bin ${PKG_BUILD}/external-firmware/qcom
262:
263:     mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8750
264:       cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8750/gen80000_zap.mbn ${PKG_BUILD}/external-firmware/qcom/sm8750
265:
266:     # KONKR Pocket FIT Elite: AW88261 speaker-amp ACF (vendor cal/profile blob,
267:     # extracted from the stock Android image). The aw88261 driver requests the
268:     # blob; the amp nodes point at it with firmware-name. Built-in so the codec
269:     # probe never depends on the rootfs firmware overlay.
270:     mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8750/konkr/pfe
271:       cp -Lv $(get_build_dir extra-firmware)/SM8750/qcom/sm8750/konkr/pfe/aw88261_acf.bin ${PKG_BUILD}/external-firmware/qcom/sm8750/konkr/pfe
272:
273:     # KONKR Pocket FIT Elite: QUAT-MI2S audio topology (the AYN tplg with its
274:     # MI2S backend retargeted SECONDARY->QUATERNARY — the konkr's speaker amps
275:     # are on QUATERNARY MI2S). Built-in firmware is searched before the rootfs,
276:     # so this also overrides any stale copy in the SYSTEM overlay.
277:       cp -Lv $(get_build_dir extra-firmware)/SM8750/qcom/sm8750/SM8750-KONKR-tplg.bin ${PKG_BUILD}/external-firmware/qcom/sm8750
278:
279:     FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
280:
281:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
282:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
283:   fi
284:
285:   # cfg80211 requests regulatory.db as soon as it initialises. Built in (=y on
286:   # every device but AMD64) that is during kernel init, while /usr/lib/firmware
287:   # is still a dangling symlink to the kernel-overlay tmpfs that
288:   # kernel-overlays-setup only populates later (scripts/image) - so the request
289:   # fails with -ENOENT, the failure is cached, and the radio stays in domain 00
290:   # with 5 GHz no-IR. Build the db into the kernel instead. The .p7s signature
291:   # goes with it because CONFIG_CFG80211_REQUIRE_SIGNED_REGDB is set. Appends to
292:   # whatever the per-device blocks above already listed (~7 KB in the image).
293:   if grep -q '^CONFIG_CFG80211=y' ${PKG_BUILD}/.config; then
294:     mkdir -p ${PKG_BUILD}/external-firmware
295:       cp -Lv $(get_build_dir wireless-regdb)/regulatory.db ${PKG_BUILD}/external-firmware
296:       cp -Lv $(get_build_dir wireless-regdb)/regulatory.db.p7s ${PKG_BUILD}/external-firmware
297:
298:     FW_LIST="$(${PKG_BUILD}/scripts/config --state CONFIG_EXTRA_FIRMWARE)"
299:     [ "${FW_LIST}" = "undef" ] && FW_LIST=""
300:
301:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE \
302:       "$(echo ${FW_LIST} regulatory.db regulatory.db.p7s | xargs)"
303:     ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
304:   fi
305:
306:   kernel_make listnewconfig
307:   if [ "${INTERACTIVE_CONFIG}" = "yes" ]; then
308:     # manually answer .config changes
309:     kernel_make oldconfig
310:   elif [ "${INTERACTIVE_CONFIG}" = "menuconfig" ]; then
311:     # manually answer .config changes
312:     kernel_make menuconfig
313:   else
314:     # accept default answers for .config changes
315:     yes "" | kernel_make oldconfig > /dev/null
316:   fi
317:
318:   if [ -f "${DISTRO_DIR}/${DISTRO}/kernel_options" ]; then
319:     while read OPTION; do
320:       [ -z "${OPTION}" -o -n "$(echo "${OPTION}" | grep '^#')" ] && continue
321:
322:       if [ "${OPTION##*=}" == "n" -a "$(${PKG_BUILD}/scripts/config --state ${OPTION%%=*})" == "undef" ]; then
323:         continue
324:       fi
325:
326:       if [ "$(${PKG_BUILD}/scripts/config --state ${OPTION%%=*})" != "$(echo ${OPTION##*=} | tr -d '"')" ]; then
327:         MISSING_KERNEL_OPTIONS+="\t${OPTION}\n"
328:       fi
329:     done < ${DISTRO_DIR}/${DISTRO}/kernel_options
330:
331:     if [ -n "${MISSING_KERNEL_OPTIONS}" ]; then
332:       print_color CLR_WARNING "LINUX: kernel options not correct: \n${MISSING_KERNEL_OPTIONS%%}\nPlease run ./tools/check_kernel_config\n"
333:     fi
334:   fi
335: }
336:
337: make_target() {
338:   DTC_FLAGS=-@ kernel_make ${KERNEL_TARGET} ${KERNEL_MAKE_EXTRACMD} modules
339:
340:   if [ "${PKG_BUILD_PERF}" = "yes" ]; then
341:     ( cd tools/perf
342:
343:       # arch specific perf build args
344:       case "${TARGET_ARCH}" in
345:         x86_64|i*86)
346:           PERF_BUILD_ARGS="ARCH=x86"
347:           ;;
348:         aarch64)
349:           PERF_BUILD_ARGS="ARCH=arm64"
350:           ;;
351:         *)
352:           PERF_BUILD_ARGS="ARCH=${TARGET_ARCH}"
353:           ;;
354:       esac
355:
356:       [[ "${DEVICE}" != "RK3588" ]] && export BUILD_BPF_SKEL=0
357:
358:       WERROR=0 \
359:       NO_LIBPERL=1 \
360:       NO_LIBPYTHON=1 \
361:       NO_SLANG=1 \
362:       NO_GTK2=1 \
363:       NO_LIBNUMA=1 \
364:       NO_LIBAUDIT=1 \
365:       NO_LIBTRACEEVENT=1 \
366:       NO_LZMA=1 \
367:       NO_SDT=1 \
368:       NO_LIBDEBUGINFOD=1 \
369:       NO_JVMTI=1 \
370:       NO_LIBLLVM=1 \
371:       NO_LIBPFM4=1 \
372:       NO_LIBBABELTRACE=1 \
373:       NO_CAPSTONE=1 \
374:       CROSS_COMPILE="${TARGET_PREFIX}" \
375:       JOBS="${CONCURRENCY_MAKE_LEVEL}" \
376:         make ${PERF_BUILD_ARGS}
377:       mkdir -p ${INSTALL}/usr/bin
378:         cp perf ${INSTALL}/usr/bin
379:     )
380:   fi
381: }
382:
383: makeinstall_target() {
384:   mkdir -p ${INSTALL}/.image
385:   cp -p System.map .config Module.symvers ${INSTALL}/.image/
386:
387:   if [ "${BOOTLOADER}" != "qcom-abl" ]; then
388:    cp -p arch/${TARGET_KERNEL_ARCH}/boot/${KERNEL_TARGET} ${INSTALL}/.image/
389:   else
390:
391:     gzip -c "arch/${TARGET_KERNEL_ARCH}/boot/${KERNEL_TARGET}" > "${INSTALL}/.image/kernel.gz"
392:     for dtb in "arch/${TARGET_KERNEL_ARCH}/boot/dts/"**/*.dtb; do
393:       if [ -f ${dtb} ]; then
394:         cat "$dtb" >> "${INSTALL}/.image/kernel.gz"
395:       fi
396:     done
397:     echo -n "dummy" > "${INSTALL}/.image/ramdisk"
398:     python3 "${TOOLCHAIN}/mkbootimg/mkbootimg.py" \
399:       --kernel "${INSTALL}/.image/kernel.gz" --ramdisk "${INSTALL}/.image/ramdisk" \
400:      --kernel_offset 0x00000000 --ramdisk_offset 0x00000000 --tags_offset 0x00000000 \
401:      --os_version 12.0.0 --os_patch_level "$(date '+%Y-%m')" --header_version 0 \
402:      --cmdline "boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} ${EXTRA_CMDLINE}" \
403:      -o "${INSTALL}/.image/${KERNEL_TARGET}" || { exit 1; }
404:   fi
405:
406:   kernel_make INSTALL_MOD_PATH=${INSTALL}/$(get_kernel_overlay_dir) modules_install
407:   rm -f ${INSTALL}/$(get_kernel_overlay_dir)/lib/modules/*/build
408:   rm -f ${INSTALL}/$(get_kernel_overlay_dir)/lib/modules/*/source
409:
410:   if [ "${BOOTLOADER}" = "arm-efi" ]; then
411:     mkdir -p ${INSTALL}/usr/share/bootloader/boot/grub
412:     for dtb in arch/${TARGET_KERNEL_ARCH}/boot/dts/**/*.dtb; do
413:       if [ -f ${dtb} ]; then
414:           cp -v ${dtb} ${INSTALL}/usr/share/bootloader/boot/grub
415:       fi
416:     done
417:   fi
418:
419:   if [ "${BOOTLOADER}" = "u-boot" ]; then
420:     mkdir -p ${INSTALL}/usr/share/bootloader
421:     for dtb in arch/${TARGET_KERNEL_ARCH}/boot/dts/**/*.dtb; do
422:       if [ -f ${dtb} ]; then
423:         if [ "${DEVICE}" = "H700" -o "${DEVICE}" = "RK3326" -o "${DEVICE}" = "RK3399" -o "${DEVICE}" = "RK3566" -o "${DEVICE}" = "RK3576" -o "${DEVICE}" = "RK3588" ]; then
424:           mkdir -p ${INSTALL}/usr/share/bootloader/device_trees
425:           cp -v ${dtb} ${INSTALL}/usr/share/bootloader/device_trees
426:         else
427:           cp -v ${dtb} ${INSTALL}/usr/share/bootloader
428:         fi
429:       fi
430:     done
431:   fi
432: }

## Unpack, read only

118:
119:   # cleanup
120:   rm -rf "${PKG_UNPACK_DIR}"
121:
122:   pkg_call_exists_opt post_unpack && pkg_call
123:
124:   if [ "${PKG_SKIP_PATCHES}" != "yes" ]; then
125:     pkg_call_exists_opt pre_patch && pkg_call
126:
127:     if [ "${TARGET_ARCH}" = "x86_64" ]; then
128:       PATCH_ARCH="x86"
129:     elif [ "${PKG_IS_KERNEL_PKG}" = "yes" ]; then
130:       PATCH_ARCH="${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}"
131:     else
132:       PATCH_ARCH="${TARGET_PATCH_ARCH:-${TARGET_ARCH}}"
133:     fi
134:
135:     PATCH_DIRS_PKG=""
136:     PATCH_DIRS_PRJ=""
137:     if [ -n "${PKG_PATCH_DIRS}" ]; then
138:       for patch_dir in ${PKG_PATCH_DIRS}; do
139:         if [[ ${patch_dir} =~ ^/ ]]; then
140:           [ -f ${patch_dir} ] && PATCH_DIRS_PKG+=" ${patch_dir}"
141:           [ -d ${patch_dir} ] && PATCH_DIRS_PKG+=" ${patch_dir}/*.patch"
142:         else
143:           [ -d ${PKG_DIR}/patches/${patch_dir} ] && PATCH_DIRS_PKG+=" ${PKG_DIR}/patches/${patch_dir}/*.patch"
144:           [ -d ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${patch_dir} ] && PATCH_DIRS_PRJ+=" ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${patch_dir}/*.patch"
145:           [ -d ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/${patch_dir} ] && PATCH_DIRS_PRJ+=" ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/${patch_dir}/*.patch"
146:         fi
147:       done
148:     fi
149:
150:     for i in ${PKG_DIR}/patches/*.patch \
151:       ${PKG_DIR}/patches/${PATCH_ARCH}/*.patch \
152:       ${PATCH_DIRS_PKG} \
153:       ${PKG_DIR}/patches/${PKG_VERSION}/*.patch \
154:       ${PKG_DIR}/patches/${PKG_VERSION}/${PATCH_ARCH}/*.patch \
155:       ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/*.patch \
156:       ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PATCH_ARCH}/*.patch \
157:       ${PATCH_DIRS_PRJ} \
158:       ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION}/*.patch \
159:       ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/*.patch; do
160:
161:       thisdir="${i%/*}"
162:
163:       if [ "${thisdir}" = "${PKG_DIR}/patches" ]; then
164:         PATCH_DESC="(common)"
165:       elif [ "${thisdir}" = "${PKG_DIR}/patches/${PATCH_ARCH}" ]; then
166:         PATCH_DESC="(common - ${PATCH_ARCH})"
167:       elif [ "${thisdir}" = "${PKG_DIR}/patches/${PKG_VERSION}" ]; then
168:         PATCH_DESC="(common - ${PKG_VERSION})"
169:       elif [ "${thisdir}" = "${PKG_DIR}/patches/${PKG_VERSION}/${PATCH_ARCH}" ]; then
170:         PATCH_DESC="(${PKG_VERSION} - ${PATCH_ARCH})"
171:       elif [ "${thisdir}" = "${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}" ]; then
172:         PATCH_DESC="(project)"
173:       elif [ "${thisdir}" = "${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PATCH_ARCH}" ]; then
174:         PATCH_DESC="(project - ${PATCH_ARCH})"
175:       elif [ "${thisdir}" = "${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION}" ]; then
176:         PATCH_DESC="(project - ${PKG_VERSION})"
177:       elif [ "${thisdir}" = "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}" ]; then
178:         PATCH_DESC="(device)"
179:       else
180:         if [[ "${thisdir}" =~ ^${PKG_DIR}/.* ]]; then
181:           PATCH_DESC="(common - ${thisdir##*/})"
182:         elif [[ "${thisdir}" =~ ^${PROJECT_DIR}/.*/devices/.* ]]; then
183:           PATCH_DESC="(device - ${thisdir##*/})"
184:         elif [[ "${thisdir}" =~ ^${PROJECT_DIR}/.* ]]; then
185:           PATCH_DESC="(project - ${thisdir##*/})"
186:         else
187:           PATCH_DESC="(absolute - ${i})"
188:         fi
189:       fi
190:
191:       if [ -f "${i}" ]; then
192:         build_msg "CLR_APPLY_PATCH" "APPLY PATCH $(print_color "CLR_PATCH_DESC" "${PATCH_DESC}")" "${i#${ROOT}/}"
193:         if grep -qE '^GIT binary patch$|^rename from|^rename to' ${i}; then
194:           git apply --directory="${PKG_BUILD}" -p1 --verbose --whitespace=nowarn --unsafe-paths <${i} >&${VERBOSE_OUT}
195:         else
196:           patch -d "${PKG_BUILD}" -p1 < <(sed -e "s#@TARGET_CPU@#${TARGET_CPU}#g" -e "s#@DEVICE@#${DEVICE}#g" "${i}") >&"${VERBOSE_OUT}"

## Config resolution, read only

1449: kernel_config_path() {
1450:   local cfg pkg_linux_dir pkg_linux_version config_name
1451:
1452:   pkg_linux_version="$(get_pkg_version linux)"
1453:   pkg_linux_dir="$(get_pkg_directory linux)"
1454:
1455:   config_name="linux.${TARGET_KERNEL_PATCH_ARCH:-$TARGET_ARCH}.conf"
1456:
1457:   for cfg in $PROJECT_DIR/$PROJECT/devices/$DEVICE/linux/$pkg_linux_version/$config_name \
1458:              $PROJECT_DIR/$PROJECT/devices/$DEVICE/linux/$LINUX/$config_name \
1459:              $PROJECT_DIR/$PROJECT/devices/$DEVICE/linux/$config_name \
1460:              $PROJECT_DIR/$PROJECT/linux/$pkg_linux_version/$config_name \
1461:              $PROJECT_DIR/$PROJECT/linux/$LINUX/$config_name \
1462:              $PROJECT_DIR/$PROJECT/linux/$config_name \
1463:              $pkg_linux_dir/config/$pkg_linux_version/$config_name \
1464:              $pkg_linux_dir/config/$LINUX/$config_name \
1465:              $pkg_linux_dir/config/$config_name \
1466:              ; do
1467:     [[ $cfg =~ /devices//linux/ ]] && continue
1468:     [ -f "$cfg" ] && echo "$cfg" && return
1469:   done
1470:
1471:   die "ERROR: Unable to locate kernel config for ${LINUX} - looking for ${config_name}"
1472: }

## arm patch arch

80:     TARGET_KERNEL_PATCH_ARCH="aarch64"

## 0010 upstream fix message

commit 9416eec2c200ad969d9e421e686fc7cbfdaca36a
Author:     JS Deck <jsdeckerido@gmail.com>
AuthorDate: Tue Oct 6 21:22:05 2026 -0300
Commit:     JS Deck <jsdeckerido@gmail.com>
CommitDate: Tue Oct 6 21:22:05 2026 -0300

    kernel: msm dp resource cleanup patch fix uninit pointer

    Previous version writes to field pointed by an uninitialized pointer.
    As noticed by armada distro, which carries a fixed version.


## 0010 diff and stat

 .../patches/7.0/0010-msm-resource-cleanup.patch    | 25 ++++++++++++----------
 .../patches/7.2/0010-msm-resource-cleanup.patch    | 25 ++++++++++++----------
 2 files changed, 28 insertions(+), 22 deletions(-)
diff --git a/projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch b/projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch
index 185aa255bb..1cc7700260 100644
--- a/projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch
+++ b/projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch
@@ -1,26 +1,27 @@
-From 2f02429bcbd2dc0235d9654456db87c6f5e9122a Mon Sep 17 00:00:00 2001
+From 832947a7b21779343f0c0def4d5c7a393c9c2e53 Mon Sep 17 00:00:00 2001
 From: JS Deck <jsdeckerido@gmail.com>
 Date: Sun, 10 May 2026 20:20:07 -0300
 Subject: [PATCH 1/7] drm/msm/dpu: release topology on reservation failure to
  avoid persistent failure due to partial reservation

 ---
- drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c | 9 ++++++++-
- 1 file changed, 8 insertions(+), 1 deletion(-)
+ drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c | 13 ++++++++++---
+ 1 file changed, 10 insertions(+), 3 deletions(-)

 diff --git a/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c b/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c
-index 0f4921b1a892..f8d8c2d7f9d6 100644
+index 42d0a529b4d5..6431e9129fa4 100644
 --- a/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c
 +++ b/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c
-@@ -1442,6 +1442,7 @@ static int dpu_crtc_assign_resources(struct drm_crtc *crtc,
-               return PTR_ERR(global_state);
+@@ -1451,16 +1451,23 @@ static int dpu_crtc_assign_resources(struct drm_crtc *crtc,

        dpu_rm_release(global_state, crtc);
-+      cstate->num_mixers = 0;

++      cstate = to_dpu_crtc_state(crtc_state);
++      cstate->num_mixers = 0;
++
        if (!crtc_state->enable)
                return 0;
-@@ -1449,8 +1450,14 @@ static int dpu_crtc_assign_resources(struct drm_crtc *crtc,
+
        topology = dpu_crtc_get_topology(crtc, dpu_kms, crtc_state);
        ret = dpu_rm_reserve(&dpu_kms->rm, global_state,
                             crtc_state->crtc, &topology);
@@ -32,12 +33,14 @@ index 0f4921b1a892..f8d8c2d7f9d6 100644
 +               */
 +              dpu_rm_release(global_state, crtc);
                return ret;
+-
+-      cstate = to_dpu_crtc_state(crtc_state);
 +      }

-       cstate = to_dpu_crtc_state(crtc_state);
-
+       num_ctl = dpu_rm_get_assigned_resources(&dpu_kms->rm, global_state,
+                                               crtc_state->crtc,
 --
-2.54.0
+2.55.0


 From 6a92dfa8cb99a772076f7106bccda0c2f0469dd9 Mon Sep 17 00:00:00 2001


## 0010 source patch opening

1: From 2f02429bcbd2dc0235d9654456db87c6f5e9122a Mon Sep 17 00:00:00 2001
2: From: JS Deck <jsdeckerido@gmail.com>
3: Date: Sun, 10 May 2026 20:20:07 -0300
4: Subject: [PATCH 1/7] drm/msm/dpu: release topology on reservation failure to
5:  avoid persistent failure due to partial reservation
6:
7: ---
8:  drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c | 9 ++++++++-
9:  1 file changed, 8 insertions(+), 1 deletion(-)
10:
11: diff --git a/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c b/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c
12: index 0f4921b1a892..f8d8c2d7f9d6 100644
13: --- a/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c
14: +++ b/drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c
15: @@ -1442,6 +1442,7 @@ static int dpu_crtc_assign_resources(struct drm_crtc *crtc,
16:             return PTR_ERR(global_state);
17:
18:     dpu_rm_release(global_state, crtc);
19: +   cstate->num_mixers = 0;
20:
21:     if (!crtc_state->enable)
22:             return 0;
23: @@ -1449,8 +1450,14 @@ static int dpu_crtc_assign_resources(struct drm_crtc *crtc,
24:     topology = dpu_crtc_get_topology(crtc, dpu_kms, crtc_state);
25:     ret = dpu_rm_reserve(&dpu_kms->rm, global_state,
26:                          crtc_state->crtc, &topology);
27: -   if (ret)
28: +   if (ret) {
29: +           /*
30: +            * Release on reserve failure to since partial reservation will prevent
31: +            * future reservation from working.
32: +            */
33: +           dpu_rm_release(global_state, crtc);
34:             return ret;
35: +   }
36:
37:     cstate = to_dpu_crtc_state(crtc_state);
38:
39: --
40: 2.54.0
41:
42:
43: From 6a92dfa8cb99a772076f7106bccda0c2f0469dd9 Mon Sep 17 00:00:00 2001
44: From: JS Deck <jsdeckerido@gmail.com>
45: Date: Sun, 10 May 2026 20:33:56 -0300
46: Subject: [PATCH 2/7] drm/msm/dpu: reset unassigned resource slots to NULL on
47:  topology update
48:
49: ---
50:  drivers/gpu/drm/msm/disp/dpu1/dpu_encoder.c | 22 ++++++++++++++-------
51:  1 file changed, 15 insertions(+), 7 deletions(-)
52:
53: diff --git a/drivers/gpu/drm/msm/disp/dpu1/dpu_encoder.c b/drivers/gpu/drm/msm/disp/dpu1/dpu_encoder.c
54: index eba1d52211f6..334a49106e6f 100644
55: --- a/drivers/gpu/drm/msm/disp/dpu1/dpu_encoder.c
56: +++ b/drivers/gpu/drm/msm/disp/dpu1/dpu_encoder.c
57: @@ -1206,9 +1206,13 @@ static void dpu_encoder_virt_atomic_mode_set(struct drm_encoder *drm_enc,
58:                                                    ARRAY_SIZE(hw_pp));
59:     }
60:
61: -   for (i = 0; i < num_cwb; i++) {
62: -           dpu_enc->hw_cwb[i] = to_dpu_hw_cwb(hw_cwb[i]);
63: -           cwb_mask |= BIT(dpu_enc->hw_cwb[i]->idx - CWB_0);
64: +   for (i = 0; i < ARRAY_SIZE(dpu_enc->hw_cwb); i++) {
65: +           if (i < num_cwb) {

## Final SM8550 patched dpu_crtc.c around num_mixers reset

1431:
1432: static int dpu_crtc_assign_resources(struct drm_crtc *crtc,
1433:                                struct drm_crtc_state *crtc_state)
1434: {
1435:   struct dpu_hw_blk *hw_ctl[MAX_CHANNELS_PER_CRTC];
1436:   struct dpu_hw_blk *hw_lm[MAX_CHANNELS_PER_CRTC];
1437:   struct dpu_hw_blk *hw_dspp[MAX_CHANNELS_PER_CRTC];
1438:   int i, num_lm, num_ctl, num_dspp;
1439:   struct dpu_kms *dpu_kms = _dpu_crtc_get_kms(crtc);
1440:   struct dpu_global_state *global_state;
1441:   struct dpu_crtc_state *cstate;
1442:   struct msm_display_topology topology;
1443:   int ret;
1444:
1445:   /*
1446:    * Release and Allocate resources on every modeset
1447:    */
1448:   global_state = dpu_kms_get_global_state(crtc_state->state);
1449:   if (IS_ERR(global_state))
1450:           return PTR_ERR(global_state);
1451:
1452:   dpu_rm_release(global_state, crtc);
1453:   cstate->num_mixers = 0;
1454:
1455:   if (!crtc_state->enable)
1456:           return 0;
1457:
1458:   topology = dpu_crtc_get_topology(crtc, dpu_kms, crtc_state);
1459:   ret = dpu_rm_reserve(&dpu_kms->rm, global_state,
1460:                        crtc_state->crtc, &topology);
1461:   if (ret) {
1462:           /*
1463:            * Release on reserve failure to since partial reservation will prevent
1464:            * future reservation from working.
1465:            */
1466:           dpu_rm_release(global_state, crtc);
1467:           return ret;
1468:   }
1469:
1470:   cstate = to_dpu_crtc_state(crtc_state);
1471:
1472:   num_ctl = dpu_rm_get_assigned_resources(&dpu_kms->rm, global_state,
1473:                                           crtc_state->crtc,
1474:                                           DPU_HW_BLK_CTL, hw_ctl,
1475:                                           ARRAY_SIZE(hw_ctl));
1476:   num_lm = dpu_rm_get_assigned_resources(&dpu_kms->rm, global_state,
1477:                                          crtc_state->crtc,
1478:                                          DPU_HW_BLK_LM, hw_lm,
1479:                                          ARRAY_SIZE(hw_lm));
1480:   num_dspp = dpu_rm_get_assigned_resources(&dpu_kms->rm, global_state,

## 0010 intent history

0c77a91dca 2026-08-21 linux: update H700 to kernel 7.2


## Polldev rename history

commit fe5216ff6999e07e74dc59d5cea8651e7621d073
Author:     Mike <7153163+hackbar@users.noreply.github.com>
AuthorDate: Wed Sep 16 17:35:46 2026 -0700
Commit:     Mike <7153163+hackbar@users.noreply.github.com>
CommitDate: Fri Oct 9 12:01:49 2026 -0700

    rocknix-joypad: update version

    Move input-polldev patch to device-specific dir for RK3326, since now
    that's the only device that needs it. It's used for
    004-input-drivers.patch there.

 .../RK3326/patches/linux/003-input-add-input-polldev-driver.patch}  | 0
 projects/ROCKNIX/packages/linux-drivers/rocknix-joypad/package.mk   | 6 +++---
 2 files changed, 3 insertions(+), 3 deletions(-)


## Polldev consumers



## BLS upstream history

commit cafbb1657d57aee0dd0c3fe507b9dcc5d7262e54
Author:     spycat88 <spycat88@users.noreply.github.com>
AuthorDate: Thu Oct 22 00:19:05 2026 +0000
Commit:     spycat88 <spycat88@users.noreply.github.com>
CommitDate: Thu Oct 22 00:27:17 2026 +0000

    Qualcomm: change from boot.img to Boot Loader Spec for booting


## Upstream recipe line 18

16: PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"
17:
18: [[ "${DEVICE}" =~ "RK3326|RK3399|S922X|H700" ]] && PKG_PATCH_DIRS+=" rocknix-joypad"
19: [[ "${DEVICE}" == RK* ]] && PKG_PATCH_DIRS+=" mainline-rockchip"
20:

## projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch

8: +    rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-2024";
19: +   rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-h";
30: +   rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-plus";
41: +   rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-sp";

## projects/ROCKNIX/devices/SM8550/patches/linux/0105-drm-panel-Add-Retroid-Pocket-Nova-panel.patch

122: +static int il97680a_rpnova_init_sequence(struct panel_info *pinfo)
165: +static const struct drm_display_mode il97680a_rpnova_modes[] = {
192: +static struct panel_desc il97680a_rpnova_desc = {
193: +  .modes = il97680a_rpnova_modes,
194: +  .num_modes = ARRAY_SIZE(il97680a_rpnova_modes),
205: +  .init_sequence = il97680a_rpnova_init_sequence,
436: +  { .compatible = "il97680a,rpnova", .data = &il97680a_rpnova_desc },

## projects/ROCKNIX/devices/SM8550/patches/linux/0501-ROCKNIX-fix-wifi-and-bt-mac.patch

4: Subject: [PATCH] drivers: use soc serial for wifi and bluetooth
20: +extern const char *qcom_serial_number;
28: + * generate_bdaddr_from_serial - Generates a BD_ADDR using the serial number
32: + * are derived from the last 6 characters of qcom_serial_number in reversed order.
36: +static int generate_bdaddr_from_serial(struct hci_dev *hdev, bdaddr_t *bdaddr)
38: +   size_t serial_len;
39: +   const char *serial = qcom_serial_number;
44: +   if (!serial) {
45: +           bt_dev_err(hdev, "qcom_serial_number is NULL");
49: +   serial_len = strlen(serial);
50: +   if (serial_len < 6) {
51: +           bt_dev_err(hdev, "qcom_serial_number is too short: %zu characters", serial_len);
56: +   memcpy(last6, serial + serial_len - 6, 6);
72: +                   bt_dev_err(hdev, "Invalid hex characters in serial number: %c%c",
118: +  /* Generate BD_ADDR from qcom_serial_number */
119: +  err = generate_bdaddr_from_serial(hdev, &generated_bdaddr);
121: +          bt_dev_err(hdev, "Failed to generate BD_ADDR from serial number");
128: +          bt_dev_err(hdev, "Failed to set the generated BD_ADDR from serial number");
153: +/* Global variable to hold the serial number */
154: +const char *qcom_serial_number;
155: +EXPORT_SYMBOL(qcom_serial_number);
161:                                                    le32_to_cpu(info->serial_num));
162:            if (!qs->attr.serial_number)
165: +          /* Assign the serial number to the global variable */
166: +          qcom_serial_number = qs->attr.serial_number;
175: +  /* Clear the global serial number */
176: +  qcom_serial_number = NULL;
188: +extern const char *qcom_serial_number;
201: + * generate_macaddr_from_serial - Generates a MAC_ADDR using the serial number
205: + * are derived from the last 6 characters of qcom_serial_number.
209: +static int generate_macaddr_from_serial(struct ath12k *ar, struct macaddr_t *macaddr)
211: +  size_t serial_len;
212: +  const char *serial = qcom_serial_number;
217: +  if (!serial) {
218: +          ath12k_err(ar->ab, "qcom_serial_number is NULL");
222: +  serial_len = strlen(serial);
223: +  if (serial_len < 6) {
224: +          ath12k_err(ar->ab, "qcom_serial_number is too short: %zu characters", serial_len);
229: +  memcpy(last6, serial + serial_len - 6, 6);
245: +                  ath12k_err(ar->ab, "Invalid hex characters in serial number: %c%c",
290: +          ret = generate_macaddr_from_serial(ar, &generated_macaddr);

## dt-id consumer

02aab33bd9842610b0d466c9c186454dc14373ee:projects/ROCKNIX/devices/H700/bootloader/update.sh:26:DT_ID=$(cat /proc/device-tree/rocknix-dt-id)


## New dispcc patch header

1: From: tiopex <tiopxyz@gmail.com>
2: Subject: [PATCH] clk: qcom: blank DSI panels before dispcc parks boot clocks
3:
4: The bootloader leaves splash on. PLL configure drops PLL_OUTCTRL and
5: clk_rcg2_shared_ops parks the MDP RCG to XO; both glitch any panel
6: that is still emitting.
7:
8: Hold every qcom,mdss-dsi-ctrl child reset GPIO (DT polarity) and wait
9: one frame before those calls, then release after clock registration
10: so the panel driver can take them. Shared helper;
11:
12: ---
13:  drivers/clk/qcom/common.c        |  62 ++++++++++++++++++++++++++++++++++++++++
14:  drivers/clk/qcom/common.h        |  11 +++++++++++
15:  drivers/clk/qcom/dispcc-sm8250.c |   8 ++++++++
16:  drivers/clk/qcom/dispcc-sm8550.c |   6 ++++++
17:  drivers/clk/qcom/dispcc-sm8750.c |   6 ++++++
18:  5 files changed, 93 insertions(+)
19:
20: diff --git a/drivers/clk/qcom/common.c b/drivers/clk/qcom/common.c

## Pristine 7.2 ramoops context

105:             * to propagate this into the DTB handed to kernels.
106:             */
107:            secmon@40000000 {
108:                    reg = <0x0 0x40000000 0x0 0x40000>;
109:                    no-map;
110:            };
111:    };
112:
113:    osc24M: osc24M-clk {
ramoops count: 0

## Ramoops fork/upstream history

cbf75c0b06 2026-09-10 Max Engel Handhelds keep their evidence across a power cycle: persistent logs, a watchdog, a crash store
ancestor rc 1
upstream ramoops names: 0

## Upstream delta

M       projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf
M       projects/ROCKNIX/devices/SM8550/patches/linux/0104-drm-panel-Add-Retroid-Pocket-6-panel.patch
A       projects/ROCKNIX/devices/SM8550/patches/linux/0508-ROCKNIX-rp6-panel-frame-length-calibration.patch
A       projects/ROCKNIX/devices/SM8550/patches/linux/0509-ROCKNIX-thor-panel-frame-length-calibration.patch
M       projects/ROCKNIX/packages/linux/patches/7.0/0010-msm-resource-cleanup.patch
A       projects/ROCKNIX/packages/linux/patches/7.2.6/0010-msm-resource-cleanup.patch
A       projects/ROCKNIX/packages/linux/patches/7.2.6/0013-drm-msm-dpu-fix-inline-rotation.patch
A       projects/ROCKNIX/packages/linux/patches/7.2.6/9998-silence-initramfs-unpack-warn.patch
A       projects/ROCKNIX/packages/linux/patches/7.2.6/9999-fix-rust-build-error.patch
M       projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch
A       projects/ROCKNIX/packages/linux/patches/7.2/0011-drm-msm-signal-hw_done-before-the-flip-event.patch
A       projects/ROCKNIX/packages/linux/patches/7.2/0012-drm-msm-dpu-qos-lut-for-scaled-compressed-fetch.patch
A       projects/ROCKNIX/packages/linux/patches/7.2/0014-drm-msm-dpu-scaled-fetch-line-width.patch
A       projects/ROCKNIX/packages/linux/patches/7.2/0015-drm-msm-dpu-sm8250-linear-danger-lut.patch
A       projects/ROCKNIX/packages/linux/patches/7.2/0017-clk-qcom-blank-dsi-panels-before-dispcc-park.patch
A       projects/ROCKNIX/packages/linux/patches/7.2/0018-drm-msm-dpu-preload-seven-pixels-in-qseed4-behind-the-inline-rotator.patch
D       projects/ROCKNIX/packages/linux/patches/mainline/0002-input-add-input-polldev-driver.patch


## Symlinks under member roofs

projects/ROCKNIX/devices/RK3566/filesystem/usr/share/alsa/ucm2/conf.d/aw88166/aw88166.conf -> ../../Anbernic/RG-DS-Plus/aw88166.conf
projects/ROCKNIX/devices/RK3566/filesystem/usr/share/alsa/ucm2/conf.d/simple-card/rk817_hp.conf -> ../../Anbernic/RG-DS-Plus/rk817_hp.conf
projects/ROCKNIX/devices/SM8750/filesystem/usr/share/alsa/ucm2/conf.d/sm8750/SM8750-KONKR.conf -> ../../KONKR/PocketFitElite/KONKR-PocketFitElite.conf

## Disabled siblings

projects/ROCKNIX/devices/H700/patches/linux/0002-rg35xx-enable-HDMI-LCD.patch
projects/ROCKNIX/devices/H700/patches/linux/0003-Update-sun8i_tcon_top.c.patch
projects/ROCKNIX/devices/H700/patches/linux/0007-rg35xx-add-GPU-opp.patch
projects/ROCKNIX/devices/H700/patches/linux/0008-v8_20260804_james_hilliard1_introduce_allwinner_h616_pwm_controller.patch
projects/ROCKNIX/devices/H700/patches/linux/0010-rg35xx-enable-pwm-backlight.patch
projects/ROCKNIX/devices/H700/patches/linux/0040-Revert-usb-musb-Fix-hardware-lockup-on-first-Rx-endp.patch
projects/ROCKNIX/devices/H700/patches/linux/0110-v2_20250226_kikuchan98_drm_panel_add_generic_mipi_panel_driver.patch
projects/ROCKNIX/devices/H700/patches/linux/0111-rg35xx-2024-use-panel-mipi-dpi-spi-driver.patch
projects/ROCKNIX/devices/H700/patches/linux/0124-battery-name.patch
projects/ROCKNIX/devices/H700/patches/linux/0126-20241018_macroalpha82_rg35xx_add_additional_hardware_support.patch
projects/ROCKNIX/devices/H700/patches/linux/0127-enable-mmc1-for-RG35XX-2024.patch
projects/ROCKNIX/devices/H700/patches/linux/0140-rg35xx-2024-use-rocknix-joypad-driver.patch
projects/ROCKNIX/devices/H700/patches/linux/0144-Update-sun50i-h700-anbernic-rg35xx-h.dts.patch
projects/ROCKNIX/devices/H700/patches/linux/0150-add-forcefeedback.patch
projects/ROCKNIX/devices/H700/patches/linux/0151-phy-fix-OTG-host-mode.patch
projects/ROCKNIX/devices/H700/patches/linux/0152-rg35xx-2024-enable-usb-otg.patch
projects/ROCKNIX/devices/H700/patches/linux/0153-enable-rgb-leds.patch
projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch
projects/ROCKNIX/devices/H700/patches/linux/0155-sun4i-set-rgb-connector-as-DSI.patch
projects/ROCKNIX/devices/H700/patches/linux/0156-rg35xx-plus-add-pcf8563-rtc.patch
projects/ROCKNIX/devices/H700/patches/linux/0157-input-axp20x-pek-do-not-report-the-key-press-that-woke-the-system.patch
projects/ROCKNIX/devices/H700/patches/linux/0158-mmc-sunxi-mmc-mask\u002ddata0-when-updating-the-clock-on-h616-emmc.patch
projects/ROCKNIX/devices/H700/patches/linux/0159-arm64-dts-rg35xx-2024-keep-the-second-sd-card-powered.patch
projects/ROCKNIX/devices/H700/patches/linux/0160-phy-sun4i-usb-disable-the-clock-that-was-enabled.patch
projects/ROCKNIX/devices/H700/patches/linux/0161-drm-sun4i-gate-the-display-pipeline-across-system-suspend.patch
projects/ROCKNIX/devices/H700/patches/linux/0162-pinctrl-sunxi-release-the-lcd0-pads-while-the-panel-is-off.patch
projects/ROCKNIX/devices/H700/patches/linux/0163-asoc-sun4i-codec-suspend-the-codec-and-switch-the-amplifier-supply.patch
projects/ROCKNIX/devices/H700/patches/linux/0200-h700-update-opps.patch
projects/ROCKNIX/devices/H700/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled
projects/ROCKNIX/devices/H700/patches/linux/0204-dts-Enable-hdmi-sound.patch
projects/ROCKNIX/devices/H700/patches/linux/0210-h616-cpu-opp-mark-480MHz-as-suspend-opp.patch
projects/ROCKNIX/devices/H700/patches/linux/0901-dts-rg35xx-2024-fix-led-1-color.patch
projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0001-pcie-update-sm8550-dtsi.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0002-qcom-dispcc-sm8550-Fix-disp_cc_mdss_mdp_clk_src.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0006-add-hw_params-callback-function-to-drm_connector_hdmi_audio_ops.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0015-touchscreen-edt-ft5x06-allow-to-override-input-name.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0030-input-rmi4-add-reset-gpio.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0031_input--Add-driver-for-RSInput-Gamepad.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0032-rmi4-silence-spam-irq-errors.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0033_leds--Add-driver-for-HEROIC-HTR3212.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0036_ASoC--qcom--sc8280xp-Add-support-for-Primary-I2S.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0047_ASoC--codecs--aw88166--AYN-Odin2-Specific-modifica.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0051-gpu-panel-add-Pocket-ACE-panel-driver.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0052-gpu-panel-add-Pocket-DMG-panel-driver.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled
projects/ROCKNIX/devices/SM8550/patches/linux/0053-edt-ft5x06-add-no_regmap_bulk_read-option.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0053-gpu-panel-st7703-add-Pocket-DS-lower-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0054-input-goodix-override-resolution-from-dt.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0054_sn3112-pwm-driver.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0055_Synaptics-TD4328-LCD-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0056_Xm-Plus-XM91080G-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0057_Chipone-ICNA35XX-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0057_DDIC-CH13726A-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0058_AYN-Odin2-Mini--backlight.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0059_AYN-Odin2-Mini--hynitron--cstxxx.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0060-Add-Silergy-SY7758-backlight-driver.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0060-input-touchscreen-add-synaptics-dsx-driver.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0060-input-touchscreen-add-synaptics-dsx-kconfig.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0062-gpu-drm-panel-add-wt0630-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0063-gpu-drm-panel-add-wt0600-1k-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0064-gpu-drm-panel-add-ar16-4inch-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0065-input-touchscreen-add-hynitron-cst66xx.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0066-drm-msm-dpu-enable-sm8550-inline-rotation.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0067-drm-msm-dpu-enable-qseed-detail-enhancer.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0071-HACK-fix-usb-boot-hang.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0104-drm-panel-Add-Retroid-Pocket-6-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0105-drm-panel-Add-Retroid-Pocket-Nova-panel.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0120-20250728_konradybcio_gpu_cc_power_requirements_reality_check.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0121-pmdomain-qcom-rpmhpd-presync-floor-gmu-rails.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0122-interconnect__qcom__sm8550__Enable_QoS_configuration.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0200-ASoC-wcd938x-add-DMIC-DAPM-inputs.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0500-ROCKNIX-set-boot-fanspeed.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0501-ROCKNIX-fix-wifi-and-bt-mac.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0502-wakeup-qcom-ipcc-remove-IRQF-NO-SUSPEND.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0503-ROCKNIX-battery-name.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0504-Enable-64-bit-processes-to-use-compat-input-syscalls.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0505-msm_gem-lock-before-put_iova_spaces.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0506-usbcore-add-interrupt-interval-override.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0507-wifi-ath12k-skip-11d-scan-on-ayaneo-pocket-s-mini.patch
projects/ROCKNIX/devices/SM8550/patches/linux/0612-ROCKNIX-odin3-q6apm-start-mi2s-port-at-prepare.patch
projects/ROCKNIX/devices/SM8550/patches/linux/1000-add-qcom-haptics-driver.patch
projects/ROCKNIX/devices/SM8550/patches/linux/1002-haptics-driver-support-periodic-sine-and-fixes.patch
projects/ROCKNIX/devices/SM8550/patches/linux/1003-rsinput-add-ff.patch
projects/ROCKNIX/devices/SM8550/patches/linux/1005-input-qcom-haptics-defer-rsinput-playback.patch
projects/ROCKNIX/devices/SM8550/patches/linux/1020-wifi-ath12k-send-the-computed-scan-priority-to-the-f.patch
projects/ROCKNIX/devices/SM8550/patches/linux/20260424_neil_armstrong_arm64_dts_qcom_sm8_456_50_add_missing_cx_power_domain_to_gcc.patch
projects/ROCKNIX/devices/SM8550/patches/linux/v6_20260210_quic_utiwari_crypto_qce_add_runtime_pm_and_interconnect_bandwidth_scaling_support.patch
