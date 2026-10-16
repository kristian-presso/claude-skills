#!/usr/bin/env python3
"""Personal filing calendar for a small UK limited company.

Standard library only. Reference, not advice: every date it prints should be
confirmed in the company's HMRC business tax account and on its Companies House
page, which show the dates that actually apply.

Rules as of 16/10/2026 (verify at gov.uk):
  Accounts               9 months after the period end; first accounts covering
                         more than 12 months: the later of 21 months after
                         incorporation or 3 months after the period end.
  Corporation Tax pay    9 months and 1 day after the end of each CT period
                         (profits up to GBP 1.5m; larger companies pay instalments).
  CT600                  12 months after the end of the accounts period. A CT period
                         is at most 12 months, so accounts longer than 12 months
                         need two returns, both due 12 months after the accounts end.
  Confirmation statement within 14 days after each 12-month review period ends.
  VAT (quarterly/monthly) 1 calendar month and 7 days after each period ends.
  VAT (annual scheme)    2 months after the VAT year ends.
  PAYE (employers)       22nd of each month for electronic payment.
  Self Assessment        31 January and 31 July; paper return 31 October.

Examples:
  python3 deadlines.py --incorporated 2023-05-15 --year-end 31-03 --vat 1 --employer --director-sa
  python3 deadlines.py --incorporated 2025-09-02 --vat none --ics deadlines.ics
"""
import argparse
import calendar
import datetime as dt
import sys

D = dt.date


def last_day(y, m):
    return calendar.monthrange(y, m)[1]


def add_months(d, n, month_end_sticky=False):
    """Add n calendar months. If month_end_sticky and d is a month end, land on a month end."""
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    if month_end_sticky and d.day == last_day(d.year, d.month):
        return D(y, m, last_day(y, m))
    return D(y, m, min(d.day, last_day(y, m)))


def parse_date(s):
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def parse_dm(s):
    d, m = s.split("-")
    return int(d), int(m)


def year_end_on(y, dm):
    d, m = dm
    return D(y, m, min(d, last_day(y, m)))


def first_period_end(inc, dm):
    default = add_months(D(inc.year, inc.month, 1), 12)
    default = D(default.year, default.month, last_day(default.year, default.month))
    if dm is None:
        return default
    limit = add_months(inc, 18)
    cands = [year_end_on(y, dm) for y in range(inc.year, inc.year + 3)]
    cands = [c for c in cands if inc < c <= limit]
    if not cands:
        return default
    return min(cands, key=lambda c: abs((c - default).days))


def fmt(d):
    return d.strftime("%d/%m/%Y")


def build(a):
    today = a.today
    horizon = add_months(today, a.months)
    out = []

    def add(date, what, who, note=""):
        if today <= date <= horizon:
            out.append((date, what, who, note))

    inc = a.incorporated
    dm = parse_dm(a.year_end) if a.year_end else None
    fpe = a.first_period_end or first_period_end(inc, dm)
    if dm is None:
        dm = (fpe.day, fpe.month)

    # Accounting periods and their deadlines
    ends = [fpe]
    while ends[-1] < horizon:
        ends.append(year_end_on(ends[-1].year + 1, dm))
    starts = [inc] + [e + dt.timedelta(days=1) for e in ends[:-1]]
    for i, (s, e) in enumerate(zip(starts, ends)):
        if i == 0 and add_months(inc, 12) <= e:
            acc = max(add_months(inc, 21), add_months(e, 3, True))
            add(acc, f"First annual accounts to Companies House (period {fmt(s)} to {fmt(e)})",
                "Companies House", "first accounts rule: later of 21 months after incorporation or 3 months after period end")
        else:
            add(add_months(e, 9, True), f"Annual accounts to Companies House (year ended {fmt(e)})", "Companies House")
        # CT periods: max 12 months
        cs = s
        while cs <= e:
            ce = min(e, add_months(cs, 12) - dt.timedelta(days=1))
            label = f"CT period {fmt(cs)} to {fmt(ce)}"
            add(add_months(ce, 9, True) + dt.timedelta(days=1), f"Corporation Tax payment ({label})", "HMRC",
                "assumes profits under GBP 1.5m; check the date in your HMRC account")
            ct600_note = "" if ce == e else "accounts run over 12 months: both returns are due 12 months after the accounts period ends"
            add(add_months(e, 12, True), f"Company Tax Return CT600 ({label})", "HMRC", ct600_note)
            cs = ce + dt.timedelta(days=1)

    # Confirmation statement
    base = a.last_confirmation or inc
    k = 1
    while True:
        review_end = add_months(base, 12 * k)
        due = review_end + dt.timedelta(days=14)
        if due > horizon:
            break
        add(due, f"Confirmation statement (review period ending {fmt(review_end)})", "Companies House",
            "every director must have verified their identity first")
        k += 1

    # VAT
    v = a.vat
    if v in ("1", "2", "3", "monthly"):
        if v == "monthly":
            months = list(range(1, 13))
        else:
            first = {"1": 3, "2": 4, "3": 5}[v]
            months = [((first - 1 + 3 * i) % 12) + 1 for i in range(4)]
        y, m = today.year - 1, 1
        while D(y, m, 1) <= horizon:
            if m in months:
                pe = D(y, m, last_day(y, m))
                add(add_months(pe, 1, True) + dt.timedelta(days=7), f"VAT return and payment (period ending {fmt(pe)})", "HMRC",
                    "money must reach HMRC by this date")
            m += 1
            if m > 12:
                y, m = y + 1, 1
    elif v == "annual":
        ve = parse_dm(a.vat_year_end) if a.vat_year_end else None
        if not ve:
            sys.exit("--vat annual needs --vat-year-end DD-MM")
        for y in range(today.year - 1, horizon.year + 1):
            pe = year_end_on(y, ve)
            add(add_months(pe, 2, True), f"Annual VAT return and balancing payment (VAT year ending {fmt(pe)})", "HMRC",
                "interim payments also fall during the year; check your VAT account")

    # Payroll
    if a.employer:
        d = D(today.year, today.month, 22)
        while d <= horizon:
            add(d, "PAYE and National Insurance payment to HMRC (electronic)", "HMRC",
                "quarterly payers: 22nd after each tax quarter instead")
            d = add_months(d, 1)
        for y in range(today.year, horizon.year + 1):
            add(D(y, 4, 5), "Tax year ends: final FPS on or before last payday", "HMRC")
            add(D(y, 5, 31), "P60s to employees", "Employees")
            add(D(y, 7, 6), "P11D and P11D(b) if benefits were provided", "HMRC", "skip if no benefits")
            add(D(y, 7, 22), "Class 1A National Insurance on benefits (electronic)", "HMRC", "skip if no benefits")

    # Director's own Self Assessment
    if a.director_sa:
        for y in range(today.year, horizon.year + 1):
            add(D(y, 1, 31), f"Self Assessment online return for {y-2}-{str(y-1)[2:]}, balancing payment and 1st payment on account",
                "HMRC (personal)")
            add(D(y, 7, 31), f"Self Assessment 2nd payment on account for {y-1}-{str(y)[2:]}", "HMRC (personal)",
                "only if payments on account apply")
            add(D(y, 10, 31), f"Self Assessment paper return for {y-1}-{str(y)[2:]}", "HMRC (personal)",
                "online filers can ignore")

    out.sort()
    return out, fpe, horizon


