#!/usr/bin/env python3
"""
check_integrity.py — pre-publish integrity gate for the blog.

Run by the GitHub Action on every push. Prints a clear, grouped report so a
failure is understandable from a phone.

Two severities:

- ERRORS (exit 1, blocking) — things that silently BREAK publishing: a bad
  filename, a missing title/date, a work Jekyll won't process. These are not
  matters of taste; the post simply will not appear correctly.
- WARNINGS (exit 0, non-blocking) — things that are probably drift but might
  be deliberate, chiefly an unrecognised `type:`/`format:` value. A vocabulary
  in flux should never block a publish; you may be mid-migration, or trying a
  new form. The warning is a nudge, not a gate.

Design notes:
- Zero third-party dependencies (standard library only), so it runs anywhere
  and never rots due to a package change.
- Deliberately conservative: it only blocks on things that are unambiguously
  broken, to avoid false positives stopping a legitimate publish.
- The valid vocabularies below track the taxonomy documented in README.md.
  Update them when the taxonomy deliberately changes (and add the matching
  CSS rule).
"""

import re
import sys
import glob
import os

# --- Vocabularies: keep in sync with README.md and the CSS rules -----------
# Posts: every post should carry exactly one `type:`. See README.md for the
# decision order and the boundary rules.
VALID_POST_TYPES = {"poetry", "essay", "journal", "fiction", "fragments"}
# Works: `format:` may be omitted (=> prose) or one of these.
VALID_WORK_FORMATS = {"poetry", "prose"}

POST_DIR = "_posts"
WORK_DIR = "_works"

FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")
DATE_LINE_RE = re.compile(r"^date:\s*(.+?)\s*$", re.MULTILINE)
TZ_OFFSET_RE = re.compile(r"[+-]\d{4}\b")
TITLE_LINE_RE = re.compile(r"^title:\s*(.*\S.*)$", re.MULTILINE)
TYPE_LINE_RE = re.compile(r"^type:\s*([^\s#]+)", re.MULTILINE)
FORMAT_LINE_RE = re.compile(r"^format:\s*([^\s#]+)", re.MULTILINE)

# Internal markdown links like ](/2021/08/18/foo/) — must resolve to a real
# post/permalink. External links (http...) and anchors (#...) are ignored.
INTERNAL_LINK_RE = re.compile(r"\]\((/[^)#\s]*)")

errors = []    # hard failures -> block publish (something is actually broken)
warnings = []  # probable drift -> reported, but never blocks
notes = []     # informational -> printed but do not block


def front_matter(text):
    """Return the YAML front-matter block (between the first two --- lines)."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def check_posts():
    files = sorted(glob.glob(os.path.join(POST_DIR, "*")))
    if not files:
        notes.append(f"No files found in {POST_DIR}/ (nothing to check).")
    for path in files:
        name = os.path.basename(path)

        # 1) Filename format
        if not FILENAME_RE.match(name):
            errors.append(
                f"[filename] {path}: must match YYYY-MM-DD-slug.md "
                f"(a bad name silently fails to publish)."
            )
            # If the name is wrong, still try to read front matter below.

        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm = front_matter(text)

        # 2) Required: title (non-empty)
        if not TITLE_LINE_RE.search(fm):
            errors.append(f"[title] {path}: missing or empty `title:`.")

        # 3) Required: date, with timezone offset
        m = DATE_LINE_RE.search(fm)
        if not m:
            errors.append(f"[date] {path}: missing `date:`.")
        elif not TZ_OFFSET_RE.search(m.group(1)):
            errors.append(
                f"[date] {path}: date `{m.group(1)}` has no timezone offset "
                f"(e.g. +0000). Without it, sort order can drift."
            )

        # 4) type vocabulary (WARNING ONLY — a vocabulary in flux must never
        #    block a publish; you may be mid-migration or trying a new form.)
        t = TYPE_LINE_RE.search(fm)
        if not t:
            warnings.append(
                f"[type] {path}: no `type:`. Every post should carry one of "
                f"{sorted(VALID_POST_TYPES)}."
            )
        elif t.group(1) not in VALID_POST_TYPES:
            warnings.append(
                f"[type] {path}: type '{t.group(1)}' is not in "
                f"{sorted(VALID_POST_TYPES)}. If this is deliberate, add it to "
                f"VALID_POST_TYPES here, add a .post--{t.group(1)} CSS rule, and "
                f"record it in README.md."
            )


def check_works():
    files = sorted(glob.glob(os.path.join(WORK_DIR, "*")))
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm = front_matter(text)

        # Works must have a title
        if not TITLE_LINE_RE.search(fm):
            errors.append(f"[title] {path}: missing or empty `title:`.")

        # format vocabulary
        f = FORMAT_LINE_RE.search(fm)
        if f and f.group(1) not in VALID_WORK_FORMATS:
            warnings.append(
                f"[format] {path}: format '{f.group(1)}' is not in "
                f"{sorted(VALID_WORK_FORMATS)}. A new format needs a matching "
                f".work-body--{f.group(1)} CSS rule."
            )

        # Works must have a file extension Jekyll will process (.md/.markdown/.html)
        # Files with no extension will NOT be processed as pages.
        base = os.path.basename(path)
        if "." not in base:
            errors.append(
                f"[extension] {path}: work file has no extension; Jekyll will "
                f"not process its front matter. Rename to {base}.md."
            )


def check_internal_links():
    """Verify internal links (starting with /) point at something real.

    We can't fully resolve permalinks without building, so this is a light
    heuristic: it collects known post permalinks and flags internal links
    that don't match any of them. Conservative — only flags clear misses.
    """
    known = set()
    for path in glob.glob(os.path.join(POST_DIR, "*.md")):
        name = os.path.basename(path)
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", name)
        if m:
            y, mo, d, slug = m.groups()
            known.add(f"/{y}/{mo}/{d}/{slug}/")
    # static pages
    known.update({
        "/", "/about/", "/books/", "/works/", "/blogroll/",
        "/browse/", "/tags/", "/types/", "/archive/",
    })

    for path in glob.glob(os.path.join(POST_DIR, "*.md")):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for link in INTERNAL_LINK_RE.findall(text):
            # normalize trailing slash
            norm = link if link.endswith("/") else link + "/"
            if norm not in known and link not in known:
                notes.append(
                    f"[link] {path}: internal link {link} did not match a "
                    f"known post/page (verify it resolves)."
                )


def main():
    check_posts()
    check_works()
    check_internal_links()

    if notes:
        print("── Notes (non-blocking) " + "─" * 30)
        for n in notes:
            print("  •", n)
        print()

    if warnings:
        print("── Warnings (non-blocking) " + "─" * 27)
        for w in warnings:
            print("  !", w)
        print(f"\n  {len(warnings)} warning(s) — taxonomy drift, not breakage.")
        print()

    if errors:
        print("── Integrity errors (publish blocked) " + "─" * 16)
        for e in errors:
            print("  ✗", e)
        print(f"\n{len(errors)} error(s). These break publishing. Fix and push again.")
        sys.exit(1)

    if warnings:
        print("✓ No breakage. See warnings above.")
    else:
        print("✓ Integrity checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
