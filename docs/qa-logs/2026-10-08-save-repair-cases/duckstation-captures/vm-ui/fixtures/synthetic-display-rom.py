#!/usr/bin/env python3
"""Original synthetic MIPS reset ROM: display an orange rectangle, then loop.

No commercial BIOS/game bytes. This is a screenshot rendering fixture, not a
replacement BIOS or a game-compatibility test. Output is exactly 512 KiB.

Pinned DuckStation v0.1-10998 references:
  src/core/bios.cpp:182-216,379-391 accepts size and warns on unknown identity;
  src/duckstation-qt/qthost.cpp:3436-3441 supports -bios;
  src/core/gpu_types.h:93-104 gives GP1 command numbers;
  src/core/gpu.cpp:221-222 supplies ordinary display timing;
  src/core/gpu_commands.cpp:1042-1072 decodes the three-word VRAM fill.
"""
import hashlib
from pathlib import Path
import struct
import sys

words = [0x3C081F80, 0x35081810]  # lui t0,0x1f80; ori t0,t0,0x1810


def write_gpu(value, gp1=False):
    # lui t1,hi; ori t1,t1,lo; sw t1,offset(t0).
    words.extend([0x3C090000 | (value >> 16), 0x35290000 | (value & 0xFFFF),
                  0xAD090004 if gp1 else 0xAD090000])


write_gpu(0x00000000, True)  # reset GPU
write_gpu(0x08000001, True)  # NTSC 320x240, 15-bit, non-interlaced
write_gpu(0x05000000, True)  # display starts at VRAM 0,0
write_gpu(0x06C60260, True)  # default horizontal range
write_gpu(0x0703FC10, True)  # default vertical range
write_gpu(0x020030E0)        # fill rectangle; RGB 224,48,0
write_gpu(0x00000000)        # VRAM x=0,y=0
write_gpu(0x00F00140)        # width320,height240
write_gpu(0x03000000, True)  # enable display
words.extend([0x1000FFFF, 0x00000000])  # beq zero,zero,self; nop delay slot

payload = b''.join(struct.pack('<I', word) for word in words).ljust(512 * 1024, b'\0')
destination = Path(sys.argv[1])
with destination.open('xb') as stream:
    stream.write(payload)
print(hashlib.sha256(payload).hexdigest(), len(payload), destination)
