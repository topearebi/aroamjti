# A Record Of A Mortal's Journey To Immortality

A personal blog and writing archive, built to be owned, portable, and
maintainable for a decade without touching settings. This document is both a
colophon and a rebuild blueprint: it records not just *what* the site is, but
*why* each choice was made, so the whole thing could be reconstructed — or
moved to another platform — from principles rather than guesswork.

---

## Guiding philosophy

Every decision on this site traces back to a small set of principles. When in
doubt, these break the tie.

1. **Own the content, always.** Everything that matters lives as plain
   Markdown files with front matter. No databases, no proprietary formats, no
   content trapped in a plugin's internal state. If the site had to move to a
   different platform tomorrow, a script reading the `.md` files' front matter
   and body would be enough to reconstruct it. Portability is the point.

2. **Sustainability over cleverness.** If a feature needs ongoing maintenance,
   a build step that can break, or a dependency that might vanish, it is ruled
   out — even if it is more powerful. The site should still build in ten years
   with no intervention.

3. **Zero JavaScript.** The site ships no JS. This constrains some features
   (no dark-mode toggle button, no client-side search, no comments) but buys
   permanence, speed, privacy, and simplicity. Where a feature seems to need
   JS, the answer is either a CSS-only equivalent or not doing it.

4. **No build tooling beyond what GitHub Pages runs natively.** No SCSS, no
   bundlers, no Node pipeline. Native CSS custom properties replace everything
   SCSS would offer. Push Markdown; the site rebuilds itself.

5. **Findable by a deliberate human, not by machines.** The site should be
   discoverable by a person who goes looking, but not mined by AI crawlers and
   not aggressively advertised to search indexes.

6. **The words come first.** It is a writing site. Design, structure, and
   features exist to make reading frictionless and to keep the content
   central — never to decorate around it.

---

## Platform & build

- **Jekyll on GitHub Pages**, built from the web interface only — no command
  line required for daily use. GitHub Pages has native Jekyll support: push
  Markdown, it builds automatically, no CI configuration needed.
- **Custom subdomain** via a `CNAME` file plus a DNS CNAME record pointing the
  subdomain at `USERNAME.github.io`. `url` in `_config.yml` matches.
- **Markdown processor:** kramdown (the GitHub Pages default).

### Plugins — only the two that are safe and serve the principles

GitHub Pages allows a fixed allowlist of plugins. Only two are used, both
maintained as part of the platform (so they will not rot):

- `jekyll-paginate` — paginates the home page. Note: its successor
  `jekyll-paginate-v2` is **not** on the GitHub Pages allowlist and will not
  run on a default build. Use `jekyll-paginate` only.
- `jekyll-feed` — generates the RSS feed at `/feed.xml`. RSS is kept
  deliberately: it is how a human follows the site without an algorithm.

`jekyll-sitemap` was **deliberately removed.** A sitemap.xml hands crawlers a
complete content map, which works against the "not mined" principle. Search
engines still index the site fine without it.

---

## Repository structure

```
.
├── _config.yml            Site settings, nav, pagination, plugins, collections
├── _layouts/
│   ├── default.html       Master template: head, nav, footer, social icons
│   ├── post.html          Adaptive post template (handles all post types)
│   └── work.html          Template for standalone long-form "works"
├── _posts/
│   └── YYYY-MM-DD-*.md     Journal posts
├── _works/
│   └── *.md               Long-form standalone compositions (a collection)
├── assets/
│   ├── style.css          All styling (native CSS custom properties)
│   └── images/            Repo-hosted images, organised by year / work
├── index.html             Home page (paginated post list, newest first)
├── about.md               About + a "now" section
├── books.md               Reading log (curation-first, series grouped)
├── blogroll.md            Curated outbound links
├── works.md               Index of the _works collection
├── 404.html
├── robots.txt             Blocks AI crawlers; allows normal search
├── favicon.ico            Serif monogram on warm paper
├── apple-touch-icon.png
├── LICENSE                CC BY-NC-ND 4.0 for the writing
├── CNAME
├── Gemfile                Local preview only
└── .gitignore
```

Generated automatically (never create these by hand): `feed.xml`, the
`/page2/`, `/page3/` … pagination pages, and each work's output page.

---

## Content model

### Front matter is the real database

Everything portable lives in front matter. Nothing meaningful is stored
anywhere else.

**Every post requires** exactly three fields:

```yaml
layout: post
title: "Quote titles that contain a colon"
date: 2021-08-18 23:00:00 +0000
```

The **timezone offset on the date is not optional.** Without it, posts written
near midnight can shift days depending on the build server, making sort order
unstable. Always include it.

**Optional post fields:**

- `tags: [lowercase, list]` — pure metadata; never affects the URL. Tags are
  always lowercased and de-duplicated by concept (e.g. `poems` and `poetry`
  were merged to one).
