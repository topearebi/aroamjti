# _drafts — work-in-progress posts

Anything in this folder **syncs across all your devices** (Obsidian on phone,
SilverBullet, GitHub web) but is **never published** to the live site. This is
Jekyll's built-in draft mechanism: GitHub Pages simply doesn't build `_drafts/`.

## Why a folder instead of `published: false`

Both work, but a folder is cleaner for capture-on-the-go:

- **No date or filename rules apply here.** You can name a draft anything
  (`idea-about-time.md`, `untitled.md`) and worry about the `YYYY-MM-DD-slug`
  format only at publish time.
- It keeps half-formed thoughts physically separate from the published
  archive, so `_posts/` stays a clean record of what's actually live.
- Nothing here can leak to the site by accident — the whole folder is
  invisible to the build.

Use `published: false` inside `_posts/` only for the rarer case of a *finished,
dated* post you want to temporarily pull from the site.

## How to start a draft

Copy `_TEMPLATE.md`, rename it to whatever you like, and write. The template
carries the correct front matter and the publish checklist.

## How to publish

Follow the checklist at the bottom of `_TEMPLATE.md`: add a timezone-stamped
`date:`, rename to `YYYY-MM-DD-slug.md`, and move the file into `_posts/`.

## Note on SilverBullet / Obsidian syntax

Post bodies should be **portable Markdown** — Jekyll (via kramdown) is the
publishing authority. SilverBullet `[[wikilinks]]`, `#inline-tags`, or other
editor-specific syntax will render as literal text on the site, so keep those
out of anything destined for `_posts/`. They're fine in private notes that
never leave `_drafts/`.
