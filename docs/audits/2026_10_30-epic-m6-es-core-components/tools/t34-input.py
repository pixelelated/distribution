"""02 § The input (#681): every input() and getHelpPrompts() in the 80 at the
pin. Asserts 14 `::input(InputConfig` and 2 inline input(), 12 `::getHelpPrompts()`
and 2 inline; the keys each input() names are read from its own body (brace
matched); each prompt row carries the condition under which it offers a direction.
    t34-input.py <ES worktree> [paths file]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import COMP, die, show, paths

W = sys.argv[1]
files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
P = {  # file:line -> (what it offers, and when; disposition; proved)
 "ButtonComponent.cpp:186": ("OK with the button's help text; no direction", "sound", "tree"),
 "CarouselComponent.cpp:354": ("`up/down` or `left/right` CHOOSE by the carousel's type alone (`:358-361`), whatever its size", "L-13: a one-entry carousel offers a direction that moves nothing; upstream surface, recorded; framed if a one-system carousel is reachable", "tree"),
 "ComponentGrid.cpp:519": ("`up/down`, `left/right` or both CHOOSE only where `canMoveCursor` finds a focusable cell (`:527-528`, `:546-550`); a child's own `up/down` suppresses the grid's (`:536-538`)", "sound (D-UI-034, fork `aa8c5da4c`); 3.1 to 3.3, G-03, G-06", "tree"),
 "ComponentList.cpp:548": ("`up/down` CHOOSE when `size() > 1` and no child names `up/down` (`:555-568`)", "**L-01:** the icon key goes through `_()` (`:568`), so under French it is `haut/bas`, which `getIconTexture` does not know: a null icon and `Unknown help icon`; 3.16, G-04 under French", "tree"),
 "ComponentTab.cpp:320": ("`left/right` SWITCH TAB when `size() > 1`, not when a child already names `left/right` (`:327-341`)", "sound (fork `8927b1760`); 3.17, G-05", "tree"),
 "ImageComponent.cpp:1057": ("OK SELECT; no direction", "sound", "tree"),
 "MenuComponent.cpp:531": ("the grid's (`mGrid.getHelpPrompts()`)", "sound: `ComponentGrid`'s rule", "tree"),
 "RatingComponent.cpp:262": ("OK `\"add star\"`; no direction", "**L-23 (new):** a help label outside `_()`, untranslated under every language; upstream's line; a words lead (Q6), contained under rule 6", "tree"),
 "SliderComponent.cpp:337": ("`left/right` CHANGE always", "sound: a slider at either end still moves the other way", "tree"),
 "SwitchComponent.cpp:165": ("OK CHANGE; no direction", "sound", "tree"),
 "TextEditComponent.cpp:390": ("`up/down/left/right` MOVE CURSOR while editing, else OK EDIT (`:395-397`)", "read at stage C against `input()`: whether up and down move the cursor in a single-line field", "tree"),
 "VideoComponent.cpp:347": ("BACK labelled `_(\"SELECT\")` (`:350`)", "**L-24 (new):** the back button's prompt names SELECT; upstream's line; a words and input lead (Q3, Q6); reached only where a video component holds focus", "tree"),
 "OptionListComponent.h:202": ("the popup's menu prompts plus BACK BACK", "sound", "tree"),
 "OptionListComponent.h:636": ("`left/right` CHANGE whenever `!mMultiSelect` (`:639-640`), whatever the count; OK SELECT", "L-13: a one-value option row offers CHANGE that changes nothing; upstream surface, recorded", "tree"),
}
DEF_IN = re.compile(r"::input\(InputConfig")
DEF_HP = re.compile(r"::getHelpPrompts\(\)")
INL_IN = re.compile(r"^\s*(virtual )?bool input\(InputConfig\* ?config, ?Input input\) ?(override)? *\{?\s*$")
INL_HP = re.compile(r"^\s*(virtual )?std::vector<HelpPrompt> getHelpPrompts\(\) ?(override)? *\{?\s*$")

def body(lines, i):
    """The text of the function whose definition starts at line index i, by brace count."""
    depth, out, started = 0, [], False
    for l in lines[i:]:
        code = l.split("//")[0]
        out.append(code)
        for c in code:
            if c == "{":
                depth += 1; started = True
            elif c == "}":
                depth -= 1
        if started and depth == 0:
            return "\n".join(out)
    die("no end of the function at line %d" % (i + 1))

inputs, prompts = [], []
for f in files:
    lines = show(W, f).split("\n")
    for i, l in enumerate(lines):
        code = l.split("//")[0]
        key = "%s:%d" % (f[len(COMP):], i + 1)
        if DEF_IN.search(code) or (f.endswith(".h") and INL_IN.match(code)):
            b = body(lines, i)
            keys = sorted(set(re.findall(r"isMappedTo\((BUTTON_[A-Z]+|\"[a-z]+\")", b)) | set('"%s"' % k for k in re.findall(r"isMappedLike\(\"([a-z]+)\"", b)))
            inputs.append((key, "inline" if not DEF_IN.search(code) else "out-of-line", keys, len(b.split("\n"))))
        if DEF_HP.search(code) or (f.endswith(".h") and INL_HP.match(code)):
            prompts.append((key, "inline" if not DEF_HP.search(code) else "out-of-line"))
ci = sum(1 for x in inputs if x[1] == "out-of-line"); ii = len(inputs) - ci
cp = sum(1 for x in prompts if x[1] == "out-of-line"); ip = len(prompts) - cp
for what, have, want in [("::input(", ci, 14), ("inline input(", ii, 2), ("::getHelpPrompts(", cp, 12), ("inline getHelpPrompts(", ip, 2)]:
    if have != want:
        die("%s: %d, expected %d" % (what, have, want))
gk = {k for k, _ in prompts}
if gk != set(P):
    die("prompt rows without a reading: %s; readings without a row: %s" % (sorted(gk - set(P)), sorted(set(P) - gk)))
print("**The inputs** (the keys each names, read from its body):")
print()
print("| `input()` | Form | Keys it names (`isMappedTo` / `isMappedLike`) | Body lines |")
print("| --- | --- | --- | ---: |")
for k, form, keys, n in inputs:
    print("| `%s` | %s | %s | %d |" % (k, form, ", ".join("`%s`" % x for x in keys) or "- (delegates)", n))
print()
print("**The help prompts** (the condition under which each offers a direction):")
print()
print("| `getHelpPrompts()` | Form | What it offers, and when | Disposition | proved |")
print("| --- | --- | --- | --- | --- |")
for k, form in prompts:
    what, disp, proved = P[k]
    print("| `%s` | %s | %s | %s | %s |" % (k, form, what, disp, proved))
print()
print("Generated, asserted by `tools/t34-input.py`: %d `input()` (%d `::input(InputConfig`, %d inline), their keys read from each body; %d `getHelpPrompts()` (%d out of line, %d inline), each with its reading." % (len(inputs), ci, ii, len(prompts), cp, ip))
