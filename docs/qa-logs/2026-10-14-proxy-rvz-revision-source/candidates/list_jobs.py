import json, os, re, sqlite3, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from raofflineproxy import cache_keys
from raofflineproxy.config import DATABASE_FILE, load_config
from raofflineproxy.rom_browser import (
    MAX_SCAN_ENTRIES, is_supported_browser_file, normalize_cached_rom_path,
)
from raofflineproxy.smart_cache import load_content_history_paths
from raofflineproxy.storage import Storage

out, mode, roms_root, es_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
walk_systems = sys.argv[5].split()
cursor_file = Path(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] else None
user = cache_keys.normalize_user(os.environ.get("RA_SCAN_USER", ""))
SKIP_DIRS = {
    "images", "videos", "manuals", "media", "downloaded_images", "downloaded_videos",
    "downloaded_manuals", "imgs", "savestates", "screenshots", "saves", "savefiles",
}
DISC_SHEETS = (".cue", ".gdi", ".m3u")


def es_systems():
    """(name, folder) per <system>, read as the interface reads them (#308
    F-RA-06): SystemData::getConfigPath takes the first of the user's
    es_systems_custom.cfg, the user's es_systems.cfg, the one beside the
    binary and the image's as the base -- a custom file is the whole base
    there too -- and loadAdditionnalConfig then merges every es_systems_*.cfg
    in the user's folder and beside the binary into it by name: a known
    system's tags replaced (a tag with no text dropped, <emulators> kept), a
    new one appended, and a file that does not parse ends the merging, as it
    does there."""
    root = None
    for cfg in (es_dir / "es_systems_custom.cfg", es_dir / "es_systems.cfg",
                Path("/usr/bin/es_systems.cfg"), Path("/etc/emulationstation/es_systems.cfg"),
                Path("/usr/config/emulationstation/es_systems.cfg")):
        if not cfg.is_file():
            continue
        try:
            root = ET.parse(cfg).getroot()
        except Exception:
            continue
        break
    if root is None:
        return []
    order, tags = [], {}
    for system in root.iter("system"):
        name = (system.findtext("name") or "").strip()
        if name and name not in tags:
            order.append(name)
            tags[name] = {child.tag: child.text or "" for child in system}
    merging = True
    for folder in dict.fromkeys((es_dir, Path("/usr/bin"))):
        if not merging:
            break
        try:
            extras = sorted(e for e in folder.iterdir() if e.name.startswith("es_systems_") and e.suffix == ".cfg")
        except OSError:
            continue
        for extra in extras:
            try:
                extra_root = ET.parse(extra).getroot()
            except Exception:
                merging = False
                break
            if extra_root.tag != "systemList":
                merging = False
                break
            for system in extra_root.findall("system"):
                name = (system.findtext("name") or "").strip()
                if not name:
                    continue
                if name not in tags:
                    order.append(name)
                    tags[name] = {child.tag: child.text or "" for child in system}
                    continue
                for child in system:
                    if child.tag == "name":
                        continue
                    tags[name].pop(child.tag, None)
                    if child.tag == "emulators" or (child.text or ""):
                        tags[name][child.tag] = child.text or ""
    found = []
    for name in order:
        folder = (tags[name].get("path") or "").strip()
        if folder:
            found.append((name, Path(os.path.expanduser(folder))))
    return found


def game_path(folder, text):
    text = text.strip()
    if text.startswith("./"):
        return folder / text[2:]
    if text.startswith("/"):
        return Path(text)
    return folder / text


def read_index(name, folder):
    """{path: (cheevosHash, cheevosId)} for one system, read as the
    interface reads it (Gamelist.cpp parseGamelist): gamelist.xml, then the
    recovery files over it. A recovery file is a game's whole metadata as the
    interface last had it, so its values replace the gamelist's -- but only
    while its parentHash names the gamelist it was written beside (the
    gamelist's size in bytes, 0 when there is none); one that names another
    is stale and skipped, as the interface skips it."""
    entries = {}

    def take(doc, parent=None):
        try:
            root = ET.parse(doc).getroot()
        except Exception:
            return
        if parent is not None:
            try:
                written_beside = int(root.get("parentHash", "0"))
            except ValueError:
                return
            if written_beside != parent:
                return
        for game in root.iter("game"):
            text = game.findtext("path") or ""
            if not text.strip():
                continue
            entries[game_path(folder, text)] = (
                (game.findtext("cheevosHash") or "").strip(),
                (game.findtext("cheevosId") or "").strip(),
            )

    gamelist = folder / "gamelist.xml"
    if not gamelist.is_file():
        gamelist = es_dir / "gamelists" / name / "gamelist.xml"
    size = 0
    if gamelist.is_file():
        try:
            size = gamelist.stat().st_size
        except OSError:
            size = 0
        take(gamelist)
    recovery = es_dir / "recovery" / name
    if recovery.is_dir():
        for dirpath, dirnames, filenames in os.walk(recovery):
            dirnames.sort()
            for fn in sorted(filenames):
                if fn.lower().endswith(".xml"):
                    take(Path(dirpath) / fn, parent=size)
    return entries


