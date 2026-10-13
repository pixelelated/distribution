import importlib.machinery,importlib.util
from pathlib import Path
src=Path('/workspace/repos/rocknix.worktrees/m7-player-setup/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
loader=importlib.machinery.SourceFileLoader('vmprofile',str(src)); spec=importlib.util.spec_from_loader(loader.name,loader); mod=importlib.util.module_from_spec(spec); loader.exec_module(mod)
original=mod.load_profile
mod.load_profile=lambda: dict(original(),memory_mib=2048)
mod.main()
