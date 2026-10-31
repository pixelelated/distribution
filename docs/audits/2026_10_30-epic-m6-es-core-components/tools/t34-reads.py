"""02 § The reads (#681): every exists(, getFileSize(, new HttpReq and live
TextureResource::get( in the 80 at the pin, joined with its writer while ES runs
and what a stale answer reads as. Asserts 10 exists( lines in 5 files, 0 of them
uncached, 1 getFileSize, 1 new HttpReq, 21 live texture lookups, and that every
grep row has a disposition and every disposition a grep row.
    t34-reads.py <ES worktree> [paths file]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import COMP, die, show, paths

W = sys.argv[1]
files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
WIN = "Windows-only: inside `#if WIN32` (`:592`), compiled to nothing on every image"
RES = "none: a resource inside the image (`:/...`), read-only"
THEME = "a theme install or update (the theme installer) while ES runs"
TEX = "a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's)"
D = {  # file:line -> (kind, what is read, the writer while ES runs, a stale answer reads as, proved, disposition)
 "CarouselComponent.cpp:765": ("exists", "a system or game entry's `marquee`/`fanart`/`cartridge`/`mix` image (`:763`)", "the scraper, writing media while ES runs", "a cached miss draws the entry as text until a game launch or a restart clears the cache", "tree", "L-20, recorded; upstream surface outside the lanes"),
 "ImageComponent.cpp:1232": ("exists", "the theme's `default` image path", THEME, "a cached miss leaves no default image until the theme reloads", "tree", "L-20, recorded"),
 "VideoComponent.cpp:327": ("exists", "the theme's video `path` (a `{`-binding is taken without the check)", THEME, "a cached miss falls back to `defaultVideoPath` (`:330`)", "tree", "L-20, recorded"),
 "VideoComponent.cpp:591": ("exists", "a `path` property, the bound `{game:video}` among them", "the scraper, writing videos while ES runs", "a video scraped mid-session reads as absent until a launch clears the cache (`es-native-ui.md:107`)", "tree", "L-20, recorded; a frame only if a scrape fits the window (G-08's guest has no media: `CANNOT`)"),
 "VideoVlcComponent.cpp:605": ("exists", "`libvlc.dll` beside the executable", WIN, "-", "tree", "dead on the images (Q7's gates)"),
 "VideoVlcComponent.cpp:639": ("exists", "`plugins/gui/libqt4_plugin.dll`", WIN, "-", "tree", "dead on the images (Q7's gates)"),
 "WebImageComponent.cpp:81": ("exists", "the downloaded copy `mLocalFile`, at destruction when the cache lasts 0 s", "`HttpReq` (tmp file, then `renameFile`, which erases the key: `FileSystemUtil.cpp:1457-1458`)", "fresh: every writer of the path erases its key", "tree", "sound"),
 "WebImageComponent.cpp:134": ("exists", "the cached copy `localFile`, before a request (`setImage`)", "`HttpReq` for an earlier component; `removeFile` here (`:141`, `:150`)", "a remembered miss here is erased when the request starts (`HttpReq.cpp:344` `removeFile(outputFilename)`) and when it lands (`:479` `renameFile`)", "tree", "sound; 3.21's first half a candidate that PASSes at the pin (stage C proves it with the real `FileSystemUtil`)"),
 "WebImageComponent.cpp:190": ("exists", "`mLocalFile` after `REQ_SUCCESS`", "`HttpReq`, `renameFile` into the path (`HttpReq.cpp:479`; the `copyFile` fallback `:501` erases too, `FileSystemUtil.cpp:1506-1507`)", "fresh at the pin: the key cached as a miss at `:134` is erased by the writer before `:190` asks (L-09 answered)", "S5: 3.21's first half PASS at the pin and after `568ef099d` (`stage-e/s5-before.txt`, `s5-after.txt`)", "L-09: sound, by the writer's erase; 3.21's case"),
 "WebImageComponent.cpp:228": ("exists", "the cache directory, before a request", "`createDirectory` here (`:229`)", "a cached miss calls `createDirectory` again: idempotent", "tree", "sound"),
 "WebImageComponent.cpp:197": ("getFileSize", "the size of `mLocalFile` after a success", "`HttpReq`", "uncached (`stat64`, `FileSystemUtil.cpp:1319-1335`)", "S5 `568ef099d` (#1319): the stub shows the pin already re-asks on the next bind (the removal erases the cached key); the case's one FAIL at the pin was the cache path kept for the answer, PASS after", "L-08: a 0-byte answer (the proxy's 204, #180) removes the file and returns; `mUrlToLoad` was cleared at `:244`, so the page asks nothing more until its next bind (ruling 5: no timer); since S5 the component also keeps no cache path for it"),
 "WebImageComponent.cpp:243": ("HttpReq", "`new HttpReq(mUrlToLoad, &options)`, the offline proxy's URLs with `X-RA-Store-Only` (`:240-241`, #199)", "writes `mLocalFile` through `<path>.tmp` and `renameFile` (T21's `HttpReq.cpp:324-344`, `:479`)", "-", "tree", "L-21: the stack `HttpReqOptions` is consumed by the constructor before it returns; sound"),
 "ImageComponent.cpp:408": ("texture", "`mPath`, any image a page shows by path", "the scraper, the save-state writer, the sign-in's QR (T26 #1221), any file rewritten under its path", TEX, "tree", "§ 1 (a): the caller's half of #1263 -- the component asks by path once per `setImage` and holds the texture; a file rewritten under the same path while the texture lives is not re-read; the cache's half named for T36 (#683)"),
 "ImageComponent.cpp:400": ("texture", "`mDefaultPath`, the theme's default", THEME, TEX, "tree", "recorded"),
 "ImageComponent.cpp:446": ("texture", "`\"\"`, an empty texture", "-", "-", "tree", "recorded"),
 "BatteryIndicatorComponent.cpp:52": ("texture", "`:/network.svg`", RES, "-", "tree", "recorded"),
 "ControllerActivityComponent.cpp:403": ("texture", "the theme's `imagePath`", THEME, TEX, "tree", "recorded"),
 "ControllerActivityComponent.cpp:406": ("texture", "the theme's `gunPath`", THEME, TEX, "tree", "recorded"),
 "ControllerActivityComponent.cpp:409": ("texture", "the theme's `wheelPath`", THEME, TEX, "tree", "recorded"),
 "ControllerActivityComponent.cpp:417": ("texture", "the theme's `networkIcon`", THEME, TEX, "tree", "recorded"),
 "ControllerActivityComponent.cpp:429": ("texture", "the theme's `planemodeIcon`", THEME, TEX, "tree", "recorded"),
 "ControllerActivityComponent.cpp:546": ("texture", "`mCurrentBatteryTexture`, a theme or resource battery glyph", "a theme install, else none", TEX, "tree", "recorded"),
 "GridTileComponent.h:152": ("texture", "a tile's background `path` (theme)", THEME, TEX, "tree", "recorded"),
 "GridTileComponent.h:158": ("texture", "a tile's selected-background `path` (theme)", THEME, TEX, "tree", "recorded"),
 "HelpComponent.cpp:185": ("texture", "a help icon from the theme's icon map", THEME, TEX, "tree", "recorded"),
 "HelpComponent.cpp:203": ("texture", "a help icon from `ICON_PATH_MAP` (`:/help/...`)", RES, "-", "tree", "recorded"),
 "NinePatchComponent.cpp:326": ("texture", "`mPath`, the frame image (theme or `:/frame.png`)", "a theme install, else none", TEX, "tree", "recorded"),
 "RatingComponent.cpp:158": ("texture", "`:/star_filled.svg`", RES, "-", "tree", "recorded"),
 "RatingComponent.cpp:161": ("texture", "`:/star_unfilled.svg`", RES, "-", "tree", "recorded"),
 "RatingComponent.cpp:220": ("texture", "the theme's `filledPath`", THEME, TEX, "tree", "recorded"),
 "RatingComponent.cpp:226": ("texture", "the theme's `unfilledPath`", THEME, TEX, "tree", "recorded"),
 "RectangleComponent.cpp:38": ("texture", "`:/white.png`", RES, "-", "tree", "recorded"),
 "VideoVlcComponent.cpp:479": ("texture", "`\"\"`, the frame texture a video draws into", "-", "-", "tree", "recorded"),
}
pat = {"exists": r"exists\(", "getFileSize": r"getFileSize\(", "HttpReq": r"new HttpReq\(", "texture": r"TextureResource::get\("}
got, per_file, uncached = {}, {}, 0
for f in files:
    for n, line in enumerate(show(W, f).split("\n"), 1):
        code = line.split("//")[0]
        for kind, rx in pat.items():
            if re.search(rx, code):
                key = "%s:%d" % (f[len(COMP):], n)
                got[key] = kind
                if kind == "exists":
                    per_file[f] = per_file.get(f, 0) + 1
                    if re.search(r"exists\([^)]*, *false\)", code):
                        uncached += 1
missing = sorted(set(got) - set(D)); extra = sorted(set(D) - set(got))
if missing or extra:
    die("grep rows without a disposition: %s; dispositions without a grep row: %s" % (missing, extra))
for k in got:
    if got[k] != D[k][0]:
        die("%s is a %s by the grep and a %s in the table" % (k, got[k], D[k][0]))
c = {k: sum(1 for v in got.values() if v == k) for k in pat}
for what, have, want in [("exists( lines", c["exists"], 10), ("files with exists(", len(per_file), 5), ("uncached exists(", uncached, 0),
                         ("getFileSize(", c["getFileSize"], 1), ("new HttpReq(", c["HttpReq"], 1), ("live TextureResource::get(", c["texture"], 21)]:
    if have != want:
        die("%s: %d, expected %d" % (what, have, want))
order = {"exists": 0, "getFileSize": 1, "HttpReq": 2, "texture": 3}
print("| Site | Kind | What is read | Its writer while ES runs | A stale answer reads as | Disposition | proved |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for k in sorted(got, key=lambda k: (order[got[k]], k.split(":")[0], int(k.split(":")[1]))):
    kind, what, writer, stale, proved, disp = D[k]
    print("| `%s` | %s | %s | %s | %s | %s | %s |" % (k, kind, what, writer, stale, disp, proved))
print()
print("Generated, asserted by `tools/t34-reads.py`: %d rows -- %d `exists(` lines in %d files, %d of them uncached; %d `getFileSize(`; %d `new HttpReq(`; %d live `TextureResource::get(` (the commented one at `VideoVlcComponent.cpp:77` excluded); every row has a disposition and every disposition a row." % (
    len(got), c["exists"], len(per_file), uncached, c["getFileSize"], c["HttpReq"], c["texture"]))
