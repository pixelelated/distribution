"""3.31 (#679): the grid's IMAGE source returns an empty path, not the thumbnail.

    python3 -I l331-grid-image.py <GridGameListView.cpp> [--control]

GridGameListView::getImagePath is extracted as written and run over a doubled
FileData whose image, marquee, thumbnail and metadata the case sets. Each image
source with its own path empty must fall back the way the function's own later
branches do: to the image where it has one, else to the thumbnail. At the pin
the first branch, `if (src == ImageSource::IMAGE) return file->getImagePath();`,
returns "" for a game with a thumbnail and no image -- FAIL. The same source's
later branch, `(src == IMAGE || src == TITLESHOT) && !getImagePath().empty()`,
is unreachable for IMAGE.
History: the early return is from 8f30c244c (upstream, 2019, "Enhanced Grid
view"); 4371e3b7d (upstream, 2021) added the fallback chain naming IMAGE and
kept the early return above it as a context line. The intent is read from the
chain; the early return is ambiguous, so the fix is a question for the stream.
--control drops the early return, to show the case can pass.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
fn = function(src, r"^const std::string GridGameListView::getImagePath\(FileData\* file\)", "3.31")
if "--control" in sys.argv:
    early = "\tif (src == ImageSource::IMAGE)\n\t\treturn file->getImagePath();\n"
    assert early in fn
    fn = fn.replace(early, "")
harness = r'''
#include <cstdio>
#include <map>
#include <string>
enum ImageSource { THUMBNAIL, IMAGE, MARQUEE, MARQUEEORTEXT, TITLESHOT, BOXART, FANART, CARTRIDGE, MIX };
enum class MetaDataId { TitleShot, BoxArt, FanArt, Cartridge, Mix };
struct FileData {
    std::string image, marquee, thumb; std::map<MetaDataId, std::string> md;
    std::string getImagePath() { return image; }
    std::string getMarqueePath() { return marquee; }
    std::string getThumbnailPath() { return thumb; }
    std::string getMetadata(MetaDataId id) { return md[id]; }
};
struct Grid { ImageSource s; ImageSource getImageSource() { return s; } };
struct GridGameListView { Grid mGrid; const std::string getImagePath(FileData* file); };
''' + fn.replace("ImageSource::", "") + r'''
int main() {
    int bad = 0;
    struct Case { const char* name; ImageSource src; FileData f; std::string want; };
    Case cases[] = {
        {"IMAGE, no image, a thumbnail", IMAGE, {"", "", "t.png", {}}, "t.png"},
        {"IMAGE, an image", IMAGE, {"i.png", "", "t.png", {}}, "i.png"},
        {"TITLESHOT, none, an image", TITLESHOT, {"i.png", "", "t.png", {}}, "i.png"},
        {"BOXART, none, a thumbnail", BOXART, {"", "", "t.png", {}}, "t.png"},
        {"MARQUEE, none, a thumbnail", MARQUEE, {"", "", "t.png", {}}, "t.png"},
    };
    for (auto& c : cases) {
        GridGameListView v; v.mGrid.s = c.src;
        std::string got = v.getImagePath(&c.f);
        printf("%-30s -> \"%s\"%s\n", c.name, got.c_str(), got == c.want ? "" : "   (want the fallback)");
        if (got != c.want) bad++;
    }
    if (bad) { printf("FAIL 3.31: the IMAGE source draws an empty tile for a game with a thumbnail and no image\n"); return 1; }
    return 0;
}
'''
run(harness, "l331")
