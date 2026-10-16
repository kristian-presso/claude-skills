"""Tests for seo-schema-gate/scripts/check_head.py. Run: python3 -I -m unittest discover -s tests"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import load, py, serve  # noqa: E402

ch = load("seo-schema-gate", "check_head.py")

GOOD = """<!doctype html><html><head>
<title>How to price a small conference: a worked example guide</title>
<meta name="description" content="A worked example of pricing a 150-person conference: fixed costs, break-even ticket price, early-bird tiers and the margin to aim for, step by step.">
<link rel="canonical" href="https://x.example/blog/price">
<meta property="og:type" content="article"><meta property="og:url" content="https://x.example/blog/price">
<meta property="og:title" content="t"><meta property="og:description" content="d">
<meta property="og:image" content="https://x.example/og.png"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[
 {"@type":"Organization","@id":"https://x.example/#org","name":"X"},
 {"@type":"BlogPosting","@id":"https://x.example/blog/price#article","datePublished":"2026-10-01","dateModified":"2026-10-10",
  "author":{"@type":"Person","name":"Sam Lee"},"publisher":{"@type":"Organization","@id":"https://x.example/#org"}}]}</script>
</head><body><svg><title>icon</title></svg><h1>x</h1></body></html>"""


def check(html, *extra):
    p = os.path.join(tempfile.mkdtemp(), "page.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    code, out, err = py("seo-schema-gate", "check_head.py", p, "--json", *extra)
    data = json.loads(out) if out.strip().startswith("{") else None
    return code, data, err


def levels(data):
    return {r["item"]: r["level"] for r in data["results"]}


class Helpers(unittest.TestCase):
    def test_top_nodes_graph_and_list(self):
        self.assertEqual(len(ch.top_nodes({"@graph": [{"@type": "A"}, {"@type": "B"}, "junk"]})), 2)
        self.assertEqual(len(ch.top_nodes([{"@type": "A"}, 3])), 1)
        self.assertEqual(ch.top_nodes("x"), [])

    def test_types_of(self):
        self.assertEqual(ch.types_of({"@type": ["A", "B"]}), {"A", "B"})
        self.assertEqual(ch.types_of({"@type": "A"}), {"A"})


class Checks(unittest.TestCase):
    def test_good_page_passes(self):
        code, data, err = check(GOOD)
        self.assertEqual(code, 0, data)
        self.assertEqual(data["fails"], 0)
        lv = levels(data)
        self.assertEqual(lv["Article author"], "PASS")
        self.assertEqual(lv["<title> length"], "PASS")  # the SVG <title> is ignored

    def test_broken_page(self):
        bad = GOOD.replace('"https://x.example/og.png"', '"/og.png"') \
                  .replace('{"@type":"Person","name":"Sam Lee"}', 'null') \
                  .replace('<link rel="canonical" href="https://x.example/blog/price">', '<link rel="canonical" href="/blog/price">')
        bad = bad.replace("</head>", '<script type="application/ld+json">{"@type":"Organization","name":"Dup",}</script>'
                                     '<script type="application/ld+json">{"@type":"Organization","name":"Theme"}</script></head>')
        code, data, _ = check(bad)
        self.assertEqual(code, 1)
        lv = levels(data)
        self.assertEqual(lv["og:image"], "FAIL")
        self.assertEqual(lv["Canonical"], "FAIL")
        self.assertEqual(lv["Article author"], "FAIL")
        self.assertEqual(lv["JSON-LD block 2"], "FAIL")
        self.assertEqual(lv["Duplicate Organization"], "FAIL")

    def test_truncated_description_and_noindex_warn(self):
        html = GOOD.replace("step by step.", "and so...").replace("</head>", '<meta name="robots" content="noindex"></head>')
        code, data, _ = check(html)
        warns = [r for r in data["results"] if r["level"] == "WARN"]
        self.assertTrue(any("ellipsis" in r["detail"] for r in warns))
        self.assertTrue(any(r["item"] == "Robots meta" for r in warns))

    def test_empty_page(self):
        code, data, _ = check("")
        self.assertEqual(code, 1)
        lv = levels(data)
        self.assertEqual(lv["Page body"], "FAIL")
        self.assertEqual(lv["<title>"], "FAIL")
        self.assertEqual(lv["JSON-LD"], "WARN")

    def test_non_utf8_file(self):
        p = os.path.join(tempfile.mkdtemp(), "l.html")
        with open(p, "wb") as f:
            f.write(b"<title>caf\xe9</title>")
        code, out, err = py("seo-schema-gate", "check_head.py", p)
        self.assertIn(code, (0, 1))
        self.assertNotIn("Traceback", err)

    def test_missing_file(self):
        code, out, err = py("seo-schema-gate", "check_head.py", "/no/such/page.html")
        self.assertEqual(code, 2)
        self.assertIn("Could not read", err)


class Live(unittest.TestCase):
    def test_served_wrong_content_type(self):
        with serve({"/feed": (200, "text/plain", GOOD, {}), "/ok": (200, "text/html; charset=utf-8", GOOD, {})}) as base:
            code, out, _ = py("seo-schema-gate", "check_head.py", base + "/feed", "--json")
            self.assertEqual(code, 1)
            self.assertEqual(levels(json.loads(out))["Served content type"], "FAIL")
            code, out, _ = py("seo-schema-gate", "check_head.py", base + "/ok", "--json")
            self.assertEqual(code, 0)

    def test_http_error_status(self):
        with serve({}) as base:
            code, out, _ = py("seo-schema-gate", "check_head.py", base + "/missing", "--json")
            self.assertEqual(code, 1)
            self.assertEqual(levels(json.loads(out))["HTTP status"], "FAIL")

    def test_unreachable(self):
        code, _, err = py("seo-schema-gate", "check_head.py", "http://127.0.0.1:9/")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