- `type: poetry` — switches the post to verse layout via CSS. The default
  (omit it) is prose. This renders identically to a **work** with
  `format: poetry` (see Works below): both share one CSS rule, so a plain
  poem looks the same whether it is a post or a work. **Adding a new post
  type means adding a CSS rule for `.post--TYPENAME`, never a new template.**
- `date_note:` — a small visible footnote for posts whose date is approximate
  (used for pre-2014 archive material with no known original dates).
- `updated:` — shown beside the date if an old post is meaningfully revised.
- `published: false` — keeps a draft out of the built site.

**Deliberately avoided:** `categories` (Jekyll injects them into the URL,
coupling taxonomy to permalinks — use tags instead); `slug` (the filename owns
it); per-post `author` (set once in `_config.yml`).

### Filenames

Posts must be named `YYYY-MM-DD-title.md`. The date and slug are read from the
filename; the permalink is `/:year/:month/:day/:title/`.

### One adaptive template, not many

`post.html` reads `page.type` and sets a class (`post--poetry`,
`post--prose`) on the article. All post types share the same HTML structure;
only CSS differs. This is why poetry, prose, and any future type never need
separate templates — the sustainability win is that new types are a CSS rule,
not a new file.

---

## Pages & sections

- **Home** — paginated list of posts, newest first, dates in monospace
  tabular figures aligned in a column (the site's one deliberate visual
  signature: a "ledger of time," fitting a journal preoccupied with time).
- **About** — includes a periodically-updated "now" section (current focus),
  in the old-web tradition.
- **Books** — a reading log that is *curation-first*: recent years are dated
  where dates are reliable; everything older is grouped by series (nested) or
  author, since exact per-book dates were lost. Bold marks standout books.
  Serves two audiences — a personal log and a recommendation resource.
- **Blogroll** — curated outbound links, newest first, one-line notes,
  optional loose tags. Zero placement friction: prepend and go.
