set -e
test ! -s /storage/qa575/launch-events
cmp /storage/.config/system/configs/system.cfg /tmp/pix-output/copy1280-settings-before.cfg
printf 'COPY1280 settings byte-identical; no launch event\n'
find /tmp/pix-output -maxdepth 2 -type f -name '*.tar*' -print
