from pathlib import Path
import json,hashlib,difflib,shutil
r=Path(__file__).parent;prior=Path('/workspace/tmp/pix570-ua-20261013')
s=(prior/'original.c').read_text();i=(prior/'instrument.c').read_text();i=i.replace('    g_free(ua);','''    g_free(ua);
    gchar *width=NULL;
    if(g_file_get_contents("/storage/qa570ua/width.txt",&width,NULL,NULL)) {
        double w=g_ascii_strtod(width,NULL);
        if(w>=320 && w<=1024) webkit_web_view_set_zoom_level(view,640.0/w);
    }
    g_free(width);''')
i=i.replace('width:innerWidth,height:innerHeight,ready:',"width:innerWidth,height:innerHeight,dpr:devicePixelRatio,screenWidth:screen.width,screenHeight:screen.height,small:matchMedia('(max-width: 480px)').matches,tablet:matchMedia('(min-width: 768px)').matches,ready:")
(r/'instrument.c').write_text(i);(r/'original.c').write_text(s)
x=s.replace('static const char *allowed_host = NULL;',i+'\nstatic const char *allowed_host = NULL;').replace('webkit_web_view_load_uri(view, argv[1]);','qa_setup(view);\n    webkit_web_view_load_uri(view, argv[1]);')
(r/'diagnostic.c').write_text(x);(r/'diagnostic.patch').write_text(''.join(difflib.unified_diff(s.splitlines(True),x.splitlines(True),fromfile='original.c',tofile='diagnostic.c')))
(r/'source.json').write_text(json.dumps({'source':'bc9dfe8141d9561dc1d8502313d00a84c4566ee8','original_sha256':hashlib.sha256(s.encode()).hexdigest(),'diagnostic_sha256':hashlib.sha256(x.encode()).hexdigest()},indent=2)+'\n')
for n in ['compile.sh','ui.py','ssh-command.json']:shutil.copy2(prior/n,r/n)