config = load_config()
storage = Storage()


def is_cached(game_id, hash_value):
    """Everything a launch reads, for this account and this dump."""
    return (
        storage.get_cache(cache_keys.patch(game_id, user)) is not None
        and storage.get_cache(cache_keys.unlocks(game_id, user)) is not None
        and storage.get_cache(cache_keys.achievementsets(hash_value, user)) is not None
    )


# The ROMs this account's patch rows name (rom_browser.load_cached_rom_paths,
# narrowed to the account), in the client's own two-component form -- where
# the game is ready for this account (whole_games: its unlocks row and an
# achievementsets row of the game), as is_cached asks of an indexed game. A patch row alone (a fetch that failed after the first write, or
# rows an older client's eviction thinned) used to pass the ROM over for
# ever; now it is a job again (#308 F-RA-14). The dump's own sets row cannot
# be asked here -- an unindexed ROM's hash is what the job finds out.
HEAD_VALUE = re.compile(r"\s*:\s*(\d+)\s*[,}]")
HEAD_COLON = re.compile(r"\s*:")
def head_game_id(head):
    depth, i, n = 0, 0, len(head)
    while i < n:
        c = head[i]
        if c == "\"":
            j = i + 1
            while j < n and head[j] != "\"":
                j += 2 if head[j] == "\\" else 1
            if j >= n:
                return None
            if depth == 1 and head[i + 1:j] == "GameId":
                whole = HEAD_VALUE.match(head, j + 1)
                if whole:
                    return int(whole.group(1))
                if HEAD_COLON.match(head, j + 1):
                    return None
            i = j + 1
            continue
        if c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
        i += 1
    return None


def whole_games():
    """The games ready for this account -- the unlocks row and an
    achievementsets row of the game, the rows a launch reads -- by the same
    rule as the shell's ready_games_into (audit of the fixes, claude G-D-08,
    gpt G-D-04). A sets row's GameId is read from its first 512 characters,
    where the service writes it, and from the whole body only when they do
    not hold it: every body parsed whole at every listing was tens of
    megabytes on a large store. The head answers only with the body's own
    key and a number that ends inside it (head_game_id above, the same text
    as in the shell's ready_games_into; audit of the fix round, gpt
    G2-D-01, claude G2-D-08)."""
    unlocks, sets = set(), set()
    try:
        db = sqlite3.connect("file:%s?mode=ro" % DATABASE_FILE, uri=True, timeout=1.0)
        rows = db.execute("SELECT cacheKey, substr(responseBody, 1, 512) FROM api_cache WHERE cacheKey LIKE ? OR cacheKey LIKE ?", ("unlocks:%", "achievementsets:%")).fetchall()
    except Exception:
        db = None
        rows = ((e.get("cacheKey") or "", e.get("responseBody") or "") for prefix in (cache_keys.PREFIX_UNLOCKS, cache_keys.PREFIX_ACHIEVEMENTSETS) for e in storage.iter_cache_by_prefix(prefix))
    for key, head in rows:
        parts = str(key).split(":")
        if parts[0] == "unlocks":
            if len(parts) == 4 and parts[2] == user and parts[3] == "0" and parts[1].isdigit():
                unlocks.add(int(parts[1]))
            continue
        if len(parts) != 3 or parts[2] != user:
            continue
        gid = head_game_id((head or "")[:512])
        if gid is None:
            try:
                body = db.execute("SELECT responseBody FROM api_cache WHERE cacheKey = ?", (key,)).fetchone()[0] if db is not None else head
                gid = int((json.loads(body) or {}).get("GameId") or 0)
            except Exception:
                gid = 0
        if gid > 0:
            sets.add(gid)
    if db is not None:
        db.close()
    return unlocks & sets


whole = whole_games()
cached_paths = {
    normalize_cached_rom_path(entry["sourceRomPath"])
    for entry in storage.cache_summaries_by_prefix(cache_keys.PREFIX_PATCH)
    if isinstance(entry.get("sourceRomPath"), str) and entry["sourceRomPath"].strip()
    and entry["cacheKey"].endswith(":" + user)
    and cache_keys.parse_game_id_from_patch_key(entry["cacheKey"]) in whole
}
try:
    history = [str(p) for p in load_content_history_paths(config)]
except Exception:
    history = []


def mtime(p):
    try:
        return p.stat().st_mtime
    except OSError:
        return 0.0


def by_history(paths):
    """The played ones first, most recent first; then the rest, newest first."""
    order = {p: i for i, p in enumerate(history)}
    played = sorted((p for p in paths if str(p) in order), key=lambda p: order[str(p)])
    rest = sorted((p for p in paths if str(p) not in order), key=mtime, reverse=True)
    return played + rest


