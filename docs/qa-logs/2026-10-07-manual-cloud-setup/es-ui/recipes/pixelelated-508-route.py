from pathlib import Path
r=Path('/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup')
p=r/'es-app/tests/unit/CloudTextTests.cpp';s=p.read_text().replace('// The four stream A sentences the interface had no entry for.','// The retained transfer sentences are localized.').replace('"THE NEW FOLDER ALREADY HAS FILES IN IT", "YOU WENT OFFLINE PART-WAY THROUGH"','"YOU WENT OFFLINE PART-WAY THROUGH"');p.write_text(s)
p=r/'es-app/src/guis/GuiMenu.cpp';s=p.read_text();old='''\t\t\t\t\t\t\twindow->pushGui(new GuiMsgBox(window,
\t\t\t\t\t\t\t\t_("YOUR CLOUD IS ANSWERING.\\n\\nYOU CAN NOW SYNC, BACK UP, AND RESTORE YOUR SAVES FROM GAME SETTINGS."),
\t\t\t\t\t\t\t\t_("OK"), [s] { s->close(); }));''';new='''\t\t\t\t\t\t\tconst size_t start = out.find("OK=") + 3;
\t\t\t\t\t\t\tconst std::string remote = Utils::String::trim(out.substr(start, out.find_first_of("\\r\\n", start) - start));
\t\t\t\t\t\t\tcloudSetupShowDoneStep(window, remote, s);''';assert old in s;s=s.replace(old,new)
a=s.index('\t// One button, and it leaves.',s.index('static void cloudOAuthShowConnected(Window* window, const CloudBackend& backend,\n\tGuiSettings* prev)\n{'));b=s.index('\n\tcloudSetupPresent(window, s, prev);',a)
s=s[:a]+'''\t// Continue to folder setup using the same selected paths as normal transfers.
\ts->getMenu().clearButtons();
\ts->getMenu().addButton(_("CONTINUE"), _("continue"), [window, s, backend]
\t{
\t\tcloudSetupShowDoneStep(window, backend.name, s);
\t});
'''+s[b:];p.write_text(s)
