import ctypes,gettext,json,re,subprocess
from pathlib import Path
O=Path('/tmp/pixelelated-m7-migration-copy01')
ES=Path('/home/max/Development/emulationstation-next.worktrees/m7-migration-copy')
FONT=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/build/es-theme-art-book-next-9a50ef366e750aabfab29e6915a2867607212971/_inc/fonts/Roboto-Bold.ttf')
s=ES.joinpath('es-app/src/guis/GuiMenu.cpp').read_text()
encoded=re.search(r'_\("(YOUR CLOUD HAS A \\u2018%s.*?PREVIOUS OS.*?CONFIRM\.)"\)',s).group(1)
en=json.loads('"'+encoded+'"')
fr=gettext.GNUTranslations(open(O/'artifacts/fr.mo','rb')).gettext(en)
assert fr!=en
F=lambda n:ctypes.c_float(n).value
results=[]
for w,h in [(640,480),(1280,800)]:
 px=int(F(int(F(min(w,h)*F(.03333333)))*F(1.31 if min(w,h)<720 else 1)))
 raw=subprocess.check_output([str(O/'font-metrics'),str(FONT),str(px)],text=True)
 metrics={int(cp):(float(advance),int(height)) for cp,advance,height in (line.split() for line in raw.splitlines())}
 lineheight=max(y for cp,(x,y) in metrics.items() if cp<128)*1.5
 buttonheight=lineheight+h*.0296296+2
 for lang,msg in [('en',en),('fr',fr)]:
  msg=msg%('/ROCKNIX','/pixelelated')
  assert all(ord(c) in metrics for c in msg if not c.isspace()),'missing glyph'
  width=.8*w-.03*w
  rest=msg;out=''
  # Reproduce Font::wrapText cut points using FT_LOAD_RENDER advances.
  while rest:
   cursor=0;linew=0;lastspace=0;lastcursor=0
   while linew<width and cursor<len(rest):
    lastcursor=cursor;char=rest[cursor];cursor+=1
    linew=0 if char in '\n\r' else linew+metrics.get(ord(char),(0,0))[0]
    if char in ' \n\t\v\f\r':lastspace=cursor
   if cursor==len(rest):out+=rest;rest=''
   else:
    cut=lastspace or lastcursor
    assert cut>0
    out+=rest[:cut]+'\n';rest=rest[cut:]
  lines=out.count('\n')+1
  total=lines*lineheight*1.225+buttonheight
  results.append(dict(surface=[w,h],language=lang,font_px=px,wrap_width=width,lines=lines,line_height=lineheight,dialog_height=total,screen_height=h,full_screen_scrolling=total>h,wrapped_text=out))
print(json.dumps({'kind':'source geometry preflight, not rendered proof','font':str(FONT),'results':results},indent=2,ensure_ascii=False))