indexed_dirs = set()
failed_rvz_paths = set()
indexed_seen = 0
indexed_jobs = {}
for name, folder in es_systems():
    if not folder.is_dir():
        continue
    index = read_index(name, folder)
    if not any(h for h, _ in index.values()):
        continue
    try:
        indexed_dirs.add(folder.resolve())
    except OSError:
        indexed_dirs.add(folder)
    for path, (hash_value, id_text) in index.items():
        # ES uses this sentinel for a failed read, not an unmatched hash.
        # A deliberate scan may try the proxy's independent RVZ reader.
        # Keep valid unmatched hashes and automatic top-ups index-only.
        if path.suffix.lower() == ".rvz" and hash_value == "0" * 32:
            failed_rvz_paths.add(path)
            continue
        try:
            game_id = int(id_text)
        except ValueError:
            game_id = 0
        if game_id <= 0 or not hash_value or not path.is_file():
            continue
        indexed_seen += 1
        if path in indexed_jobs or is_cached(game_id, hash_value):
            continue
        indexed_jobs[path] = (game_id, hash_value)
storage.close()

def read_cursor():
    try:
        return cursor_file.read_text(encoding="utf-8", errors="surrogateescape").rstrip("\n") if cursor_file else ""
    except OSError:
        return ""


def propose_cursor(value):
    """The cursor this walk proposes -- the path of the last file it took,
    or nothing when the walk came round -- written whole to
    scan-cursor.next for the ctl to keep once the run has worked through its
    jobs (commit_cursor): a run cancelled or stopped after its listing
    leaves the cursor where it was, so the next scan takes the same slice
    (audit of the fixes, claude G-D-06). False when it could not be written
    -- and the ctl says so rather than promising a continuation it cannot
    keep (gpt G-D-06)."""
    if cursor_file is None:
        return True
    proposal = cursor_file.with_name(cursor_file.name + ".next")
    tmp = proposal.with_name(proposal.name + ".tmp")
    try:
        tmp.write_text(value + "\n" if value else "", encoding="utf-8", errors="surrogateescape")
        os.replace(tmp, proposal)
        return True
    except OSError:
        try:
            tmp.unlink()
        except OSError:
            pass
        return False


# The walk is a circle from a cursor (#307 PL-059). Cached files are passed
# over before the cap counts (#186 PL-17), but a file that never caches -- a
# ROM RetroAchievements does not know is skipped, and stays uncached --
# counted every run, so the first MAX_SCAN_ENTRIES such files held the front
# of the walk for ever and the files past them were never reached. So a walk
# the cap cuts proposes the path of the last file it took (scan-cursor.next),
# the ctl keeps it as scan-cursor once the run has worked through its jobs,
# and the next walk takes the files after it first, then comes round to the
# start. A walk that fits under the cap removes the cursor; a cursor that
# names a file the walk no longer meets (deleted, or its folder now indexed)
# starts the circle from the top.
walked = []
walked_cached = 0
truncated = 0
cursor_saved = 1
if mode == "all":
    cursor = read_cursor()
    passed = not cursor
    before, after = [], []   # the candidates up to the cursor, and past it
    full = False
    for name in walk_systems:
        root = roms_root / name
        if not root.is_dir():
            continue
        try:
            indexed_root = root.resolve() in indexed_dirs
        except OSError:
            indexed_root = root in indexed_dirs
        # Only revisit a root that can actually contain one of the failed
        # paths; use the same path form as the membership check in the walk.
        if indexed_root and not any(path.is_relative_to(root) for path in failed_rvz_paths):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d.lower() not in SKIP_DIRS)
            has_sheet = any(f.lower().endswith(DISC_SHEETS) for f in filenames)
            for fn in sorted(filenames):
                if fn.startswith("."):
                    continue
                path = Path(dirpath) / fn
                if indexed_root and path not in failed_rvz_paths:
                    continue
                at_cursor = not passed and str(path) == cursor
                # Before the cursor only the first cap's worth is ever
                # taken (the circle's tail), so past that the walk only
                # looks for the cursor.
                if not passed and len(before) > MAX_SCAN_ENTRIES:
                    passed = passed or at_cursor
                    continue
                take = False
                if is_supported_browser_file(path) and not (has_sheet and fn.lower().endswith(".bin")):
                    try:
                        take = path.is_file() and path.stat().st_size > 0
                    except OSError:
                        take = False
                if take and normalize_cached_rom_path(path) in cached_paths:
                    walked_cached += 1
                    take = False
                if take:
                    (after if passed else before).append(path)
                passed = passed or at_cursor
                if len(after) > MAX_SCAN_ENTRIES:
                    full = True
                    break
            if full:
                break
        if full:
            break
    candidates = after + before
    walked = candidates[:MAX_SCAN_ENTRIES]
    truncated = 1 if len(candidates) > MAX_SCAN_ENTRIES else 0
    cursor_saved = 1 if propose_cursor(str(walked[-1]) if truncated and walked else "") else 0

hash_jobs = walked

lines = [f"I\t{indexed_jobs[p][0]}\t{indexed_jobs[p][1]}\t{p}\n" for p in by_history(list(indexed_jobs))]
lines += [f"H\t\t\t{p}\n" for p in by_history(hash_jobs)]
out.write_text("".join(lines), encoding="utf-8")
found = indexed_seen + len(walked) + walked_cached
new = len(lines)
print(f"found={found} new={new} cached={found - new} indexed={len(indexed_jobs)} hashing={len(hash_jobs)} truncated={truncated} cursor_saved={cursor_saved}")
