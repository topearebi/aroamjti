#!/usr/bin/env python3
"""
tag_report.py — a maintenance report on the blog's tag taxonomy.

This is a *report*, not a gate. It never fails a build. Its job is to make
the shape of your tag vocabulary visible so you can decide what to merge,
rename, or leave alone. Run it whenever you want a health check on tags
(and it's wired into the scheduled maintenance workflow).

What it surfaces:
  1. Full frequency table (most-used first).
  2. Style inconsistency: posts using the YAML dash-list form vs the inline
     [a, b] form — both work, but consistency makes bulk edits predictable.
  3. Likely near-duplicates: tags that are singular/plural of each other, or
     differ only by a hyphen/spacing, or share a stem.
  4. Tags that duplicate the `type:` field's job (e.g. a `poetry` tag on a
     post that should just use `type: poetry`).
  5. Singletons: tags used exactly once (a long tail is fine, but worth a look).

Standard library only. No network. Safe to run anywhere.
"""

import re
import glob
import os
import sys
from collections import defaultdict

POST_DIR = "_posts"

# Tags that overlap with the `type:` front-matter field's responsibility.
TYPE_LIKE_TAGS = {"poetry", "prose", "poems", "verse"}

INLINE_TAGS_RE = re.compile(r"^tags:\s*\[(.*?)\]", re.MULTILINE)
BLOCK_TAGS_RE = re.compile(r"^tags:\s*$", re.MULTILINE)


def front_matter(text):
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def parse_tags(fm):
    """Return (tags_list, style) where style is 'inline', 'block', or None."""
    m = INLINE_TAGS_RE.search(fm)
    if m:
        raw = m.group(1)
        tags = [t.strip() for t in raw.split(",") if t.strip()]
        return tags, "inline"
    if BLOCK_TAGS_RE.search(fm):
        # collect subsequent "  - tag" lines
        tags = []
        after = fm[BLOCK_TAGS_RE.search(fm).end():]
        for line in after.splitlines():
            lm = re.match(r"\s*-\s*(\S.*)$", line)
            if lm:
                tags.append(lm.group(1).strip())
            elif line.strip() and not line.startswith(" "):
                break
        return tags, "block"
    return [], None


def stem(tag):
    """Very light stemmer for near-duplicate detection."""
    t = tag.lower().replace("-", "").replace("_", "")
    for suf in ("ies", "es", "s"):
        if t.endswith(suf) and len(t) > len(suf) + 2:
            return t[: -len(suf)]
    return t


def main():
    freq = defaultdict(int)
    style_of = {}
    tag_posts = defaultdict(list)

    files = sorted(glob.glob(os.path.join(POST_DIR, "*.md")))
    for path in files:
        with open(path, encoding="utf-8") as fh:
            fm = front_matter(fh.read())
        tags, style = parse_tags(fm)
        if style:
            style_of[path] = style
        for t in tags:
            freq[t] += 1
            tag_posts[t].append(os.path.basename(path))

    if not freq:
        print("No tags found.")
        return

    print("=" * 60)
    print("TAG CONSISTENCY REPORT")
    print("=" * 60)

    # 1. Frequency table
    print("\n1. Frequency (most used first)")
    print("-" * 40)
    for tag, n in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {n:3d}  {tag}")

    # 2. Style inconsistency
    inline = [p for p, s in style_of.items() if s == "inline"]
    block = [p for p, s in style_of.items() if s == "block"]
    print("\n2. Tag style")
    print("-" * 40)
    print(f"  inline [a, b] : {len(inline)} posts")
    print(f"  block  (- a)  : {len(block)} posts")
    if block and inline:
        print("  ⚠ Mixed styles. Both are valid YAML, but standardizing on")
        print("    the inline form makes bulk edits predictable. Block-style:")
        for p in block:
            print(f"      • {os.path.basename(p)}")

    # 3. Near-duplicates (shared stem)
    stems = defaultdict(list)
    for tag in freq:
        stems[stem(tag)].append(tag)
    dupes = {s: ts for s, ts in stems.items() if len(ts) > 1}
    print("\n3. Possible near-duplicates (same stem)")
    print("-" * 40)
    if dupes:
        for s, ts in sorted(dupes.items()):
            joined = ", ".join(f"{t} ({freq[t]})" for t in sorted(ts))
            print(f"  ⚠ {joined}")
    else:
        print("  none detected")

    # 4. type-like tags
    type_like = [t for t in freq if t.lower() in TYPE_LIKE_TAGS]
    print("\n4. Tags that overlap the `type:` field")
    print("-" * 40)
    if type_like:
        for t in type_like:
            print(f"  ⚠ '{t}' ({freq[t]}) — consider using `type:` instead of a tag.")
            for pn in tag_posts[t]:
                print(f"      • {pn}")
    else:
        print("  none")

    # 5. Singletons
    singletons = sorted(t for t, n in freq.items() if n == 1)
    print("\n5. Singletons (used once)")
    print("-" * 40)
    if singletons:
        print("  " + ", ".join(singletons))
        print(f"  ({len(singletons)} single-use tags — fine in moderation, but")
        print("   worth scanning for one-offs that could fold into a broader tag.)")
    else:
        print("  none")

    print("\n" + "=" * 60)
    print("Report only — nothing was changed. Review and edit tags by hand.")
    sys.exit(0)


if __name__ == "__main__":
    main()
