/* SPDX-License-Identifier: GPL-2.0
 * Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
 * #576: compile/link fixture, then coordinator-owned disposable VM API probe.
 * NOT a sign-in-window port, renderer benchmark, or functional acceptance.
 * Opens no page and receives no account data. Requires a display if executed.
 */
#include <gtk/gtk.h>
#include <webkit/webkit.h>

int main(void)
{
    gtk_init();
    WebKitNetworkSession *session = webkit_network_session_new_ephemeral();
    GtkWidget *parent = g_object_ref_sink(g_object_new(WEBKIT_TYPE_WEB_VIEW,
        "network-session", session, NULL));
    /* A related view inherits its context and network session. Passing a
     * second network-session here is explicitly rejected by WebKit2.54.1. */
    GtkWidget *popup = g_object_ref_sink(g_object_new(WEBKIT_TYPE_WEB_VIEW,
        "related-view", parent,
        "settings", webkit_web_view_get_settings(WEBKIT_WEB_VIEW(parent)), NULL));

    WebKitNetworkSession *parent_session =
        webkit_web_view_get_network_session(WEBKIT_WEB_VIEW(parent));
    WebKitNetworkSession *popup_session =
        webkit_web_view_get_network_session(WEBKIT_WEB_VIEW(popup));
    gboolean valid = parent_session == session && popup_session == session &&
        webkit_network_session_is_ephemeral(parent_session) &&
        webkit_network_session_is_ephemeral(popup_session);
    g_object_unref(popup);
    g_object_unref(parent);
    g_object_unref(session);
    g_print("%s: ephemeral related-view construction only\n", valid ? "PASS" : "FAIL");
    return valid ? 0 : 1;
}
