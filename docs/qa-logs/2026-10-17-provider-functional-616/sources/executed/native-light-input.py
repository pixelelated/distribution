#!/usr/bin/env python3
"""UNRUN. One bounded native broker input action on the local calibration page only."""
import argparse
import ipaddress
import json
import os
from pathlib import Path
import socket
import urllib.parse
import urllib.request

ROOT = Path('/storage/qa616-provider')
STATE = Path('/var/run/cloud_oauth')

def main(action):
    if os.geteuid() != 0 or os.uname().machine != 'x86_64':
        raise ValueError('disposable x86_64 guest only')
    case = json.loads(Path('/run/qa616-provider/current.json').read_text())
    state = json.loads((STATE / 'session.json').read_text())
    binding = json.loads((ROOT / 'binding.json').read_text())
    page = urllib.parse.urlsplit((STATE / 'page').read_text().strip())
    if (case['provider'] != 'light' or state.get('backend') != 'dropbox'
            or state.get('status') != 'waiting' or (STATE / 'signed-in').exists()
            or page.scheme != 'http' or page.hostname != '127.0.0.1'
            or page.port != binding['calibration_port'] or page.path != '/page'):
        raise ValueError('not the waiting local calibration page')
    if action == 'type-q' and not (STATE / 'field').exists():
        raise ValueError('native field marker absent; inspect focus first')
    address = urllib.parse.urlsplit(state['address'])
    if address.scheme != 'http' or address.port != 8080 or address.username or address.password:
        raise ValueError('unexpected installed broker address')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        probe.connect(('192.0.2.1', 9))  # Route lookup only; sends no packet.
        local = probe.getsockname()[0]
    if address.hostname != local or not ipaddress.ip_address(local).is_private:
        raise ValueError('broker must be on this isolated guest address')
    # This helper never types on a provider page. Enter is allowed solely to
    # activate the reviewed local negative-control button, never a login form.
    fields = {'pin': state['pin']}
    if action == 'type-q':
        fields['type'] = 'q'
    else:
        fields['key'] = {'backspace': 'backspace', 'tab': 'tab',
                         'activate-negative': 'enter', 'escape': 'escape'}[action]
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(state['address'] + '/',
        data=urllib.parse.urlencode(fields).encode(), method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with opener.open(request, timeout=3) as response:
        if response.status != 204 or response.read(1):
            raise ValueError('unexpected broker response')
    print(json.dumps({'action': action, 'broker_http_status': 204,
                      'dom_delivery_proven_by_this_command': False}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['type-q', 'backspace', 'tab', 'activate-negative', 'escape'])
    args = parser.parse_args()
    try:
        main(args.action)
    except Exception as error:
        # Never export a URL, PIN, session, response body or exception detail.
        print(json.dumps({'status': 'REFUSED', 'error_class': type(error).__name__}))
        raise SystemExit(1)
