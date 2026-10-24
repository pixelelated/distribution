# Q4 (b): the three recipes classed by hand (2026-10-24 ~03:15 UTC)

`tools/q4-pins.py` covers the 148 `github.com` recipes. Its run of 2026-10-24 (03:06 to 03:11 UTC, then from its cache after two fixes) wrote `q4-pins.json` and `q4-pins-table.md`: 151 rows, `current` 39, `behind-project` 102, `behind-upstream` 1, `pin-not-on-project` 6, and 3 `by-hand`, with rc 0 and no empty cell. The three by-hand rows are resolved here, each with its host's public API. **These classes replace `by-hand` in `04` § Q4 (b).**

| Recipe | Pin | Pin date | Project head | Days | Class | How it was read |
| --- | --- | --- | --- | ---: | --- | --- |
| `libxmp-lite` (an `easyrpg-lr` sub-recipe, fork-own) | `4.5.0` (a SourceForge release tarball) | libxmp 4.5.0, tag `libxmp-4.5.0` (`a9701bd6aa`) | `libxmp-4.7.4`, 2026-10-10 (the project releases on GitHub now: `gh api repos/libxmp/libxmp/releases?per_page=5` lists 4.7.4, 4.7.3, 4.7.2, 4.7.1, 4.7.0) | (releases, not commits) | **behind-project** | `gh api repos/libxmp/libxmp/releases`; `PKG_SITE` is `http://sourceforge.net/projects/xmp` |
| `emuscv-lr` | `dfce10df09` | 2022-10-18 | `33900ce24f`, 2026-10-14; `compare?from=<pin>&to=master` lists 54 commits | 1,457 | **behind-project** | GitLab API `projects/16943127`. The recipe's path `MaaaX-EmuSCV/libretro-emuscv` answers **301**: the project is now `MaaaX-EPOCH84/libretro-emuscv`, so `PKG_SITE` names a moved project (Q7) |
| `idtech-lr` (fork-own) | `1.0`, with `PKG_URL` at `ROCKNIX/packages` commit `4cb65b687c` (`doom.tar.gz`) | 2024-04-19 | the repository's head is `691f24bceb` (2026-09-10), but `commits?path=doom.tar.gz` names only `4cb65b687c` | 0 for the file | **current** (the file has not changed since its pin) | `gh api repos/ROCKNIX/packages/...` |

API facts the scan recorded for other rows, carried into `04`:

- `fbalpha2019-lr`'s `PKG_SITE` repository answers as **`libretro/beetle-finalarcade2019`**, a rename.
- `mu-lr`'s answers as **`SquirrelJME/Mu`**, a move.
- **`mupen64plus-lr`'s repository is archived** (the pin is its head, so the class is `current`, and the project is read-only).
