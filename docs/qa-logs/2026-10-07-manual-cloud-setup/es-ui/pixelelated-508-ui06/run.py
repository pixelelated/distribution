import sys
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote("printf 'blocking synthetic folder creation\\n' > /storage/qa-manual-ui/provider/pixelelated")
walk('640-en-url-editor-repeat','key x\nwait-for-change\nkey down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot url-editor')
walk('640-en-url-filled-repeat','\n'.join('key '+({':':'shift-semicolon','/':'slash','.':'dot'}.get(c,c)) for c in 'http://127.0.0.1:9867')+'\nkey down\nkey x\nwait 1\nshot filled-form')
walk('640-en-real-confirm','key down x5\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot confirm\nkey x\nwait-for-change 30 0\nwait 5\nsettle\nshot seed-failure')
log=remote("grep -E 'cloud_remote create:|cloud_setup wizard: folders=' /var/log/es_log.txt");(A/'640-en-real-form.log').write_text(log);assert 'folders=incomplete' in log,log
