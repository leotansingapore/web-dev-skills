#!/usr/bin/env python3
"""Local decisions page (competitor-site-buildout skill): serves index.html and
decisions.json, the copy drafts listed in decisions.json under /md/<path relative to
~/Documents>, and saves POST /save to answers.json. Restart after editing decisions.json
(the draft allow-list is read at start). Port: 8765 (change below if taken)."""
import json, os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.expanduser('~/Documents')
ALLOWED = set()
with open(os.path.join(HERE, 'decisions.json')) as f:
    for _slug, _url, path in json.load(f)['drafts']:
        ALLOWED.add(path)


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)

    def do_GET(self):
        if self.path.startswith('/md/'):
            rel = unquote(self.path[4:].split('?')[0])
            if rel not in ALLOWED:
                return self.send_error(404)
            with open(os.path.join(DOCS, rel), 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        if self.path in ('/answers.json', '/serve.py'):
            return self.send_error(404)
        return super().do_GET()

    def do_POST(self):
        if self.path != '/save':
            return self.send_error(404)
        n = int(self.headers.get('Content-Length', 0))
        payload = json.loads(self.rfile.read(n) or b'{}')
        with open(os.path.join(HERE, 'answers.json'), 'w') as f:
            json.dump(payload, f, indent=2)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')


if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8765), H).serve_forever()
