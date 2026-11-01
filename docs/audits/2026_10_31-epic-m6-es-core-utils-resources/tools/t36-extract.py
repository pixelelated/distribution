"""Lift the parse-only seams' lines from the pin, verbatim, into <out>/x_<name>.inc for
T36's utils-resources-tests (#683; T35's t35-extract.py shape). Each spec names its file,
its line range and the code its first and last lines must hold; a range that no longer
holds it is refused (exit 1, nothing written), so a case never runs against lines it was
not written for. The linkable-whole sources (FileSystemUtil.cpp, StringUtil.cpp, md5.cpp,
TimeUtil.cpp) are compiled whole by the build script, not lifted here.
    t36-extract.py <ES worktree> <pin> <out dir>"""
import os
import subprocess
import sys

W, PIN, OUT = sys.argv[1:4]
S = "es-core/src/"
SPECS = [  # name, file, first, last, the first line holds, the last line holds
    # 3.7, L-13: runSystemCommand returns 0 and reads neither name nor window (a text/tree proof).
    ("runsys", "utils/Platform.cpp", 853, 880, "int runSystemCommand(const std::string& cmd_utf8, const std::string& name, Window* window)", "}"),
    # 3.9, L-06 (T26's collision control): GetShOutput drops the last byte of each chunk.
    ("gsh", "utils/Platform.cpp", 891, 905, "std::string GetShOutput(const std::string& mStr)", "}"),
    # L-05: run()'s wrap, the literal the host runs (3.5 builds the command from these lines).
    ("run_wrap", "utils/Platform.cpp", 162, 168, "std::string cmdOutput = \"((((\"", "return WEXITSTATUS(n);"),
    # 3.24, L-18: quitES leaks the SDL_Event (recorded from the text).
    ("quites", "utils/Platform.cpp", 216, 239, "int quitES(QuitMode mode)", "}"),
    # 3.8, 3.16, L-07/L-08: Font's scaling and the height's growth, read as text.
    ("font_ctor_scale", "resources/Font.cpp", 93, 120, "Font::Font(int size, const std::string& path, bool menuScaling)", "}"),
    ("font_glyph_grow", "resources/Font.cpp", 422, 423, "if (glyphSize.y() > mMaxGlyphHeight", "mMaxGlyphHeight = glyphSize.y();"),
    ("font_getheight", "resources/Font.cpp", 756, 759, "float Font::getHeight(float lineSpacing) const", "}"),
    ("font_fromtheme_scale", "resources/Font.cpp", 1233, 1258, "std::shared_ptr<Font> Font::getFromTheme(", "}"),
    # 3.23, L-11: cleanupVRAM's eviction loop, read as text.
    ("cleanupvram", "resources/TextureDataManager.cpp", 135, 194, "void TextureDataManager::cleanupVRAM()", "}"),
    # 3.17, L-09: the flag glyph's width and the newline's advance, read as text.
    ("font_sizetext", "resources/Font.cpp", 716, 754, "Vector2f Font::sizeText(const std::string& text, float lineSpacing)", "}"),
    # 3.22: secondsToString's thresholds, read as text (linking TimeUtil.cpp cascades).
    ("secstostr", "utils/TimeUtil.cpp", 519, 588, "std::string secondsToString(const long seconds, bool asTime)", "}"),
]
got = {}
for name, f, a, b, first, last in SPECS:
    r = subprocess.run(["git", "-C", W, "show", f"{PIN}:{S}{f}"], capture_output=True, text=True, errors="replace")
    if r.returncode:
        sys.exit(f"t36-extract: {f} not at {PIN}")
    L = r.stdout.split("\n")
    lines = L[a - 1:b]
    if not lines or first not in lines[0] or last not in lines[-1]:
        sys.exit(f"t36-extract: {f}:{a}-{b} no longer holds its code "
                 f"(first {lines[0].strip()[:60]!r}, last {lines[-1].strip()[:60]!r}); nothing written")
    got[name] = f"// {S}{f}:{a}-{b} at {PIN}, verbatim\n" + "\n".join(lines) + "\n"
os.makedirs(OUT, exist_ok=True)
for name, text in got.items():
    open(os.path.join(OUT, f"x_{name}.inc"), "w").write(text)
print(f"t36-extract: {len(got)} extracts at {PIN}")
