/* SPDX-License-Identifier: GPL-2.0-only
 * Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
 * Diagnostic #576: synthetic content and native-input API spike, UNCOMPILED.
 * This is not the product sign-in window. No provider/account navigation.
 */
#include <gtk/gtk.h>
#include <webkit/webkit.h>
#include <glib-unix.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

static GMainLoop *loop;
static GtkWidget *stack, *window;
static WebKitWebView *parent, *active, *popup;
static int channel = -1;
static guint ack_watch, ack_deadline;
static gboolean pending;
static int failure;

static void stop(void)
{
    g_main_loop_quit(loop);
}
static gboolean on_close(GtkWindow *win, gpointer ignored)
{
    (void)win; (void)ignored;
    stop();
    return TRUE;
}
static gboolean deadline(gpointer ignored)
{
    (void)ignored;
    ack_deadline = 0;
    failure = 2;
    g_printerr("FAIL native input acknowledgement timeout\n");
    stop();
    return G_SOURCE_REMOVE;
}
static gboolean on_ack(gint fd, GIOCondition condition, gpointer ignored)
{
    (void)ignored;
    unsigned char response;
    if ((condition & (G_IO_HUP | G_IO_ERR)) || recv(fd, &response, 1, 0) != 1 || response != 1) {
        failure = 2;
        ack_watch = 0;
        g_printerr("FAIL native input channel closed or rejected\n");
        stop();
        return G_SOURCE_REMOVE;
    }
    pending = FALSE;
    if (ack_deadline) { g_source_remove(ack_deadline); ack_deadline = 0; }
    return G_SOURCE_CONTINUE;
}
static void request_key(guint keyval)
{
    /* One bounded in-flight request. Diagnostic input must await its receipt.
     * A production keyboard requires a reviewed bounded queue and busy UI. */
    if (pending) { g_printerr("BUSY native input request\n"); return; }
    uint32_t packet = htonl(keyval);
    if (send(channel, &packet, sizeof packet, MSG_DONTWAIT | MSG_NOSIGNAL) != sizeof packet) {
        failure = 2; stop(); return;
    }
    pending = TRUE;
    ack_deadline = g_timeout_add_seconds(2, deadline, NULL);
}
static void on_button(GtkButton *button, gpointer data)
{
    (void)button;
    gtk_widget_grab_focus(GTK_WIDGET(active));
    request_key(GPOINTER_TO_UINT(data));
}
static gboolean on_key(GtkEventControllerKey *controller, guint keyval,
                       guint keycode, GdkModifierType state, gpointer ignored)
{
    (void)controller; (void)keycode; (void)state; (void)ignored;
    if (keyval == GDK_KEY_Escape) { stop(); return TRUE; }
    /* Proposed control namespace: the real pad producer must use these.
     * Regular Return/Backspace/Tab are never interpreted as OSK commands. */
    switch (keyval) {
    case GDK_KEY_F13: request_key(GDK_KEY_a); return TRUE;
    case GDK_KEY_F14: request_key(GDK_KEY_A); return TRUE;
    case GDK_KEY_F15: request_key(GDK_KEY_BackSpace); return TRUE;
    case GDK_KEY_F16: request_key(GDK_KEY_Tab); return TRUE;
    case GDK_KEY_F17: request_key(GDK_KEY_Return); return TRUE;
    default: return FALSE;
    }
}
static gboolean policy(WebKitWebView *view, WebKitPolicyDecision *decision,
                       WebKitPolicyDecisionType type, gpointer ignored)
{
    (void)view; (void)ignored;
    if (type != WEBKIT_POLICY_DECISION_TYPE_NAVIGATION_ACTION &&
        type != WEBKIT_POLICY_DECISION_TYPE_NEW_WINDOW_ACTION) return FALSE;
    WebKitNavigationAction *action = webkit_navigation_policy_decision_get_navigation_action(
        WEBKIT_NAVIGATION_POLICY_DECISION(decision));
    const char *uri = webkit_uri_request_get_uri(webkit_navigation_action_get_request(action));
    if (g_strcmp0(uri, "about:blank") != 0) {
        webkit_policy_decision_ignore(decision);
        g_print("navigation refused by synthetic-only fixture\n");
        return TRUE;
    }
    return FALSE;
}
static void popup_close(WebKitWebView *view, gpointer ignored)
{
    (void)ignored;
    active = parent;
    gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(parent));
    gtk_widget_grab_focus(GTK_WIDGET(parent));
    gtk_stack_remove(GTK_STACK(stack), GTK_WIDGET(view));
    popup = NULL;
}
static void popup_ready(WebKitWebView *view, gpointer ignored)
{
    (void)ignored;
    active = view;
    gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(view));
    gtk_widget_grab_focus(GTK_WIDGET(view));
}
static GtkWidget *popup_create(WebKitWebView *view, WebKitNavigationAction *action, gpointer ignored)
{
    (void)ignored;
    const char *uri = webkit_uri_request_get_uri(webkit_navigation_action_get_request(action));
    if (popup || g_strcmp0(uri, "about:blank") || !webkit_navigation_action_is_user_gesture(action)) return NULL;
    popup = WEBKIT_WEB_VIEW(g_object_new(WEBKIT_TYPE_WEB_VIEW,
        "related-view", view, "settings", webkit_web_view_get_settings(view), NULL));
    WebKitNetworkSession *session = webkit_web_view_get_network_session(view);
    if (webkit_web_view_get_network_session(popup) != session || !webkit_network_session_is_ephemeral(session)) {
        g_object_ref_sink(popup); g_object_unref(popup); popup = NULL;
        failure = 2; stop(); return NULL;
    }
    g_signal_connect(popup, "decide-policy", G_CALLBACK(policy), NULL);
    g_signal_connect(popup, "ready-to-show", G_CALLBACK(popup_ready), NULL);
    g_signal_connect(popup, "close", G_CALLBACK(popup_close), NULL);
    gtk_stack_add_named(GTK_STACK(stack), GTK_WIDGET(popup), "popup");
    return GTK_WIDGET(popup);
}
static void realized(GtkWidget *widget, gpointer ignored)
{
    (void)ignored;
    GskRenderer *renderer = gtk_native_get_renderer(GTK_NATIVE(widget));
    g_print("realized GSK renderer: %s\n", renderer ? G_OBJECT_TYPE_NAME(renderer) : "absent");
}
static const char fixture[] =
    "<!doctype html><meta charset=utf-8><title>GTK4 native input fixture</title>"
    "<style>body{font:20px sans-serif}input,button{font:inherit}</style>"
    "<p>Synthetic input only. F13 a; F14 A; F15 delete; F16 Tab; F17 Enter.</p>"
    "<form onsubmit='event.preventDefault();document.querySelector(\"output\").textContent=\"submitted locally\"'>"
    "<input aria-label=first autofocus><input aria-label=second><button>Submit locally</button></form>"
    "<button onclick=\"let p=window.open('about:blank');if(p)p.document.write('<input autofocus><button onclick=window.close()>Close popup</button>')\">Related popup</button>"
    "<p>Trusted keydown/input events: <span id=k>0</span>/<span id=i>0</span>. Untrusted: <span id=u>0</span>.</p><output></output>"
    "<script>let k=0,i=0,u=0;for(let t of ['keydown','input'])document.addEventListener(t,e=>{if(!e.isTrusted)u++;else if(t==='keydown')k++;else i++;document.querySelector('#k').textContent=k;document.querySelector('#i').textContent=i;document.querySelector('#u').textContent=u;});</script>";