def to_markdown(rows, today):
    lines = ["| Date | Days away | Flag | What | Where |", "|---|---|---|---|---|"]
    for d, what, who, note in rows:
        days = (d - today).days
        flag = "DUE SOON" if days <= 14 else ("upcoming" if days <= 60 else "")
        wk = " (weekend)" if d.weekday() >= 5 else ""
        extra = f" - {note}" if note else ""
        lines.append(f"| {fmt(d)}{wk} | {days} | {flag} | {what}{extra} | {who} |")
    return "\n".join(lines)


def to_ics(rows, remind_days):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//uk-deadlines//EN", "CALSCALE:GREGORIAN"]
    for i, (d, what, who, note) in enumerate(rows):
        out += [
            "BEGIN:VEVENT",
            f"UID:uk-deadline-{d.isoformat()}-{i}@local",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(d + dt.timedelta(days=1)).strftime('%Y%m%d')}",
            "SUMMARY:" + _esc(f"DUE: {what}"),
            "DESCRIPTION:" + _esc(f"{who}. {note} Reference only: confirm the date in your HMRC or Companies House account."),
            "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + _esc(what),
            f"TRIGGER:-P{remind_days}D", "END:VALARM",
            "END:VEVENT",
        ]
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def _esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="12-month UK company filing calendar (reference, not advice).")
    p.add_argument("--incorporated", type=parse_date, required=True, help="incorporation date, YYYY-MM-DD")
    p.add_argument("--year-end", help="accounting reference date, DD-MM (default: Companies House default)")
    p.add_argument("--first-period-end", type=parse_date, help="override the first accounting period end, YYYY-MM-DD")
    p.add_argument("--last-confirmation", type=parse_date, help="date of the last confirmation statement, YYYY-MM-DD")
    p.add_argument("--vat", default="none", choices=["none", "1", "2", "3", "monthly", "annual"],
                   help="VAT stagger: 1 = quarters end Mar/Jun/Sep/Dec, 2 = Apr/Jul/Oct/Jan, 3 = May/Aug/Nov/Feb")
    p.add_argument("--vat-year-end", help="for --vat annual: VAT year end, DD-MM")
    p.add_argument("--employer", action="store_true", help="company runs a payroll")
    p.add_argument("--director-sa", action="store_true", help="include the director's own Self Assessment dates")
    p.add_argument("--today", type=parse_date, default=D.today(), help="start date, YYYY-MM-DD (default today)")
    p.add_argument("--months", type=int, default=12)
    p.add_argument("--ics", help="also write an .ics calendar file to this path")
    p.add_argument("--remind-days", type=int, default=14, help="reminder lead time in the .ics file")
    a = p.parse_args(argv)
    rows, fpe, horizon = build(a)
    print(f"Calendar {fmt(a.today)} to {fmt(horizon)}. First accounting period end used: {fmt(fpe)}.")
    print(to_markdown(rows, a.today))
    if a.ics:
        with open(a.ics, "w", newline="") as f:
            f.write(to_ics(rows, a.remind_days))
        print(f"\nWrote {len(rows)} events to {a.ics}")


if __name__ == "__main__":
    main()
