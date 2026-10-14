#!/usr/bin/env python3
"""UNRUN independent host guard: retire this exact container if its runner disappears."""
import os
from pathlib import Path
import signal
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import identity, read, require, same_process, write
from docker_owner import DockerOwner


def main():
    require(len(sys.argv)==2,'stage directory required')
    stage=Path(sys.argv[1]);meta=read(stage/'container-owner.json');result={'status':'FAIL'}
    forced=[]
    def requested(sig,frame):forced.append(sig)
    signal.signal(signal.SIGTERM,requested)
    signal.signal(signal.SIGINT,requested)
    write(stage/'watchdog-ready.json',{'identity':identity(os.getpid())})
    def retire_clients():
        receipts=list((stage/'host-docker').glob('*.start.json'))
        if (stage/'docker-client.json').exists():receipts.append(stage/'docker-client.json')
        originals=[read(path).get('identity') for path in receipts]
        originals=[item for item in originals if item]
        for sig in (signal.SIGTERM,signal.SIGKILL):
            for item in originals:
                if same_process(item):
                    require(item['pgrp']==item['pid'],'Docker client lost its owned process group')
                    try:os.killpg(item['pid'],sig)
                    except ProcessLookupError:pass
            until=time.monotonic()+5
            while any(same_process(item) for item in originals) and time.monotonic()<until:time.sleep(.1)
        survivors=[item for item in originals if same_process(item)]
        result['host_clients']={'identities':originals,'survivors':survivors}
        return not survivors
    try:
        while True:
            if (stage/'cleanup-complete.json').exists():
                require(read(stage/'cleanup-complete.json')['status']=='PASS','parent cleanup was not proved')
                result['status']='PASS';result['reason']='parent completed exact cleanup';return 0
            reason=None
            if (stage/'cleanup-request.json').exists():reason='parent cleanup incomplete'
            elif forced:reason='watchdog interrupted'
            elif not same_process(meta['host_runner']):reason='host runner exited or identity changed'
            elif time.monotonic()>=meta['deadline_monotonic']:reason='family deadline exhausted'
            if reason:
                result['reason']=reason
                clients_closed=retire_clients()
                result['cleanup']=DockerOwner(stage,stage/'watchdog-docker').cleanup()
                require(clients_closed,'Docker host client survives')
                # Guard intervention remains a failure even if retirement succeeds.
                return 1
            time.sleep(.5)
    except BaseException as exc:result['error']=repr(exc);return 1
    finally:write(stage/'watchdog-result.json',result)


if __name__=='__main__':raise SystemExit(main())
