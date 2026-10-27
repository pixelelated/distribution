# Stage B reading notes (T26, #673) -- the first reader's, at the pin, as read

Line numbers are `GuiMenu.cpp` at `16dbac5211` unless a file is named. Each
note is what the lines say; a lead is graded in `02` and at stage C.

## The file cache (es-core/src/utils/FileSystemUtil.cpp at the pin)

- `queryCacheEntry` (`:200-216`): with `UseFileCache` on, a lookup that
  misses stats once (`statKey`) and inserts the answer -- a miss included --
  and the entry stands until `resetCache` (`:258`, called at `:345`).
- `fromStat64` (`:138-166`, the Linux arm) writes `mFileCache[hash]` on every
  call, with no `UseFileCache` test: an uncached `exists(p, false)` (`:1122-1146`)
  therefore also refreshes the cached answer for `p`.
- `isRegularFile` (`:1164-1179`) has no flag: the cache first, then a stat.

## The content picker and its helpers (:4086-4609)

- `:4133-4150` `cloudSelectionRead` reads through `isRegularFile` (cached);
  the comment at `:4154-4156` says the scan files are read "uncached". A
  first read that misses (a scan file absent, a selection file whose rename
  failed) is remembered for the session: every later read of that path
  returns false while the file is there. `cloudSaveSelection` (`:4205-4220`)
  then reports COULDN'T SAVE WHAT YOU TICKED on every press until a restart.
  Exposure: the scan reads follow `--stamp-valid` (`:4589`); the selection
  read follows `--set-systems`, which writes the file -- so the miss needs a
  write that failed first. Narrow, as the brief says.
- `:4188` `cloudScanStamped` runs `timeout 5 ... --stamp-valid` on the
  interface thread: one of the two bounded starts.
- `:4207` `--set-systems` (`executeScriptLegacy`), no bound, interface
  thread, at three call sites (`:4464`, `:4518` from BACK's save hook,
  `:4569`); the save hook at `:4515-4519` runs it on every BACK.
- `:4300-4585` the page: build from `CloudScanResult`; rc 69 -> COULDN'T
  REACH (`:4306-4310`); other nonzero -> COULDN'T READ (`:4311-4315`). With
  `cloud_scan` present `rc` is 0 or -1 from the stamp (`:4589`), so a
  failed stamp reads COULDN'T READ YOUR CLOUD'S CONTENT, never NOT ONLINE.
- `:4529-4584` the posted rebuild, weakly held (`weak` at `:4530`, posted at
  `:4536`), the page owning `buttons` through `onFinalize` (`:4584`): sound,
  as the digest says.
- `:4419`, `:4426` carry `·` (U+00B7) in string literals, not comments.

## The LAST rows, the transfer options, the scans, the match (:4610-5420)

- `:4645` the stamp read is uncached; `:4655` parses through `CloudText`.
- `:4838` `cloudOpenTransferOptions` opens only after `cloudScanStamped("done")`
  (bounded 5 s); else THE CLOUD CHECK IS NO LONGER CURRENT (`:4194-4195`).
- `:4919-4926` the ticks are written by an `addSaveFunc` through the alias
  `conf` (`:4921`), which also flushes `SystemConf` on BACK.
- `:4956-5158` `run`: copies `window` before `s->close()` (`:4967`, `:5156-5157`).
- `:5006` the composer keeps the last nonzero part, a 9 included: T18's
  PL-21 composers' half (latent). `:5125` `backuptool backup >/dev/null`:
  T18's PL-17. `:5378` DOWNLOADED and `:5616` BRING DATA BACK: PL-17.
- `:5050-5099` the settings-restore YES runs from a `GuiMsgBox`, whose
  `deleteMeAndCall` copies the function before deleting the box
  (`GuiMsgBox.cpp:286-294`): every dialog callback here runs on its own copy,
  so `s->close()` inside one (`:5074`, `:5081`) cannot free the running lambda.
  A positive for Q1.
