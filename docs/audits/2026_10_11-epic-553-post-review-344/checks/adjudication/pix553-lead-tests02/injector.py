from pathlib import Path
p=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs/tools/raofflineproxy-integration-test')
s=p.read_text()
line='from linux.tests.test_linux_caching_queue import QueueTestCase, CREDENTIALS'
assert s.count(line)==1
s=s.replace(line,line+'\nsetattr(QueueTestCase, "test_upstream_added", lambda self: self.fail("UPSTREAM BASE MUST NOT BE COLLECTED"))')
__file__=str(p)
exec(compile(s,str(p),'exec'),globals())
