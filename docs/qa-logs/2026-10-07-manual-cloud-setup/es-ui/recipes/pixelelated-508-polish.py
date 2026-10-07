from pathlib import Path
import subprocess
r=Path('/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup')
p=r/'locale/lang/pt_PT/LC_MESSAGES/emulationstation2.po';p.write_bytes(subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(r))],cwd=r))
p=r/'es-app/src/guis/GuiMenu.cpp';s=p.read_text();s=s.replace('\tcloudSetupAddInfoRow(s, window, _U("\\uF058  ") + _("YOUR CLOUD IS ANSWERING:") + " " + cloudSetupDisplayName(remote));','\tif (seedOk)\n\t\tcloudSetupAddInfoRow(s, window, _U("\\uF058  ") + _("YOUR CLOUD IS ANSWERING:") + " " + cloudSetupDisplayName(remote));')
a=s.index('\tif (seedOk)\n\ts->addEntry(_("BACK UP SETTINGS AND SAVES NOW")');b=s.index('\n\ts->getMenu().clearButtons();',a)
block=s[a:b];lines=block.splitlines();s=s[:a]+lines[0]+'\n\t{\n'+'\n'.join('\t'+l for l in lines[1:])+'\n\t}\n'+s[b:];p.write_text(s)
