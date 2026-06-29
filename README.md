# My Blog

A minimalist Jekyll blog on GitHub Pages. Designed to stay maintenance-free:
push Markdown, and the site rebuilds itself. No settings to revisit over time.

## Repo structure

```
.
├── _config.yml          Site settings, nav, pagination, plugins
├── _layouts/
│   ├── default.html     Master template (head, nav, footer)
│   └── post.html        Adaptive post template (handles all post types)
├── _posts/
│   └── YYYY-MM-DD-*.md   Posts
├── assets/
│   ├── style.css        All styling
│   └── images/          Post images
├── index.html           Home page (paginated post list, newest first)
├── about.md             About page
├── books.md             Reading log
├── 404.html             Custom not-found page
├── robots.txt           Points crawlers to the sitemap
├── favicon.ico          Replace the placeholder with a real icon
├── apple-touch-icon.png Replace the placeholder (180x180)
├── CNAME                Custom subdomain
├── Gemfile              Local preview only
├── .gitignore
└── README.md
```

Generated automatically by plugins (do not create these yourself):
`feed.xml` (RSS), `sitemap.xml`, and the `/page2/`, `/page3/` ... pagination pages.

## Adding a post

Create `_posts/YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Your Title"
date: 2026-06-28 09:00:00 +0000
---

Your content in Markdown.
```

Commit and push. That's the whole workflow.

### Front matter reference

Required on every post:
- `layout: post`
- `title:` — quote it if it contains a colon
- `date:` — always include the timezone offset (e.g. `+0000`) to keep
  sort order and displayed dates stable regardless of build server.

Optional:
- `tags: [one, two]` — metadata only; never affects the URL.
- `type: poetry` — switches the post to line-break-preserving layout.
  Default (omit it) is `prose`. Add new types by adding a CSS rule for
  `.post--TYPENAME`, never a new template.
- `excerpt:` — one line used for previews / meta description.
- `updated: YYYY-MM-DD` — shown next to the date if you revise an old post.
- `published: false` — keeps a draft out of the built site.

## Pagination

Controlled in `_config.yml`: `paginate: 25` sets posts per page. Page 1 is `/`,
later pages are `/page2/`, `/page3/`, etc. Change the one number to adjust.

## Setup checklist (one time)

1. Push this repo to GitHub.
2. Settings -> Pages -> source: your branch (e.g. `main`), root folder.
3. Put your real subdomain in `CNAME`.
4. At your DNS provider, add a CNAME record:
   your subdomain -> `YOURUSERNAME.github.io`.
5. Set `url` in `_config.yml` to your subdomain, and update the Sitemap
   line in `robots.txt` to match.
6. Replace `favicon.ico` and `apple-touch-icon.png` with real icons.

## Preview locally (optional)

```
bundle install
bundle exec jekyll serve
```
Open http://localhost:4000

## Migrating posts from Bear

Use `bear_to_jekyll.py` (kept outside the repo or in a tools folder):

```
python3 bear_to_jekyll.py <bear-exports-dir> <output-dir>
```

Move the output into `_posts/`. The script remaps front matter, fixes
paragraph spacing for kramdown, preserves poems and lists, and never edits
your words.

## Moving off Jekyll later

Everything that matters lives in the `.md` files: front matter (title, date,
tags, type) plus the Markdown body. To migrate to any other platform, read the
front matter and body from each file in `_posts/`. Nothing meaningful is stored
anywhere else — no databases, no data files, no plugin-only state.
