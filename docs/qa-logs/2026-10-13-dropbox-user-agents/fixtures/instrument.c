/* Diagnostic-only observer; never collects field values, cookies or queries. */
static gint64 qa_start;
static gboolean qa_pending;
static unsigned qa_resources, qa_finished, qa_failed;
static gint64 qa_lengths;
static double qa_seconds(void) { return (g_get_monotonic_time()-qa_start)/1000000.0; }
static void qa_resource_done(WebKitWebResource *r, gpointer unused) {
    WebKitURIResponse *resp=webkit_web_resource_get_response(r);
    qa_finished++;
    if(resp) qa_lengths+=webkit_uri_response_get_content_length(resp);
}
static void qa_resource_failed(WebKitWebResource *r, GError *e, gpointer unused) { qa_failed++; }
static void qa_resource(WebKitWebView *v, WebKitWebResource *r, WebKitURIRequest *req, gpointer unused) {
    qa_resources++;
    g_signal_connect(r,"finished",G_CALLBACK(qa_resource_done),NULL);
    g_signal_connect(r,"failed",G_CALLBACK(qa_resource_failed),NULL);
}
static void qa_value(GObject *view, GAsyncResult *result, gpointer started) {
    GError *error=NULL;
    JSCValue *v=webkit_web_view_evaluate_javascript_finish(WEBKIT_WEB_VIEW(view),result,&error);
    double latency=(g_get_monotonic_time()-*(gint64 *)started)/1000.0;
    g_free(started); qa_pending=FALSE;
    if(v) { char *s=jsc_value_to_string(v); g_printerr("QA_JSON {\"t\":%.3f,\"eval_ms\":%.3f,\"requested\":%u,\"finished\":%u,\"failed\":%u,\"response_lengths\":%" G_GINT64_FORMAT ",\"page\":%s}\n",qa_seconds(),latency,qa_resources,qa_finished,qa_failed,qa_lengths,s);g_free(s);g_object_unref(v); }
    else { g_printerr("QA_EVAL_ERROR %.3f %.3f\n",qa_seconds(),latency); if(error)g_error_free(error); }
}
static gboolean qa_poll(gpointer view) {
    if(qa_pending)return G_SOURCE_CONTINUE;
    qa_pending=TRUE;gint64 *t=g_new(gint64,1);*t=g_get_monotonic_time();
    webkit_web_view_evaluate_javascript(WEBKIT_WEB_VIEW(view),
      "JSON.stringify((()=>{const q=window.__qa570||{};const n=performance.getEntriesByType('navigation')[0];const rs=performance.getEntriesByType('resource');const f=Array.from(document.querySelectorAll('input')).filter(x=>!x.disabled&&x.getBoundingClientRect().width>0);return{ua:navigator.userAgent,host:location.hostname,path:location.pathname,width:innerWidth,height:innerHeight,ready:document.readyState,emailVisible:f.some(x=>x.type==='email'||x.name==='login_email'),inputCount:f.length,heartbeatCount:q.n||0,heartbeatMax:q.max||0,heartbeatSlow:q.slow||0,resources:rs.map(x=>({host:(new URL(x.name)).hostname,path:(new URL(x.name)).pathname,kind:x.initiatorType,duration:x.duration,transfer:x.transferSize,encoded:x.encodedBodySize,decoded:x.decodedBodySize})),navigation:n?{ttfb:n.responseStart,dom:n.domContentLoadedEventEnd,load:n.loadEventEnd,transfer:n.transferSize}:null}})())",
      -1,NULL,NULL,NULL,qa_value,t);
    return G_SOURCE_CONTINUE;
}
static void qa_setup(WebKitWebView *view) {
    qa_start=g_get_monotonic_time();
    gchar *ua=NULL;
    if(g_file_get_contents("/storage/qa570ua/ua.txt",&ua,NULL,NULL)&&ua&&*g_strstrip(ua))
        webkit_settings_set_user_agent(webkit_web_view_get_settings(view),ua);
    g_free(ua);
    WebKitUserScript *s=webkit_user_script_new("(()=>{const q=window.__qa570={n:0,max:0,slow:0};let prev=performance.now();setInterval(()=>{const now=performance.now(),d=now-prev;prev=now;q.n++;q.max=Math.max(q.max,d);if(d>500)q.slow++},100)})()",WEBKIT_USER_CONTENT_INJECT_TOP_FRAME,WEBKIT_USER_SCRIPT_INJECT_AT_DOCUMENT_START,NULL,NULL);
    webkit_user_content_manager_add_script(webkit_web_view_get_user_content_manager(view),s);webkit_user_script_unref(s);
    g_signal_connect(view,"resource-load-started",G_CALLBACK(qa_resource),NULL);
    g_timeout_add(2000,qa_poll,view);
}
