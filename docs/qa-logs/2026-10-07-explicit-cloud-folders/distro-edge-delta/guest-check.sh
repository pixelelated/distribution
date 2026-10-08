#!/bin/bash
# Bounded #508 delta fixture for the already-owned GENERIC_X64 QA guest.
set -eu
[ "$(sha256sum /usr/bin/cloud_setup | cut -d' ' -f1)" = a7eea3879848ec4879f279f3b7e2a2c08f3531c970ec4dd9858b09290975265c ]
grep -q '^HW_DEVICE="GENERIC_X64"$' /etc/os-release
[ -d /storage/qa-508/upper ]
! pgrep -x emulationstation >/dev/null
O=/storage/qa-508-edge-readback
P=/storage/.config/profile.d/zz-508-edge-readback.sh
[ ! -e "$O" ] && [ ! -e "$P" ]
mkdir -p "$O/bin" "$O/logs" /storage/.config/profile.d
cp -p /storage/.config/cloud_sync.conf "$O/original.conf"
credentials_before=$(sha256sum /storage/.config/rclone/rclone.conf)
cleanup() {
  cp -p "$O/original.conf" /storage/.config/cloud_sync.conf
  rm -f "$P" "$O/original.conf" "$O/rclone.conf"
  rm -rf "$O/cloud" "$O/bin"
}
trap cleanup EXIT
cat > "$O/rclone.conf" <<EOF
[edge]
type = alias
remote = $O/cloud
EOF
cat > "$P" <<EOF
export PATH=$O/bin:\$PATH
export RCLONE_CONFIG=$O/rclone.conf
EOF
cat > "$O/bin/rclone" <<'EOF'
#!/bin/bash
O=/storage/qa-508-edge-readback
printf '%s\n' "$*" >> "$O/logs/argv.log"
mode=none; code=5
[ ! -e "$O/mode" ] || read -r mode code < "$O/mode"
if [ "$1 $2" = 'lsf edge:/Mine/Saves' ]; then
 case "$mode" in
  direct) printf 'direct partial exit%s\n' "$code" >> "$O/logs/fired.log"; printf 'README.txt\n'; exit "$code" ;;
  parent) printf 'direct empty exit5\n' >> "$O/logs/fired.log"; exit 5 ;;
 esac
fi
if [ "$1 $2 $3" = 'lsf --dirs-only edge:/Mine/' ] && [ "$mode" = parent ]; then
 printf 'parent partial exit%s\n' "$code" >> "$O/logs/fired.log"
 printf 'Saves/\n'; exit "$code"
fi
exec /usr/bin/rclone "$@"
EOF
chmod 755 "$O/bin/rclone"
conf() {
 cp /usr/config/cloud_sync.conf /storage/.config/cloud_sync.conf
 sed -i -e "s|^SAVES_REMOTE=.*|SAVES_REMOTE=\"$1\"|" -e 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE="/Mine/Backups"|' -e 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="/Mine/Content"|' /storage/.config/cloud_sync.conf
}
for folder in GAMES Saves /GAMES Mine/Saves; do
 rm -rf "$O/cloud"; mkdir -p "$O/cloud/${folder#/}"
 conf "$folder"
 before=$(sha256sum /storage/.config/cloud_sync.conf)
 tag=$(printf '%s' "$folder" | tr / _)
 /usr/bin/cloud_setup --folder-state > "$O/logs/empty-$tag.log" 2>&1
 grep -qx 'STATE=ready' "$O/logs/empty-$tag.log"
 [ "$before" = "$(sha256sum /storage/.config/cloud_sync.conf)" ]
 printf 'VERIFIED empty %s reports ready; config unchanged\n' "$folder"
done
for mode in direct parent; do
 for code in 3 4 5; do
  rm -rf "$O/cloud"; mkdir -p "$O/cloud/Mine/Saves/gb"
  printf 'preserved progress\n' > "$O/cloud/Mine/Saves/gb/QA.srm"
  initial=$(sha256sum "$O/cloud/Mine/Saves/gb/QA.srm")
  conf /Mine/Saves
  before=$(sha256sum /storage/.config/cloud_sync.conf)
  printf '%s %s\n' "$mode" "$code" > "$O/mode"
  rc=0
  /usr/bin/cloud_setup --seed-folders > "$O/logs/$mode-$code.log" 2>&1 || rc=$?
  [ "$rc" -ne 0 ]
  ! grep -qx 'OK /Mine/Saves' "$O/logs/$mode-$code.log"
  grep -q "^>>> why YOUR CLOUD FOLDERS COULDN'T BE CREATED" "$O/logs/$mode-$code.log"
  [ "$before" = "$(sha256sum /storage/.config/cloud_sync.conf)" ]
  [ "$initial" = "$(sha256sum "$O/cloud/Mine/Saves/gb/QA.srm")" ]
  printf 'VERIFIED %s partial exit%s refuses seed rc=%s; config/payload unchanged\n' "$mode" "$code" "$rc"
 done
done
rm -f "$O/mode"
[ "$credentials_before" = "$(sha256sum /storage/.config/rclone/rclone.conf)" ]
sha256sum /usr/bin/cloud_setup
printf 'VERIFIED original configured provider credentials untouched; synthetic payload cleanup follows\n'
