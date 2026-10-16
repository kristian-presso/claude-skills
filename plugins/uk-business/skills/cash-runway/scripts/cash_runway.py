#!/usr/bin/env python3
"""Cash today, money already owed to HMRC, true free cash and runway, from a bank CSV.

Standard library only. Reads a bank statement export, works out the latest balance
and the monthly in/out over a window, subtracts the tax set-asides you pass in, and
prints the headline. It reads only; it never moves money or files anything.

Reference, not advice. The set-asides are estimates; your accounting software or
accountant has the real figures.

Examples:
  python3 cash_runway.py statement.csv
  python3 cash_runway.py statement.csv --window-days 90 --exclude "SAVINGS|TAX POT" \
      --vat-owed 4200 --ct-owed 9100 --paye-owed 1850 --committed 1200
  python3 cash_runway.py --balance 52000 --monthly-in 18000 --monthly-out 23500 --vat-owed 3000
"""
import argparse
import csv
import datetime as dt
import re
import sys
from collections import defaultdict

DATE_FORMATS = ["%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%d-%m-%Y", "%d %b %Y", "%d %B %Y", "%d.%m.%Y", "%Y/%m/%d"]


def parse_date(s):
    s = s.strip()
    for f in DATE_FORMATS:
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    raise ValueError(f"unrecognised date: {s!r}")


def parse_amount(s):
    if s is None:
        return None
    s = s.strip()
    if not s:
        return None
    neg = s.startswith("(") and s.endswith(")")
    s2 = re.sub(r"[£$€,\s()]", "", s)
    suffix = ""
    m = re.match(r"^(-?[\d.]+)(CR|DR)?$", s2, re.I)
    if not m:
        raise ValueError(f"unrecognised amount: {s!r}")
    v = float(m.group(1))
    suffix = (m.group(2) or "").upper()
    if neg or suffix == "DR":
        v = -abs(v)
    return v


def find_col(headers, wanted, override=None):
    if override:
        for h in headers:
            if h.strip().lower() == override.strip().lower():
                return h
        sys.exit(f"column {override!r} not found; headers are {headers}")
    low = {h: h.strip().lower() for h in headers}
    for w in wanted:
        for h, l in low.items():
            if l == w:
                return h
    for w in wanted:
        for h, l in low.items():
            if w in l:
                return h
    return None


def read_csv(path, a):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        r = csv.DictReader(f, dialect=dialect)
        headers = r.fieldnames or []
        c_date = find_col(headers, ["date", "transaction date", "posting date", "value date"], a.date_col)
        c_amt = find_col(headers, ["amount", "value", "amount (gbp)"], a.amount_col)
        c_in = find_col(headers, ["paid in", "money in", "credit", "credit amount", "in"], a.in_col)
        c_out = find_col(headers, ["paid out", "money out", "debit", "debit amount", "out"], a.out_col)
        c_bal = find_col(headers, ["balance", "running balance"], a.balance_col)
        c_desc = find_col(headers, ["description", "details", "narrative", "memo", "reference", "name", "payee"], a.desc_col)
        if not c_date:
            sys.exit(f"no date column found; headers are {headers}. Use --date-col.")
        if not c_amt and not (c_in or c_out):
            sys.exit(f"no amount or paid in/out columns found; headers are {headers}. Use --amount-col or --in-col/--out-col.")
        rows = []
        for i, row in enumerate(r):
            raw = (row.get(c_date) or "").strip()
            if not raw:
                continue
            d = parse_date(raw)
            if c_amt and (row.get(c_amt) or "").strip():
                amt = parse_amount(row[c_amt])
            else:
                pin = parse_amount(row.get(c_in)) if c_in else None
                pout = parse_amount(row.get(c_out)) if c_out else None
                amt = (pin or 0.0) - abs(pout or 0.0)
            bal = parse_amount(row.get(c_bal)) if c_bal else None
            desc = (row.get(c_desc) or "") if c_desc else ""
            rows.append({"i": i, "date": d, "amt": amt, "bal": bal, "desc": desc})
    if not rows:
        sys.exit("no transactions read")
    return rows


def latest_balance(rows):
    with_bal = [r for r in rows if r["bal"] is not None]
    if not with_bal:
        return None, None
    newest_first = rows[0]["date"] > rows[-1]["date"]
    pick = with_bal[0] if newest_first else with_bal[-1]
    return pick["bal"], pick["date"]


def gbp(v):
    if v is None:
        return "unavailable"
    return ("-£" if v < 0 else "£") + f"{abs(v):,.0f}"


