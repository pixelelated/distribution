"""Observe installed pacing returns; do not replace product functions."""
import json
import os
import sys
path = os.environ.get('PIXELELATED_QA_THROTTLE_TRACE')
if path:
    assert os.readlink('/proc/self/ns/net') == os.environ['PIXELELATED_QA_NET_NS']
    def observe(frame, event, arg):
        if event != 'return' or frame.f_code.co_name != 'wait':
            return
        if frame.f_globals.get('__name__') != 'raofflineproxy.network':
            return
        obj = frame.f_locals.get('self')
        if type(obj).__name__ != 'RequestThrottle':
            return
        row = dict(pid=os.getpid(), at=obj._last_request_at,
                   action=frame.f_locals.get('action'),
                   filename=frame.f_code.co_filename,
                   namespace=os.readlink('/proc/self/ns/net'))
        with open(path, 'a') as out:
            out.write(json.dumps(row) + '\n')
    sys.setprofile(observe)
