taskset -c 8-23 python3 -B - <<'PY'
import hashlib, subprocess
D='a0d4c4fda7a0c16c04d57edf921ffeb741eff19b'
S='8710a6210a40de0110244d03a886161ee06faf29'
A='docs/audits/2026_11_03-epic-m6-records/'
def git(*args):
    return subprocess.check_output(['git', *args])
assert git('rev-parse', D+'^{commit}').decode().strip() == D
assert git('show', '-s', '--format=%P', D).decode().strip() == S
paths=[p for p in git('ls-tree','-r','--name-only','-z',D,'--',A).split(b'\0') if p]
assert len(paths) == 311
for path, digest in [
    ('docs/audits/README.md','17269ce0820878e809890a9f737cd665c77d32ff07a20e779aed4fac1b745d79'),
    ('.claude/rules/instruction-files.md','ca638c32b6bbf991c02a865b9c3ab19279416806e7baa0a320713989610da845')]:
    assert hashlib.sha256(git('show',D+':'+path)).hexdigest() == digest
print('PASS T46 stream binding: D a0d4c4fda7a0 / 311 audit files / 1 owned documentation path')
PY
