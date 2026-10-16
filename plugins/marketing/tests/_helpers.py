"""Shared helpers for the marketing script tests. Standard library only."""
import contextlib
import http.server
import importlib.util
import io
import os
import subprocess
import sys
import threading

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def script(skill, name):
    return os.path.join(PLUGIN, "skills", skill, "scripts", name)


def load(skill, name):
    spec = importlib.util.spec_from_file_location("_t_" + name.split(".")[0], script(skill, name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd, stdin=""):
    """Run a script in a clean interpreter; return (code, stdout, stderr)."""
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=60,
                       env={k: v for k, v in os.environ.items() if not k.lower().endswith("_proxy")})
    return p.returncode, p.stdout, p.stderr


def py(skill, name, *args, stdin=""):
    return run([sys.executable, "-I", script(skill, name), *args], stdin)


@contextlib.contextmanager
def serve(routes):
    """Serve {path: (status, content_type, body, extra_headers)} on 127.0.0.1; yields the base URL."""

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split("?")[0]
            status, ctype, body, extra = routes.get(path, (404, "text/plain", "not found", {}))
            data = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            for k, v in extra.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}"
    finally:
        srv.shutdown()
        srv.server_close()
