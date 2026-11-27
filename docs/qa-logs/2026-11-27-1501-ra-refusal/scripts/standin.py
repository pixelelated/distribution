# A loopback RetroAchievements stand-in for #1501 and #1502 on a QA guest: every
# API request (/dorequest.php) is answered with one status (401 refuses the
# sign-in, 503 is a server that cannot answer). No real account or service is
# involved.
import json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
port, status = int(sys.argv[1]), int(sys.argv[2])
class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        sys.stderr.write("standin %s %s\n" % (self.command, self.path.split("?")[0])); sys.stderr.flush()
    def answer(self):
        # The API answers <status>; anything else (the client's own check
        # that the site is up) answers 200, as the real server does when the
        # site is up and only the account is refused.
        code = status if self.path.startswith("/dorequest.php") else 200
        body = json.dumps({"Success": code == 200, "Error": "local fixture", "Status": code}).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers()
        if self.command != "HEAD": self.wfile.write(body)
    do_GET = do_POST = do_HEAD = answer
ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
