#!/usr/bin/env python3
"""Group keywords into clusters by how much their search results overlap.

If two keywords return mostly the same top results, the search engine treats them
as one need, and one page can rank for both. If the results diverge, they need
separate pages. Standard library only.

Input (stdin or file): TSV, one result per line
    keyword <TAB> url
List the top organic URLs (ideally 10) for each keyword. Order does not matter.
Lines starting with # are ignored.

Output: one block per cluster, largest first, with the keywords and the URLs
they share. Pairs are linked when Jaccard overlap >= threshold, and clusters are
the connected groups (so A~B and B~C puts A, B and C together).

Usage:
  python3 serp_cluster.py serps.tsv
  python3 serp_cluster.py serps.tsv --threshold 0.3 --tsv   # keyword<TAB>cluster_id

Threshold guide: 0.4 is a sensible start. Raise to 0.5 if clusters come out too
broad; lower to 0.3 in a thin niche where results naturally vary.
"""
import argparse
import sys
import urllib.parse
from collections import defaultdict


def norm_url(u):
    p = urllib.parse.urlsplit(u.strip())
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host + (p.path.rstrip("/") or "/")


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--threshold", type=float, default=0.4)
    ap.add_argument("--tsv", action="store_true", help="print keyword<TAB>cluster_id instead of blocks")
    args = ap.parse_args()
    if not 0 < args.threshold <= 1:
        ap.error("--threshold must be above 0 and at most 1")

    try:
        src = open(args.file, encoding="utf-8", errors="replace") if args.file else sys.stdin
    except OSError as e:
        sys.exit(f"cannot read {args.file}: {e.strerror}")
    serps = defaultdict(set)
    order = []
    for line in src:
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            print(f"skipping line without a tab: {line.strip()[:60]}", file=sys.stderr)
            continue
        kw, url = parts[0].strip().lower(), parts[1].strip()
        if kw not in serps:
            order.append(kw)
        if url:
            serps[kw].add(norm_url(url))

    if not order:
        print("no input rows", file=sys.stderr)
        sys.exit(1)

    parent = {k: k for k in order}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    pair_scores = {}
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            s = jaccard(serps[a], serps[b])
            if s > 0 and s >= args.threshold:  # no shared result never links two keywords
                pair_scores[(a, b)] = s
                parent[find(a)] = find(b)

    groups = defaultdict(list)
    for k in order:
        groups[find(k)].append(k)
    clusters = sorted(groups.values(), key=lambda g: (-len(g), g[0]))

    if args.tsv:
        print("keyword\tcluster_id")
        for i, g in enumerate(clusters, 1):
            for k in g:
                print(f"{k}\tc{i}")
        return

    for i, g in enumerate(clusters, 1):
        shared = set.intersection(*(serps[k] for k in g)) if len(g) > 1 else set()
        print(f"## Cluster c{i} ({len(g)} keyword{'s' if len(g) != 1 else ''})")
        for k in g:
            print(f"- {k}  [{len(serps[k])} urls]")
        if len(g) > 1:
            links = [f"{a} ~ {b}: {s:.2f}" for (a, b), s in pair_scores.items() if a in g and b in g]
            print("  overlaps: " + "; ".join(links))
            print(f"  urls shared by all: {len(shared)}")
        print()


if __name__ == "__main__":
    main()
