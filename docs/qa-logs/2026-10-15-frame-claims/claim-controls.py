#!/usr/bin/env python3
"""UNRUN #591 host-only controls. Synthetic PNGs; no VM, network, baseline acceptance.

Run with --source CANDIDATE --out NEW_DIRECTORY. The independent old-source
control uses --only adjacent --expect-old-failure with the frozen original.
Every original subprocess report/exit stays in its own named case directory.
"""
import argparse
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import zlib

SCREEN = 'walk/frame.png'


def png(width=16, height=16, pixels=()):
    rows = [bytearray(width * 3) for _ in range(height)]
    for x, y in pixels:
        rows[y][3*x:3*x+3] = b'\xff\x20\x10'
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind+data) & 0xffffffff)
    raw = b''.join(b'\0'+bytes(row) for row in rows)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def claim(rect, issue='591', build='base', screen=SCREEN):
    return f'{build} {screen} ' + ' '.join(map(str, rect)) + f' #{issue}\n'


def cases():
    left = claim((2,2,3,3))
    right = claim((3,2,4,3), issue='578')
    whole = claim((0,0,16,16))
    pair = [(2,2),(3,2)]
    return [
        dict(name='adjacent', pixels=pair, claims=left+right, rc=0,
             require=['**PASS**', 'claimed by 591', 'claimed by 578'], claimed_pixels=2),
        dict(name='uncovered-connecting-pixel', pixels=[(2,2),(3,2),(4,2)],
             claims=left+claim((4,2,5,3), issue='578'), rc=1,
             require=['**FAIL**', 'x 3..3, y 2..2 | 1 px | **UNCLAIMED**'], claimed_pixels=2),
        dict(name='bounding-rectangle-gap', pixels=[(2,2),(3,3),(4,4)],
             claims=left+claim((4,4,5,5)), rc=1,
             require=['x 3..3, y 3..3 | 1 px | **UNCLAIMED**'], claimed_pixels=2),
        dict(name='overlap-counted-once', pixels=pair,
             claims=claim((2,2,4,3))+claim((3,2,5,3), issue='578'), rc=0,
             require=['**PASS**'], claimed_pixels=2),
        dict(name='half-open-edge', pixels=[(3,2)], claims=left, rc=1,
             require=['x 3..3, y 2..2 | 1 px | **UNCLAIMED**']),
        dict(name='stale-build-cannot-claim', pixels=pair,
             claims=claim((0,0,16,16),build='other'), rc=1,
             require=['0 live, 1 stale', 'stale claim, line 1', '**FAIL**']),
        dict(name='mixed-live-and-stale', pixels=pair,
             claims=left+claim((3,2,4,3),build='other'), rc=1,
             require=['1 live, 1 stale', 'x 3..3, y 2..2 | 1 px | **UNCLAIMED**']),
        dict(name='wrong-screen-cannot-claim', pixels=pair,
             claims=claim((0,0,16,16),screen='other/*.png'), rc=1, require=['**FAIL**']),
        dict(name='wildcard-build-unchanged', pixels=pair,
             claims=claim((0,0,16,16),build='*'), rc=0, require=['**PASS**']),
        dict(name='new-needs-single-whole-claim', pixels=pair, new=True,
             claims=claim((0,0,8,16))+claim((8,0,16,16)), rc=1,
             require=['NEW screen | 16x16 | **UNCLAIMED**']),
        dict(name='new-whole-claim-unchanged', pixels=pair, new=True,
             claims=whole, rc=0, require=['NEW screen | 16x16 | claimed by']),
        dict(name='missing-cannot-claim', missing=True, claims=whole, rc=1,
             require=['MISSING from the run', '1 screen(s) missing']),
        dict(name='size-mismatch-cannot-claim-or-mask', pixels=pair, size=(17,16),
             claims=claim((0,0,100,100)), masks=f'{SCREEN} 0 0 100 100\n', rc=1,
             require=['the frame size differs | 17x16 | **UNCLAIMED**']),
        dict(name='mask-removes-only-owned-gap', pixels=[(2,2),(3,2),(4,2)],
             claims=left+claim((4,2,5,3)), masks=f'{SCREEN} 3 2 4 3\n', rc=0,
             require=['**PASS**'], claimed_pixels=2),
        dict(name='mask-half-open-edge', pixels=[(3,2)],
             masks=f'{SCREEN} 2 2 3 3\n', rc=1, require=['**UNCLAIMED**']),
        dict(name='masked-only-identical-message', pixels=[(3,2)],
             masks=f'{SCREEN} 3 2 4 3\n', rc=0,
             require=['Every walked screen is pixel-identical to the baseline outside the masks.']),
        dict(name='foreground-label-still-checked', pixels=[(1,1),(8,8)],
             claims=claim((0,0,16,2))+claim((0,2,2,16)), rc=1,
             require=['x 8..8, y 8..8 | 1 px | **UNCLAIMED**']),
        dict(name='no-baseline-stays-exit2', pixels=pair, no_baseline=True,
             claims=whole, rc=2, require=['no baseline']),
        dict(name='unchanged', pixels=[], claims=left+right, rc=0,
             require=['Every walked screen is pixel-identical']),
        dict(name='explicit-pixel-threshold', pixels=[(2,2)], args=['--min-pixels','2'],
             rc=0, require=['**PASS**']),
    ]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--only', choices=[case['name'] for case in cases()])
    parser.add_argument('--expect-old-failure', action='store_true')
    args=parser.parse_args()
    if args.expect_old_failure and args.only != 'adjacent':
        parser.error('--expect-old-failure requires --only adjacent')
    source=args.source.resolve(strict=True)
    args.out.mkdir(parents=True, exist_ok=False)
    results=[]
    for case in cases():
        if args.only and args.only!=case['name']:
            continue
        dest=args.out/case['name']
        base, run=dest/'baseline',dest/'run'
        (base/'walk').mkdir(parents=True)
        (run/'walk').mkdir(parents=True)
        if not case.get('no_baseline'):
            (base/'BASELINE.txt').write_text('build base\n')
        if not case.get('new'):
            (base/SCREEN).write_bytes(png())
        if not case.get('missing'):
            width,height=case.get('size',(16,16))
            (run/SCREEN).write_bytes(png(width,height,case.get('pixels',())))
        claims=dest/'claims.txt';claims.write_text(case.get('claims',''))
        masks=dest/'masks.txt';masks.write_text(case.get('masks',''))
        command=[sys.executable,str(source),'compare',str(base),str(run),
                 '--claims',str(claims),'--masks',str(masks)]+case.get('args',[])
        result=subprocess.run(command, capture_output=True, text=True, timeout=20)
        (dest/'stdout.txt').write_text(result.stdout)
        (dest/'stderr.txt').write_text(result.stderr)
        (dest/'command.json').write_text(json.dumps(command,indent=2)+'\n')
        (dest/'exit.txt').write_text(str(result.returncode)+'\n')
        if args.expect_old_failure:
            expected,required=1,['**FAIL**','**UNCLAIMED**']
        else:
            expected,required=case['rc'],case.get('require',[])
        errors=[]
        if result.returncode != expected: errors.append(f'exit {result.returncode}, expected {expected}')
        for text in required:
            if text not in result.stdout:errors.append('missing expected report text: '+text)
        if not args.expect_old_failure and 'claimed_pixels' in case:
            total=sum(int(n) for n in re.findall(r'\| (\d+) px \| claimed by ',result.stdout))
            if total!=case['claimed_pixels']:errors.append(f'claimed {total} pixels, expected {case["claimed_pixels"]}')
        results.append({'name':case['name'],'subprocess_exit':result.returncode,'expected_exit':expected,
                        'passed':not errors,'errors':errors})
        print(('PASS ' if not errors else 'FAIL ')+case['name'])
    (args.out/'result.json').write_text(json.dumps({'source':str(source),'results':results},indent=2)+'\n')
    return 0 if all(result['passed'] for result in results) else 1


if __name__=='__main__':
    sys.exit(main())
