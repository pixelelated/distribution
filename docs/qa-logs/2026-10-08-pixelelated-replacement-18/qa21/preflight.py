from pathlib import Path
import socket
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:first=p.read_bytes().split(b'\0',1)[0].decode()
 except (OSError,UnicodeError):continue
 assert not Path(first).name.startswith('qemu-system-'),str(p)
for port in [10022,10023,5909,5910,9010,9012,9013]:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
print('PASS no existing guest or provider at suite addresses')
