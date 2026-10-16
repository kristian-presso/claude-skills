#!/usr/bin/env python3
"""Deterministic search-intent classifier. Standard library only.

Reads keywords (one per line) from stdin or a file, prints TSV:
    keyword <TAB> intent <TAB> matched_tokens

Intent is one of: navigational, transactional, commercial, informational.

Precedence when several classes match:
  1. navigational  - the keyword contains one of YOUR brand terms (--brand)
  2. transactional - buying or acting signals ("price", "buy", "free trial")
  3. commercial    - comparing before buying ("best", "vs", "alternatives")
  4. informational - learning signals ("how", "what", "guide")
  5. informational - default when nothing matches (most long-tail queries)

Matching is case-insensitive and whole-word ("cheapest" does not match "cheap").
This is a first pass. Always sanity-check the clusters that matter against the
live results page: the SERP is the real arbiter of intent.

Usage:
  printf 'best crm for charities\\ncrm pricing\\n' | python3 classify_intent.py
  python3 classify_intent.py keywords.txt --brand "acme,acme crm"
"""
import argparse
import re
import sys

TRANSACTIONAL = [
    "buy", "purchase", "order", "download", "subscribe", "book", "booking", "register",
    "hire", "quote", "quotes", "price", "prices", "pricing", "cost", "costs", "cheap",
    "cheapest", "discount", "deal", "deals", "coupon", "offer", "sale", "affordable", "demo",
    "checkout", "near me", "for sale", "low cost", "how much", "free trial", "sign up",
]
COMMERCIAL = [
    "best", "top", "review", "reviews", "comparison", "compare", "vs", "versus",
    "alternative", "alternatives", "recommended", "rated", "ranking", "roundup",
    "pros and cons", "worth it",
]
INFORMATIONAL = [
    "how", "what", "why", "when", "where", "who", "which", "is", "are", "does", "can",
    "should", "guide", "tutorial", "tips", "ideas", "examples", "example", "definition",
    "meaning", "difference", "explained", "learn", "overview", "introduction",
    "beginner", "beginners", "basics", "checklist", "template", "templates",
]


def compile_tokens(tokens):
    return [(t, re.compile(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])")) for t in tokens]


T_RE, C_RE, I_RE = compile_tokens(TRANSACTIONAL), compile_tokens(COMMERCIAL), compile_tokens(INFORMATIONAL)


def classify(keyword, brand_res):
    kw = re.sub(r"[^\w\s'&.-]", " ", keyword.lower()).strip()
    if not kw:
        return "informational", []
    for name, rx in brand_res:
        if rx.search(kw):
            return "navigational", [name]
    for label, table in (("transactional", T_RE), ("commercial", C_RE), ("informational", I_RE)):
        hits = [t for t, rx in table if rx.search(kw)]
        if hits:
            return label, hits
    return "informational", []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="file with one keyword per line (default: stdin)")
    ap.add_argument("--brand", default="", help="comma-separated brand or domain terms that mean navigational")
    ap.add_argument("--header", action="store_true", help="print a header row")
    args = ap.parse_args()

    brands = [b.strip().lower() for b in args.brand.split(",") if b.strip()]
    brand_res = compile_tokens(brands)
    src = open(args.file, encoding="utf-8") if args.file else sys.stdin
    if args.header:
        print("keyword\tintent\tmatched")
    for line in src:
        kw = line.strip()
        if not kw or kw.startswith("#"):
            continue
        intent, hits = classify(kw, brand_res)
        print(f"{kw}\t{intent}\t{','.join(hits)}")


if __name__ == "__main__":
    main()
