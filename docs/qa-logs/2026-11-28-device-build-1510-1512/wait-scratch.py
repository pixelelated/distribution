import importlib.machinery, importlib.util, subprocess, sys, time
sys.dont_write_bytecode = True
loader = importlib.machinery.SourceFileLoader('device_build', sys.argv[1])
spec = importlib.util.spec_from_loader(loader.name, loader)
m = importlib.util.module_from_spec(spec); loader.exec_module(m)
root = sys.argv[2]
def stamp(): return time.strftime('%H:%M:%S', time.gmtime())
print(stamp(), 'no holder:', m.wait_free(root, 20))
p = subprocess.Popen(['sleep', '10'], cwd=root + '/.ccache')
t0 = time.monotonic(); u = m.wait_free(root, 30)
print(stamp(), f'holder that exits after 10 s: users after {time.monotonic()-t0:.0f} s = {u}  -> proceeds' if not u else f'REFUSED {u}')
p.wait()
q = subprocess.Popen(['sleep', '300'], cwd=root + '/.ccache')
t0 = time.monotonic(); u = m.wait_free(root, 20)
print(stamp(), f'holder that stays: users after {time.monotonic()-t0:.0f} s:')
for x in u: print('   ', x)
print('   -> refused' if u else '   -> PROCEEDED (wrong)')
q.kill(); q.wait()
