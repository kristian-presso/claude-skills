"""Tests for content-atomisation/scripts/validate_map.sh. Run: python3 -I -m unittest discover -s tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import run, script  # noqa: E402

SH = script("content-atomisation", "validate_map.sh")
HEAD = "sequence\tlag_days\tchannel\tformat\tcore_claim\tlink_target\tcta\n"
HUB = "1\t0\tblog\tguide\tThesis\thttps://x.example/hub\tN/A\n"


def v(text, *args):
    return run(["bash", SH, *args], stdin=text)


class ValidateMap(unittest.TestCase):
    def test_valid(self):
        code, out, err = v(HEAD + HUB + "2\t1\tlinkedin\tpost\tClaim A\thttps://x.example/hub\tRead it\n"
                           "3\t5\temail\tfeature\tClaim B\thttps://x.example/hub\tReply\n")
        self.assertEqual(code, 0, err)
        self.assertEqual(out.strip(), "VALID rows=3 derivatives=2 span_days=5")

    def test_file_argument_and_crlf(self):
        p = os.path.join(tempfile.mkdtemp(), "m.tsv")
        with open(p, "w", newline="") as f:
            f.write((HUB + "2\t1\tlinkedin\tpost\tClaim A\thttps://x.example/hub\tRead it\n").replace("\n", "\r\n"))
        code, out, err = run(["bash", SH, p])
        self.assertEqual(code, 0, err)

    def check_bad(self, text, fragment):
        code, out, err = v(text)
        self.assertEqual(code, 1)
        self.assertIn(fragment, err)

    def test_no_hub(self):
        self.check_bad("2\t1\tlinkedin\tpost\tA\tu\tc\n", "no hub row")

    def test_hub_not_day_zero(self):
        self.check_bad("1\t2\tblog\tguide\tT\tu\tN/A\n2\t3\tx\tp\tA\tu\tc\n", "must have lag_days 0")

    def test_no_derivatives(self):
        self.check_bad(HUB, "no derivative rows")

    def test_derivative_same_day(self):
        self.check_bad(HUB + "2\t0\tx\tp\tA\tu\tc\n", "at least 1 day after the hub")

    def test_empty_field(self):
        self.check_bad(HUB + "2\t1\tx\tp\tA\tu\t \n", "field 7 is empty")

    def test_wrong_field_count(self):
        self.check_bad(HUB + "2\t1\tx\tp\tA\tu\n", "expected 7 tab-separated fields, got 6")

    def test_gap_and_duplicate_sequence(self):
        self.check_bad(HUB + "3\t1\tx\tp\tA\tu\tc\n", "sequence 2 is missing")
        self.check_bad(HUB + "2\t1\tx\tp\tA\tu\tc\n2\t2\tx\tp\tB\tu\tc\n", "appears more than once")

    def test_duplicate_claim_ignores_case_and_spacing(self):
        self.check_bad(HUB + "2\t1\tx\tp\tReply  fast\tu\tc\n3\t2\tx\tp\treply fast\tu\tc\n", "duplicates sequence 2")

    def test_goes_backwards(self):
        self.check_bad(HUB + "2\t3\tx\tp\tA\tu\tc\n3\t2\tx\tp\tB\tu\tc\n", "publishes before sequence 2")

    def test_non_numeric(self):
        self.check_bad(HUB + "two\t1\tx\tp\tA\tu\tc\n", "is not a whole number")
        self.check_bad(HUB + "2\t-1\tx\tp\tA\tu\tc\n", "is not a whole number")

    def test_empty_input(self):
        code, _, err = v("")
        self.assertEqual(code, 1)
        self.assertIn("no rows", err)

    def test_usage_errors(self):
        code, _, _ = run(["bash", SH, "a", "b"])
        self.assertEqual(code, 2)
        code, _, err = run(["bash", SH, "/no/such/map.tsv"])
        self.assertEqual(code, 2)
        self.assertIn("cannot read", err)


if __name__ == "__main__":
    unittest.main()