- **Works** — a Jekyll *collection* (`_works/`) for long-form standalone
  compositions that should be read whole, kept out of the post feed. The
  index sorts by an `order` field, so adding a work is dropping in a file.
  Each work sets a `format:` field that picks its rendering (parallel to a
  post's `type:`):
  - `format: poetry` — simple left-aligned verse. Same CSS as a post's
    `type: poetry`; use for a plain poem (e.g. *Contrition*). Single line
    breaks are kept; a blank line starts a new stanza.
  - `format: verse` — composed/sectioned verse: centered, with
    `<section class="work-section">` blocks, optional
    `<p class="work-label">` framing, and interleaved `<figure class="work-figure">`
    artwork. Use for richer illustrated works (e.g. *10000 Days of the Sun*).
  - `format: prose` — normal paragraphs (the default).

  Long image-based works are transcribed to real text on-site with the
  original offered as a downloadable file (portability + accessibility
  without losing the artifact). **A new format is a CSS rule for
  `.work-body--FORMAT`, never a new template** — the same adaptive-template
  principle as posts.

---

## Design system

The look is warm and literary, and it is defined once as CSS custom
properties, then flipped for dark mode. Cohesion across every page comes from
all of them sharing these tokens.

- **Palette:** warm off-white paper, warm near-black ink (never pure black —
  it vibrates on warm paper and tires the eye), an ochre/terracotta accent
  used sparingly for links and markers, hairline rules. Dark mode uses a warm
  near-black ground and warm off-white text (never pure white), with the
  accent **lifted brighter** because the light-mode ochre is too dark to read
  on a dark ground.
- **Dark mode, no JS:** `@media (prefers-color-scheme: dark)` overrides the
  variables. It follows the reader's system setting. There is deliberately no
  toggle — a toggle needs JavaScript.
- **Typography:** a system serif stack (no web-font download, no external
  dependency, no load cost) for body; a monospace utility face for dates,
  meta, and tags. Reading measure capped near 66 characters — the proven
  comfortable line length. Generous line-height for prose.
- **Poetry** gets its own rhythm. Plain verse (post `type: poetry` or work
  `format: poetry`) preserves line breaks with `white-space: pre-wrap` — tight
  *within* a stanza, a gap *between* stanzas (a blank line in the source) via
  paragraph spacing — and long lines still wrap on narrow screens. Composed
  works (`format: verse`) instead center their `.work-section` blocks and use
  `white-space: pre-line`. Italic titles mark verse apart from prose at a glance.
- **Responsive:** on narrow screens the home list stacks dates above titles
  rather than crushing them into a column.

---

## Navigation, footer, icons

- **Nav** is data-driven from a `nav:` list in `_config.yml` — one place to
  edit. Order: Home · About · Books · Works · Blogroll.
- **Footer** carries icon-only social links (inline SVG, so no icon font or
  library; they inherit text colour and adapt to dark mode automatically),
  driven by a `social:` list in `_config.yml`, plus the copyright and license
  line.
- **Icons** are a serif monogram on warm paper — favicon (multi-resolution
  .ico) and a 180×180 apple-touch-icon. Kept simple because favicons render as
  small as 16px, where simpler always wins.

---

## Discoverability & anti-scraping

The goal: findable by a human searching by name, not mined by machines. This
is about *discovery*, not *access* — a public static site cannot truly prevent
scraping, so these are consent signals that compliant crawlers honour, not a
wall.

- **`robots.txt`** disallows ~20 named AI training/scraping crawlers (GPTBot,
  ClaudeBot, Google-Extended, CCBot, PerplexityBot, Bytespider, etc.) while
  allowing normal search engines. The list is plain text — add a new
  `User-agent` / `Disallow: /` block whenever a new crawler appears.
- **`<meta name="robots" content="noai, noimageai">`** in the head — an
  emerging "don't train on this" signal, separate from search indexing, so it
  does not affect being findable by name.
- **No sitemap** (see plugins) — nothing advertises a full content inventory.
- **RSS is kept** — deliberate human following, not algorithmic discovery.

---

## Licensing

The **writing** is licensed **CC BY-NC-ND 4.0** (share with attribution; no
commercial use; no derivatives) — a Creative Commons license, correct for
creative work rather than a software license. The **site code** (layouts, CSS,
config) is separate and freely reusable; the `LICENSE` file states this split
explicitly so the CC terms are not accidentally applied to the templates.

---

## Writing & publishing workflow

Writing happens mostly on mobile. The stack separates *where you write* from
*how you publish*:

- **Write** in Obsidian (a dedicated blog-only vault — kept small and separate
  from other notes so mobile Git sync stays stable).
- **Publish** by syncing that vault to the repo. A post template pre-fills the
  front matter (layout, title, timezone-stamped date) so writing a post is
  "new note from template → write → sync," never hand-typing front matter or
  filenames.
- **Safety habit:** the draft exists as a plain note in the vault before sync
  touches it, so a failed sync never costs writing — at worst, publish that one
  post via the GitHub web interface. Pull before writing; push when done; never
  edit the same post on two devices with unsynced changes.

---

## Migrating content in (how the archive was built)

The existing archive was migrated from Bear blog and a Google Docs poetry
collection. The reusable lessons:

- **Bear → Jekyll:** remap front matter (`published_date` → `date` with a
  timezone offset; comma tags → a YAML list; drop Bear-only fields). Rename
  files to `YYYY-MM-DD-slug.md`. Convert CRLF to LF. Insert blank lines between
  run-together paragraphs so kramdown renders them — **but** preserve poems and
  lists (never blindly reflow). Never edit the words themselves; migrations
  surface typos, but fixing them is a separate, deliberate pass.
- **Titles with colons** must be quoted in YAML or the build breaks.
- **Duplicate slugs** must be disambiguated (append a number) or files collide.
- **Detecting structure in a Word doc** (e.g. splitting a poetry collection):
  read the raw formatting XML, not the extracted text — font size and
  alignment are the only reliable boundary markers, and they are lost in a
  plain-text export. Export as `.docx`, not `.txt` or `.pdf`.
- **Approximate dates:** when original dates are unknown, assign sequential
  dates backward from a known cutoff purely for stable ordering, and add a
  visible `date_note` so the imprecision is honest.

---

## Hard-won gotchas (things that cost time to discover)

- `{% feed_meta %}` (a `jekyll-feed` Liquid tag) can fail the build on GitHub
  Pages. Use a plain `<link rel="alternate" type="application/rss+xml">` in the
  head instead — it needs no plugin at parse time and cannot break the build.
- `jekyll-paginate-v2` is not allowed on GitHub Pages. Use `jekyll-paginate`.
- `jekyll-paginate` only paginates an `.html` file (hence `index.html`, not
  `index.md`).
- A filename with a space or capital letters (e.g. from a bad upload) produces
  a broken URL — keep post filenames strictly `YYYY-MM-DD-lowercase-slug.md`.
- "Deployment failed, try again later" at the `deploy-pages` step is almost
  always a transient GitHub-side issue, not a repo problem — re-run the job;
  check githubstatus.com if it persists.
- Hand-drawn SVG brand icons read fine at footer size but are approximations;
  swap in official paths (e.g. Simple Icons) if exactness is ever needed.
- Never hotlink images from a host you do not control — store them in
  `assets/images/` so they cannot vanish.

---

## Rebuild checklist (from zero)

1. New repo; enable GitHub Pages (Settings → Pages → branch, root).
2. `CNAME` + DNS CNAME record → `USERNAME.github.io`; set `url` in `_config.yml`.
3. `_config.yml`: title, author, nav, `paginate: 25`, the two plugins, the
   `works` collection, and the `social:` list.
4. `_layouts/default.html` (head with icons + RSS link + noai meta; nav;
   footer with social SVGs), `post.html` (adaptive), `work.html`.
5. `assets/style.css` — the token system and dark-mode override.
6. `index.html`, `about.md`, `books.md`, `blogroll.md`, `works.md`.
7. `robots.txt`, `404.html`, `LICENSE`, favicon + apple-touch-icon,
   `.gitignore`, `Gemfile`.
8. Add posts to `_posts/`, works to `_works/`. Push. It builds itself.
