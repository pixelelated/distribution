# GPT-6 Astra's 42 items, graded by the first reader

Each item was re-read at its lines in the full file at the pin (and `8ebaf8daad` for the scripts), not only in the packet's excerpts. **Grades:** *accepted*, *in part*, *plausible*, *rejected*. The new items it raised are leads L-31 to L-42 in `02` § Corrections and new leads from the seat.

| Item | Astra | Grade | The first reader's reading |
| --- | --- | --- | --- |
| GM-1 | confirmed | accepted | L-09 as written. |
| GM-2 | confirmed | accepted | L-10 as written. |
| GM-3 | narrowed | accepted | No third wrong store or key. The "eleven unread rows" are not "eleven ineffective settings": AUDIO PROFILE calls its API and WIREGUARD VPN runs its commands directly (`:2743-2749`, `:10308-10316`), and the DMD rows are reached only through a `BATOCERA`-gated opener (`:2979-2981`), which the per-line ROCKNIX column cannot see. L-13 restated: compiled, reachable, persisted, applied directly. |
| GM-4 | narrowed | accepted | L-07: the coverage is every caller; the contract is the hidden-value, untouched-blank case, not a general non-empty-and-changed guard, and it is T21's branch, not the pin. Worded so. |
| GM-5 | narrowed | accepted | **L-08 corrected:** the empty-`root.password`-versus-device split exists at the pin -- the row is `password=false` and the pin's editor writes an empty string unguarded (`:3265`; `GuiSettings.cpp:218-237`); S1 is not its onset. |
| GM-6 | confirmed | accepted | L-11: two conditional writes at one page's (SOUND SETTINGS) construction; the guest's mtime change is the page's normal save (`GuiSettings.cpp:82-95`), not evidence of either branch. |
| GM-7 | narrowed | accepted | L-12: the four relink sub-pages, not six; the provider form and ADD CONNECTION use `addInputTextRow` into their own maps (`:7260-7262`, `:7361-7365`, `:7900-7919`). And `03`'s "every settings page's close writes both stores" is wrong: a page with no save function writes nothing (`GuiSettings.cpp:88-89`). |
| GM-8 | confirmed | accepted | L-14 stands. |
| GM-9 | narrowed | accepted | L-15: `reboot` is set too, so the notice shows; what is absent is the `ExitOnRebootRequired` quit (`:976-982`, `:3281-3290`). |
| GM-10 | narrowed | accepted | L-04 restated: the count is caller-side process sites by the tool's method, not 116 indefinite blocks. The tool's bound column is wrong for `cloudFolderContext()` (its own `timeout 5`, `:6916-6919`) and too broad for `cloudScanContent` and `cloudOpenTransfer` (the scan itself is a transfer page; only the stamp checks are bounded). **New, accepted:** each `cloud_oauth cancel` sleeps one second (`cloud_oauth:2816`) on the interface thread -- at every sign-in start (`:7515`) and twice on the waiting dialog's cancel (`:7835` then the page's `onFinalize`, `:6476`). `cloud_remote list` reads configuration and does not visibly run rclone (`cloud_remote:244-254`). |
| GM-11 | confirmed | accepted | L-01: "until the cache is reset" (USE FILESYSTEM CACHE resets it, `:1455`; so does a restart), not "until restart". |
| GM-12 | narrowed | accepted | L-02: the route is reachable on an image or session without the window and through the legacy `url` fallback (`:7599-7603` leaves `onDevice` false); the texture key includes `shareId`, so the old code's rendering is unproved until the sharing default is read. Stays a conditional lead. |
| GM-13 | narrowed | accepted | L-03: `:4589` is not a gate; both scan files are read whatever the stamp said. The consequences differ by file: the selection's is COULDN'T SAVE WHAT YOU TICKED; a poisoned scan file reads as nothing matches; a poisoned settings-facts file as no settings archive. |
| GM-14 | narrowed | accepted | L-30: `wg0.conf` (`:10303`) is a mutable file read cached (L-34). |
| GM-15 | narrowed | accepted | L-16: reliance on the default position, not a shown clipping. |
| GM-16 | narrowed | accepted | L-17: the cycles keep the switch and its closure, not the page or its list; the `!wifienabled` local-play branch is hard to reach (LOCAL PLAY MODE shows only with Wi-Fi on; turning Wi-Fi off rebuilds behind a loader). `04` § Q1 now says "plausible-safe at the levels read", as `02` does. |
| GM-17 | confirmed | accepted | L-18: the fix uses the pin's label, CLOUD CONNECTIONS. |
| GM-18 | confirmed | accepted | L-19. |
| GM-19 | confirmed | accepted | L-20 is an extraction gap: the runtime `_()` would translate a catalog entry nobody can generate. |
| GM-20 | narrowed | accepted | L-21: the case finding; the URL is for a computer and is not itself a rule break. |
| GM-21 | confirmed | accepted | L-22 is two sites; and back on the completed settings restore's OK reboots (`:383-384`, `:419-421`), which is that dialog's only button and the restore the player asked for -- recorded, not a defect. |
| GM-22 | narrowed | accepted | L-23: the map's heading was read by the first reader (`docs/es-menu-map.md:405`); outside the seat's packet. |
| GM-23 | narrowed | accepted | L-24: `addWithLabel` upper-cases its label (the comment at `:10443-10445`), so `ZeroTier One` and `Emulator` render upper-case; the ejection dialog's method is `BATOCERA`-only (`GuiMenu.h:94-96`). L-24 keeps only the fuel gauge's French and the three `Reboot now` / `later` dialogs. |
| GM-24 | narrowed | accepted | L-25: a blank HOSTNAME is writable at the pin; S1 is not its onset. AUTO stays a proposal. |
| GM-25 | confirmed | accepted | L-27; the nine credential sites are not a whole-file quoting audit: the timezone, the LED colour and the USB gadget choice are unquoted (`:1868`, `:2167`, `:10244`); the LED colour is L-35. |
| GM-26 | narrowed | accepted | L-05: `:7422`'s search can match a CR that survives; a lost byte loses the diagnosis, it does not fail open; and `CloudConnectionsPage`'s snapshot comparison reads through the same reader (`:5579`, `:5589`). |
| GM-27 | confirmed | accepted | L-06, citing both producers (`cloud_remote:257-266`, `:320-335`). |
| GM-28 | confirmed | accepted | L-26, and LOCAL PLAY MODE discards its result too (`:10172`). |
| GM-29 | narrowed | accepted | L-28: "integration hotspots", not "certain to conflict". |
| GM-30 | narrowed | accepted | The positive is narrowed: the gated row re-checks only when built unconfigured (`:6290-6294`); and a page is not always one function (`openRestoreRelink` builds five sub-pages). |
| GM-31 | new | accepted | **L-31, High.** Read at the lines: the picker's row closes the setup page `s` (`:8234`) and then calls `cloudSetupShowSshStep`, which returns early without presenting when `cloudSetupInfo()` reports no IP (`:6662-6667`); the picker stays, every row still holding the deleted `s`, and a second press calls `s->close()` on freed memory (`GuiSettings.cpp:73-80`). Reached when the network drops between opening CLOUD STORAGE SETUP (which checked for an IP, `:8165`) and the press. |
| GM-32 | new | accepted | **L-32, Medium**, folded with L-08: SSH PASSWORD and DEVICE PASSWORD skip `setrootpass` on an empty entry but `GuiSettings::save()` saves `SystemConf` anyway (`GuiSettings.cpp:82-95`), so `root.password=` is persisted while the device keeps its password. |
| GM-33 | new | accepted | **L-33, Low**, folded with L-17: the hub's two switches, the provider form's boolean switches (with the values map, which can hold an entered secret) and the network service switches capture themselves (`:5651`, `:5658`, `:7301`, `:10182`, `:10201`, `:10220`): leaks on every visit. |
| GM-34 | new | accepted | **L-34, Low**, folded with L-03: `exists(wg0.conf)` is cached (`:10303`). |
| GM-35 | new | accepted | **L-35, Low**: a stored `led.color` (kept as an option when the list lacks it, `:2160-2161`) reaches `sh -lc "..."` unquoted (`:2167`); ROCKNIX-built behind `DEVICE_LED_CONTROL`. The writer of `led.color` is this row and `set_setting`; no outside party is shown. |
| GM-36 | new | accepted | **L-36, Low**, folded with L-20: `providerLabel()` returns the table's label without gettext (`CloudText.cpp:39-46`) into CONNECTED TO and the connections pages (`:5679-5682`, `:8012`, `:8078`), and the form's choice and subprovider labels are the script's text (`:7323-7328`, `:7452-7455`). |
| GM-37 | new | accepted | **L-37, Low**, folded with L-19: `runMaintenanceCommand` upper-cases the script's why into the dialog with no `CloudText::localizedWhy` (`:360-389`). |
| GM-38 | new | plausible | **L-38, Low**: `atoi("")` is 0, so an empty answer reads YOUR CLOUD IS ANSWERING (`:8445-8453`); reaching it needs the shell to die before its own `echo $?`, or `popen` to fail (L-39). A fault path, kept. |
| GM-39 | new | accepted | **L-39, Low**, folded with L-05: `GetShOutput` does not test `popen`'s result (`Platform.cpp:893-897`). `es-core`'s, upstream's: a #585 line. |
| GM-40 | new | accepted | **L-40, Low**: the relink WI-FI PASSWORD page's `onFinalize` reconnects whenever Wi-Fi, SSID and key are set, changed or not (`:8307-8318`): opening it and pressing back starts an association. |
| GM-41 | new | in part | **L-41, Low**: FINISH ignores `std::remove`'s result (`:8491`). The failure keeps the marker, so the page returns at the next start (the safe direction, `02`'s reading); what is missing is a word that it did. |
| GM-42 | new | accepted | **L-42, Low (latent)**: with `cloud_scan` absent the fallback opens `cloudOpenTransferOptions`, whose first act is `cloudScanStamped("done")`, false with no run id (`:5253-5256`, `:4838-4841`, `:4183-4186`): the older-scripts route ends at THE CLOUD CHECK IS NO LONGER CURRENT. Every image ships `cloud_scan`. |

**Totals** (counted from the table by `awk` over the Grade column): 42 items; accepted 40, in part 1, plausible 1.