def main(argv=None):
    p = argparse.ArgumentParser(description="Cash, set-asides, true free cash and runway (reference, not advice).")
    p.add_argument("csv", nargs="?", help="bank statement CSV export")
    p.add_argument("--window-days", type=int, default=90, help="days of history used for the monthly average")
    p.add_argument("--exclude", help="regex on description: transactions to leave out of burn (own-account transfers, loans in)")
    p.add_argument("--balance", type=float, help="cash today, overrides the CSV balance (add other accounts here)")
    p.add_argument("--monthly-in", type=float, help="typical monthly cash in, if no CSV")
    p.add_argument("--monthly-out", type=float, help="typical monthly cash out, if no CSV")
    p.add_argument("--vat-owed", type=float, default=None, help="VAT owed to HMRC and not yet paid")
    p.add_argument("--ct-owed", type=float, default=None, help="Corporation Tax set-aside: unpaid prior years plus accrued this year")
    p.add_argument("--paye-owed", type=float, default=None, help="PAYE and NI deducted but not yet paid to HMRC")
    p.add_argument("--committed", type=float, default=0.0, help="other committed outgoings due soon (rent, loan repayments, declared dividends)")
    for c in ["date", "amount", "in", "out", "balance", "desc"]:
        p.add_argument(f"--{c}-col", dest=f"{c}_col", help=f"name of the {c} column if not detected")
    a = p.parse_args(argv)

    cash = a.balance
    as_of = None
    m_in, m_out = a.monthly_in, a.monthly_out
    months = {}
    excluded = 0.0
    if a.csv:
        rows = read_csv(a.csv, a)
        bal, bal_date = latest_balance(rows)
        last = max(r["date"] for r in rows)
        first = min(r["date"] for r in rows)
        start = last - dt.timedelta(days=a.window_days - 1)
        if start < first:
            start = first
        span = (last - start).days + 1
        pat = re.compile(a.exclude, re.I) if a.exclude else None
        tin = tout = 0.0
        by_month = defaultdict(lambda: [0.0, 0.0])
        for r in rows:
            if r["date"] < start:
                continue
            if pat and pat.search(r["desc"]):
                excluded += r["amt"]
                continue
            if r["amt"] >= 0:
                tin += r["amt"]
                by_month[r["date"].strftime("%Y-%m")][0] += r["amt"]
            else:
                tout += -r["amt"]
                by_month[r["date"].strftime("%Y-%m")][1] += -r["amt"]
        scale = 30.44 / span
        if m_in is None:
            m_in = tin * scale
        if m_out is None:
            m_out = tout * scale
        months = dict(sorted(by_month.items()))
        if cash is None:
            cash = bal
        as_of = bal_date or last
        print(f"Read {len(rows)} transactions, {fmt(first)} to {fmt(last)}. Window used: {fmt(start)} to {fmt(last)} ({span} days).")
        if span < 60:
            print("Warning: under 60 days of history; the monthly average will be noisy.")
        if a.exclude:
            print(f"Excluded from burn by pattern: net {gbp(excluded)}.")
        if bal is None and a.balance is None:
            print("No balance column found: pass --balance with today's cash.")
        print("\n| Month | In | Out | Net |\n|---|---|---|---|")
        for k, (i, o) in months.items():
            print(f"| {k} | {gbp(i)} | {gbp(o)} | {gbp(i - o)} |")
        print("(Part months at the edges of the window are included as they are.)")

    if cash is None:
        sys.exit("need a bank CSV with a balance column, or --balance")

    set_asides = [("VAT owed", a.vat_owed), ("Corporation Tax set-aside", a.ct_owed), ("PAYE and NI owed", a.paye_owed)]
    known = [v for _, v in set_asides if v is not None]
    total_set = sum(known) + a.committed
    free = round(cash - total_set, 2)  # to the penny, so float noise never reads as 'short by £0'

    print("\n## Cash position" + (f" as of {fmt(as_of)}" if as_of else ""))
    print(f"\n| Line | Amount |\n|---|---|")
    print(f"| Cash today | {gbp(cash)} |")
    for name, v in set_asides:
        print(f"| less {name} | {gbp(v) if v is not None else 'not given - treat as unknown, not zero'} |")
    if a.committed:
        print(f"| less other committed outgoings | {gbp(a.committed)} |")
    print(f"| **True free cash** | **{gbp(free)}** |")

    missing = [n for n, v in set_asides if v is None]
    short = -free if free < 0 else 0.0
    at_least = "at least " if missing else ""
    if free < 0:
        print(f"\n**WARNING: the company already owes more than it holds.** Short by {at_least}{gbp(short)}: "
              f"cash {gbp(cash)} against {gbp(total_set)} already owed or committed. "
              "Some of the money in the bank belongs to HMRC or is already promised. Talk to your accountant "
              "before paying anything that is not essential; if a tax bill cannot be paid on time, contact HMRC "
              "before it is due (gov.uk/difficulties-paying-hmrc).")

    if m_in is not None and m_out is not None:
        net = m_out - m_in
        if net > 0:
            print(f"\nMonthly cash in {gbp(m_in)}, out {gbp(m_out)}, net burn {gbp(net)} a month.")
        else:
            print(f"\nMonthly cash in {gbp(m_in)}, out {gbp(m_out)}, net inflow {gbp(-net)} a month.")
        if free < 0:
            if net > 0:
                print(f"Runway: already short by {at_least}{gbp(short)}, and the gap grows by {gbp(net)} a month at this burn.")
            elif net < 0:
                print(f"Runway: already short by {at_least}{gbp(short)}. At this net inflow the gap would close in about "
                      f"{short / -net:.1f} months, only if the inflow holds and nothing new falls due.")
            else:
                print(f"Runway: already short by {at_least}{gbp(short)}, and money in only matches money out, so the gap is not closing.")
        elif free == 0:
            if net > 0:
                print("Runway: none. Every pound in the bank is already owed or committed, and the company is burning cash.")
            else:
                print("Runway: none to spare. Every pound in the bank is already owed or committed; free cash only grows if the inflow holds.")
        elif net <= 0:
            print(f"Runway: not being used up. More comes in than goes out on this window, so true free cash of {gbp(free)} is not being drawn down.")
        else:
            print(f"Runway on true free cash: {free / net:.1f} months. On raw bank balance it would look like {cash / net:.1f} months.")
    elif free < 0:
        print(f"\nRunway: already short by {at_least}{gbp(short)}.")
    if missing:
        print(f"\nNot included because not given: {', '.join(missing)}. The free cash figure is overstated by whatever these are.")
    print("\nReference, not advice: an estimate from bank data. Confirm tax figures in your accounting software or with your accountant.")


def fmt(d):
    return d.strftime("%d/%m/%Y")


if __name__ == "__main__":
    main()