- `:5075` spells `cloudSelectionNotSaved(false)`'s sentence again (the brief's).
- `:5142` the item count reads the selection through the cached reader.
- `:5202-5206` `onFinalize` drops the two switches' callbacks, breaking the
  cycle `rebuildButtons` made (#308 F-ES-11): a positive.
- `:5233`, `:5263` the scan pages continue only when the run id is current
  and the stamp is valid.
- `:5288-5296` the match preview runs on a `GuiLoading` worker: a positive.
- `:5313-5326` **lead (Q5):** the match's refusal is the script's own
  English sentences, upper-cased (`said`), as the dialog's text: a player
  in French reads English, and nothing maps them through the `>>> why`
  table or `CloudText::localizedWhy`. Read against `es-player-text.md`
  § "Every fork string ships in English and French" (script-supplied text).

## The hub (:5420-5746)

- `:5505-5528` `CloudHubRefresher`: an invisible `EXTRACHILDREN` component,
  ticked once a second by the page's update -- reads `CloudTransferJob::current()`
  and the fonts; no process.
- `:5574-5600` `CloudConnectionsPage`: `cloud_remote list` in the
  constructor (`:5579`) and again on every return to the top (`:5589`,
  posted, guarded by `mAlive` and `peekGui() == this`, then `mRefresh();
  close();` -- the posted lambda is the window's, not the page's: sound).
- `:5602-5745` `openCloud`: `exists(rclone.conf, false)` (`:5604`);
  `cloudSetupInfo()` (`:5678`, `cloud_setup --info`: rclone listremotes, a
  route lookup and systemctl); so opening CLOUD starts at least two
  processes on the interface thread, unbounded (the constructor's list and
  `--info`), and a return to it one more.
- `:5651-5661` the two sync toggles write and `saveSystemConf()` at once.
- `:5688-5709` CHECK CONNECTION runs `cloud_setup --check` on a worker
  (bounded by the script, the comment says: 10 s to connect, 30 s to answer).
- `:5717` CHANGE CLOUD FOLDER: `onDone` rebuilds the hub then closes `s`
  (`cloud-folder-reopen.py` covers `cloudOpenFolderSettings`' transition).
- `:5730` the restore marker uncached; `:5739-5741` the FINISH RESTORE
  PROCESS row (built again at `:10269-10271`).

## GAME SETTINGS' cloud rows and the wizard (:6100-7090)

- `:6124-6158` the three save rows on `ThreadedCloudSync` cards; `:6140` the
  manual sync exits on the restore's code, a 9 included (T18's PL-21, `:6140`).
- `:6245-6261` `cloudSetupInfo()` is `timeout 10 /usr/bin/cloud_setup --info`:
  **bounded** -- the hub's `--info` (`:5678`) and every wizard step's
  (`:6662`, `:6719`, `:6796`, `:6857`) wait at most 10 s, on the interface
  thread. (`t26-pages.py`'s bound column looked at the call site only; it is
  corrected to read a helper's own bound.)
- `:6288-6327` `cloudAddGatedEntry`: the press re-reads `rclone.conf`
  uncached (`:6315`) and undims the row (audit #307 PL-062): a positive.
- `:6466-6478` `cloudOAuthOwnSession`: the page that is left (not handed on)
  runs `cloud_oauth cancel` through `runSystemCommand` at `onFinalize`: the
  interface thread, no bound.
- `:6484-6504` `cloudSetupPresent`: sizes 0.75 and does not position
  (`:6496`), positions the 0.90 page only (`:6497-6499`); its own comment
  (`:6493-6495`) states the rule the 0.75 branch does not keep. The 0.75 page
  fits because GuiSettings' 15% top offset plus 0.75 is 0.90 (#540's shape).
- `:6523-6542` SSH PASSWORD: the current device password shown as a fact
  (`:6526`), by the wizard's design (it is typed into a computer's ssh
  prompt; `:6732-6735` says so); the change row is guarded -- non-empty and
  changed (`:6533`) -- and quoted (`:6537`, #198).
- `:6564` the folder change runs `timeout 30` on a worker.
- `:6627-6630` the comment calls `--check` "the only slow call in the
  wizard" and the only one behind `GuiLoading`; on the interface thread
  besides: `--info` per step (10 s bound), `--connected` (`:6749`, no
  bound), `systemctl enable/start sshd` and two more (`:6695-6698`, no
  bound), `--free-auth-port` (`:6846`, no bound).
- `:6639` `--check` reads through `GetShOutput` (bytes dropped, newlines
  joined) and parses `RC=` with `rfind`: the code survives; the name is the
  text after the first space.
- `:6883-7057` the folder pages (D-CLOUD-175/178/179): CHECK FOLDERS reads
  only (`--validate-folders`, `timeout 35`, on a worker, `:6976-6986`);
  CREATE FOLDERS asks YES/NO first (`:7036-7045`); `stillSelected`
  (`:7012-7019`) refuses a press on paths that changed meanwhile;
  `cloudFolderContext()` (`timeout 5`) runs on the interface thread at build
  (`:6993`) and at each press (`:7014`). **No join, follow or move**: the
  pin's 27 hits for join/follow/migrat are the keyboard layout, Wi-Fi and
  the screen layout (`grep -n -i -E 'join|follow|migrat'`).
- `:7058-7070` the done step: `cloud_remote active` (`:7060`, no bound);
  CONNECTION SAVED for a remote not made active.
- Side notes, to read at their lines later: `:1842` (the keyboard layout to
  `system()` inside double quotes) and `:1519` (MANUAL UPDATES, naming the
  fork's URL).

## The readers this file's commands go through (es-core/src/utils/Platform.cpp at the pin)

- `GetShOutput` (`:891-905`): `fgets` into 256 bytes, then
  `result += file.substr(0, file.size() - 1)` -- every read loses its last
  byte. A read that ended at `\n` loses the newline (lines are joined with
  no separator); a line longer than 254 bytes is read in pieces and loses
  one real byte per 255; a last line with no newline loses its last
  character. `popen`'s result is not checked (`fgets(NULL)`).
- `GetShOutputLines` (`:907-935`): accumulates, splits on `\n`, keeps a last
  line without one -- correct; `cloudRemoteLines` (`:7125-7137`) uses it, and
  its comment says why.
- `runSystemCommand` (`:853-880`): forks, the child forks and waits for the
  grandchild, the parent waits for the child: synchronous for the whole
  command, and `return 0` whatever happened -- the status is never read.

## The provider form (:7090-7480)

- `:7139-7156` `cloudConnectionError` matches `cloud_remote`'s sentences by
  substring in `GetShOutput`'s joined text.
- `:7183-7194` `cloudShellQuote`: `'` -> `'\''`, wrapped in single quotes.
- `:7285` masks a field the backend calls a password **or** sensitive.
- `:7301-7304`, `:7351-7355` the form's switches and lists write the values
  map at once, not through `addSaveFunc` (`:7336-7348` says why: the vendor
  was once dropped with a success dialog).
- `:7404-7433` CONNECT runs `timeout 100 /usr/bin/cloud_remote create|update
  ... 2>&1` on a worker through `GetShOutput`, masks the log (`:7414`),
  and on `OK=` takes the name to `find_first_of("\r\n")` (`:7422`) -- which
  never finds one, since the reader removed every newline: dead, and
  harmless because `OK=<name>` is the last stdout line (the brief's,
  `cloud_remote:265`, `:322`). A matched error sentence is at risk only on a
  line longer than 254 bytes (a fixture decides how often a real rclone
  error line is that long).
- `:7397`/`:7435` CONNECT / NO (verb first, NO last): back lands on NO.

## The OAuth sign-in (:7480-7925)

- `:7515` `cloud_oauth cancel` through `runSystemCommand` (interface thread,
  no bound) before every start; `:7525-7531` the serve detached with
  `setsid ... &` (the `runSystemCommand` returns when `sh` has backgrounded it).
- `:7539-7604` the wait for a waiting session runs on a `GuiLoading` worker
  (`:7624-7635`), 60 polls of 500 ms, fails closed (`:7596-7597`).
- `:7684` `launchCloudSignIn` blocks while the window is up (by design,
  `:7864-7866`).
- `:7692`, `:7708`, `:7813`, `:7848` `cloud_oauth status` through
  `GetShOutputLines` on the interface thread, no bound; `:7835` `cancel` too.
- `:7702-7717`, `:7824-7827` TRY AGAIN / CANCEL SIGN-IN: no button named NO
  or OK, so back lands on CANCEL SIGN-IN (`GuiMsgBox.cpp:116-133`), which
  closes the page and cancels the session through `onFinalize` (`:6468-6478`)
  -- the brief's style call for the pause.
- `:7767-7771` `rm -f` then `qrencode` through `runSystemCommand` (its status
  never read), then `:7792` `exists(qrPath)` **cached**: the session's first
  answer stands. A first attempt with no QR (qrencode failing, `/tmp` not
  writable) leaves every later attempt text-only; a first with one makes
  `exists` say yes over a later failure (the image then draws nothing beside
  the text). The brief's Q4 lead, confirmed at its lines.
- **New lead (Q4, a read that can be stale):** the QR image is asked for by
  path through `TextureResource::get` (`ImageComponent.cpp:408`), which
  returns any **live** texture with the same key (`TextureResource.cpp:100-131`).
  A sign-in page built while the previous one is still alive draws the
  previous session's code. The route: `cloudOAuthPresentChoice` with
  `ready.started` and not `ready.onDevice` builds the new sign-in page with
  `prev` the old one (`:7644-7646`), pushed before `prev` is closed
  (`cloudSetupPresent`, `:6501-6503`) -- reached from TRY AGAIN (`:7826`,
  `:7715`). With `ON_DEVICE=yes` every retry goes through the choice page,
  which closes the old page first, so the texture has expired. `ON_DEVICE` is
  `yes` only when the sign-in window exists and a graphical session is found
  (`cloud_oauth:882-885`, `:2804` at `8ebaf8daad`). Proof: tree; the guest
  reads `cloud_oauth info`'s ON_DEVICE on the M6 image.
- `:7856-7858` CONTINUE copies `finishSignIn` before calling it ("completion
  can delete s"): a positive.
- `:7861-7870` the page is presented before the blocking window opens;
  statements follow `cloudSetupPresent` here on purpose (`:7864-7868`:
  `backend` and `remoteName` are the function's own copies).
- `:7888-7922` ADD CONNECTION reads `cloud_remote list` (interface thread).

## The connections pages and CLOUD STORAGE SETUP (:7925-8243)

- `:7930`, `:8027`, `:8091` `cloudRemoteBackends()` -> `cloud_remote providers`
  (rclone config providers) on the interface thread, no bound; CLOUD
  CONNECTIONS (`:8063-8085`) starts `cloud_remote list` twice at build (the
  class's constructor, `:5579`, and `:8066`).
- `:7992-8006` select/remove on a worker (`timeout 60`) through
  `GetShOutput`, success read as `startsWith(result, "OK=")` (`:7998`), where
  CONNECT reads `find("OK=")` (`:7419`). `cloud_remote` prints `OK=<name>`
  and nothing else on success (`:320-323` at `8ebaf8daad`), so it holds today;
  two parsers of one answer is the fragility (recorded, not a defect).
- `:8020-8058` USE CONNECTION / CANCEL, SIGN IN / CANCEL, REMOVE CONNECTION /
  CANCEL: back lands on CANCEL (safe); `cloudConnectionManual` (`:7983-7990`)
  refuses while either automatic sync is on.
- `:8083` and `:8155` USE A COMPUTER INSTEAD twice (D-UI-005's row, from two pages).
- `:8162-8242` CLOUD STORAGE SETUP: `cloudSetupInfo()` (10 s bound); the
  picker (`:8226-8239`) closes the chooser from the picker's row, as its
  comment says (safe).

## FINISH RESTORE PROCESS (:8244-8497)

- `:8292-8335` WI-FI PASSWORD: the key row (`:8297`) writes memory only; the
  sub-page's `onFinalize` saves the file (`:8309`), closes the parent and
  rebuilds it, and the association runs behind `networkApplyWifi`'s spinner.
- `:8297`, `:8353`, `:8356`, `:8371`, `:8374`, `:8392` the brief's
  unguarded credential rows **at the pin**: an untouched editor under
  `system.security.enabled=1` opens blank (`GuiSettings.cpp:245-248`) and OK
  writes the empty value, which the sub-page's `onFinalize` saves. **T21's
  S1 changes `buildInputTextConfigRow` itself** (`ba0e82c1f` on
  `feature/m6-es-state-and-bridge-668` at `3ae9610b0`: `TextRowEdit::writes
  (openedBlank, newVal)` -- a popup opened blank over a hidden value and OK'd
  with nothing typed changes nothing, #1185): every caller of the row,
  these six included. This file needs no change; the proof is the pin's
  move (T21's unit, and the guest walk on an image that carries it).
- `:8354-8357` `#ifndef CHEEVOS_DEV_LOGIN` drops the WEB API KEY row on a
  build with a compiled pair (the brief's; D-WORKFLOW-166's builds set the
  ScreenScraper pair, not this one -- read against the build's flags).
- `:8413-8423` DEVICE PASSWORD: guarded (non-empty and changed) and quoted.
- `:8445` `--check >/dev/null 2>&1; echo $?` on a worker: `GetShOutput`
  returns the code without its newline -- correct.
- **New lead (Q5, a word or a dialog; upgrade-and-install's "does any string
  still name the old path?"):** `:8460` tells a player whose cloud does not
  answer to "USE CONNECT OR REPAIR CLOUD STORAGE IN GAME SETTINGS > MANAGE
  CLOUD STORAGE." No row has that name at the pin: `c8dc72cf9` (2026-10-11)
  renamed it CLOUD CONNECTIONS (its `:70`/`:74`) and updated the hub's
  sentence (`:5706`), and missed this one. The French catalog keeps the
  old msgids (`.po:5547`, `:5556`, `:5976`). Proof: history and tree.
- `:8465` BLUETOOTH CONTROLLERS MUST BE PAIRED AGAIN is an `addEntry` with
  no function: a fact built as a selectable action row.
- `:8484-8494` LATER / FINISH; FINISH's `std::remove` result unchecked (a
  failure keeps the marker, so the page returns: fail-safe).

## NETWORK SETTINGS (:9744-10300)

- `:9769-9804`, `:9830-9847` three detached threads post through the gated
  `AppWindow::post` with weakly held rows: sound; `queryInterfaceAddresses`
  has no bound (`:9776`).
- `:9909-9912` NETWORK NAME from `system.hostname`; `:9929` the HOSTNAME row.
  After T21's S1 an empty hostname is stored empty and means the device's
  own name; the row then shows a blank value where `es-ui-style-guide.md`
  § Text gives `AUTO` for "system decides" (a word for Q5, read against
  T21's ruling).
- The Wi-Fi verdict is composed three ways: the page's close says WI-FI
  ENABLED on success (`:10084-10090`), the relink page says nothing on
  success (`:8320-8332`), the ENABLE WI-FI switch says nothing either way and
  rebuilds (`:10124-10129`).
- `:10149-10153` (Wi-Fi off) `delete s` runs inside `enable_adhoc`'s own
  change callback. The closure survives: it captures `enable_adhoc` (and
  `enable_wifi`, `optionsAdhocID`), a cycle that keeps each rebuilt page's
  switches alive (a leak per rebuild). Up the input path,
  `SwitchComponent::input` ends `onStateChanged(); return true;` (`:64-67`)
  and `ComponentList::input` returns `true` straight after the child's input
  (`:164-165`): nothing at those two levels touches the deleted list. The
  same shape as upstream's `:1616` (`delete updateGui` in the torrent
  switch's callback). Levels above `ComponentList` not read: plausible-safe.
- `:10178-10228` SSH, SAMBA, SIMPLE HTTP: `systemctl` through
  `runSystemCommand` in change callbacks (interface thread, no bound).
- `:10232`, `:10237`, `:10246` `usbgadget` through `GetShOutput` at build and
  close.

## Elsewhere in the file, at the leads' lines

- `:188-191` the RETROACHIEVEMENTS row: `isScriptingSupported(RETROACHIVEMENTS)`,
  `global.retroachievements`, `Settings`' `RetroachievementsMenuitem`, a
  username (T20's handed-over gates).
- `:1100` `exitreboot` set on FRONTEND DEVELOPER OPTIONS, whose `onFinalize`
  (`:1457-1466`) reads only `reboot` (upstream's PublicWebAccess row; D-UI-079).
- `:1513-1521` MANUAL UPDATES is **the fork's** (`975235429`, 2026-10-02,
  #337, #383): sentence-case prose and a URL in a `GuiMsgBox`, in the fork's
  code where the fork dialect is ALL CAPS -- the brief called it upstream's;
  corrected by history.
- `:1842` the keyboard layout and variant (from `rocknix-keyboard`'s own
  listing) to `system()` inside double quotes; `:1857-1870` the timezone
  seeded from `timeinfo` at open and written by every close -- both ROCKNIX's
  code under `#if defined(ROCKNIX)`.
- `:2146-2195` the LED COLOR / LED BRIGHTNESS rows (`DEVICE_LED_CONTROL`) write
  `led.color` -- the key the scripts read -- and run `ledcontrol`.
- **`:2987-3103` the RGB LED page is `#ifdef BATOCERA`**, and `:3105-3246`
  (the first SECURITY page, `:3209`'s `getRootPassword()` literal) is
  `#if defined(BATOCERA)`: no ROCKNIX image builds either. The brief's
  `led.colour` lead and T21's `:2989` and `:3209` notes are therefore
  `gated: never built` (no fork commit adds `led.colour`: `git log -S`).
- `:3126-3154` STORAGE DEVICE: `setStorage`'s result ignored before the
  reboot flag (T21's PL-06 family, #1194; `ROCKNIX`-built).
- `:3261-3275` the ROCKNIX SECURITY page: ROOT PASSWORD is
  `addInputTextConfigRow(..., "root.password", false)` -- unmasked; a
  `rootpassword` TextComponent is built and never shown (`:3264`); every
  close saves `system.cfg` and runs `setrootpass` (`:3267-3273`), changed or
  not. `setrootpass` refuses an empty password and changes nothing
  (`:20-26` at `8ebaf8daad`), so the device's password is never cleared;
  but each close of the page re-hashes the shadow, re-runs `smbpasswd` and
  `syncthing generate` and restarts the services found active, on the
  interface thread, unchanged or not; and after T21's S1 a typed-empty entry
  is written to `system.cfg` (`:3268`) before the script refuses, so
  `root.password` reads empty while the device keeps its password -- the
  wizard's CURRENT PASSWORD then shows blank (`:6734`). Against its guarded
  twins (`:6533`, `:8417`).
- **New lead (Q5):** `:8116` `_(want.second.c_str())` over
  `CloudText::recommendedProviders()` (`CloudText.cpp:18-35`): a runtime
  msgid xgettext cannot extract, and none of the fourteen labels is in the
  French catalog. Twelve are names; WINDOWS SHARE (SMB) and AMAZON S3 AND
  COMPATIBLE are phrases a French player reads in English.
- `:10349` `ZeroTier One` and `:10860` `Emulator`: labels not upper-cased in
  the source.
- `:11587` `writeAllText` writes the theme-set file (Backlog #1186: this
  slice's to move onto the atomic writer).
