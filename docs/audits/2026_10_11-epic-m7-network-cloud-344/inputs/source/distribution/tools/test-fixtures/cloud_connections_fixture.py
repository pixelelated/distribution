"""External-rclone adapter for the historical OAuth race fixtures.

The production transaction, locks, state guards and atomic writes run unchanged.
Only the fixture rclone's successful config-create side effect is simulated.
Real-rclone transactions are covered separately by cloud-connections-test.
"""
import configparser
import io
from pathlib import Path
import sys
import subprocess

def configure(module, directory):
    c = module.connections
    root = Path(directory)
    c.CONFIG = root / 'rclone.conf'
    c.ACTIVE = root / 'active-connection'
    c.LOCK = root / 'cloud.lock'
    c.SYSTEM = root / 'system.cfg'
    def run(args):
        stage = Path(args[1])
        command = args[2:]
        if module.subprocess is subprocess and module.RCLONE == '/usr/bin/rclone':
            raise RuntimeError('OAuth fixture needs its fake provider')
        answer = module.subprocess.run([module.RCLONE] + command, capture_output=True, text=True)
        if answer.returncode:
            raise c.Refused('The connection could not be verified. Your settings were not changed.')
        if command[:2] == ['config', 'create']:
            parser = configparser.RawConfigParser()
            parser.read(stage)
            parser.add_section(command[2])
            parser.set(command[2], 'type', command[3])
            with stage.open('w') as stream: parser.write(stream)
        return answer.stdout
    c.run = run
    if hasattr(module, 'main'):
        original = module.main
        def main(argv):
            try: return original(argv)
            except c.Refused as error:
                sys.stderr.write(str(error) + '\n')
                return 2
        module.main = main
