#include <gst/gst.h>
int main(int argc, char **argv) {
  GError *error = NULL;
  gst_init(&argc, &argv);
  GstPlugin *plugin = gst_plugin_load_file("/usr/lib/gstreamer-1.0/libgstopengl.so", &error);
  if (!plugin) { g_printerr("FAIL: %s\n", error ? error->message : "plugin missing"); return 1; }
  gst_object_unref(plugin);
  GstElementFactory *app = gst_element_factory_find("appsink");
  GstElementFactory *gl = gst_element_factory_find("glupload");
  if (!app || !gl) { g_printerr("FAIL: missing appsink or glupload\n"); return 2; }
  gst_object_unref(app); gst_object_unref(gl);
  g_print("PASS: opengl plugin loads; appsink and glupload registered\n");
  gst_deinit(); return 0;
}
