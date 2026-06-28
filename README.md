# My Blog

A minimalist Jekyll blog hosted on GitHub Pages.

## Structure

```
.
├── _config.yml          Site settings, nav, domain
├── _layouts/
│   ├── default.html     Master template (nav + footer)
│   └── post.html        Template for individual posts
├── _posts/
│   └── YYYY-MM-DD-*.md  Your posts go here
├── assets/
│   └── style.css        All styling
├── index.html           Home page (lists posts, newest first)
├── about.md             About page
├── books.md             Reading log
├── CNAME                Your custom subdomain
└── Gemfile              For local preview only
```

## Adding a post

Create a file in `_posts/` named `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Your Title"
date: 2026-06-28
---

Your content in Markdown.
```

Commit and push. GitHub Pages rebuilds automatically.

## Setup checklist

1. Push this repo to GitHub.
2. Repo Settings → Pages → set source to your branch (e.g. `main`), root.
3. Edit `CNAME` to your real subdomain.
4. At your DNS provider, add a CNAME record pointing your subdomain
   to `YOURUSERNAME.github.io`.
5. Update `url` in `_config.yml` to match.

## Preview locally (optional)

```
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000
