#!/bin/sh
# T32 (#679): the window's fixtures, all on the lane's own guest. Ten gb games, ten first letters
# (G-02, G-03); Alpha's manual named in gamelist.xml and absent (G-09); 100 screenshots (L-14's N).
set -e
R=/storage/roms
mkdir -p $R/gb $R/screenshots
for g in Alpha Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliet; do printf 'T32 fixture %s\n' "$g" > "$R/gb/$g.gb"; done
printf '<?xml version="1.0"?>\n<gameList>\n<game><path>./Alpha.gb</path><name>Alpha</name><manual>/storage/roms/gb/manuals/Alpha.pdf</manual></game>\n</gameList>\n' > $R/gb/gamelist.xml
echo 'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAGCAIAAABxZ0isAAAAEUlEQVR4nGMwSJiAFTEMpAQAwXc2AQqC30UAAAAASUVORK5CYII=' | base64 -d > /tmp/t32.png
i=0; for g in Alpha Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliet; do for n in 0 1 2 3 4 5 6 7 8 9; do cp /tmp/t32.png "$R/screenshots/$g-26102${n}-16${i}000.png"; i=$(( (i+1) % 10 )); done; done
echo "gb: $(ls $R/gb | grep -c '\.gb$') games; screenshots: $(ls $R/screenshots | grep -c '\.png$') png"
systemctl restart essway
echo seeded
