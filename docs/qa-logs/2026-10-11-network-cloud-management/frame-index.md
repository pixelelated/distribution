# Reviewed UI flow index

All links below are actual reviewed VM frames, bound by `frame-index.json` to the frozen source, ES binary and runtime French catalog. EN/FR at 640×480 and 1280×800, positive 60 Hz refresh. Synthetic provider/radio fixtures; no owner data.

| Flow | Expected state | EN 640 | FR 640 | EN 1280 | FR 1280 |
| --- | --- | --- | --- | --- | --- |
| NC01 | Saved connections and active selection | [Frame](connections/en640/lifecycle/03-connections.png) | [Frame](connections/fr640/lifecycle/03-connections.png) | [Frame](connections/en1280/lifecycle/03-connections.png) | [Frame](connections/fr1280/lifecycle/03-connections.png) |
| NC02 | Connection actions | [Frame](connections/en640/lifecycle/04-details.png) | [Frame](connections/fr640/lifecycle/04-details.png) | [Frame](connections/en1280/lifecycle/04-details.png) | [Frame](connections/fr1280/lifecycle/04-details.png) |
| NC03 | Switch with explicit folder warning | [Frame](connections/en640/lifecycle/05-use-confirm.png) | [Frame](connections/fr640/lifecycle/05-use-confirm.png) | [Frame](connections/en1280/lifecycle/05-use-confirm.png) | [Frame](connections/fr1280/lifecycle/05-use-confirm.png) |
| NC04 | Local removal confirmation | [Frame](connections/en640/lifecycle/07-remove-confirm.png) | [Frame](connections/fr640/lifecycle/07-remove-confirm.png) | [Frame](connections/en1280/lifecycle/07-remove-confirm.png) | [Frame](connections/fr1280/lifecycle/07-remove-confirm.png) |
| NC05 | Removed active connection leaves no selection | [Frame](connections/en640/lifecycle/09-removed-unselected.png) | [Frame](connections/fr640/lifecycle/09-removed-unselected.png) | [Frame](connections/en1280/lifecycle/09-removed-unselected.png) | [Frame](connections/fr1280/lifecycle/09-removed-unselected.png) |
| NC06 | Edit keeps blank fields | [Frame](connections/en640/edit/02-edit-form.png) | [Frame](connections/fr640/edit/02-edit-form.png) | [Frame](connections/en1280/edit/02-edit-form.png) | [Frame](connections/fr1280/edit/02-edit-form.png) |
| NC07 | Edit replacement confirmation | [Frame](connections/en640/edit/03-edit-confirm.png) | [Frame](connections/fr640/edit/03-edit-confirm.png) | [Frame](connections/en1280/edit/03-edit-confirm.png) | [Frame](connections/fr1280/edit/03-edit-confirm.png) |
| NC08 | Saved edit does not switch selection | [Frame](connections/en640/saved/01-edited-connection-saved.png) | [Frame](connections/fr640/saved/01-edited-connection-saved.png) | [Frame](connections/en1280/saved/01-edited-connection-saved.png) | [Frame](connections/fr1280/saved/01-edited-connection-saved.png) |
| NC09 | Add a separate named connection | [Frame](connections/en640/add-name/05-separate-name.png) | [Frame](connections/fr640/add-name/05-separate-name.png) | [Frame](connections/en1280/add-name/05-separate-name.png) | [Frame](connections/fr1280/add-name/05-separate-name.png) |
| NC10 | Renew existing account | [Frame](pairing/en640/start/03-renew-confirm.png) | [Frame](pairing/fr640/start/03-renew-confirm.png) | [Frame](pairing/en1280/start/03-renew-confirm.png) | [Frame](pairing/fr1280/start/03-renew-confirm.png) |
| NC11 | Failed pairing offers real retry/cancel | [Frame](pairing/en640/failed/02-pairing-failed.png) | [Frame](pairing/fr640/failed/02-pairing-failed.png) | [Frame](pairing/en1280/failed/02-pairing-failed.png) | [Frame](pairing/fr1280/failed/02-pairing-failed.png) |
| NC12 | Cancel returns with saved account intact | [Frame](pairing/en640/cancelled/01-cancelled-return.png) | [Frame](pairing/fr640/cancelled/01-cancelled-return.png) | [Frame](pairing/en1280/cancelled/01-cancelled-return.png) | [Frame](pairing/fr1280/cancelled/01-cancelled-return.png) |
| WF01 | Open network joins without key prompt | [Frame](wifi/en640/full-happy/open-connected/01-open-connected.png) | [Frame](wifi/fr640/full-happy/open-connected/01-open-connected.png) | [Frame](wifi/en1280/full-happy/open-connected/01-open-connected.png) | [Frame](wifi/fr1280/full-happy/open-connected/01-open-connected.png) |
| WF02 | Unknown security still prompts | [Frame](wifi/en640/full-happy/unknown-password/01-unknown-password.png) | [Frame](wifi/fr640/full-happy/unknown-password/01-unknown-password.png) | [Frame](wifi/en1280/full-happy/unknown-password/01-unknown-password.png) | [Frame](wifi/fr1280/full-happy/unknown-password/01-unknown-password.png) |
| WF03 | Saved network actions | [Frame](wifi/en640/full-happy/saved-choice/01-saved-choice.png) | [Frame](wifi/fr640/full-happy/saved-choice/01-saved-choice.png) | [Frame](wifi/en1280/full-happy/saved-choice/01-saved-choice.png) | [Frame](wifi/fr1280/full-happy/saved-choice/01-saved-choice.png) |
| WF04 | Forget targets saved profile name | [Frame](wifi/en640/full-happy/forget-confirm/01-forget-confirm.png) | [Frame](wifi/fr640/full-happy/forget-confirm/01-forget-confirm.png) | [Frame](wifi/en1280/full-happy/forget-confirm/01-forget-confirm.png) | [Frame](wifi/fr1280/full-happy/forget-confirm/01-forget-confirm.png) |
| WF05 | Open network connection failure | [Frame](wifi/en640/failed/open-failed/01-open-failed.png) | [Frame](wifi/fr640/failed/open-failed/01-open-failed.png) | [Frame](wifi/en1280/failed/open-failed/01-open-failed.png) | [Frame](wifi/fr1280/failed/open-failed/01-open-failed.png) |
| WF06 | Protected network failure | [Frame](wifi/en640/failed/protected-failed/01-protected-failed.png) | [Frame](wifi/fr640/failed/protected-failed/01-protected-failed.png) | [Frame](wifi/en1280/failed/protected-failed/01-protected-failed.png) | [Frame](wifi/fr1280/failed/protected-failed/01-protected-failed.png) |
| WF07 | Multiple profiles require a choice | [Frame](wifi/en640/multiple-profiles/profiles/01-profiles.png) | [Frame](wifi/fr640/multiple-profiles/profiles/01-profiles.png) | [Frame](wifi/en1280/multiple-profiles/profiles/01-profiles.png) | [Frame](wifi/fr1280/multiple-profiles/profiles/01-profiles.png) |

