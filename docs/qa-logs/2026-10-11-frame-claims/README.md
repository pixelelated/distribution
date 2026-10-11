# Approved cloud changes in the image19 comparison — #544

The original 78-frame comparison against accepted baseline d72084ccad failed
on six unclaimed regions. Direct review attributes each to approved source:
#537 changes the cloud-management row and its subtitle; #538 changes RESET to
CLEAR in the keyboard and help bar. #527 already accounts for the added folder
validator row and focused-hub scrolling. Its prior frame confirms the same
partially clipped offscreen startup-status line; the selected row remains legible.

The corrected claims extend only the two existing hub regions and name the
four CLEAR glyph/help regions. No image baseline or mask changed. The original
report remains FAIL. A fresh comparison with the original claims fails on the
same six regions; the corrected comparison passes all78 with45 claimed regions,
0 unclaimed and0 missing screens. This is separate corrective evidence, not a
replacement original result. review.json binds current/baseline frames and actual
ES c8dc72cf9 source; all-frame-sha256.json identifies the complete compared set.

Approved EN/FR640/1280 behavior and callback proof remains in
[the editor record](../2026-10-11-network-cloud-management/editor/review.json).
Firmware source a0f60255ab and its product pin are unchanged. Device builds remain
behind the other image19 upgrade/installed/branch gates in #344.
