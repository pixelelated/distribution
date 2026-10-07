import sys,importlib.machinery
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
walk('640-en-url-editor','key down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot url-editor')
walk('640-en-url-entered','\n'.join('key '+({':':'shift-semicolon','/':'slash','.':'dot'}.get(c,c)) for c in 'http://127.0.0.1:9867')+'\nkey down\nkey x\nwait 1\nshot filled-form')
walk('640-en-connect-confirm','key up\nwait-for-change\nkey up\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot confirm')
