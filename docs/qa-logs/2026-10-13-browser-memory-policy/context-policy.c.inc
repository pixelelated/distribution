/* Diagnostic only, Refs #570. Insert immediately before main().
 * Both modes construct the same ephemeral context. Change only the strict
 * fraction; preserve the engine's memory base, conservative fraction, poll
 * interval, and optional kill configuration. */
static WebKitWebContext *m7_memory_policy_context(void)
{
    const char *mode = g_getenv("CLOUD_SIGNIN_MEMORY_POLICY");
    if (!mode)
        mode = "default";
    if (g_strcmp0(mode, "default") != 0 && g_strcmp0(mode, "strict35") != 0)
        g_error("Unknown CLOUD_SIGNIN_MEMORY_POLICY (use default or strict35)");

    WebKitMemoryPressureSettings *pressure = webkit_memory_pressure_settings_new();
    if (g_strcmp0(mode, "strict35") == 0)
        webkit_memory_pressure_settings_set_strict_threshold(pressure, 0.35);

    /* Mirrors webkit_web_context_new_ephemeral() in 2.54.1. The context
     * refs the manager and copies the boxed settings during construction. */
    WebKitWebsiteDataManager *manager = webkit_website_data_manager_new_ephemeral();
    WebKitWebContext *context = WEBKIT_WEB_CONTEXT(g_object_new(
        WEBKIT_TYPE_WEB_CONTEXT,
        "website-data-manager", manager,
        "memory-pressure-settings", pressure,
        NULL));
    if (!webkit_web_context_is_ephemeral(context))
        g_error("M7 memory diagnostic requires an ephemeral context");

    /* No URI, page content, credential, cookie, or account values. A zero
     * kill fraction is NOT proof that WebKit's fallback kill is disabled. */
    g_printerr("M7_MEMORY_POLICY mode=%s webkit=%u.%u.%u base_mib=%u "
               "conservative=%.2f strict=%.2f kill_fraction=%.2f "
               "poll_seconds=%.2f ephemeral=1\n",
               mode, webkit_get_major_version(), webkit_get_minor_version(),
               webkit_get_micro_version(),
               webkit_memory_pressure_settings_get_memory_limit(pressure),
               webkit_memory_pressure_settings_get_conservative_threshold(pressure),
               webkit_memory_pressure_settings_get_strict_threshold(pressure),
               webkit_memory_pressure_settings_get_kill_threshold(pressure),
               webkit_memory_pressure_settings_get_poll_interval(pressure));
    webkit_memory_pressure_settings_free(pressure);
    g_object_unref(manager);
    return context;
}
