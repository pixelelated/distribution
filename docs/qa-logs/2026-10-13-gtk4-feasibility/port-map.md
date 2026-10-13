**Source-port map — current cloud-signin-window.c at4a1274ab806b**

Line references name
`projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c`.
The input manifest binds its bytes. The most recent change to that file is
`bc2dceb406969a401d987de168acfb3ae60b7e01`; no product source was edited here.

| Current source | GTK4/WebKit6 direction | Behavior that must survive |
| --- | --- | --- |
| Includes, lines25–27 | `gtk/gtk.h` and `webkit/webkit.h`; link `gtk4 webkitgtk-6.0` | Exact2.54.1 engine, libsoup3, libatomic |
| `osk_type`,133–155 | No public direct replacement for fabricated GDK events | Native key/input semantics, focused field, press/release, modifiers, printable ASCII, deletion, Enter, and Tab |
| OSK build/highlight,261–330 | `gtk_widget_add/remove_css_class`, `gtk_box_append`, explicit expand/alignment, `gtk_widget_set_focusable(FALSE)` | Buttons remain clickable but never steal WebView focus; same grid and labels |
| Spinner,344–372 | `gtk_drawing_area_set_draw_func`; callback receives width/height, returns void | Same visible progress drawing and timing, independent of icon loaders |
| Key handler,531–653 | `GtkEventControllerKey` with deliberate propagation phase; keyval/keycode/state arguments | Escape, pad navigation, A/B/X/Y, scrolling, normal phone keys, and focus |
| CSS,1007–1012 | Provider for `GdkDisplay`; GTK4 CSS API signature | Native640×480 and1280×800 readability, selected key, focus |
| Packing,984–1048 | `gtk_window_set_child`, `gtk_revealer_set_child`, box append; stack expands vertically | Page shrinks for OSK, hints stay visible, spinner/page/popup selection remains correct |
| Main loop,951–1051 | `gtk_init()`; `GApplication` or owned `GMainLoop`; close-request/window destroy ownership | Escape/close/pad exit, broker liveness, no orphan processes |
| Ephemeral construction,960–966 | `webkit_network_session_new_ephemeral()` and WebView `network-session` construct property | No default persistent session; fresh setup starts clean |
| Popup,864–915 | `g_object_new(WEBKIT_TYPE_WEB_VIEW, "related-view", parent, "settings", settings, NULL)` | Opener, same context/session, one popup, return/focus/probe state |
| Popup removal,878 | `gtk_stack_remove()`; retain references only as long as needed | Parent selected before removing popup; no stale pointer or timer target |

GTK's [migration guide](https://docs.gtk.org/gtk4/migrating-3to4.html) covers the
container, drawing, event-controller, and main-loop changes. The public/private
GTK4.24.1 header excerpts in `research/upstream-evidence.json` show the keyboard
gap: `GdkEvent` is opaque publicly; `gdk_key_event_new` is in a private header.
The old path fills `event->key`, calls `gtk_main_do_event`, then frees it.
Event-controller forwarding forwards an existing event; it cannot turn a pad
Return into an arbitrary selected letter. Emitting a controller signal is not
native WebKit input. Do not vendor GTK private event structures or symbols.

The recommended keyboard spike uses the already established native input route
as its starting point. `cloud_oauth`'s `RemoteKeyboard` (1465–1568) owns a uinput
device and deliberately separates press/release and modifiers. The GTK4 OSK
would need a narrow, locally owned channel to a keyboard producer, with pad
control events distinguished from generated page keys. Simply sending Return
back through uinput while the OSK is open can re-enter OSK activation; Backspace
can hide it instead of deleting. This is a protocol/ordering problem to solve,
not a `gtk_box_append` problem. Phone/pad/OSK messages must share ordering and
session ownership, with bounded queueing, cancellation, and no secret logging.
No new network listener or page-to-native privileged bridge is proposed.

An alternative custom input-method context could commit text, but does not by
itself establish Enter/Tab/Backspace or provider keydown semantics. DOM value
assignment and synthetic JavaScript KeyboardEvents are not accepted substitutes
for the current native route. The first experiment must show actual native input
events and provider-style validation on a synthetic form before that design is
chosen. No keyboard implementation is claimed in this packet.

Lifecycle needs explicit attention, even if the initial diagnostic process is
short lived. Track/remove the60ms spinner and500ms probe sources before their
widgets or state are freed. Cancel or safely discard asynchronous replies on
close, page switch, and popup removal. Preserve the existing `on_probe` source
identity check (line390), which ignores replies from the covered parent. A
future `GApplication` lifetime must not reuse the existing function-static
`probing` flag across a new sign-in and silently omit its timer. Test closing
while evaluation is outstanding; do not treat process exit as a proof that a
different GTK4 destruction order is safe.

WebKit's exact2.54.1 [migration source](https://github.com/WebKit/WebKit/blob/webkitgtk-2.54.1/Source/WebKit/gtk/migrating-to-webkitgtk-6.0.md)
documents the new construction/session APIs. `WebKitWebView.cpp:935–1002`
establishes a specific trap: when `related-view` is supplied, context and network
session are inherited; explicitly supplying either alongside it logs a critical
and ignores that supplied value. Without a related view or explicit session,
the default persistent session is selected. `api-smoke.c` captures the correct
parent/related construction and pointer/ephemeral assertions, but has not been
compiled or run. It proves neither storage disposal nor actual popup navigation.

Preserve the current security behavior precisely:

- `host_permitted` (36–59) permits localhost/127.0.0.1, the configured host and
  dot-separated subdomains, plus four exact identity-provider hosts for Dropbox.
  A similar suffix such as `dropbox.com.example.invalid` must not match.
- `on_decide_policy` (793–862) filters HTTP(S) navigation **with a user gesture**.
  It deliberately does not use frame-name as a main-frame test; an unnamed
  iframe also reportsNULL. Resources, non-gesture navigation, and nonnetwork
  schemes are not comprehensively blocked. Preserve this policy; do not describe
  it as a network firewall or silently tighten it until captcha/subframe flows
  fail. The launch URL and omitted-host behavior are not newly validated here.
- `on_auth_create` (893–915) permits an allowed HTTP(S) host or gesture-created
  `about:blank`, refuses another popup while one exists, and keeps the related
  view. Parent and popup retain the navigation policy. Nested popup support is
  not newly introduced.
- `page_worth_recording` (663–676) suppresses localhost/127.0.0.1 callback URLs,
  which may contain OAuth credentials. Preserve page/field/done-file protocol,
  page-transition field invalidation, ownership, and EN/FR finishing behavior.
  Synthetic callback tests must assert no callback code appears in the page file,
  not just that a redirect occurred. The current policy allows loopback hosts
  without enforcing a callback port/path; do not claim stronger restrictions.
- Keep normal TLS validation, settings, related-session cookies, and actual
  callback handling. Do not add certificate exceptions, persistent profile
  fallback, unrestricted popups, debug keystroke logging, or auth-state replay.

The existing `CLOUD_SIGNIN_DEBUG` handler logs keys; it is unsuitable for real
credentials. New diagnostics should report timing/counts only. This assignment
used no account or authentication input. It changes no proxy/award lifecycle.
