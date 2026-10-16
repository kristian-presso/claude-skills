"""Tests for ai-search-visibility/scripts/ai_visibility_audit.py, against a local server.
Run: python3 -I -m unittest discover -s tests"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import load, py, serve  # noqa: E402

av = load("ai-search-visibility", "ai_visibility_audit.py")

ROBOTS = """User-agent: Googlebot
Allow: /

User-agent: ChatGPTBot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: *
Disallow: /
"""

PAGE = """<html><head><title>Venue hire prices in Bristol for 2026 events</title>
<meta name="description" content="Half day, full day and evening venue hire prices for our 120-capacity Bristol venue, with what each package includes.">
<link rel="canonical" href="https://x.example/pricing">
<script type="application/ld+json">{"@type":"Organization","name":"A",}</script>
<script type="application/ld+json">{"@graph":[{"@type":"Organization","@id":"#a"},{"@type":"Organization","@id":"#b"}]}</script>
</head><body><h1>Prices</h1><h2>How much does venue hire cost?</h2><h2>Packages</h2><h3>Is VAT included?</h3></body></html>"""


def routes(robots=ROBOTS, llms=True):
    r = {"/robots.txt": (200, "text/plain", robots, {}),
         "/": (200, "text/html", PAGE, {}),
         "/pricing": (200, "text/html", PAGE, {"X-Robots-Tag": "noindex"})}
    if llms:
        r["/llms.txt"] = (200, "text/plain", "# x", {})
    return r


class Parser(unittest.TestCase):
    def test_page_parser(self):
        p = av.PageParser()
        p.feed(PAGE)
        self.assertEqual(p.h1, 1)
        self.assertEqual(len(p.ld_blocks), 2)
        self.assertEqual(p.canonicals, ["https://x.example/pricing"])

    def test_top_level_nodes_ignore_nested(self):
        nodes = av.top_level_nodes('{"@type":"BlogPosting","publisher":{"@type":"Organization"}}')
        self.assertEqual([n["@type"] for n in nodes], ["BlogPosting"])
        self.assertIn("Organization", av.ld_types('{"@type":"BlogPosting","publisher":{"@type":"Organization"}}'))


class Audit(unittest.TestCase):
    def audit(self, r, *args):
        with serve(r) as base:
            code, out, err = py("ai-search-visibility", "ai_visibility_audit.py", base, "--json", *args)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def test_robots_and_wrong_names(self):
        sm = '<?xml version="1.0"?><urlset><url><loc>{b}/pricing</loc></url></urlset>'
        rr = routes()  # the sitemap is added once the server's base URL is known
        with serve(rr) as base:
            rr["/sitemap.xml"] = (200, "application/xml", sm.format(b=base), {})
            code, out, err = py("ai-search-visibility", "ai_visibility_audit.py", base, "--json")
            self.assertEqual(code, 0, err)
            res = json.loads(out)
        agents = {a["agent"]: a for a in res["robots"]["agents"]}
        self.assertTrue(agents["Googlebot"]["allowed_root"])
        self.assertFalse(agents["OAI-SearchBot"]["allowed_root"])
        self.assertFalse(agents["GPTBot"]["allowed_root"])
        self.assertTrue(agents["GPTBot"]["named"])
        self.assertEqual(res["robots"]["wrong_names"], ["ChatGPTBot"])
        self.assertTrue(res["llms_txt"])
        self.assertTrue(res["sitemap_found"])
        pricing = [p for p in res["pages"] if p["url"].endswith("/pricing")][0]
        self.assertTrue(pricing["noindex"])
        self.assertIn("noindex but listed in sitemap", pricing["flags"])
        self.assertEqual(pricing["jsonld_invalid"], 1)
        self.assertEqual(pricing["duplicate_singletons"], ["Organization"])
        self.assertEqual(pricing["question_headings"], 2)

    def test_no_robots_means_all_allowed(self):
        r = routes(llms=False)
        del r["/robots.txt"]
        res = self.audit(r, "--single")
        self.assertTrue(all(a["allowed_root"] for a in res["robots"]["agents"]))
        self.assertIn("allowed by default", res["robots"]["note"])
        self.assertFalse(res["llms_txt"])
        self.assertEqual(len(res["pages"]), 1)

    def test_page_errors_are_reported_not_raised(self):
        r = routes()
        r["/"] = (500, "text/html", "boom", {})
        res = self.audit(r, "--single")
        self.assertEqual(res["pages"][0]["error"], "HTTP 500")

    def test_text_report(self):
        with serve(routes()) as base:
            code, out, _ = py("ai-search-visibility", "ai_visibility_audit.py", base, "--single")
        self.assertEqual(code, 0)
        self.assertIn("OAI-SearchBot      BLOCKED", out)
        self.assertIn("rules for agent names that do not exist: ChatGPTBot", out)

    def test_unreachable_exits_2(self):
        code, _, err = py("ai-search-visibility", "ai_visibility_audit.py", "http://127.0.0.1:9")
        self.assertEqual(code, 2)
        self.assertIn("Could not fetch", err)


if __name__ == "__main__":
    unittest.main()
