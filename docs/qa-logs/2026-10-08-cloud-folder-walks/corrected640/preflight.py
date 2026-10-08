from pathlib import Path
import socket
mem=dict((x.split(':',1)[0],int(x.split()[1])) for x in Path('/proc/meminfo').read_text().splitlines())
assert mem['MemAvailable']>16*1024*1024,mem['MemAvailable']
for port in (10026,5912,19087):
 with socket.socket() as sock:sock.bind(('127.0.0.1',port))
assert not Path('/tmp/rocknix-qemu-d.pid').exists()
print('PASS separate addresses and >16GiB available before third guest')
