"""Tests for skills/uk-deadlines/scripts/deadlines.py. Run: python3 -I -m unittest discover -s tests"""
import argparse
import datetime as dt
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import load, run_main  # noqa: E402

dl = load("uk-deadlines", "deadlines.py")
D = dt.date


def args(**kw):
    base = dict(incorporated=D(2023, 5, 15), year_end=None, first_period_end=None, last_confirmation=None,
                vat="none", vat_year_end=None, employer=False, director_sa=False, today=D(2026, 10, 16), months=12)
    base.update(kw)
    if isinstance(base["year_end"], str):
        base["year_end"] = dl.parse_dm(base["year_end"])
    return argparse.Namespace(**base)


def rows(**kw):
    out, fpe, horizon = dl.build(args(**kw))
    return {(d.isoformat(), what.split(" (")[0]) for d, what, _, _ in out}, out, fpe


class DateHelpers(unittest.TestCase):
    def test_add_months_clamps_and_sticks(self):
        self.assertEqual(dl.add_months(D(2026, 1, 31), 1), D(2026, 2, 28))
        self.assertEqual(dl.add_months(D(2024, 1, 31), 1), D(2024, 2, 29))
        self.assertEqual(dl.add_months(D(2026, 2, 28), 1, True), D(2026, 3, 31))
        self.assertEqual(dl.add_months(D(2026, 2, 28), 1), D(2026, 3, 28))
        self.assertEqual(dl.add_months(D(2026, 11, 30), 3, True), D(2027, 2, 28))
        self.assertEqual(dl.add_months(D(2026, 12, 15), -12), D(2025, 12, 15))

    def test_parse_dm_variants(self):
        self.assertEqual(dl.parse_dm("31-03"), (31, 3))
        self.assertEqual(dl.parse_dm("31/03"), (31, 3))
        self.assertEqual(dl.parse_dm("29.02"), (29, 2))

    def test_parse_dm_rejects_rubbish(self):
        for bad in ("31-13", "32-01", "31-04", "0-05", "March", "31", "1-2-3"):
            with self.subTest(bad=bad):
                with self.assertRaises(argparse.ArgumentTypeError):
                    dl.parse_dm(bad)

    def test_year_end_on_leap_day(self):
        self.assertEqual(dl.year_end_on(2027, (29, 2)), D(2027, 2, 28))
        self.assertEqual(dl.year_end_on(2028, (29, 2)), D(2028, 2, 29))


class FirstPeriod(unittest.TestCase):
    def test_default_is_month_end_of_anniversary(self):
        self.assertEqual(dl.first_period_end(D(2025, 2, 3), None), D(2026, 2, 28))
        self.assertEqual(dl.first_period_end(D(2023, 5, 15), None), D(2024, 5, 31))

    def test_chosen_year_end_within_18_months(self):
        self.assertEqual(dl.first_period_end(D(2023, 5, 15), (31, 3)), D(2024, 3, 31))

    def test_chosen_year_end_closest_to_default(self):
        self.assertEqual(dl.first_period_end(D(2021, 11, 8), (31, 12)), D(2022, 12, 31))


