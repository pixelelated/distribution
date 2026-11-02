### Pins-read count correction — 2026-11-02

The § 10 `pins-read` row's "two PKG_PATCH_DIRS lines" is a specification
error. At accepted source `02aab33bd9842610b0d466c9c186454dc14373ee` and
handback `61a1a674c10d520f9d93748c5a73deaadb08b158`, the unchanged Linux
override has five anchored PKG_VERSION assignments (lines 23/30/37/43/49),
four anchored PKG_PATCH_DIRS assignments (16/27/40/46), and a separate
conditional assignment at line 18. All ten lines must be quoted literally
with their line numbers in 02, plus case-label context and the exact source
ref. Keep the distinction between the whole recipe read and T41's selected
pins: provenance rows still admit only `7.2`, `7.1.2`, `v2026.01`, `20260309`.
Other device branches are context, not new membership. The prior summary
does not satisfy this quotation requirement; append a records-only correction
and preserve every accepted source/program/receipt. No application, generator
control or whole-stage replay is required by this presentation correction.
