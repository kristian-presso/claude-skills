"""Tests for skills/cash-runway/scripts/cash_runway.py. Run: python3 -I -m unittest discover -s tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import load, run_main  # noqa: E402

cr = load("cash-runway", "cash_runway.py")


def write(tmp, name, text):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return p


class ParseAmount(unittest.TestCase):
    def test_plain_and_signed(self):
        self.assertEqual(cr.parse_amount("1234.50"), 1234.5)
        self.assertEqual(cr.parse_amount("-20"), -20.0)
        self.assertEqual(cr.parse_amount("+20"), 20.0)

    def test_currency_and_commas(self):
        self.assertEqual(cr.parse_amount("£1,234.56"), 1234.56)
        self.assertEqual(cr.parse_amount(" -£2,000.00 "), -2000.0)

    def test_brackets_and_dr_cr(self):
        self.assertEqual(cr.parse_amount("(45.00)"), -45.0)
        self.assertEqual(cr.parse_amount("45.00DR"), -45.0)
        self.assertEqual(cr.parse_amount("45.00 CR"), 45.0)

    def test_trailing_minus_and_unicode_minus(self):
        self.assertEqual(cr.parse_amount("1,234.56-"), -1234.56)
        self.assertEqual(cr.parse_amount("−12.00"), -12.0)

    def test_blank_is_none(self):
        self.assertIsNone(cr.parse_amount(""))
        self.assertIsNone(cr.parse_amount("   "))
        self.assertIsNone(cr.parse_amount(None))

    def test_rubbish_raises(self):
        for bad in ("abc", "1.2.3", "01/09/2026", "--5", "."):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    cr.parse_amount(bad)


class ParseDate(unittest.TestCase):
    def test_uk_formats(self):
        for s in ("30/09/2026", "30/09/26", "2026-09-30", "30-09-2026", "30 Sep 2026", "30 September 2026", "30.09.2026"):
            with self.subTest(s=s):
                self.assertEqual(cr.parse_date(s).isoformat(), "2026-09-30")

    def test_impossible_date_raises(self):
        with self.assertRaises(ValueError):
            cr.parse_date("31/02/2026")


class FindCol(unittest.TestCase):
    def test_exact_beats_substring(self):
        self.assertEqual(cr.find_col(["Running balance", "Balance"], ["balance"]), "Balance")

    def test_whole_word_only(self):
        # 'in' must not match 'Posting' or 'Description'
        self.assertIsNone(cr.find_col(["Posting", "Description"], ["in"]))

    def test_taken_columns_skipped(self):
        headers = ["Value Date", "Description", "Value"]
        self.assertEqual(cr.find_col(headers, ["value"], taken=["Value Date"]), "Value")

    def test_missing_override_exits(self):
        with self.assertRaises(SystemExit):
            cr.find_col(["Date"], ["date"], override="When")


class EndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def run_cli(self, *argv):
        return run_main(cr.main, list(argv))

    def test_single_amount_newest_first(self):
        p = write(self.tmp, "a.csv",
                  "Date,Description,Amount,Balance\n"
                  "28/09/2026,Rent,-1000.00,9000.00\n"
                  "15/08/2026,Client,3000.00,10000.00\n"
                  "01/07/2026,Opening,0.00,7000.00\n")
        code, out, _ = self.run_cli(p, "--vat-owed", "2000", "--ct-owed", "1000", "--paye-owed", "0")
        self.assertEqual(code, 0)
        self.assertIn("Cash position as of 28/09/2026", out)
        self.assertIn("| Cash today | £9,000 |", out)
        self.assertIn("**£6,000**", out)

    def test_paid_in_out_oldest_first_and_exclude(self):
        p = write(self.tmp, "b.csv",
                  "Date,Description,Paid in,Paid out,Balance\n"
                  "01/07/2026,Client A,\"1,000.00\",,\"6,000.00\"\n"
                  "02/07/2026,TRANSFER TO SAVINGS,,500.00,\"5,500.00\"\n"
                  "29/09/2026,Supplier,,\"2,000.00\",\"3,500.00\"\n")
        code, out, _ = self.run_cli(p, "--exclude", "savings")
        self.assertEqual(code, 0)
        self.assertIn("| Cash today | £3,500 |", out)
        self.assertIn("Excluded from burn by pattern: net -£500.", out)
        self.assertIn("treat as unknown, not zero", out)
        self.assertIn("overstated", out)

    def test_value_date_header_not_read_as_amount(self):
        p = write(self.tmp, "c.csv",
                  "Value Date,Description,Debit,Credit,Balance\n"
                  "01/09/2026,Client,,100.00,1100.00\n"
                  "02/09/2026,Rent,50.00,,1050.00\n")
        code, out, err = self.run_cli(p)
        self.assertEqual(code, 0, err)
        self.assertIn("| 2026-09 | £100 | £50 | £50 |", out)

    def test_semicolon_dialect_and_bom(self):
        p = write(self.tmp, "d.csv",
                  "﻿Date;Description;Amount;Balance\n"
                  "01/09/2026;Client;500;1500\n"
                  "30/09/2026;Rent;-200;1300\n")
        code, out, err = self.run_cli(p)
        self.assertEqual(code, 0, err)
        self.assertIn("| Cash today | £1,300 |", out)

    def test_already_short_warning(self):
        code, out, _ = self.run_cli("--balance", "18400", "--monthly-in", "14000", "--monthly-out", "12000",
                                    "--vat-owed", "9800", "--paye-owed", "2100", "--ct-owed", "4300", "--committed", "5000")
        self.assertEqual(code, 0)
        self.assertIn("WARNING", out)
        self.assertIn("Short by £2,800", out)
        self.assertIn("already short by £2,800", out)
        self.assertNotIn("not being used up", out)

    def test_short_with_missing_figure_says_at_least(self):
        code, out, _ = self.run_cli("--balance", "1000", "--vat-owed", "1500")
        self.assertIn("Short by at least £500", out)

    def test_exactly_zero_free_cash(self):
        code, out, _ = self.run_cli("--balance", "3000", "--monthly-in", "1000", "--monthly-out", "2000",
                                    "--vat-owed", "1000", "--ct-owed", "1000", "--paye-owed", "1000")
        self.assertIn("Runway: none.", out)

    def test_float_noise_is_not_short(self):
        code, out, _ = self.run_cli("--balance", "0.3", "--vat-owed", "0.1", "--ct-owed", "0.2", "--paye-owed", "0")
        self.assertNotIn("WARNING", out)

    def test_runway_months(self):
        code, out, _ = self.run_cli("--balance", "52000", "--monthly-in", "18000", "--monthly-out", "23500",
                                    "--vat-owed", "3000", "--ct-owed", "0", "--paye-owed", "0")
        self.assertIn("Runway on true free cash: 8.9 months", out)
        self.assertIn("9.5 months", out)

    def test_inflow_not_drawn_down(self):
        code, out, _ = self.run_cli("--balance", "10000", "--monthly-in", "5000", "--monthly-out", "4000",
                                    "--vat-owed", "0", "--ct-owed", "0", "--paye-owed", "0")
        self.assertIn("not being used up", out)

    # Broken input
    def test_no_input_at_all(self):
        code, _, err = self.run_cli()
        self.assertNotEqual(code, 0)
        self.assertIn("--balance", err)

    def test_missing_file(self):
        code, _, err = self.run_cli(os.path.join(self.tmp, "nope.csv"))
        self.assertNotEqual(code, 0)
        self.assertIn("cannot read", err)

    def test_no_date_column(self):
        p = write(self.tmp, "e.csv", "When,Amount\n01/09/2026,5\n")
        code, _, err = self.run_cli(p)
        self.assertNotEqual(code, 0)
        self.assertIn("no date column", err)

    def test_bad_row_reports_line(self):
        p = write(self.tmp, "f.csv", "Date,Amount,Balance\n01/09/2026,5,5\n31/02/2026,1,6\n")
        code, _, err = self.run_cli(p)
        self.assertNotEqual(code, 0)
        self.assertIn("line 3", err)

    def test_header_only(self):
        p = write(self.tmp, "g.csv", "Date,Amount,Balance\n")
        code, _, err = self.run_cli(p)
        self.assertNotEqual(code, 0)
        self.assertIn("no transactions", err)

    def test_empty_file(self):
        p = write(self.tmp, "h.csv", "")
        code, _, err = self.run_cli(p)
        self.assertNotEqual(code, 0)

    def test_bad_window_and_regex(self):
        code, _, _ = self.run_cli("--balance", "1", "--window-days", "0")
        self.assertEqual(code, 2)
        code, _, _ = self.run_cli("--balance", "1", "--exclude", "(")
        self.assertEqual(code, 2)

    def test_no_balance_column_needs_balance_flag(self):
        p = write(self.tmp, "i.csv", "Date,Amount\n01/09/2026,5\n")
        code, out, err = self.run_cli(p)
        self.assertNotEqual(code, 0)
        self.assertIn("No balance column", out)
        code, out, _ = self.run_cli(p, "--balance", "100")
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
