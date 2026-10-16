#!/usr/bin/env python3
"""AI search visibility audit for a live site. Standard library only.

Checks what a crawler actually receives, not what the repo says:
  - robots.txt rules for the main AI crawler agents (allowed or blocked for /)
  - llms.txt presence
  - per page: status, noindex, meta description, canonical, title, H1 count,
    question-style headings, JSON-LD block count and whether each block parses,
    and whether the page is in the sitemap while carrying noindex

Usage:
  python3 ai_visibility_audit.py https://example.com            # home page + sitemap sample
  python3 ai_visibility_audit.py https://example.com --max 50   # up to 50 sitemap URLs
  python3 ai_visibility_audit.py https://example.com/page --single
  python3 ai_visibility_audit.py https://example.com --json     # machine-readable output

Exit code: 0 when the audit ran, 2 when the start URL could not be fetched.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; ai-visibility-audit/0.1)"

# Agent names as of October 2026. Re-check the vendors' own crawler docs yearly.
AI_AGENTS = [
    ("OpenAI", "GPTBot", "training"),
    ("OpenAI", "OAI-SearchBot", "search index (ChatGPT citations)"),
    ("OpenAI", "ChatGPT-User", "user-triggered fetch"),
    ("Anthropic", "ClaudeBot", "training"),
    ("Anthropic", "Claude-SearchBot", "search index"),
    ("Anthropic", "Claude-User", "user-triggered fetch"),
    ("Perplexity", "PerplexityBot", "search index"),
    ("Perplexity", "Perplexity-User", "user-triggered fetch"),
    ("Google", "Googlebot", "search index incl. AI Overviews"),
    ("Google", "Google-Extended", "control token for Gemini use"),
    ("Microsoft", "Bingbot", "search index (feeds Copilot and others)"),
    ("Apple", "Applebot", "search index"),
    ("Apple", "Applebot-Extended", "control token for Apple model training"),
    ("Common Crawl", "CCBot", "open crawl used by many model builders"),
]

# Names that look right but match no real agent.
KNOWN_WRONG_NAMES = ["ChatGPTBot", "ClaudeBot-User", "Claude-Web", "AnthropicBot", "PerplexityAI"]

QUESTION_START = re.compile(
    r"^(how|what|why|when|where|who|which|is|are|does|do|can|should|will)\b", re.I
)


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            return r.status, r.headers.get("Content-Type", ""), body, r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", "") if e.headers else "", "", e.headers
    except Exception as e:  # network error, bad URL, timeout
        return None, "", str(e), None


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.canonicals = []
        self.titles = []
        self.h1 = 0
        self.headings = []
        self.ld_blocks = []
        self._cur = None
        self._buf = []
        self._svg = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "svg":
            self._svg += 1
            return
        if self._svg:
            return  # <title> inside an inline SVG is not the page title
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta.setdefault(key, []).append(a.get("content", ""))
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        elif tag == "title":
            self._cur, self._buf = "title", []
        elif tag in ("h1", "h2", "h3"):
            if tag == "h1":
                self.h1 += 1
            self._cur, self._buf = tag, []
        elif tag == "script" and "ld+json" in a.get("type", "").lower():
            self._cur, self._buf = "ld", []

    def handle_data(self, data):
        if self._cur:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "svg" and self._svg:
            self._svg -= 1
            return
        if self._cur is None:
            return
        text = "".join(self._buf).strip()
        if self._cur == "title" and tag == "title":
            self.titles.append(text)
            self._cur = None
        elif self._cur in ("h1", "h2", "h3") and tag == self._cur:
            self.headings.append((self._cur, re.sub(r"\s+", " ", text)))
            self._cur = None
        elif self._cur == "ld" and tag == "script":
            self.ld_blocks.append(text)
            self._cur = None


def ld_types(block):
    data = json.loads(block)
    found = []

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if t:
                found.extend(t if isinstance(t, list) else [t])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(data)
    return found


def top_level_nodes(block):
    """Top-level entities only (the root object or @graph members), so a nested
    publisher Organization does not count as a second Organization."""
    data = json.loads(block)
    roots = data if isinstance(data, list) else [data]
    nodes = []
    for r in roots:
        if isinstance(r, dict) and isinstance(r.get("@graph"), list):
            nodes.extend(n for n in r["@graph"] if isinstance(n, dict))
        elif isinstance(r, dict):
            nodes.append(r)
    return nodes


def audit_page(url, in_sitemap):
    status, ctype, body, headers = fetch(url)
    row = {"url": url, "status": status, "content_type": ctype}
    if status != 200 or not body:
        row["error"] = "not fetched" if status is None else f"HTTP {status}"
        return row
    p = PageParser()
    p.feed(body)
    robots_meta = " ".join(p.meta.get("robots", [])).lower()
    x_robots = (headers.get("X-Robots-Tag", "") if headers else "").lower()
    noindex = "noindex" in robots_meta or "noindex" in x_robots
    desc = p.meta.get("description", [])
    ld_ok, ld_bad, types, top = 0, 0, [], {}
    for b in p.ld_blocks:
        try:
            types.extend(ld_types(b))
            for n in top_level_nodes(b):
                t = n.get("@type")
                for tt in (t if isinstance(t, list) else [t]):
                    if tt in ("Organization", "WebSite"):
                        top.setdefault(tt, set()).add(n.get("@id") or id(n))
            ld_ok += 1
        except Exception:
            ld_bad += 1
    singletons = [t for t, ids in top.items() if len(ids) > 1]
    q_heads = [h for lvl, h in p.headings if lvl in ("h2", "h3") and (h.endswith("?") or QUESTION_START.match(h))]
    row.update({
        "title": p.titles[0] if p.titles else "",
        "title_len": len(p.titles[0]) if p.titles else 0,
        "title_count": len(p.titles),
        "description_len": len(desc[0]) if desc else 0,
        "description_count": len(desc),
        "canonical": p.canonicals[0] if p.canonicals else "",
        "canonical_count": len(p.canonicals),
        "og_image": (p.meta.get("og:image") or [""])[0],
        "h1_count": p.h1,
        "question_headings": len(q_heads),
        "jsonld_valid": ld_ok,
        "jsonld_invalid": ld_bad,
        "jsonld_types": sorted(set(types)),
        "duplicate_singletons": singletons,
        "noindex": noindex,
        "in_sitemap": in_sitemap,
    })
    flags = []
    if row["title_count"] != 1:
        flags.append(f"{row['title_count']} <title> tags")
    elif not 30 <= row["title_len"] <= 65:
        flags.append(f"title {row['title_len']} chars")
    if row["description_count"] == 0:
        flags.append("no meta description")
    elif not 70 <= row["description_len"] <= 170:
        flags.append(f"description {row['description_len']} chars")
    if row["canonical_count"] != 1:
        flags.append(f"{row['canonical_count']} canonicals")
    elif not row["canonical"].startswith("http"):
        flags.append("relative canonical")
    if row["og_image"] and not row["og_image"].startswith("http"):
        flags.append("relative og:image")
    if row["h1_count"] != 1:
        flags.append(f"{row['h1_count']} H1s")
    if row["jsonld_valid"] + row["jsonld_invalid"] == 0:
        flags.append("no JSON-LD")
    if row["jsonld_invalid"]:
        flags.append(f"{row['jsonld_invalid']} JSON-LD block(s) do not parse")
    if singletons:
        flags.append("duplicate " + "/".join(singletons))
    if noindex and in_sitemap:
        flags.append("noindex but listed in sitemap")
    row["flags"] = flags
    return row


def sitemap_urls(base, limit):
    urls, seen = [], set()
    queue = [urllib.parse.urljoin(base, "/sitemap.xml"), urllib.parse.urljoin(base, "/sitemap_index.xml")]
    while queue and len(urls) < limit:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        status, _, body, _ = fetch(sm)
        if status != 200:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
        if "<sitemapindex" in body:
            queue.extend(locs)
        else:
            for u in locs:
                if u not in urls:
                    urls.append(u)
    return urls[:limit]


def robots_report(base):
    robots_url = urllib.parse.urljoin(base, "/robots.txt")
    status, _, body, _ = fetch(robots_url)
    report = {"robots_url": robots_url, "status": status, "agents": [], "wrong_names": []}
    if status != 200:
        report["note"] = "no robots.txt served: every agent is allowed by default"
        for vendor, agent, job in AI_AGENTS:
            report["agents"].append({"vendor": vendor, "agent": agent, "job": job, "allowed_root": True, "named": False})
        return report
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.splitlines())
    named = {m.lower() for m in re.findall(r"(?im)^\s*user-agent\s*:\s*(\S+)", body)}
    root = urllib.parse.urljoin(base, "/")
    for vendor, agent, job in AI_AGENTS:
        report["agents"].append({
            "vendor": vendor, "agent": agent, "job": job,
            "allowed_root": rp.can_fetch(agent, root),
            "named": agent.lower() in named,
        })
    report["wrong_names"] = [w for w in KNOWN_WRONG_NAMES if w.lower() in named]
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--max", type=int, default=20, help="max sitemap URLs to audit (default 20)")
    ap.add_argument("--single", action="store_true", help="audit only the given URL")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = ap.parse_args()

    start = args.url if "://" in args.url else "https://" + args.url
    parts = urllib.parse.urlsplit(start)
    base = f"{parts.scheme}://{parts.netloc}"

    status, _, _, _ = fetch(start)
    if status is None:
        print(f"Could not fetch {start}", file=sys.stderr)
        sys.exit(2)

    def norm(u):
        return u.rstrip("/")

    sm = [] if args.single else sitemap_urls(base, args.max)
    if args.single:
        sm_set = {norm(u) for u in sitemap_urls(base, 500)}
        targets = [start]
    else:
        sm_set = {norm(u) for u in sm}
        targets = ([start] + [u for u in sm if norm(u) != norm(start)])[: args.max]

    llms_status = fetch(urllib.parse.urljoin(base, "/llms.txt"))[0]
    result = {
        "base": base,
        "robots": robots_report(base),
        "llms_txt": llms_status == 200,
        "sitemap_found": bool(sm) or bool(sm_set),
        "pages": [audit_page(u, norm(u) in sm_set) for u in targets],
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    r = result["robots"]
    print(f"# AI visibility audit: {base}\n")
    print(f"robots.txt: HTTP {r['status']}" + (f" ({r['note']})" if r.get("note") else ""))
    for a in r["agents"]:
        state = "allowed" if a["allowed_root"] else "BLOCKED"
        print(f"  {a['agent']:<18} {state:<8} named={'yes' if a['named'] else 'no ':<3}  {a['vendor']}, {a['job']}")
    if r["wrong_names"]:
        print(f"  WARNING: rules for agent names that do not exist: {', '.join(r['wrong_names'])}")
    print(f"llms.txt: {'present' if result['llms_txt'] else 'missing'}")
    print(f"sitemap: {'found' if result['sitemap_found'] else 'not found at /sitemap.xml or /sitemap_index.xml'}\n")
    print("## Pages\n")
    for p in result["pages"]:
        if p.get("error"):
            print(f"- {p['url']}: {p['error']}")
            continue
        verdict = "OK" if not p["flags"] else "; ".join(p["flags"])
        print(f"- {p['url']}")
        print(f"    title {p['title_len']}c, desc {p['description_len']}c, H1 {p['h1_count']}, "
              f"question headings {p['question_headings']}, JSON-LD {p['jsonld_valid']} ok / {p['jsonld_invalid']} bad "
              f"{p['jsonld_types'] or ''}")
        print(f"    {verdict}")


if __name__ == "__main__":
    main()