class Build(unittest.TestCase):
    def test_long_first_period(self):
        got, out, fpe = rows(incorporated=D(2025, 2, 3), vat="3")
        self.assertEqual(fpe, D(2026, 2, 28))
        self.assertIn(("2026-11-03", "First annual accounts to Companies House"), got)
        self.assertIn(("2026-11-03", "Corporation Tax payment"), got)
        self.assertIn(("2026-12-01", "Corporation Tax payment"), got)
        ct600 = [r for r in out if r[1].startswith("Company Tax Return")]
        self.assertEqual([r[0] for r in ct600], [D(2027, 2, 28), D(2027, 2, 28)])
        self.assertIn(("2027-01-07", "VAT return and payment"), got)
        self.assertIn(("2027-02-17", "Confirmation statement"), got)

    def test_established_company_with_payroll(self):
        got, out, _ = rows(incorporated=D(2021, 11, 8), year_end="31-12", vat="1", employer=True)
        for expected in [("2026-10-22", "PAYE and National Insurance payment to HMRC"),
                         ("2026-11-07", "VAT return and payment"),
                         ("2026-11-22", "Confirmation statement"),
                         ("2026-12-31", "Company Tax Return CT600"),
                         ("2027-05-31", "P60s to employees"),
                         ("2027-09-30", "Annual accounts to Companies House"),
                         ("2027-10-01", "Corporation Tax payment")]:
            self.assertIn(expected, got)
        paye = [r for r in out if r[1].startswith("PAYE")]
        self.assertEqual(len(paye), 12)

    def test_weekend_dates_do_not_move(self):
        got, _, _ = rows(incorporated=D(2019, 3, 10), year_end="31-07")
        self.assertIn(("2027-05-01", "Corporation Tax payment"), got)
        self.assertIn(("2027-07-31", "Company Tax Return CT600"), got)

    def test_vat_monthly_and_annual(self):
        got, out, _ = rows(vat="monthly")
        self.assertEqual(len([r for r in out if r[1].startswith("VAT")]), 12)
        got, out, _ = rows(vat="annual", vat_year_end=(31, 3))
        self.assertIn(("2027-05-31", "Annual VAT return and balancing payment"), got)

    def test_vat_none_has_no_vat(self):
        _, out, _ = rows()
        self.assertFalse([r for r in out if "VAT" in r[1]])

    def test_director_sa(self):
        got, _, _ = rows(director_sa=True)
        self.assertIn(("2027-01-31", "Self Assessment online return for 2025-26, balancing payment and 1st payment on account"), got)
        self.assertIn(("2027-07-31", "Self Assessment 2nd payment on account for 2026-27"), got)

    def test_last_confirmation_moves_cycle(self):
        got, _, _ = rows(last_confirmation=D(2026, 1, 10))
        self.assertIn(("2027-01-24", "Confirmation statement"), got)

    def test_rows_sorted_and_inside_horizon(self):
        _, out, _ = rows(vat="1", employer=True, director_sa=True)
        dates = [r[0] for r in out]
        self.assertEqual(dates, sorted(dates))
        self.assertTrue(all(D(2026, 10, 16) <= d <= D(2027, 10, 16) for d in dates))


class Output(unittest.TestCase):
    def test_markdown_flags(self):
        md = dl.to_markdown([(D(2026, 10, 22), "PAYE", "HMRC", ""), (D(2026, 11, 7), "VAT", "HMRC", "n"),
                             (D(2027, 3, 1), "Later", "HMRC", "")], D(2026, 10, 16))
        lines = md.splitlines()
        self.assertIn("DUE SOON", lines[2])
        self.assertIn("07/11/2026 (weekend)", lines[3])
        self.assertIn("upcoming", lines[3])
        self.assertNotIn("upcoming", lines[4])

    def test_ics_is_valid_shape(self):
        rows_ = [(D(2026, 10, 22), "PAYE and National Insurance payment to HMRC (electronic), quarterly; long " * 2,
                  "HMRC", "note, with; specials\\ and more")]
        ics = dl.to_ics(rows_, 14)
        self.assertTrue(ics.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertTrue(ics.endswith("END:VCALENDAR\r\n"))
        for line in ics.split("\r\n"):
            self.assertLessEqual(len(line.encode("utf-8")), 75, line)
        unfolded = ics.replace("\r\n ", "")
        self.assertIn("TRIGGER:-P14D", unfolded)
        self.assertIn("DTSTART;VALUE=DATE:20261022", unfolded)
        self.assertIn("DTEND;VALUE=DATE:20261023", unfolded)
        self.assertIn(r"\,", unfolded)
        self.assertIn(r"\;", unfolded)

    def test_fold_keeps_multibyte_whole(self):
        line = "SUMMARY:" + "£" * 60
        folded = dl._fold(line)
        for part in folded.split("\r\n"):
            self.assertLessEqual(len(part.encode("utf-8")), 75)
        self.assertEqual(folded.replace("\r\n ", ""), line)


class Cli(unittest.TestCase):
    def test_writes_ics(self):
        tmp = tempfile.mkdtemp()
        p = os.path.join(tmp, "x.ics")
        code, out, _ = run_main(dl.main, ["--incorporated", "2023-05-15", "--year-end", "31/03", "--vat", "1",
                                          "--today", "2026-10-16", "--ics", p])
        self.assertEqual(code, 0)
        self.assertIn("First accounting period end used: 31/03/2024", out)
        with open(p, newline="") as f:
            self.assertIn("BEGIN:VEVENT", f.read())

    def test_bad_inputs_exit_2(self):
        for argv in (["--incorporated", "15/05/2023"],
                     ["--incorporated", "2023-05-15", "--year-end", "31-13"],
                     ["--incorporated", "2023-05-15", "--vat", "4"],
                     ["--incorporated", "2023-05-15", "--vat", "annual"],
                     ["--incorporated", "2027-01-01", "--today", "2026-10-16"],
                     ["--incorporated", "2023-05-15", "--months", "0"],
                     []):
            with self.subTest(argv=argv):
                code, _, _ = run_main(dl.main, argv)
                self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
