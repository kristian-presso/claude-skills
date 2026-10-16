"""Tests for keyword-research/scripts. Run: python3 -I -m unittest discover -s tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import load, py  # noqa: E402

ci = load("keyword-research", "classify_intent.py")
sc = load("keyword-research", "serp_cluster.py")


class Classify(unittest.TestCase):
    def c(self, kw, brands=()):
        return ci.classify(kw, ci.compile_tokens(list(brands)))

    def test_each_intent(self):
        self.assertEqual(self.c("bookkeeping prices uk")[0], "transactional")
        self.assertEqual(self.c("xero vs quickbooks")[0], "commercial")
        self.assertEqual(self.c("how to do a vat return in xero")[0], "informational")
        self.assertEqual(self.c("bookkeeper bristol")[0], "informational")  # default, no tokens

    def test_precedence(self):
        self.assertEqual(self.c("best price crm"), ("transactional", ["price"]))
        self.assertEqual(self.c("how much is the best crm")[0], "transactional")
        self.assertEqual(self.c("clifton books pricing", ["clifton books"]), ("navigational", ["clifton books"]))

    def test_whole_words_only(self):
        self.assertEqual(self.c("cheapest crm")[1], ["cheapest"])
        self.assertEqual(self.c("bestow crm")[0], "informational")
        self.assertEqual(self.c("near me plumber")[1], ["near me"])

    def test_punctuation_and_empty(self):
        self.assertEqual(self.c("CRM -- Pricing!!")[0], "transactional")
        self.assertEqual(self.c("!!!"), ("informational", []))
        self.assertEqual(self.c(""), ("informational", []))

    def test_cli_stdin_and_header(self):
        code, out, _ = py("keyword-research", "classify_intent.py", "--header", "--brand", "acme,acme crm",
                          stdin="# comment\n\nacme crm login\nbest crm\n")
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(lines[0], "keyword\tintent\tmatched")
        self.assertEqual(lines[1], "acme crm login\tnavigational\tacme")
        self.assertEqual(lines[2], "best crm\tcommercial\tbest")
        self.assertEqual(len(lines), 3)

    def test_cli_missing_file(self):
        code, _, err = py("keyword-research", "classify_intent.py", "/no/such/file.txt")
        self.assertNotEqual(code, 0)
        self.assertIn("cannot read", err)

    def test_cli_bad_bytes_do_not_crash(self):
        p = os.path.join(tempfile.mkdtemp(), "k.txt")
        with open(p, "wb") as f:
            f.write(b"caf\xe9 prices\n")
        code, out, _ = py("keyword-research", "classify_intent.py", p)
        self.assertEqual(code, 0)
        self.assertIn("transactional", out)


SERPS = (
    "Bookkeeper Bristol\thttps://www.a.example/\n"
    "bookkeeper bristol\thttps://b.example/x/\n"
    "bookkeeper bristol\thttps://c.example/y\n"
    "bookkeeping bristol\thttps://a.example\n"
    "bookkeeping bristol\thttps://b.example/x\n"
    "bookkeeping bristol\thttps://d.example/z\n"
    "xero vat\thttps://e.example/1\n"
    "xero vat\thttps://f.example/2\n"
)


class Cluster(unittest.TestCase):
    def test_norm_url(self):
        self.assertEqual(sc.norm_url("https://WWW.Example.com/Path/"), "example.com/Path")
        self.assertEqual(sc.norm_url("http://example.com"), "example.com/")
        self.assertEqual(sc.norm_url("https://example.com/p?utm=1"), "example.com/p")

    def test_jaccard(self):
        self.assertEqual(sc.jaccard({1, 2}, {2, 3}), 1 / 3)
        self.assertEqual(sc.jaccard(set(), {1}), 0.0)

    def test_tsv_clusters(self):
        code, out, _ = py("keyword-research", "serp_cluster.py", "--tsv", stdin=SERPS)
        self.assertEqual(code, 0)
        rows = dict(l.split("\t") for l in out.splitlines()[1:])
        self.assertEqual(rows["bookkeeper bristol"], rows["bookkeeping bristol"])
        self.assertNotEqual(rows["bookkeeper bristol"], rows["xero vat"])

    def test_threshold_splits(self):
        code, out, _ = py("keyword-research", "serp_cluster.py", "--tsv", "--threshold", "0.9", stdin=SERPS)
        rows = dict(l.split("\t") for l in out.splitlines()[1:])
        self.assertNotEqual(rows["bookkeeper bristol"], rows["bookkeeping bristol"])

    def test_blocks_report_overlap(self):
        code, out, _ = py("keyword-research", "serp_cluster.py", stdin=SERPS)
        self.assertIn("## Cluster c1 (2 keywords)", out)
        self.assertIn("urls shared by all: 2", out)

    def test_no_shared_results_never_link(self):
        code, out, _ = py("keyword-research", "serp_cluster.py", "--tsv", "--threshold", "0.01",
                          stdin="a\thttps://x.example/1\nb\thttps://y.example/2\n")
        self.assertIn("a\tc1", out)
        self.assertIn("b\tc2", out)

    def test_bad_threshold(self):
        for t in ("0", "-1", "1.5"):
            with self.subTest(t=t):
                code, _, _ = py("keyword-research", "serp_cluster.py", "--threshold", t, stdin=SERPS)
                self.assertEqual(code, 2)

    def test_empty_and_malformed_input(self):
        code, _, err = py("keyword-research", "serp_cluster.py", stdin="")
        self.assertEqual(code, 1)
        self.assertIn("no input rows", err)
        code, out, err = py("keyword-research", "serp_cluster.py", stdin="no tab here\nk\thttps://a.example/\n")
        self.assertEqual(code, 0)
        self.assertIn("skipping line without a tab", err)
        self.assertIn("- k", out)

    def test_missing_file(self):
        code, _, err = py("keyword-research", "serp_cluster.py", "/no/such.tsv")
        self.assertNotEqual(code, 0)
        self.assertIn("cannot read", err)


if __name__ == "__main__":
    unittest.main()
