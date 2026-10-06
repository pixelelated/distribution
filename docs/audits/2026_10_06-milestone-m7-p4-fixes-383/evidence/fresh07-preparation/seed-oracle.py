import re
NOTE_SHA = {
 'SAVES': '81283a71c8db19f49232b395e3527170b14ae38add60d5180071196f24c283bf',
 'BACKUPS': 'a2e91a3dddf28269cbf704b1b7e2540608e9851a88f09679701e0c6629fd7f5c',
 'CONTENT': 'cb0db1a29003ebedb5a5f92d17c49e7eadebedcc10e883e9d9af052fd4a57456',
 'CONTENT/ROMs': 'cdbf34d6dc27ad558261bd99b99bbc91850ba28a1150ef2488b18dbe87637bcd',
 'CONTENT/BIOS': '12345b222d272bcccee06cac35e9b0d4ac10a76617a32b72cefa8542a90d1f67',
}
def expected_notes(pointers):
    values={}
    for line in pointers.splitlines():
        match=re.fullmatch(r'(SAVES|SETTINGS|CONTENT)_REMOTE="([/A-Za-z0-9_-]*)"',line)
        if not match or match[1] in values: raise ValueError('unexpected fixture pointer syntax')
        values[match[1]]=match[2]
    if set(values)!={'SAVES','SETTINGS','CONTENT'}: raise ValueError('incomplete fixture pointers')
    roots={'SAVES':values['SAVES'],'BACKUPS':values['SETTINGS'],
           'CONTENT/ROMs':values['CONTENT']+'/ROMs','CONTENT/BIOS':values['CONTENT']+'/BIOS'}
    if values['CONTENT']: roots['CONTENT']=values['CONTENT']
    if any(not root.startswith('/') for root in roots.values()): raise ValueError('nonabsolute fixture root')
    return {root.lstrip('/')+'/README.txt':NOTE_SHA[key] for key,root in roots.items()}
def valid_seed(before,after,notes):
    allowed=dict(notes, **{'pixelelated/.layout':'be68d69fa1fe3ddbcaa9295b8e3e732fd0113d909e38cf643d95aab41c9b1a22'})
    return (all(after.get(p)==h for p,h in before.items())
            and all(after.get(p)==h for p,h in notes.items())
            and all(p in before or allowed.get(p)==h for p,h in after.items()))
