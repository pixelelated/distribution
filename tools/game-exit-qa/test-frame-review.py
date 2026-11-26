#!/usr/bin/env python3
"""Offline review of original and deliberately changed 640x480 QA frames."""
import hashlib
from pathlib import Path
import struct
import tempfile
import zlib

import visible_quit as q


FIXTURES = Path(__file__).with_name('fixtures')


def picture(pixels):
    def chunk(kind, data):
        return (struct.pack('>I',len(data))+kind+data+
                struct.pack('>I',zlib.crc32(kind+data)))
    return (q.PNG+chunk(b'IHDR',struct.pack('>IIBBBBB',640,480,8,2,0,0,0))+
            chunk(b'IDAT',zlib.compress(pixels))+chunk(b'IEND',b''))


def compare(a,b,phase,view):
    return q.compare_frames(a,b,hashlib.sha256(a.read_bytes()).hexdigest(),phase,view)[1]


def main():
    with tempfile.TemporaryDirectory(prefix='game-exit-frame-test-') as tmp:
        change = Path(tmp)/'change.png'
        for n,phase,view in (('01','confirmation','quit-confirmation'),
                             ('02','quit','quit-highlighted'),
                             ('03','confirmation','quit-confirmation')):
            a,b = (FIXTURES/f'backup-{n}-{leg}.png' for leg in ('preview','confirmed'))
            before,after = (q.resume_raster(p.read_bytes()) for p in (a,b))
            assert q.patch_bytes(before,q.CLOCK) != q.patch_bytes(after,q.CLOCK)
            result = compare(a,b,phase,view)
            assert result=='ozone-'+view+'-outline-clock-masked', (n,result)
            print('PASS',n,view,result)
            for x,y in ((25,200),(576,5),(626,11),(577,12),(320,240)):
                changed = after.copy()
                changed[q.row_span(x,x+1,y).start] ^= 128
                change.write_bytes(picture(changed))
                assert compare(a,change,phase,view)==q.NEEDS_REVIEW, (n,x,y)
            print('PASS',n,'five changes outside the masks request a second review')

        # The fixed clock region applies even without a menu outline.
        old = q.resume_raster(a.read_bytes())
        old[q.row_span(577,578,5).start] ^= 128
        change.write_bytes(picture(old))
        assert compare(a,change,'game','game')=='clock-masked'
        assert q.RECHECK_REVIEW == 20 and q.RECHECK_AGE == 32
        print('PASS clock-only without an outline; review 20 s, capture age 32 s')


if __name__=='__main__':
    main()
