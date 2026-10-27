# T33 G-04: two gamelist.xml files written from outside ES while it runs
# (the cloud game-content restore's shape, D-CLOUD-049, without the cloud).
# gb: an entry for Bravo; gb then gets a dirty file (Alpha's favourite) in the UI.
# gbc: a control system with no dirty file.
cat > /storage/roms/gb/gamelist.xml <<'X'
<?xml version="1.0"?>
<gameList>
	<game>
		<path>./Bravo.gb</path>
		<name>Bravo</name>
		<desc>T33 written from outside ES while it ran</desc>
	</game>
</gameList>
X
mkdir -p /storage/roms/gbc
: > /storage/roms/gbc/Delta.gbc
cp /storage/roms/gb/gamelist.xml /storage/roms/gbc/gamelist.xml
sed -i 's#./Bravo.gb#./Delta.gbc#; s#<name>Bravo#<name>Delta#' /storage/roms/gbc/gamelist.xml
md5sum /storage/roms/gb/gamelist.xml /storage/roms/gbc/gamelist.xml
date -u +%T
