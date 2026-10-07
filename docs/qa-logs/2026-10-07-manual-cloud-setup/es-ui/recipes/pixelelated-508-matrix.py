import sys,json,time
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
res=sys.argv[1] if len(sys.argv)>1 else '640x480'
# This owner only restages the exact compiled payload; source scripts are frozen.
remote('systemctl stop essway')
# The previous bind mount still owns its old inode; replace with fresh filenames.
scp('/tmp/pixelelated-508-es-host07/emulationstation','/storage/qa-manual-ui/es-final');scp('/tmp/pixelelated-508-es-host07/artifacts/fr.mo','/storage/qa-manual-ui/fr-final.mo')
remote('chmod 755 /storage/qa-manual-ui/es-final; sync; mount --bind /storage/qa-manual-ui/es-final /usr/bin/emulationstation; mount --bind /storage/qa-manual-ui/fr-final.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo')
for lang in ['en_US','fr_FR']:
 tag=res+'-'+lang
 remote("systemctl stop essway; : > /storage/.config/rclone/rclone.conf; rm -rf /storage/qa-manual-ui/provider/pixelelated; printf 'synthetic refusal fixture\\n' > /storage/qa-manual-ui/provider/pixelelated; sync")
 start(lang)
 walk(tag+'-hub',(R/'tools/vm-walks/to-manage-cloud-storage.steps').read_text())
 walk(tag+'-form','key up\nwait-for-change\nkey up\nwait-for-change\nkey x\nwait-for-change\nkey down x8\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot form\nkey down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot address')
 walk(tag+'-filled','\n'.join('key '+({':':'shift-semicolon','/':'slash','.':'dot'}.get(c,c)) for c in 'http://127.0.0.1:9867')+'\nkey down\nkey x\nwait 1\nshot filled-form')
 walk(tag+'-failure','key down x5\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot confirm\nkey x\nwait-for-change 30 0\nwait 5\nsettle\nshot failure')
 log=remote("grep -E 'cloud_remote create:|cloud_setup wizard: folders=' /var/log/es_log.txt");assert 'OK=webdav' in log and 'folders=incomplete' in log,log
 remote('rm /storage/qa-manual-ui/provider/pixelelated')
 walk(tag+'-retry','key down\nwait-for-change\nkey x\nwait-for-change 30 0\nwait 3\nsettle\nshot ready\nkey down\nwait-for-change\nsettle\nshot manual-guidance')
 proof=remote("grep -E 'cloud_remote create:|cloud_setup wizard: folders=' /var/log/es_log.txt; sha256sum /usr/bin/emulationstation /usr/bin/cloud_setup /usr/bin/cloud_scan /usr/bin/cloud_backup /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; test ! -e /usr/bin/cloud_migrate_layout && echo MIGRATION_ABSENT; pgrep emulationstation | while read p; do tr '\\000' '\\n' < /proc/$p/environ | grep -E '^(LANG|LC_ALL|LANGUAGE|LOCPATH)='; done; find /storage/qa-manual-ui/provider -type f -exec sha256sum {} \\;")
 assert 'folders=ready' in proof and sha('/tmp/pixelelated-508-es-host07/emulationstation') in proof and '67c6f9be8b2c30ad903139ee34be3ccfb64dcf7b462e1abbf0c0ec648d3860b6' in proof
 (A/(tag+'-proof.log')).write_text(proof)
 # Finish is a real page close. No reboot or migration step should follow it.
 walk(tag+'-finish','key down\nwait-for-change\nkey down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot finished')
 print('PASS actual provider create/folder refusal/retry/finish',tag,flush=True)
Path('/tmp/pixelelated-508-ui-matrix-'+res+'.json').write_text(json.dumps({'capture':'PASS','res':res,'languages':['en_US','fr_FR'],'visual_review':'PENDING'})+'\n')
