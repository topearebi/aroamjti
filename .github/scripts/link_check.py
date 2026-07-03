#!/usr/bin/env python3
"""
link_check.py — outbound link-rot report for the archive.

Scans posts, works, and pages for external (http/https) links and checks
whether they still resolve. This is a *report*: it is meant to run on a
schedule (see the maintenance workflow), not on every push, and it must not
block publishing — a link dying on someone else's server is not a reason to
stop you posting.

Behavior:
  - Collects links from markdown [text](url), bare/autolink <url>, and raw
    URLs in body text.
  - De-duplicates, then checks each once.
  - Uses HEAD first (cheap); falls back to GET if HEAD is rejected.
  - Reports: dead (4xx/5xx/connection error), and "moved" (redirects) so you
    can update links before they fully rot.
  - Exit code is 0 even when links are dead, UNLESS run with --strict.

Standard library only (urllib) — no external HTTP library to maintain.
"""

import re
import glob
import os
import sys
import argparse
from urllib import request, error
from collections import defaultdict

SCAN_GLOBS = ["_posts/*.md", "_works/*", "*.md"]
TIMEOUT = 15
USER_AGENT = "aroamjti-linkcheck/1.0 (+maintenance script; non-malicious)"

URL_PATTERNS = [
    re.compile(r"\]\((https?://[^)\s]+)\)"),   # markdown [text](url)
    re.compile(r"<(https?://[^>\s]+)>"),        # autolink <url>
    re.compile(r"(?<![(<\"])\bhttps?://[^\s)>\"']+"),  # raw url in text
]

# Hosts we expect to be flaky or hostile to bots; report but don't alarm.
KNOWN_FLAKY = ("instagram.com", "music.youtube.com", "youtube.com")


def collect_links():
    links = defaultdict(list)  # url -> [files it appears in]
    seen_files = set()
    for pat in SCAN_GLOBS:
        for path in glob.glob(pat):
            if path in seen_files:
                continue
            seen_files.add(path)
            try:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            for rx in URL_PATTERNS:
                for m in rx.finditer(text):
                    url = m.group(1) if m.groups() else m.group(0)
                    url = url.rstrip(".,;:")   # trim trailing punctuation
                    links[url].append(os.path.basename(path))
    return links


def check(url):
    """Return (status, detail). status in {ok, moved, dead}."""
    for method in ("HEAD", "GET"):
        try:
            req = request.Request(url, method=method,
                                  headers={"User-Agent": USER_AGENT})
            with request.urlopen(req, timeout=TIMEOUT) as resp:
                final = resp.geturl()
                if final.rstrip("/") != url.rstrip("/"):
                    return "moved", f"→ {final}"
                return "ok", str(resp.status)
        except error.HTTPError as e:
            if e.code in (403, 405) and method == "HEAD":
                continue  # some servers refuse HEAD; try GET
            return "dead", f"HTTP {e.code}"
        except error.URLError as e:
            return "dead", f"{e.reason}"
        except Exception as e:  # noqa
            return "dead", f"{type(e).__name__}: {e}"
    return "dead", "no response"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any link is dead")
    args = ap.parse_args()

    links = collect_links()
    if not links:
        print("No outbound links found.")
        return

    dead, moved, flaky = [], [], []
    print(f"Checking {len(links)} unique outbound link(s)...\n")
    for url in sorted(links):
        status, detail = check(url)
        where = ", ".join(sorted(set(links[url])))
        if status == "dead":
            (flaky if any(h in url for h in KNOWN_FLAKY) else dead).append(
                (url, detail, where))
        elif status == "moved":
            moved.append((url, detail, where))

    if dead:
        print("── DEAD links (update or remove) " + "─" * 20)
        for url, detail, where in dead:
            print(f"  ✗ {url}  [{detail}]")
            print(f"      in: {where}")
    if moved:
        print("\n── MOVED / redirected (consider updating) " + "─" * 10)
        for url, detail, where in moved:
            print(f"  → {url}  {detail}")
            print(f"      in: {where}")
    if flaky:
        print("\n── Unreachable but on bot-hostile hosts (verify by hand) " + "─" * 4)
        for url, detail, where in flaky:
            print(f"  ? {url}  [{detail}]")
            print(f"      in: {where}")

    if not (dead or moved or flaky):
        print("✓ All outbound links resolved.")

    print(f"\nSummary: {len(dead)} dead, {len(moved)} moved, "
          f"{len(flaky)} flaky-host, "
          f"{len(links) - len(dead) - len(moved) - len(flaky)} ok.")

    if args.strict and dead:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