Runtime receipts beside each cohort verify unchanged folder paths/test payload, explicit unselected state, blank-field preservation, fresh sign-in attempt/session/PIN, stopped authorization child and unchanged credentials after cancellation. Wi-Fi fixtures assert saved-profile selection and protected/open behavior; they do not claim physical radio validation.

The shared editor has eight separately reviewed EN/FR, small/large, keyboard/OSK cases in [editor/review.json](editor/review.json). The actual WebKit provider fixture has sixteen controls in [browser/result.json](browser/result.json), including ordered input, protected editing/provider key handling, browser Back, popup/opener and Close. Rejected original frames and original failing controls remain separate.

## Audit repair supplement — final build54 / matrix55

These 16 reviewed frames are bound separately by [repair-frame-index.json](repair-frame-index.json) and the schema1 index to final repaired source, binary and French catalog. The original frames above retain their original identity. Twelve walks completed at positive 60 Hz.

| Flow | Expected state | EN 640 | FR 640 | EN 1280 | FR 1280 |
| --- | --- | --- | --- | --- | --- |
| NC13 | The connection answers; its complete name is retained | [Frame](repair54/en640/NC13.png) | [Frame](repair54/fr640/NC13.png) | [Frame](repair54/en1280/NC13.png) | [Frame](repair54/fr1280/NC13.png) |
| NC14 | The refusal explains choosing another connection; prior settings are preserved | [Frame](repair54/en640/NC14.png) | [Frame](repair54/fr640/NC14.png) | [Frame](repair54/en1280/NC14.png) | [Frame](repair54/fr1280/NC14.png) |
| NC15 | No connection in use; choose a connection before cloud tools | [Frame](repair54/en640/NC15.png) | [Frame](repair54/fr640/NC15.png) | [Frame](repair54/en1280/NC15.png) | [Frame](repair54/fr1280/NC15.png) |
| NC16 | Explicitly choose a connection under CLOUD CONNECTIONS; both buttons remain visible | [Frame](repair54/en640/NC16.png) | [Frame](repair54/fr640/NC16.png) | [Frame](repair54/en1280/NC16.png) | [Frame](repair54/fr1280/NC16.png) |

On small panels, inherited long terminal-instruction suffixes still elide; the repaired selection direction and both final-page buttons are readable. This supplement does not claim to redesign every terminal instruction.
