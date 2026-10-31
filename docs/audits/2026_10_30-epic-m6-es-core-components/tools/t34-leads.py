"""02 § The leads (#681): the brief's L-01 to L-21 and floor rows 3.1 to 3.34
(their lines cells read from the brief, never retyped), the read's new leads
L-22 to L-24, each with its family, owners, disposition, proof and question; and
the brief's § 1 rulings (a) to (j), each pointing at its 02 row. Asserts 24 L
leads, 34 floor rows, 10 rulings, and every lead and ruling answered.
    t34-leads.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import BRIEF, die

FAM = {1: "layout from what it produced / a moving number", 2: "a house constant a surface does not keep", 3: "a prompt where the key moves nothing", 4: "a lifetime or a thread",
       5: "a read of a file another process writes", 6: "a player sentence outside the vocabulary or without French", 7: "a structure or merge-debt fact"}
text = open(BRIEF, encoding="utf-8").read()
cells = {}
for m in re.finditer(r"^\| (L-\d\d|\*\*3\.\d+\*\*|3\.\d+) \| (.+?) \| (.+?) \|", text, re.M):
    cells[m.group(1).strip("*")] = m.group(2).strip()
NEW = {"L-22": "`AsyncNotificationComponent.cpp:117-121`, `:261-299`; h `:72`, `:74`",
       "L-23": "`RatingComponent.cpp:262-266`",
       "L-24": "`VideoComponent.cpp:347-351`"}
cells.update(NEW)
L = {  # id -> (family, question, owners, disposition, proved)
 "L-01": (6, "Q3, Q6", "T34 (`ComponentList.cpp:568`, upstream's line); `InputConfig.cpp` T35's, cited", "a defect in an upstream line: under French every settings list's CHOOSE prompt draws no icon and logs `Unknown help icon`; 3.16's case FAILs at the pin, G-04 under French is the frame; contained fix under rule 6 (drop the `_()`), a `bug` at stage D, a #585 line; the catalog's orphan is a row for the pause", "tree"),
 "L-02": (1, "Q1", "T34; `resources/Font.cpp` T36's, cited", "the moving number at a row's construction; a read trace and G-05's reopened-page pair; a rasterise-first in the component or a record is the pause's", "tree"),
 "L-03": (1, "Q1", "T34 (upstream's formula, moved whole by the fork's `48d43c0fb`)", "3.4 FAILs at the pin (the shares sum to 0.987 and 1.013); `git log -S` first at stage C; the pause rules whether the component's shares are made to sum to 1 (a register row)", "tree"),
 "L-04": (2, "Q2", "T34; the pages with wide bars T26's and T31's", "3.26's arithmetic; the widest bars framed at 640 (G-03); a bar that fits its cell, or the pages' labels, is the pause's", "tree"),
 "L-05": (2, "Q2, Q7", "the comment T34's; the popup T35's", "recorded, not deleted (`engineering-practices.md:576`); the comment corrected or the claim kept at the pause", "tree"),
 "L-06": (2, "Q2", "T34 (upstream's constant); `rowInset()`'s two fork pages T26's and T31's", "framed at both sizes (G-04, G-11); a screen fraction under D-UI-012's family is a register row for the pause", "tree"),
 "L-07": (7, "Q7", "T34 (the include line); `CloudText` T18's, the CMake T35's", "recorded with how it resolves; a `CloudText` that moves to es-core is T18's and T35's call", "tree"),
 "L-08": (5, "Q5", "T34", "by design per `:191-196`; the player sees a blank badge until the page's next bind, which asks again (the stub at the pin, S5); ruling 5: no timer; the uncached state is S5's fix (#1319); `tools/ra-ui-test`'s 204-then-200 fixture is the guest half", "S5 `568ef099d`: `stage-e/s5-before.txt`, `s5-after.txt`"),
 "L-09": (5, "Q5", "T34; `HttpReq` T21's, `FileSystemUtil` T36's, cited", "sound at the pin: the writer's `removeFile` (`HttpReq.cpp:344`) and `renameFile` (`:479` -> `FileSystemUtil.cpp:1457-1458`) erase the cached miss before `:190` asks; 3.21's first half a candidate that PASSes at the pin", "tree"),
 "L-10": (4, "Q4", "T34 (upstream surface, outside the lanes)", "a data race on `ctx->component` and a call into a component being destroyed; recorded with the two threads named (§ The lifetimes); G-10 `CANNOT` (no media); a contained fix (an atomic, or a wait) under rule 6 only if the pause opens it", "tree"),
 "L-11": (4, "Q4", "T34", "sound by the invariant: each `delete this` is the last thing its handler does; 3.19's ASan harness at stage C", "tree"),
 "L-12": (4, "Q4", "T34; `Window::postToUiThread` T35's, `AppWindow` T33's", "a use after free if the field dies before the post runs; 3.20's case at stage C with the fakes' `Window.h`; a weak token the posts check is the pause's", "tree"),
 "L-13": (3, "Q3", "T34 (upstream surfaces)", "recorded; framed if a one-system carousel or a one-value option row is reachable on the guest", "tree"),
 "L-14": (7, "Q7", "T34", "a one-commit tidy if the pause opens it", "tree"),
 "L-15": (7, "Q3", "T34; `GuiMenu.cpp:591` T26's", "an unstated invariant: the cast is safe only because the MAIN MENU's `mButtons` is empty and the index guard `:508` returns first; written into `02` beside `MenuComponent.h:53-56`; a `dynamic_pointer_cast` plus a null check is the contained fix", "tree"),
 "L-16": (1, "Q1", "T34; `TextListComponent.h` an upstream surface", "the seven reads tabled in § The layouts with their surfaces; disposition with L-02's", "tree"),
 "L-17": (1, "Q1", "T34 (upstream's `TextComponent.cpp`)", "#48's root, unchanged at the pin: 3.5's case, a 640x480 frame of a padded auto-height text that is not a `GuiMsgBox`, the reproducer for #585; the root fix (re-heights every padded auto-height text) is the pause's, a register row", "tree"),
 "L-18": (6, "Q6", "T34", "a reading, not a check: no fork label carries the brand through the six formatters at the pin; a `tools/vocabulary-check` rule (the brand inside `addEntry|addButton|setTitle|addWithDescription|addGroup` arguments) proposed for the coordinator", "tree"),
 "L-19": (2, "Q2", "T34", "dead text, harmless; recorded", "tree"),
 "L-20": (5, "Q5", "T34 (upstream surfaces); the scraper T32's", "recorded with the scraper as the writer; a frame only if a scrape then a game open fits the window, else `CANNOT`", "tree"),
 "L-21": (4, "Q4", "T34; `HttpReq` T21's", "sound; recorded so the next reader does not re-derive it", "tree"),
 "L-22": (4, "Q4", "T34 (a lane surface); the holders T18's and T20's", "**new:** `close()` writes `mClosing` and `mFadeTime` unlocked from the holders' threads while `update()` reads them on the interface thread; a host ThreadSanitizer case at stage C; a `bug` at stage D if it fires; § 1 (b)'s component half beside it", "tree"),
 "L-23": (6, "Q6", "T34 (upstream's line)", "**new:** the rating's OK prompt `\"add star\"` is outside `_()`; contained under rule 6 with its French in the same commit; a #585 line", "tree"),
 "L-24": (3, "Q3, Q6", "T34 (upstream's line)", "**new:** a focused video component's help bar names BACK as `SELECT`; reached only where a video component holds focus; recorded, contained under rule 6 if the pause opens it", "tree"),
}
FAIL7 = {"3.4", "3.6", "3.7", "3.8", "3.16", "3.21", "3.26"}
F = {  # floor row -> (family, question, disposition)
 "3.1": (3, "Q3", "a case at stage C; expected PASS (D-UI-034's fix)"), "3.2": (3, "Q3", "a case at stage C; expected PASS"), "3.3": (3, "Q3", "a case at stage C; expected PASS"),
 "3.4": (1, "Q1", "FAIL at the pin (L-03); 300 `setDescription` calls hold the height (#241)"), "3.5": (1, "Q1", "L-17's case: the measured height one line short"),
 "3.6": (1, "Q1", "FAIL at the pin: the limit 20 px too large"), "3.7": (6, "Q6", "FAIL at the pin: `\"Auto\"`; the precision cases expected PASS"),
 "3.8": (3, "Q3", "FAIL candidate: `listInput(-7)` on a size-3 carousel; the landing index asserted in `[0, sz)` per loop type"),
 "3.9": (1, "Q1", "a case; a 0 tile size is guarded only by a `LOG`"), "3.10": (1, "Q1", "a case on the partial last row"), "3.11": (1, "Q1", "a case on the extra row past the cutoff"),
 "3.12": (7, "Q7", "a case on the date steps (an extraction or a fake `InputConfig`)"), "3.13": (6, "Q6", "PASS at the pin as written: a blank, not `<NOT SET>`; a style question for the pause"),
 "3.14": (7, "Q7", "a case; `:69`'s unused `680.0f` is lint"), "3.15": (3, "Q3", "a case, the landing index for 3.8"),
 "3.16": (6, "Q3, Q6", "FAIL at the pin: `haut/bas` -> `nullptr` and the `Unknown help icon` line (L-01)"), "3.17": (3, "Q3", "a case; expected PASS"),
 "3.18": (2, "Q6", "a case: the width handed to `chooseThatFits` is the row's cell, never 0.9 W"), "3.19": (4, "Q4", "ASan over an extracted popup (L-11)"),
 "3.20": (4, "Q4", "post, delete, drain (L-12)"), "3.21": (5, "Q5", "first half a candidate that PASSes at the pin (L-09); second half: the 204 then 200 is never asked again (L-08, by design)"),
 "3.22": (1, "Q5", "a case on the fit after a turn"), "3.23": (1, "Q5", "a case; turn 1 four times is identity"), "3.24": (1, "Q5", "a case on the normaliser"),
 "3.25": (2, "Q2", "a case; expected PASS"), "3.26": (2, "Q2", "FAIL candidate: five 128 px buttons at 640 overhang (L-04)"), "3.27": (1, "Q1", "a case on the strict `<`"),
 "3.28": (1, "Q1", "a case incl. the signed/unsigned compare"), "3.29": (1, "Q1", "the same for the game list"), "3.30": (3, "Q3", "a case on the tri-state cycle"),
 "3.31": (2, "Q3", "a case on the clamp and the sentinel"), "3.32": (7, "Q7", "a case on the accumulation's drift"), "3.33": (7, "Q7", "a case on a cursor inside a UTF-8 sequence (T21's `moveCursor`)"),
 "3.34": (3, "Q3", "a case incl. a count of 1 and a divide by 0"),
}
S0 = {  # floor row -> its result at the pin, stage E's S0 (`stage-e/s0-before.txt`); the rest stay pending until their stream
 "3.11": "tool-run; S0: PASS at the pin (`stage-e/s0-before.txt`)",
 "3.14": "tool-run; S0: PASS at the pin; its PL-40 half (content 10 px narrower) FAIL: `-10 >= 0` and the vertical scroll never moves (`stage-e/s0-before.txt`)",
 "3.15": "tool-run; S0: PASS at the pin (`stage-e/s0-before.txt`)",
 "3.29": "tool-run; S0: PASS at the pin (`stage-e/s0-before.txt`)",
}
SE = dict(S0)  # every stage-E result by row: S0's four, then each stream's floor cases
SE.update({
 "3.18": "tool-run; S2: PASS at the pin, written before the fix and run again after it (`stage-e/s2-before.txt`, `s2-after.txt`)",
 "3.33": "tool-run; S2: PASS at the pin, written before the fix and run again after it (`stage-e/s2-before.txt`, `s2-after.txt`)",
 "3.4": "fix-unit-test; S3: FAIL at the pin (stage D), PASS after `db12b1598` (`stage-e/s3-after.txt`)",
 "3.5": "fix-unit-test; S3: FAIL at the pin (28 against 48, 20 against 40), PASS after `db12b1598` (`stage-e/s3-before.txt`, `s3-after.txt`)",
 "3.6": "fix-unit-test; S3: FAIL at the pin (stage D), PASS after `db12b1598` (`stage-e/s3-after.txt`)",
 "3.25": "tool-run; S3: PASS at the pin and after (`stage-e/s3-before.txt`, `s3-after.txt`)",
 "3.28": "tool-run; S3: PASS at the pin and after (`stage-e/s3-before.txt`, `s3-after.txt`)",
 "3.1": "tool-run; S4: PASS at the pin and after, one case for 3.1-3.3 (`stage-e/s4-before.txt`, `s4-after.txt`)",
 "3.2": "tool-run; S4: PASS at the pin and after, with 3.1 and 3.3",
 "3.3": "tool-run; S4: PASS at the pin and after, with 3.1 and 3.2",
 "3.7": "fix-unit-test; S4: FAIL at the pin (stage D, `Auto`), PASS after `a9017ff50` (`stage-e/s4-after.txt`)",
 "3.12": "tool-run; S4: PASS at the pin and after (`stage-e/s4-before.txt`, `s4-after.txt`)",
 "3.13": "fix-unit-test; S4 (PL-25, #1322): FAIL at the pin (a blank), PASS after `a9017ff50`: `<NOT SET>` through `_()`",
 "3.16": "fix-unit-test; S4: FAIL at the pin (`0 == 1`), PASS after `a9017ff50`; since S4 the case reads the list's own line through a catalog double (`stage-e/s4-checks.txt`)",
 "3.17": "tool-run; S4: PASS at the pin and after (`stage-e/s4-before.txt`, `s4-after.txt`)",
 "3.31": "tool-run; S4: PASS at the pin and after",
 "3.32": "tool-run; S4: PASS at the pin and after; five presses reach 1.0 exactly in float",
 "3.34": "tool-run; S4: PASS at the pin and after, one entry and none included",
 "3.21": "fix-unit-test; S5: the first half PASS at the pin and after; the second (PL-13, #1319): the pin already re-asks on the next bind, and its one FAIL, the cache path kept, PASS after `568ef099d`",
 "3.22": "tool-run; S5: PASS at the pin and after, with 3.23 and 3.24 (`stage-e/s5-before.txt`, `s5-after.txt`)",
 "3.23": "tool-run; S5: PASS at the pin and after: four turns are the identity",
 "3.24": "tool-run; S5: PASS at the pin and after: -1, 4, 5 and 0 normalise to 3, 0, 1 and 0",
 "3.9": "tool-run; S6: PASS at the pin and after, with 3.10: the dimensions of three grids (`stage-e/s6-before.txt`, `s6-after.txt`)",
 "3.10": "tool-run; S6: PASS at the pin and after: a partial last row read, and a whole one",
 "3.27": "tool-run; S7: PASS at the pin and after: a row that would end exactly at the cap is left out by the strict `<` (277 of 300), recorded",
 "3.30": "tool-run; S7: PASS at the pin and after: auto, on, off and back, and a plain toggle",
 "3.8": "tool-run; stage D: PASS at the pin for every size 1 to 12 and every loop type (`stage-d/components-tests.run.log`), PL-24 withdrawn; PASS at every stage-E tip",
 "3.19": "tool-run; stage D: `SAN asan-popup (-fsanitize=address): rc 0; no sanitizer report` over a double of the popup's shape (not its lines), at the pin and at every stage-E tip",
 "3.20": "fix-unit-test; S2 (#1311): `SAN asan-textedit` rc 1, heap-use-after-free, at the pin; rc 0 after `2cbb62d7b` (`stage-e/s2-before.txt`, `s2-after.txt`)",
 "3.26": "tool-run; stage D: FAIL at the pin, `710.4 <= 576` (four buttons fit); PL-14 recorded, not fixed; `doctest::may_fail` with PL-14 named since the hand-back (ruling 9)",
})
R = [  # (ruling, the 02 row)
 ("(a) T32 PL-07 / #1263, the caller's half", "§ The reads, `ImageComponent.cpp:408`"),
 ("(b) T2 PC-1, the card's half", "§ The lifetimes, `AsyncNotificationComponent.cpp:123`, with L-22 at `:119`"),
 ("(c) T26 PL-27, the callback types", "§ The lifetimes, `SwitchComponent.h:53` and `OptionListComponent.h:658`"),
 ("(d) T31 L-03 / #1243's invariant", "§ The lifetimes, `OptionListComponent.h:310` and `:323`"),
 ("(e) #1266's grid after `clear()`", "§ The lifetimes, `ImageGridComponent.h:91`"),
 ("(f) #48's `TextComponent` root", "§ The layouts, `TextComponent.cpp:338` and `:483`"),
 ("(g) batocera's `setOpacity` guard", "§ The structure: `HelpComponent.cpp:212-213` dereference `mGrid` unguarded, `:251` is inside `render`'s `if (mGrid)` (`:218`); `mGrid` is null when `ShowHelpPrompts` is off or there are no prompts (`:67-70`); nothing calls `HelpComponent::setOpacity` on the fork's images (`Window.cpp` constructs the one bar at `:41` and never calls it; the bar is no component's child): unreachable at the pin, recorded; the guard arrives with batocera's `9dbd4b9bf` at the reconciliation"),
 ("(h) `UntintedImageComponent`", "§ The structure: it lives at `es-app/src/guis/GuiMenu.cpp:6401` (T26's file; the QR at `:6425`), not under `components/`; lifting an untinted mode into `ImageComponent` (h `:76`) is the pause's question"),
 ("(i) `ComponentList.cpp:568`'s `_(\"up/down\")`", "§ The words, L-01, and § The input, `ComponentList.cpp:548`"),
 ("(j) the two lanes' `AsyncNotificationComponent.h` doubles", "§ The structure: a header change in T34 is named as a collision at the hand-back; the fakes are not the lane's"),
]
Ls = sorted(k for k in cells if k.startswith("L-")); Fs = sorted((k for k in cells if not k.startswith("L-")), key=lambda k: int(k.split(".")[1]))
if len(Ls) != 24 or set(Ls) != set(L):
    die("L leads: %d; unanswered %s; answered without a cell %s" % (len(Ls), sorted(set(Ls) - set(L)), sorted(set(L) - set(Ls))))
if len(Fs) != 34 or set(Fs) != set(F):
    die("floor rows: %d; unanswered %s" % (len(Fs), sorted(set(Fs) - set(F))))
if set(S0) != {"3.11", "3.14", "3.15", "3.29"}:
    die("S0 rows: %s" % sorted(S0))
if not set(SE) <= set(F):
    die("stage-E rows not on the floor: %s" % sorted(set(SE) - set(F)))
if len(R) != 10:
    die("rulings: %d, expected 10" % len(R))
print("| Lead | Lines at the pin | Family | Owner | Disposition | proved | question: |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for k in Ls:
    fam, q, own, disp, proved = L[k]
    print("| %s | %s | %s | %s | %s | %s | %s |" % (k, cells[k], FAM[fam], own, disp, proved, q))
for k in Fs:
    fam, q, disp = F[k]
    print("| %s | %s | %s | T34 | %s | %s | %s |" % ("**%s**" % k if k in FAIL7 else k, cells[k], FAM[fam], disp, SE.get(k, "pending: fixture at stage C"), q))
print()
print("**The brief's § 1 rulings, each with its row:**")
print()
print("| Ruling | Its row in this file |")
print("| --- | --- |")
for r, row in R:
    print("| %s | %s |" % (r, row))
print()
print("Generated, asserted by `tools/t34-leads.py`: %d L leads (the brief's 21 and the read's L-22 to L-24), %d floor rows (the seven FAIL-at-pin in bold), each answered, %d run at the pin in S0 and %d in the streams; %d rulings, each with its row." % (len(Ls), len(Fs), len(S0), len(SE) - len(S0), len(R)))
