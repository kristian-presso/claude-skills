#!/usr/bin/env python3
"""Check a page's SEO meta and JSON-LD against the seo-schema-gate checklist.

Works on a live URL or a local built HTML file. Standard library only.

Usage:
  python3 check_head.py https://example.com/blog/post
  python3 check_head.py dist/blog/post/index.html
  python3 check_head.py https://example.com/page --json

Exit code: 0 if every hard check passes, 1 if any FAIL, 2 if the page could not be read.
WARN lines are advisory and do not change the exit code.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

ARTICLE_TYPES = {"Article", "BlogPosting", "NewsArticle", "TechArticle"}
SINGLETONS = {"Organization", "WebSite"}


class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.titles, self.ld = {}, [], [], []
        self._cur, self._buf, self._svg = None, [], 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "svg":
            self._svg += 1
            return
        if self._svg:
            return
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta.setdefault(key, []).append(a.get("content", ""))
        elif tag == "link":
            self.links.append(a)
        elif tag == "title":
            self._cur, self._buf = "title", []
        elif tag == "script" and "ld+json" in a.get("type", "").lower():
            self._cur, self._buf = "ld", []

    def handle_data(self, d):
        if self._cur:
            self._buf.append(d)

    def handle_endtag(self, tag):
        if tag == "svg" and self._svg:
            self._svg -= 1
            return
        if self._cur == "title" and tag == "title":
            self.titles.append("".join(self._buf).strip())
            self._cur = None
        elif self._cur == "ld" and tag == "script":
            self.ld.append("".join(self._buf).strip())
            self._cur = None


def load(target):
    if re.match(r"https?://", target):
        req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0 (seo-schema-gate)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", "replace"), r.status, r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            return "", e.code, ""
        except Exception as e:
            print(f"Could not fetch {target}: {e}", file=sys.stderr)
            sys.exit(2)
    try:
        with open(target, encoding="utf-8") as f:
            return f.read(), None, None
    except OSError as e:
        print(f"Could not read {target}: {e}", file=sys.stderr)
        sys.exit(2)


def top_nodes(data):
    roots = data if isinstance(data, list) else [data]
    out = []
    for r in roots:
        if isinstance(r, dict) and isinstance(r.get("@graph"), list):
            out.extend(n for n in r["@graph"] if isinstance(n, dict))
        elif isinstance(r, dict):
            out.append(r)
    return out


def types_of(node):
    t = node.get("@type", [])
    return set(t if isinstance(t, list) else [t])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="URL or path to a built HTML file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    html, status, ctype = load(args.target)
    results = []

    def add(level, item, detail=""):
        results.append({"level": level, "item": item, "detail": detail})

    if status is not None:
        if status != 200:
            add("FAIL", "HTTP status", str(status))
        if ctype and "text/html" not in ctype.lower():
            add("FAIL", "Served content type", f"{ctype} (expected text/html)")
        elif ctype:
            add("PASS", "Served content type", ctype)
    if not html:
        add("FAIL", "Page body", "empty")
    h = Head()
    h.feed(html)
    m = h.meta

    # Title
    if len(h.titles) != 1:
        add("FAIL", "<title>", f"{len(h.titles)} found, expected 1")
    else:
        n = len(h.titles[0])
        add("PASS" if 50 <= n <= 60 else "WARN", "<title> length", f"{n} chars (aim 50 to 60): {h.titles[0][:70]}")

    # Description
    desc = m.get("description", [])
    if len(desc) != 1:
        add("FAIL", "Meta description", f"{len(desc)} found, expected 1")
    else:
        n = len(desc[0])
        add("PASS" if 150 <= n <= 160 else "WARN", "Meta description length", f"{n} chars (aim 150 to 160)")
        if desc[0].rstrip().endswith(("...", "…")):
            add("WARN", "Meta description", "ends with an ellipsis; looks truncated rather than written")

    # Canonical
    canon = [l.get("href", "") for l in h.links if "canonical" in l.get("rel", "").lower().split()]
    if len(canon) != 1:
        add("FAIL", "Canonical", f"{len(canon)} found, expected 1")
    elif not canon[0].startswith("http"):
        add("FAIL", "Canonical", f"relative: {canon[0]}")
    else:
        add("PASS", "Canonical", canon[0])

    # Robots
    robots = " ".join(m.get("robots", [])).lower()
    if "noindex" in robots:
        add("WARN", "Robots meta", f"'{robots}' - fine only if this page should stay out of search")

    # Open Graph
    for key in ("og:type", "og:url", "og:title", "og:description", "og:image"):
        v = (m.get(key) or [""])[0]
        if not v:
            add("FAIL", key, "missing")
        elif key in ("og:image", "og:url") and not v.startswith("http"):
            add("FAIL", key, f"relative: {v}")
        else:
            add("PASS", key, v[:80])

    # Twitter / X card
    card = (m.get("twitter:card") or [""])[0]
    add("PASS" if card == "summary_large_image" else "WARN", "twitter:card", card or "missing (falls back to Open Graph on most platforms)")

    # JSON-LD
    if not h.ld:
        add("WARN", "JSON-LD", "no blocks found")
    seen = {}
    for i, block in enumerate(h.ld, 1):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            add("FAIL", f"JSON-LD block {i}", f"does not parse: {e.msg} at line {e.lineno} col {e.colno}")
            continue
        nodes = top_nodes(data)
        tlist = sorted({t for n in nodes for t in types_of(n)})
        add("PASS", f"JSON-LD block {i}", f"parses; types {tlist}")
        for n in nodes:
            ts = types_of(n)
            for t in ts & SINGLETONS:
                seen.setdefault(t, set()).add(n.get("@id") or id(n))
            if ts & ARTICLE_TYPES:
                if not n.get("datePublished"):
                    add("FAIL", f"{'/'.join(ts & ARTICLE_TYPES)} datePublished", "missing")
                if not n.get("dateModified"):
                    add("WARN", f"{'/'.join(ts & ARTICLE_TYPES)} dateModified", "missing")
                author = n.get("author")
                names = []
                for a in (author if isinstance(author, list) else [author]):
                    if isinstance(a, dict) and a.get("name"):
                        names.append(a["name"])
                if not names:
                    add("FAIL", "Article author", "no author with a name")
                else:
                    add("PASS", "Article author", ", ".join(names))
            if not n.get("@id") and ts & (SINGLETONS | ARTICLE_TYPES | {"WebPage", "Person"}):
                add("WARN", f"{'/'.join(sorted(ts))} @id", "missing; a stable @id lets other nodes reference it")
    for t, ids in seen.items():
        if len(ids) > 1:
            add("FAIL", f"Duplicate {t}", f"{len(ids)} top-level {t} nodes; usually one from the theme and one from your code")

    fails = sum(r["level"] == "FAIL" for r in results)
    if args.json:
        print(json.dumps({"target": args.target, "fails": fails, "results": results}, indent=2))
    else:
        print(f"# seo-schema-gate: {args.target}\n")
        for r in results:
            print(f"{r['level']:<5} {r['item']}: {r['detail']}")
        print(f"\n{fails} fail(s). Confirm vocabulary with Google's Rich Results Test and validator.schema.org.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