int main(void)
{
    const char *value = g_getenv("PIX_GTK4_INPUT_FD");
    char *end = NULL;
    long parsed = value ? strtol(value, &end, 10) : -1;
    if (!value || !*value || !end || *end || parsed < 3 || parsed > 1024) return 2;
    channel = (int)parsed;
    int type = 0; socklen_t size = sizeof type;
    struct sockaddr_storage address; socklen_t address_size = sizeof address;
    if (getsockopt(channel, SOL_SOCKET, SO_TYPE, &type, &size) || type != SOCK_SEQPACKET ||
        getsockname(channel, (struct sockaddr *)&address, &address_size) || address.ss_family != AF_UNIX) return 2;
    gtk_init();
    loop = g_main_loop_new(NULL, FALSE);
    window = gtk_window_new();
    gtk_window_set_default_size(GTK_WINDOW(window), 640, 480);
    gtk_window_set_title(GTK_WINDOW(window), "GTK4 diagnostic input fixture");
    g_signal_connect(window, "close-request", G_CALLBACK(on_close), NULL);
    g_signal_connect_after(window, "realize", G_CALLBACK(realized), NULL);
    WebKitNetworkSession *session = webkit_network_session_new_ephemeral();
    parent = WEBKIT_WEB_VIEW(g_object_new(WEBKIT_TYPE_WEB_VIEW, "network-session", session, NULL));
    g_object_unref(session);
    active = parent;
    g_signal_connect(parent, "decide-policy", G_CALLBACK(policy), NULL);
    g_signal_connect(parent, "create", G_CALLBACK(popup_create), NULL);
    GtkEventController *keys = gtk_event_controller_key_new();
    gtk_event_controller_set_propagation_phase(keys, GTK_PHASE_CAPTURE);
    g_signal_connect(keys, "key-pressed", G_CALLBACK(on_key), NULL);
    gtk_widget_add_controller(window, keys);
    GtkWidget *outer = gtk_box_new(GTK_ORIENTATION_VERTICAL, 4);
    stack = gtk_stack_new(); gtk_widget_set_vexpand(stack, TRUE);
    gtk_stack_add_named(GTK_STACK(stack), GTK_WIDGET(parent), "parent");
    gtk_box_append(GTK_BOX(outer), stack);
    GtkWidget *row = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 4);
    const char *labels[] = {"a", "A", "Delete", "Tab", "Enter"};
    const guint values[] = {GDK_KEY_a, GDK_KEY_A, GDK_KEY_BackSpace, GDK_KEY_Tab, GDK_KEY_Return};
    for (guint i = 0; i < G_N_ELEMENTS(values); i++) {
        GtkWidget *button = gtk_button_new_with_label(labels[i]);
        gtk_widget_set_focusable(button, FALSE);
        g_signal_connect(button, "clicked", G_CALLBACK(on_button), GUINT_TO_POINTER(values[i]));
        gtk_box_append(GTK_BOX(row), button);
    }
    gtk_box_append(GTK_BOX(outer), row);
    gtk_window_set_child(GTK_WINDOW(window), outer);
    ack_watch = g_unix_fd_add(channel, G_IO_IN | G_IO_HUP | G_IO_ERR, on_ack, NULL);
    webkit_web_view_load_html(parent, fixture, "about:blank");
    gtk_window_present(GTK_WINDOW(window));
    gtk_widget_grab_focus(GTK_WIDGET(parent));
    g_main_loop_run(loop);
    if (ack_watch) g_source_remove(ack_watch);
    if (ack_deadline) g_source_remove(ack_deadline);
    close(channel);
    gtk_window_destroy(GTK_WINDOW(window));
    g_main_loop_unref(loop);
    return failure;
}
