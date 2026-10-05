from pathlib import Path

owner = Path(__file__).resolve().parent
for name in ('pair', 'artifacts'):
    path = owner / name
    if path.is_symlink():
        raise SystemExit('Refusing symlinked owned directory: ' + name)
    path.mkdir(mode=0o700, exist_ok=True)
    if not path.is_dir() or path.stat().st_mode & 0o077:
        raise SystemExit('Owned directory must be private: ' + name)
print('PASS owned private pair/artifacts directories ready')
