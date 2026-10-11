from pathlib import Path
import os
p=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs/tools/raofflineproxy-integration-test')
s=p.read_text()
line='from linux.tests.test_linux_caching_queue import QueueTestCase, CREDENTIALS'
assert s.count(line)==1
s=s.replace(line,line+'\nsetattr(QueueTestCase, "test_upstream_added", lambda self: self.fail("UPSTREAM BASE MUST NOT BE COLLECTED"))')
if os.environ.get('ADD_FORK_TEST') == '1':
    marker="if __name__=='__main__':"
    assert s.count(marker)==1
    s=s.replace(marker,'class NewForkTest(unittest.TestCase):\n    def test_new_fork_method(self):\n        self.assertTrue(True)\n\n'+marker)
__file__=str(p)
exec(compile(s,str(p),'exec'),globals())
