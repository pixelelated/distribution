"""Execute only the installed module against temporary synthetic OS fixtures."""
from pathlib import Path
import json,tempfile
from raofflineproxy import config
assert str(Path(config.__file__).resolve()).startswith('/usr/lib/')
assert config.running_on_rocknix(), 'actual pixelelated OS must be recognized'
rows=[]
original_release=config.OS_RELEASE_PATH;original_settings=config.DEFAULT_ROCKNIX_SYSTEM_CFG
try:
 with tempfile.TemporaryDirectory(prefix='qa-proxy-identity-') as temporary:
  root=Path(temporary);release=root/'os-release';settings=root/'system.cfg';settings.touch()
  config.OS_RELEASE_PATH=release;config.DEFAULT_ROCKNIX_SYSTEM_CFG=settings
  for record,expected in [('OS_NAME="ROCKNIX"',True),('OS_NAME="pixelelated"',True),('OS_NAME="RASTERATOPS"',False),('# OS_NAME="ROCKNIX"',False),('PREVIOUS_OS_NAME="ROCKNIX"',False)]:
   release.write_text(record+'\n');actual=config.running_on_rocknix();assert actual==expected,(record,actual)
   if expected:assert config.detect_rocknix_system_cfg()==str(settings)
   rows.append({'record':record,'recognized':actual})
finally:
 config.OS_RELEASE_PATH=original_release;config.DEFAULT_ROCKNIX_SYSTEM_CFG=original_settings
print(json.dumps({'passed':True,'installed_module':config.__file__,'actual_os_recognized':True,'cases':rows}))
