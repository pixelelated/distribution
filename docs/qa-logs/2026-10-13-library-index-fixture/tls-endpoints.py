#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""UNRUN disposable-guest fixture. Two fixed RA URLs, no upstream client."""
import argparse
import json
import os
from pathlib import Path
import signal
import socket
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path)
    a = p.parse_args()
    root = a.root.resolve(strict=True)
    config = json.loads((root / "case.json").read_text())
    if socket.if_nameindex() != [(1, "lo")]:
        raise RuntimeError("loopback namespace required")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(root / "cert.pem", root / "key.pem")
    counts = {"hashlibrary": 0, "officialgameslist": 0, "denied": 0,
              "connections": 0, "tls_errors": 0}

    def record():
        tmp = root / "tls-counts.tmp"
        tmp.write_text(json.dumps(counts) + "\n")
        tmp.replace(root / "tls-counts.json")

    def sni(sock, name, unused):
        if name != "retroachievements.org":
            return ssl.ALERT_DESCRIPTION_UNRECOGNIZED_NAME
    context.set_servername_callback(sni)

    class Handler(BaseHTTPRequestHandler):
        # HTTP/1.0 closes each connection; no uploads, cookies, redirects or proxy.
        protocol_version = "HTTP/1.0"

        def log_message(self, *unused):
            pass

        def do_GET(self):
            allowed = {
                "/dorequest.php?r=hashlibrary": "hashlibrary",
                "/dorequest.php?r=officialgameslist": "officialgameslist",
            }
            category = allowed.get(self.path)
            if (self.headers.get("Host") != "retroachievements.org" or
                    self.headers.get("Content-Length", "0") != "0" or
                    self.headers.get("Transfer-Encoding") or category is None):
                self.reject()
                return
            counts[category] += 1
            record()
            if sum(counts[k] for k in allowed.values()) > 8:
                self.send_error(429)
                return
            status = 503 if config["case"] == "failure" and category == "hashlibrary" else 200
            body = ({"Error": "Synthetic hash library unavailable"} if status == 503 else
                    {"MD5List": {"11111111111111111111111111111111": 4242001}}
                    if category == "hashlibrary" else
                    {"Response": {"4242001": "Library setup fixture"}})
            data = json.dumps(body).encode("ascii")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def reject(self):
            counts["denied"] += 1
            record()
            # Never echo a request target, header or body, even on refusal.
            self.send_response(403)
            self.send_header("Content-Length", "0")
            self.end_headers()

        do_POST = do_PUT = do_CONNECT = do_HEAD = do_DELETE = do_OPTIONS = reject

        def send_error(self, code, message=None, explain=None):
            # Covers malformed/unsupported HTTP without reflecting input bytes.
            self.reject()

    class Server(HTTPServer):
        allow_reuse_address = False

        def get_request(self):
            raw, address = self.socket.accept()
            counts["connections"] += 1
            raw.settimeout(3)
            record()
            try:
                return context.wrap_socket(raw, server_side=True), address
            except (ssl.SSLError, OSError):
                raw.close()
                counts["tls_errors"] += 1
                record()
                raise OSError("fixture TLS handshake refused") from None

        def handle_error(self, request, client_address):
            counts["denied"] += 1
            record()

    stop = False

    def finish(signum, frame):
        nonlocal stop
        stop = True
    signal.signal(signal.SIGTERM, finish)
    signal.signal(signal.SIGINT, finish)
    server = Server(("127.0.0.1", 443), Handler)
    server.timeout = 0.2
    record()
    (root / "tls-ready.json").write_text(json.dumps({"pid": os.getpid(), "port": 443}) + "\n")
    deadline = time.monotonic() + 230
    try:
        while not stop and time.monotonic() < deadline and counts["connections"] < 32:
            server.handle_request()
    finally:
        server.server_close()
        record()
    return 0 if stop else 124


if __name__ == "__main__":
    raise SystemExit(main())
