make_target() {
  local RC="$(get_build_dir raofflineproxy-rcheevos)"
  local CHDR="$(get_build_dir raofflineproxy-libchdr)"
  local GLUE="${PKG_BUILD}/third_party/rcheevos_glue"
  local LZMA_SDK="${PKG_BUILD}/third_party/lzma-sdk"
  mkdir -p "${PKG_BUILD}/.${TARGET_NAME}"
  ${CC} ${CFLAGS} ${LDFLAGS} -shared -Os -fPIC \
    -DRC_HASH_NO_ENCRYPTED \
    -DZ7_PPMD_SUPPORT \
    -DWANT_RAW_DATA_SECTOR=1 \
    -DWANT_SUBCODE=1 \
    -DVERIFY_BLOCK_CRC=1 \
    -I"${RC}/include" -I"${RC}/src" -I"${RC}/src/rhash" \
    -I"${GLUE}" -I"${GLUE}/shim" \
    -I"${CHDR}/include" -I"${CHDR}/src" \
    -I"${CHDR}/deps/miniz-3.1.2" -I"${CHDR}/deps/lzma-26.02/include" -I"${CHDR}/deps/zstd-1.5.7" \
    -I"${LZMA_SDK}" \
    -o "${PKG_BUILD}/.${TARGET_NAME}/libraproxy_rchash.so" \
    "${RC}/src/rhash/hash.c" \
    "${RC}/src/rhash/hash_rom.c" \
    "${RC}/src/rhash/hash_disc.c" \
    "${RC}/src/rhash/hash_zip.c" \
    "${RC}/src/rhash/cdreader.c" \
    "${RC}/src/rhash/md5.c" \
    "${RC}/src/rc_compat.c" \
    "${GLUE}/chd_stream.c" \
    "${GLUE}/cdfs_chd.c" \
    "${GLUE}/cdfs_pbp.c" \
    "${GLUE}/strl_compat.c" \
    "${GLUE}/sevenzip.c" \
    "${GLUE}/rchash_glue.c" \
    "${CHDR}/src/libchdr_bitstream.c" \
    "${CHDR}/src/libchdr_cdrom.c" \
    "${CHDR}/src/libchdr_chd.c" \
    "${CHDR}/src/libchdr_codec_avhuff.c" \
    "${CHDR}/src/libchdr_codec_cdfl.c" \
    "${CHDR}/src/libchdr_codec_cdlz.c" \
    "${CHDR}/src/libchdr_codec_cdzl.c" \
    "${CHDR}/src/libchdr_codec_cdzs.c" \
    "${CHDR}/src/libchdr_codec_flac.c" \
    "${CHDR}/src/libchdr_codec_huff.c" \
    "${CHDR}/src/libchdr_codec_lzma.c" \
    "${CHDR}/src/libchdr_codec_zlib.c" \
    "${CHDR}/src/libchdr_codec_zstd.c" \
    "${CHDR}/src/libchdr_flac.c" \
    "${CHDR}/src/libchdr_huffman.c" \
    "${CHDR}/deps/miniz-3.1.2/miniz.c" \
    "${CHDR}/deps/lzma-26.02/src/LzmaDec.c" \
    "${CHDR}/deps/zstd-1.5.7/zstddeclib.c" \
    "${LZMA_SDK}"/*.c
}
