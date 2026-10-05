from pathlib import Path
import runpy
read_png=runpy.run_path(str(Path(__file__).parent/'frame-diff.py'))['read_png']
def matches(path):
    expected=read_png(str(Path(__file__).parent/'expected-finishing-640x480.png'))
    actual=read_png(str(path))
    return actual[:2]==(640,480) and actual==expected
