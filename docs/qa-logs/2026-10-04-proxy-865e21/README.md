# Pre-freeze proxy refresh — #426

New865e218660e9914e3ba0b4326b5d430af995c843 archive `97e9f4207852aefaff46a37a9f7256f77e79a638eb3b5fa4cb75ea06d174880e`.
The17-file upstream diff changes15 Android files and two unshipped Linux
bundle builders. Reviewed builder changes fail early on absent Python/pygame,
instead of emitting incomplete Onion/Allium bundles; both pass Bash syntax.
Our recipe invokes neither builder and installs its own native library/module.
All105 consumed Python/native files and268 Linux/native/test files excluding
those bundle scripts exactly match aec99c raw and patched sources. All15
fork patches apply at fuzz0. Storage schema bytes and coupled rcheevos/libchdr
pins are identical; the exact schema review comment now names the new pin.
Prior199 upstream/eight fork source test results trace to identical modules
and tests. This is byte equivalence, not new installed-image qualification.

The current1e6a image's offline preservation and synthetic HTTP subset retry
passed but remains historical. Build/source custody and installed regression
on the refreshed replacement remain required. Original image/source untouched.
