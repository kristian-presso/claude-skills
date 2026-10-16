"""Shared helpers for the uk-business script tests. Standard library only."""
import contextlib
import importlib.util
import io
import os
import sys

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(skill, script):
    """Import a skill's script as a module without touching sys.path."""
    path = os.path.join(PLUGIN, "skills", skill, "scripts", script)
    name = "_t_" + script.replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_main(fn, argv):
    """Call main(argv) and return (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            fn(argv)
        except SystemExit as e:
            if isinstance(e.code, str):
                err.write(e.code)
                code = 1
            else:
                code = e.code or 0
    return code, out.getvalue(), err.getvalue()
