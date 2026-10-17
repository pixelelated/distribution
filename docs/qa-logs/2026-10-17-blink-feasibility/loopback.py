#!/usr/bin/env python3
"""Synthetic sign-in fixture. UNRUN. Loopback-only, no account input or provider."""
import argparse
import json
import pathlib
import signal
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

PAGE = r'''<!doctype html><html lang=en><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Renderer fixture</title>
<style>body{font:20px sans-serif;margin:24px;background:#fff;color:#111}input,button,a{font:inherit;margin:8px;padding:8px}#paint{padding:8px;background:#eee}#square{width:64px;height:64px;background:#1963ff;transform:translateX(0)}</style>
<h1>Local sign-in fixture</h1><p>No account or real authorization is used.</p>
<label>Type <b>fixture</b><input id=entry autocomplete=off></label>
<div id=paint>Waiting for input</div><div id=square></div>
<button id=proceed>Continue locally</button><button id=popup>Related window</button>
<a id=denied>Disallowed host control</a><p>Escape closes the probe.</p>
<script>
const entry=document.getElementById('entry'), paint=document.getElementById('paint');
const log=(kind,data)=>fetch('/event',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kind,...data})});
const box=entry.getBoundingClientRect(), hit=document.elementFromPoint(box.x+box.width/2,box.y+box.height/2);
const priorCookie=document.cookie.includes('qa617='),priorStorage=localStorage.getItem('qa617')!==null;
requestAnimationFrame(()=>requestAnimationFrame(()=>log('ready',{
 width:innerWidth,height:innerHeight,dpr:devicePixelRatio,visible:box.width>0&&box.height>0&&hit===entry,
 priorCookie,priorStorage,
 userAgent:navigator.userAgent
})));
document.cookie='qa617=fixture-only; SameSite=Strict';localStorage.setItem('qa617','fixture-only');
entry.addEventListener('input',e=>{const start=performance.now();paint.textContent='Characters: '+entry.value.length;
document.getElementById('square').style.transform='translateX('+entry.value.length*4+'px)';
requestAnimationFrame(()=>requestAnimationFrame(()=>log('input',{trusted:e.isTrusted,length:entry.value.length,twoRafMs:performance.now()-start})));});
document.getElementById('proceed').onclick=()=>{if(entry.value==='fixture')location.href='/continue?value=fixture&state=fixture-only';};
document.getElementById('popup').onclick=()=>window.open('/popup','qa617-popup','width=400,height=300');
document.getElementById('denied').href='http://localhost:'+location.port+'/blocked';
window.addEventListener('message',e=>{if(e.origin===location.origin&&e.data==='fixture-popup')log('popup-message',{sameOrigin:true});});
window.addEventListener('keydown',e=>{if(e.key==='Escape')log('page-escape',{trusted:e.isTrusted});});
</script></html>'''

POPUP = '''<!doctype html><html lang=en><meta charset=utf-8><title>Related fixture</title>
<h1>Related local window</h1><button onclick="window.opener.postMessage('fixture-popup',location.origin);window.close()">Return to fixture</button></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    parser.add_argument('--seconds', type=int, default=120)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535 or not 1 <= args.seconds <= 180:
        parser.error('port must be unprivileged; duration must be 1..180 seconds')
    # No overwriting earlier evidence; HTTP payloads and input values are not logged.
    with args.output.open('x', encoding='utf-8') as output:
        started = time.monotonic()
        records = 0
        def record(kind, **data):
            nonlocal records
            records += 1
            if records > 512:
                raise RuntimeError('event cap reached')
            output.write(json.dumps({'t':time.monotonic()-started,'kind':kind,**data})+'\n')
            output.flush()

        class Handler(BaseHTTPRequestHandler):
            def setup(self):
                super().setup()
                self.connection.settimeout(2)
            def log_message(self, *_):
                pass
            def allowed(self):
                return self.headers.get('Host') == f'127.0.0.1:{args.port}'
            def reply(self, status, data='', location=None):
                self.send_response(status)
                self.send_header('Content-Type','text/html; charset=utf-8')
                self.send_header('Cache-Control','no-store')
                self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; form-action 'self'; object-src 'none'; base-uri 'none'")
                if location:
                    self.send_header('Location',location)
                payload=data.encode()
                self.send_header('Content-Length',str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            def do_GET(self):
                if not self.allowed():
                    record('denied-host-reached-server')
                    return self.reply(403)
                uri=urlsplit(self.path)
                if uri.path == '/' and not uri.query:
                    record('page-request')
                    return self.reply(200,PAGE)
                if uri.path == '/popup' and not uri.query:
                    record('popup-request')
                    return self.reply(200,POPUP)
                if uri.path == '/continue' and parse_qs(uri.query) == {'value':['fixture'],'state':['fixture-only']}:
                    record('synthetic-submit')
                    return self.reply(302,location='/callback?code=fixture-only&state=fixture-only')
                if uri.path == '/callback' and parse_qs(uri.query) == {'code':['fixture-only'],'state':['fixture-only']}:
                    record('synthetic-callback')
                    return self.reply(200,'<!doctype html><meta charset=utf-8><h1>Local callback received</h1><p>Escape closes the probe.</p>')
                return self.reply(404)
            def do_POST(self):
                if not self.allowed() or self.path != '/event':
                    return self.reply(403)
                try:
                    length=int(self.headers.get('Content-Length','0'))
                    if not 1 <= length <= 2048:
                        return self.reply(413)
                    data=json.loads(self.rfile.read(length))
                    kind=data.pop('kind')
                    fields={
                        'ready':{'width','height','dpr','visible','priorCookie','priorStorage','userAgent'},
                        'input':{'trusted','length','twoRafMs'},
                        'popup-message':{'sameOrigin'},
                        'page-escape':{'trusted'},
                    }
                    if kind not in fields or set(data) != fields[kind]:
                        return self.reply(400)
                    if any(not isinstance(v,(str,int,float,bool)) or isinstance(v,str) and len(v)>512 for v in data.values()):
                        return self.reply(400)
                    record(kind,**data)
                except (ValueError,KeyError,TypeError):
                    return self.reply(400)
                return self.reply(204)

        stop=False
        def stopped(*_):
            nonlocal stop
            stop=True
        signal.signal(signal.SIGTERM,stopped)
        signal.signal(signal.SIGINT,stopped)
        with HTTPServer(('127.0.0.1',args.port),Handler) as server:
            server.timeout=0.2
            record('server-ready',port=args.port,seconds=args.seconds)
            print(json.dumps({'ready':True,'port':args.port}),flush=True)
            while not stop and time.monotonic()-started < args.seconds:
                server.handle_request()
            record('server-exit',reason='signal' if stop else 'deadline')


if __name__ == '__main__':
    main()
