proxy_listening() {
  local proc="${RAOFFLINEPROXY_PROC_NET:-/proc/net}" f readable=0 sl addr rem st rest
  for f in "${proc}/tcp" "${proc}/tcp6"; do
    [ -r "${f}" ] || continue
    readable=1
    while read -r sl addr rem st rest; do
      [ "${st}" = "0A" ] || continue
      case "${addr}" in
        0100007F:1F90|00000000:1F90|0000000000000000FFFF00000100007F:1F90) return 0 ;;
      esac
    done < "${f}"
  done
  [ "${readable}" -eq 1 ] && return 1
  return 2
}
