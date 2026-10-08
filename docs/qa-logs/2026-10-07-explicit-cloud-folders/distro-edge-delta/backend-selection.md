# Current content-directory controls — read-only inventory

The current backend has a single independent `CONTENT_REMOTE` root on the first
configured rclone remote. It does not have separate per-system provider paths or
independent ROM/BIOS roots.

- `cloud_setup --set-content-remote` changes only `CONTENT_REMOTE`, without moving
  files or changing saves/settings pointers. It accepts top-level or deeper names,
  spaces, apostrophes, and dots within names. It normalizes leading/trailing slashes
  and rejects empty/root, shell/control characters, repeated inner separators, and
  dot/traversal components. It does not require the chosen folder to exist.
- `--use-content-root` stores an empty value explicitly, selecting the provider root.
- `--set-saves-remote` selects all three sibling paths, including `CONTENT_REMOTE`,
  so subsequently using that general setter replaces an earlier independent content
  choice. The content-only setter does not replace saves/settings choices.
- Content backup writes `<CONTENT_REMOTE>/ROMs/<system>` and
  `<CONTENT_REMOTE>/BIOS`. These child names are fixed. Choosing a folder that
  directly contains system directories does not make backup write that flat shape.
- Restore reads the configured tiered shape, a flat `<CONTENT_REMOTE>/<system>`
  shape, and a legacy provider-root fallback for recognized local directories.
  Therefore a selected content root is not presently an exclusive read boundary.
- `--set-systems` stores system directory names, not cloud paths. BIOS joins the
  ROMs-and-BIOS selection when present. Partial local libraries do not instruct the
  ordinary backup to delete cloud-only systems.

Source locations at the delta: `cloud_setup` lines757,787,833;
`cloud_content_backup` root construction204 and `remote_for`466;
`cloud_content_restore` root construction241, `remote_for`404, `resolve_src`428,
and `--set-systems`1374. This describes current mechanics only. It does not decide
the held product-flow question or add a new migration/tidying feature.

The remaining `cloud_backup:1454` warning tells players to use TIDY UP YOUR CLOUD
FOLDERS for nested settings/content. That guidance remains a held #510 issue;
it was not removed by this delta and may affect public ROCKNIX adoption.
