# T33 G-02/G-03 fixture: three zero-byte gb stubs, a custom collection
# holding one of them, and the collection selected -- ES stopped while the
# files are written, then started.
systemctl stop essway
mkdir -p /storage/roms/gb
for n in Alpha Bravo Charlie; do : > /storage/roms/gb/$n.gb; done
printf '%s\n' /storage/roms/gb/Alpha.gb > /storage/.config/emulationstation/collections/custom-t33.cfg
cat > /storage/.config/emulationstation/es_settings.cfg <<'X'
<?xml version="1.0"?>
<config>
	<string name="CollectionSystemsCustom" value="t33" />
</config>
X
ls -la /storage/roms/gb /storage/.config/emulationstation/collections
cat /storage/.config/emulationstation/collections/custom-t33.cfg
systemctl start essway
