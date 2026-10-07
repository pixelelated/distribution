from pathlib import Path
import hashlib, json, os, subprocess

owner = Path(__file__).resolve().parent
args = json.loads((owner / 'command.json').read_text())
build = Path(args[-1]).parents[2] / '.x86_64-linux-gnu'
env = dict(os.environ, CCACHE_DISABLE='1')
(owner / 'artifacts/compiler.txt').write_text(subprocess.check_output(['/usr/bin/g++', '--version'], text=True))
source = (owner / 'original.cpp').read_text()
old = 'return std::vector<uint32_t>(inst->words().begin() + 2, inst->words().end());'
assert source.count(old) == 1
alternate = source.replace(old, '''std::vector<uint32_t> members;
  for (size_t i = 2; i < inst->words().size(); ++i) {
    members.push_back(inst->words()[i]);
  }
  return members;''')
(owner / 'loop.cpp').write_text(alternate)
results = []
for name, src, extra, expected in [
    ('original', 'original.cpp', [], 1),
    ('warning-only', 'original.cpp', ['-Wno-error=free-nonheap-object'], 0),
    ('unoptimized', 'original.cpp', ['-O0'], 0),
    ('equivalent-loop', 'loop.cpp', [], 0),
]:
    command = list(args)
    command[-1] = str(owner / src)
    command[command.index('-o') + 1] = str(owner / 'artifacts' / (name + '.o'))
    command[command.index('-MF') + 1] = str(owner / 'artifacts' / (name + '.d'))
    command[1:1] = extra
    # Last optimization flag wins; keep the original command except this control.
    if name == 'unoptimized':
        command = ['-O0' if x == '-O2' else x for x in command]
    with (owner / 'artifacts' / (name + '.log')).open('x') as log:
        result = subprocess.run(command, cwd=build, env=env, stdout=log, stderr=subprocess.STDOUT)
    data = (owner / 'artifacts' / (name + '.log')).read_text()
    assert result.returncode == expected, (name, result.returncode)
    if name == 'original': assert '-Werror=free-nonheap-object' in data
    if name == 'warning-only': assert '-Wfree-nonheap-object' in data
    results.append({'name': name, 'returncode': result.returncode, 'command': command})
    print('PASS expected compiler control ' + name, flush=True)
(owner / 'unused.cpp').write_text('int main() { int unused; return 0; }\n')
command = ['/usr/bin/g++', '-O2', '-Wall', '-Werror', '-Wno-error=free-nonheap-object', '-c', str(owner / 'unused.cpp'), '-o', str(owner / 'artifacts/unused.o')]
result = subprocess.run(command, capture_output=True, text=True)
(owner / 'artifacts/unrelated-warning.log').write_text(result.stdout + result.stderr)
assert result.returncode != 0 and '-Werror=unused-variable' in result.stderr
results.append({'name': 'unrelated-warning-stays-error', 'returncode': result.returncode, 'command': command})
(owner / 'artifacts/result.json').write_text(json.dumps({'result': 'PASS', 'controls': results}, indent=2) + '\n')
print('PASS all isolated compiler controls; no build-source mutation', flush=True)
