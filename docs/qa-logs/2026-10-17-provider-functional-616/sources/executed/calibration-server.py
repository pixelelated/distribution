#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""UNRUN fixture: allocated guest loopback only; bounded request-UA hash echo."""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import signal
import socket
import time
from urllib.parse import urlsplit


def main(args):
    output = args.output
    output.mkdir(mode=0o700)
    page = (Path(__file__).resolve().parent / 'calibration.html').read_bytes()
    events = []
    stop = False
    started = time.monotonic()

    class Handler(BaseHTTPRequestHandler):
        timeout = 2

        def log_message(self, *_args):
            pass

        def do_GET(self):
            path = urlsplit(self.path).path
            routes = {'/fixture': 'original', '/start': 'original', '/page': 'final',
                      '/status503': 'error503', '/drop': 'dropped'}
            route = routes.get(path, 'unknown')
            ua = self.headers.get('User-Agent', '')
            safe = bool(ua) and len(ua) <= 512 and all(32 <= ord(char) <= 126 for char in ua)
            event = {'sequence': len(events) + 1, 'route': route,
                     'elapsed_ms': (time.monotonic() - started) * 1000,
                     'ua_sha256': hashlib.sha256(ua.encode()).hexdigest() if safe else 'unknown'}
            if len(events) >= 64:
                self.send_error(429)
                return
            events.append(event)
            (output / 'requests.json').write_text(json.dumps(events, indent=2) + '\n')
            if route == 'dropped':
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                return
            body = page if route == 'final' else b'Synthetic HTTP error' if route == 'error503' else b''
            status = 302 if route == 'original' else 200 if route == 'final' else 503 if route == 'error503' else 404
            self.send_response(status)
            if route == 'original':
                self.send_header('Location', '/page')
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

    def finish(_number, _frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGTERM, finish)
    signal.signal(signal.SIGINT, finish)
    server = HTTPServer(('127.0.0.1', 18761), Handler)
    server.timeout = .25
    (output / 'ready.json').write_text(json.dumps({'pid': __import__('os').getpid(),
        'port': 18761, 'page_sha256': hashlib.sha256(page).hexdigest(), 'max_seconds': 240}) + '\n')
    try:
        while not stop and len(events) < 64 and time.monotonic() - started < 240:
            server.handle_request()
    finally:
        server.server_close()
        (output / 'result.json').write_text(json.dumps({'seconds': time.monotonic() - started,
            'requests': len(events), 'stop_requested': stop, 'no_provider_requests': True}) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
