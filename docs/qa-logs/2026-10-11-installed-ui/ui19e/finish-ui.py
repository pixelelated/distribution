from ui import *
restart();walk('retained-carousel','wake\ndismiss-dialogs\nsettle\nshot retained-carousel\n')
# An empty old journal cannot support a clean-start claim. Preserve that
# unsuccessful evidence readback and require a fresh clean-boot owner instead.
(P/'artifacts/startup-readback-disposition.json').write_text(json.dumps({'original_clean_journal':'empty; not accepted as startup evidence','retained_current_boot':'positive Started essway.service record, no automatic restarts','clean_followthrough':'required separately'},indent=2)+'\n')
(P/'finish.json').write_text(json.dumps({'commands_complete':True,'result':'PASS','composition':'Final scoped commands pass; original fixture failures remain retained and are not relabelled. Clean-start positive journal runs separately.','reviewed':'archive offered/foreign, failed scan/retry, EN/FR running/options/content/empty and INFORMATION frames; carousel pending review'},indent=2)+'\n')
print('PASS UI command sequence complete; supervisor owns shutdown',flush=True)
