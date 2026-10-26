# T20 (#667) L-01: a self-signed TLS listener on the guest's loopback, for #1154's unfixed half.
# Logs whether a request arrived over a certificate no CA signed, with every
# z, y, u and p value masked before anything is written. Answers a refusal.
import http.server, ssl, sys, re, time
LOG = sys.argv[3]
MASK = re.compile(r"(?i)\b(z|y|u|p)=[^&\s]*")
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        line = MASK.sub(lambda m: m.group(1) + "=<masked>", self.path)
        with open(LOG, "a") as f:
            f.write("%s GET %s host=%s\n" % (time.strftime("%H:%M:%S"), line, self.headers.get("Host", "")))
        body = b'{"Success":false,"Error":"t20 probe endpoint"}'
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    do_POST = do_GET
    def log_message(self, *a): pass
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); ctx.load_cert_chain(sys.argv[1], sys.argv[2])
srv = http.server.HTTPServer(("127.0.0.1", 443), H); srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
srv.serve_forever()
