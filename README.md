# A Record Of A Mortal's Journey To Immortality

A personal blog and writing archive, built to be owned, portable, and
maintainable for a decade without touching settings. This document is both a
colophon and a rebuild blueprint: it records not just *what* the site is, but
*why* each choice was made, so the whole thing could be reconstructed — or moved
to another platform — from principles rather than guesswork.

---

## Guiding philosophy

Every decision traces back to a small set of principles. When in doubt, these
break the tie.

1. **Own the content, always.** Everything that matters lives as plain Markdown
   with front matter. No databases, no proprietary formats, no content trapped
   in a plugin's internal state. A script reading the `.md` files would be
   enough to reconstruct the site elsewhere. Portability is the point.

2. **Sustainability over cleverness.** If a feature needs ongoing maintenance, a
   build step that can break, or a dependency that might vanish, it is ruled out
   — even if more powerful. The site should still build in ten years with no
   intervention.

3. **Zero JavaScript.** No JS ships. This costs some features (no dark-mode
   toggle, no client-side search, no comments) but buys permanence, speed,
   privacy, and simplicity. Where a feature seems to need JS, the answer is a
   CSS-only equivalent or not doing it.

4. **No build tooling beyond what GitHub Pages runs natively.** No SCSS, no
   bundlers, no Node. Native CSS custom properties replace everything SCSS would
   offer. Push Markdown; the site rebuilds itself.

5. **Findable by a deliberate human, not by machines.** Discoverable by a person
   who goes looking; not mined by AI crawlers.

6. **The words come first.** Design, structure, and features exist to make
   reading frictionless — never to decorate around the writing.

7. **Coherent navigation of mood.** The north star for the taxonomy. A reader
   browsing a tag should stay inside one emotional weather system. This is why
   the tags are few, capped, and ruthlessly bounded (see *Taxonomy*).

8. **Fix it in CSS, never in the source.** Markdown fights verse in several
   specific ways. Every one of them is answered with a stylesheet rule rather
   than an escape, a `<br>`, or a trailing double-space — so the `.md` files
   stay clean, readable, portable plain text. This principle is why the poetry
   rules look the way they do.

---

## Platform & build

- **Jekyll on GitHub Pages**, edited from the web interface and Obsidian — no
  command line required. Push Markdown; it builds automatically.
- **Custom subdomain** via `CNAME` plus a DNS CNAME record pointing at
  `USERNAME.github.io`. `url` in `_config.yml` matches.
- **Markdown processor:** kramdown (the GitHub Pages default).

### Plugins — only the two that are safe

GitHub Pages allows a fixed allowlist. Only two are used, both maintained as
part of the platform (so they cannot rot):

- `jekyll-paginate` — paginates the home page. Its successor
  `jekyll-paginate-v2` is **not** allowlisted and will not run.
- `jekyll-feed` — generates `/feed.xml`. RSS is kept deliberately: it is how a
  human follows the site without an algorithm.

`jekyll-sitemap` was **deliberately removed** — a sitemap hands crawlers a
complete content map, working against the "not mined" principle.

Everything else — the browse pages, tag descriptors, per-type numbering,
composed works, and work backlinks — is **pure Liquid**. No plugin was added to
achieve any of it.

---

## Repository structure

```
.
├── _config.yml            Settings, nav, pagination, plugins, collections
├── _data/
│   └── tags.yml           Canonical tag descriptors (drives /tags/)
├── _layouts/
│   ├── default.html       Master template: head, nav, footer, social icons
│   ├── post.html          Adaptive post template + type kicker + work backlink
│   └── work.html          Unified work template (inline + composed)
├── _posts/
│   └── YYYY-MM-DD-*.md    Every post
├── _drafts/
│   ├── TEMPLATE.md        Copy to start a draft (never published)
│   └── README.md          Drafts workflow
├── _works/
│   └── *.md               Long-form compositions (a Jekyll collection)
├── assets/
│   └── style.css          All styling (native CSS custom properties)
├── .github/
│   ├── workflows/
│   │   ├── integrity.yml     Push gate
│   │   └── maintenance.yml   Weekly link/tag reports (non-blocking)
│   └── scripts/
│       ├── check_integrity.py
│       ├── tag_report.py
│       └── link_check.py
├── index.html             Home (paginated post list, newest first)
├── browse.md              Browse hub → tags / types / archive
├── tags.html              All tags, alphabetical, with descriptors + counts
├── types.html             All types, curated order, with descriptions
├── archive.html           Every post by year
├── about.md               About + a "now" section
├── books.md               Reading log
├── blogroll.md            Curated outbound links
├── works.md               Index of the _works collection
├── 404.html
├── robots.txt             Blocks AI crawlers; allows normal search
├── humans.txt
├── favicon.ico · apple-touch-icon.png
├── LICENSE                CC BY-NC-ND 4.0 for the writing
├── CNAME · Gemfile · .gitignore · .gitattributes
└── README.md              This file
```

Generated automatically (never create by hand): `feed.xml`, `/page2/` … , and
each work's output page.

---

## Content model

### Front matter is the real database

**Every post requires:**

```yaml
layout: post
title: "Quote titles that contain a colon"
date: 2021-08-18 23:00:00 +0000
type: poetry
tags: [love]
```

The **timezone offset is not optional.** Without it, posts written near midnight
shift days depending on the build server, making sort order unstable. This is
one of the few things the integrity gate hard-fails on.

**Times matter too.** Where several posts share a date, give each a distinct
time (09:00, 10:00, 11:00 …). Two posts of the same type with an identical
timestamp tie, and their per-type numbers (see *The type kicker*) are then
decided by Jekyll's internal tiebreak rather than by you — not broken, but
arbitrary.

**Optional post fields:**

- `date_note:` — a visible footnote where a date is approximate. Over half the
  archive carries this: pre-2014 material whose real date is unknown, where the
  date is a placeholder for ordering only.
- `updated:` — shown beside the date if an old post is meaningfully revised.
- `published: false` — keeps a finished, dated post temporarily unpublished.

**Deliberately avoided:** `categories` (Jekyll injects them into the URL,
coupling taxonomy to permalinks); `slug` (the filename owns it); per-post
`author` (set once in `_config.yml`). And notably **no work/series field** — a
post never records that it belongs to a work; see *Works*.

### Filenames

`YYYY-MM-DD-lowercase-slug.md`. The date and slug are read from the filename;
the permalink is `/:year/:month/:day/:title/`. A filename with a space or a
capital produces a broken URL. If the filename date and the front-matter date
disagree, Jekyll uses the front matter — which is silent, and was the cause of
one real ordering collision.

### One adaptive template, not many

`post.html` reads `page.type` and sets a class (`post--poetry`, `post--essay`
…). All types share one HTML structure; only CSS differs. **A new type is a CSS
rule, never a new template.**

Only `poetry` currently carries type-specific styling, and that is correct
rather than an omission: prose types render properly with the base rules, and a
rule added for symmetry alone would be dead weight. The class hook exists on
every type for the day one genuinely needs it.

---

## Taxonomy

The source of truth for classification. The whole point is to stop drift: a new
tag is a deliberate decision, not something invented mid-draft.

**Two independent axes, never mixed:**

- **`type:`** — the *form* of the piece. Exactly one per post.
- **`tags:`** — the *subject/mood*. **Strict maximum of two.**

"Is it a poem?" is a type question. "Is it about love?" is a tag question. A
love poem is `type: poetry` + `tags: [love]`.

### The rules

1. **1 tag minimum, 2 maximum.** Never three. If a post seems to need three, you
   have not yet found its dominant weather.
2. **Zero tags is valid** — but only for `fragments`: a genuinely themeless
   jotting. Do not force a theme onto a post that has none.
3. **Tags name subject or mood, never technique.** The single exception is
   `satire`. No future tag may name a technique — no "dialogue", no
   "epistolary", no "list-poem". One declared exception stays clean; two becomes
   a second axis nobody decided to build.
4. **Force the dominant choice.** Name the one weather system a reader is
   immersed in, plus at most one genuine secondary. If everything is tagged
   everywhere, the tags mean nothing.

### Tie-breaking (when a post feels like 3+ tags)

1. What is the reader's dominant *feeling* leaving this post? That is tag one.
2. Is a second thread strong enough that its absence would misrepresent the
   post? If unsure, there isn't — stop at one.
3. Am I tagging a theme merely *present* rather than *driving*? Cut it.
4. Two tags from the same family (love + heartbreak; struggle + malice)? Pick
   the stronger.

### Types (5) — the form axis

Decision order — take the first that applies:

1. **`poetry`** — stanza-based, rhythmic, lyrical. Lineated verse of any length.
   A three-line image and a 500-word lyric are both poetry.
2. **`fiction`** — invented. Characters or events that aren't lived experience.
   *If it happened to you but is told story-style, it is journal, not fiction.*
   For narrative verse: if it has characters and a plot, it is fiction
   regardless of whether it rhymes.
3. **`fragments`** — set down, not finished. The test is **intent, not length**:
   did you consider it done, or just jot it and leave it? A long unpolished
   scribble is a fragment; a tight finished couplet is poetry.
4. **`journal`** — true, personal, time-bound. The record of a day, a meal, a
   mood. *Records* rather than reflects outward.
5. **`essay`** — true and personal, but travels outward: philosophy, social
   commentary, polished thought. **Record vs. reflect** is the line — if you
   could remove the personal anecdote and still have a piece, it's an essay; if
   the anecdote *is* the piece, it's a journal.

### Tags (15) — the subject axis

Descriptors live in `_data/tags.yml`, which drives `/tags/`. Each tag below
lists its boundary against the tag it is most often confused with — the boundary
is the useful part; descriptions alone don't help you choose.

| Tag | What it is | Boundary |
|---|---|---|
| `love` | affection, attachment, longing; the beginning and middle of the arc | vs `desire`: love is the bond, desire is the body. vs `heartbreak`: alive or hoped-for = love; over = heartbreak |
| `desire` | physical intimacy, passion, heat | if removing the body leaves the poem intact, it's love |
| `heartbreak` | endings, loss of love, the grief of a bond's close | vs `struggle`: heartbreak has a named cause — a lost person |
| `struggle` | **personal, felt** suffering: depression, fear, numbness, healing | vs `malice`: suffering you undergo, not vice you enact. vs `haunting`: real pain, not surreal dread. vs `existential`: personal, not cosmic |
| `malice` | human darkness as subject: envy, betrayal, cruelty, cold self-interest | **the active-vice rule** — active vice, or the external pull of the dark = malice; internal suffering and failing to resist = struggle |
| `mortality` | death itself, time passing, the body's limits | vs `existential`: death *as death*, not death as meaning |
| `existential` | cosmic indifference, duality, meaning, the human place in an uncaring world | *indifferent* cosmos = existential; *contested* divine = faith; society and ethics = philosophy |
| `haunting` | the surreal and dreadful: demons, voids, shadows, unreality | unreal dread, not felt fear |
| `neurodivergence` | autism, time-blindness, a differently wired mind | only when the wiring is the *subject*, not the backdrop |
| `philosophy` | human nature, society, ethics, the examined life | the tag most at risk of becoming a catch-all. If a post is only *loosely* reflective, find its truer mood first |
| `faith` | religion, belief, doubt, the sacred — the **contested** cosmos | wrestling with the divine = faith; its absence = existential |
| `growth` | discipline, practice, progress, mastering something | **the experience/effort rule** — being in the world (a meal, a walk, a date) = life; the effort to change or master (a workout log, a habit) = growth |
| `life` | everyday lived experience: food, places, the body, dating, work | see `growth`. `life` is the *subject*; `journal` is the *form* — don't confuse the axes |
| `craft` | the making of art: the muse, creative block, the writer and the word | making art = craft; practising any skill = growth |
| `satire` | **the one mode-tag.** The comic and critical register | marks *voice*, not mood — almost always pair it with a subject tag so the post also lives in its true weather |

### Adding to the taxonomy later

- A new **subject** may become a tag only if you expect ≥3–4 posts *where it is
  the dominant note*. A theme that is always the second-strongest thing on a
  post never earns a tag — this is why "writing" didn't, while `craft`, reframed
  around *the making*, did.
- New **types** should be rare. Add a sixth only for a genuinely new *form*.
- When unsure, prefer an existing tag. Drift is the enemy.
- Record it **here first**, then in `_data/tags.yml`, then in `VALID_POST_TYPES`
  in `check_integrity.py` if it is a type, then add the CSS.

---

## The type kicker

Every post opens with its form and an ascending per-type number:

```
POETRY № 115
Like Gravity
November 27, 2016
```

It names the weather before the reader reads a word — the north star applied at
the post level rather than only at `/browse/`.

**The number is computed at build time** in `post.html`: `site.posts` is
reversed and same-type posts are counted until this one is reached. Nothing is
stored on the post.

**It counts from the oldest, deliberately.** № 1 means *the first of this type I
ever wrote* — a fact about the archive. Counting from the newest was rejected:
every new post would shift every existing number, permanently and by design.
Ascending converges instead. Inserting a rediscovered old post only shifts the
posts after it, and since the pre-2014 archive is finite and closing, that
shifted set shrinks with every piece found. Recent posts, which is where readers
land, never move.

**Cost:** an O(n) loop per post (~40k iterations at 200 posts). Fine at this
scale; it grows quadratically, so revisit if the archive reaches thousands.

**Precondition:** unique timestamps within a type. See *Front matter*.

---

## Pages & sections

- **Home** — paginated posts, newest first; dates in monospace tabular figures
  aligned in a column (the site's one visual signature: a "ledger of time").
- **Browse** — a hub linking the three discovery axes, framed by what each
  answers: tags are *what a piece is about*, types are *what kind of writing it
  is*, the archive is *the whole record*. Its counts are computed at build time
  so the hub cannot fall out of step. All three pages are pure Liquid and
  self-maintaining: a new tag, type, or year appears automatically.
  - **`/tags/`** — every tag alphabetically with its descriptor (from
    `_data/tags.yml`) and post count. Tags *not* in that file render without a
    descriptor under **Unsorted** — a deliberate migration dashboard: anything
    appearing there is drift to clean up.
  - **`/types/`** — the five types in curated reading order (journal · essay ·
    poetry · fiction · fragments) with teaching descriptions. Empty types are
    hidden; untyped posts collect under **Unclassified**.
  - **`/archive/`** — every post by year, newest first.
- **About** — includes a periodically-updated "now" section.
- **Books** — a curation-first reading log; recent years dated, older grouped by
  series or author. Bold marks standouts.
- **Blogroll** — curated outbound links, newest first.
- **Works** — see below.

---

## Works

A **work** is a curated reading order laid over posts — a view, not a container.
`_works/` is a Jekyll collection kept out of the post feed; the index sorts by an
`order` field.

### The central property

**Posts are never edited and never know they belong to a work.** Membership
lives only on the work's side. A post carries no `work:` or `series:` field —
nothing at all. This is what makes adoption non-destructive: a referenced post
keeps its normal life in the feed and in `/tags/`, gaining no new presence
anywhere.

It also means the two ways a work comes into being collapse to the same one-list
edit:

- *Planning a collection* — create the work file, append each poem's slug as you
  publish it.
- *A collection drawing on existing posts* — create the work file, list the
  slugs. Nothing about those posts changes.

Making a new work is: create a file, list the parts, write the context. Never
"go modify N published posts."

### Composition — `parts:`

A work may carry an ordered list of parts. Three kinds, mixable in any order:

```yaml
parts:
  - heading: "III"              # a section marker
  - inline: |                   # literal text, transcribed here
      A letter from me to you...
  - post: some-post-slug        # pulls that post's title + body
```

The reader cannot tell which chapters are pulled from posts and which are
transcribed inline — that seam is deliberately invisible, which is why
`.work-part--inline` is intentionally left unstyled.

### Appendix — `beyond:`

Separately, a work may list posts that belong to its body of work but were not
part of the published selection:

```yaml
beyond_title: "Beyond the book"
beyond_note: "Poems from the same season that did not make the selection."
beyond:
  - the-most-awake
  - like-gravity
```

### Open works and closed works

This distinction decides whether `beyond:` applies at all:

- **An open work** was cherry-picked from a larger, still-growing pool. The book
  is a *selection*; more of the body of work exists and may yet surface.
  `beyond:` names that gap, and the download note says the text above is the
  curated selection. *(10000 Days of the Sun.)*
- **A closed work** is complete: the book *is* the body of work. Anything absent
  from the site is missing for a reason other than curation — in Contrition's
  case an **authorship boundary**, since the omitted half is the co-author's
  words and the blog carries only its author's. There is no pool to reveal, so a
  `beyond:` section would not merely be empty, it would be false. A closed work
  stays inline permanently. That is a correct end state, not an unfinished
  migration.

### Backlinks

A post that appears in any work's `beyond:` or `parts:` shows *Part of [work]*
in its footer. This is **derived at build time** by scanning `site.works` for the
post's slug — consistent with the central property, nothing is stored on the
post. A closed work with no references produces no backlinks, correctly.

### Backwards compatibility

A work with no `parts:` renders `{{ content }}` exactly as a plain inline
document, so the composed model was added without touching what already worked.
An unresolvable slug renders a quiet placeholder rather than breaking the build
— a half-migrated work is always safe.

### Work fields

| Field | Purpose |
|---|---|
| `title` `subtitle` `year` `order` | identity; `order` sorts the index |
| `format` | `poetry` or `prose` — picks the CSS, parallel to a post's `type:` |
| `blurb` | shown on the `/works/` index |
| `context` | markdown intro on the work page (`intro:` is the older plain-text version) |
| `media` | list of `{src, caption}` images |
| `original_url` `original_label` `original_note` | the downloadable artifact and its framing |
| `parts` | the ordered composition (above) |
| `beyond` `beyond_title` `beyond_note` | appendix of post references |

Long image-based works are transcribed to real text on-site with the original
offered as a download — portability and accessibility without losing the
artifact. **A new format is a rule for `.work-body--FORMAT`, never a new
template.**

---

## Design system

Defined once as CSS custom properties, then flipped for dark mode. Every page
shares the tokens; that is where cohesion comes from.

- **Palette:** warm off-white paper, warm near-black ink (never pure black — it
  vibrates on warm paper), an ochre/terracotta accent used sparingly, hairline
  rules. Dark mode uses a warm near-black ground and warm off-white text (never
  pure white), with the accent **lifted brighter** — the light-mode ochre is too
  dark to read on a dark ground.
- **Dark mode, no JS:** `@media (prefers-color-scheme: dark)` overrides the
  variables, following the reader's system setting. No toggle — a toggle needs
  JavaScript.
- **Typography:** a system serif stack (no web font, no external dependency, no
  load cost) for body; a monospace face for dates, meta, kickers, and tags.
  Measure capped near 66 characters.
- **Titles are set roman across every type.** Poetry titles were briefly italic;
  it was removed. Italic conventionally marks a title-of-a-work or emphasis, not
  a genre — using it to mean "this is a poem" is a private code the reader must
  learn, and with poetry two thirds of the archive it marked the norm rather
  than the exception.
- **Responsive:** on narrow screens the home list stacks dates above titles.

### Poetry — the one place CSS does real work

HTML collapses newlines into spaces. Without intervention every poem renders as
a run-on paragraph. Markdown offers no clean way out: trailing double-spaces are
invisible and fragile, `hard_wrap` would break prose site-wide, and `<br>` tags
pollute the source. So the stylesheet does it — principle 8.

**The central rule: `white-space: pre-wrap` goes on the text blocks (`p`, `li`),
never on the container.** This is the whole trap. A container holds not just text
but the HTML *source formatting* — the newlines kramdown emits between `</p>` and
`<p>`, around `<ul>`, around each `<li>`. Normal HTML collapses that inter-tag
whitespace to nothing; `pre-wrap` on the container renders every bit of it as a
real line break. Stanza gaps become the paragraph margin *plus* a line for the
newline after `</p>` *plus* a line for the newline before the next — three or
four blank lines where one belongs, and worse around lists, which carry more
tags. Scoping `pre-wrap` to `p`/`li` fixes it at the mechanism.

Two further collisions, both answered in CSS:

- **Indented lines become code.** Markdown turns any line indented 4+ spaces into
  `<pre><code>`. The concrete poems (*Tears For Bread*, *My Dreams Aren't Big
  Enough*) trip this. The code block is styled back into verse — the poem's face
  and size, no grey chrome, `white-space: pre` so the spatial layout cannot
  reflow, and horizontal scroll rather than a broken shape.
- **A leading `- ` becomes a bullet.** Attribution lines like *"- there are 10000
  forms of pleasure"* are list syntax. The marker is suppressed and the indent
  removed.

**Quoted verse inside prose** works the same way: `blockquote p` also gets
`pre-wrap`, so a stanza quoted mid-essay reads as a stanza. Write these as a real
markdown blockquote (`> ` on each line) — bare quote marks on their own lines
render as a stray paragraph containing one character.

The poetry rules serve posts (`type: poetry`) and works (`format: poetry`)
alike, so a poem renders identically either way.

---

## Navigation, footer, icons

- **Nav** is data-driven from `nav:` in `_config.yml`. Order: Home · Browse ·
  About · Books · Works · Blogroll.
- **Footer** carries icon-only social links (inline SVG — no icon font, they
  inherit text colour and adapt to dark mode), driven by `social:` in
  `_config.yml`, plus copyright and license.
- **Icons** are a serif monogram on warm paper. Kept simple: favicons render as
  small as 16px, where simpler always wins.

---

## Discoverability & anti-scraping

Findable by a human searching by name; not mined by machines. These are consent
signals compliant crawlers honour, not a wall — a public static site cannot truly
prevent scraping.

- **`robots.txt`** disallows ~20 named AI crawlers (GPTBot, ClaudeBot,
  Google-Extended, CCBot, PerplexityBot, Bytespider …) while allowing normal
  search. Add a new `User-agent` / `Disallow: /` block as new crawlers appear.
- **`<meta name="robots" content="noai, noimageai">`** — an emerging "don't train
  on this" signal, separate from search indexing.
- **No sitemap** — nothing advertises a full content inventory.
- **RSS is kept** — deliberate human following. The feed carries full post content
  and a complete Atom author element (`author` in `_config.yml` is a map: name /
  email / uri).
- **`humans.txt`** — small-web credit and a plain statement of the no-JS /
  no-tracking / findable-by-name ethos.

---

## Licensing

The **writing** is **CC BY-NC-ND 4.0** — a Creative Commons license, correct for
creative work. The **site code** (layouts, CSS, config) is separate and freely
reusable; `LICENSE` states the split explicitly so the CC terms are not
accidentally applied to the templates.

---

## Writing & publishing workflow

Writing happens mostly on mobile. The stack separates *where you write* from *how
you publish*:

- **Write** in Obsidian (a blog-only vault — kept small and separate so mobile
  Git sync stays stable).
- **Publish** by syncing that vault to the repo. A template pre-fills front
  matter, so publishing is "new note from template → write → sync."
- **Safety habit:** the draft exists as a plain note before sync touches it, so a
  failed sync never costs writing. Pull before writing; push when done; never
  edit the same post on two devices with unsynced changes.

### Drafts

`_drafts/` is Jekyll's built-in draft folder: files sync across devices but never
publish. No date or filename rules apply there. To publish: add a
timezone-stamped `date:`, rename to `YYYY-MM-DD-slug.md`, move to `_posts/`. See
`_drafts/README.md`.

### Cross-platform sync (Obsidian · SilverBullet · GitHub web)

The `.md` files are the single source of truth; anything a tool derives from them
must never sync.

- **`.gitignore`** ignores build output (`_site/`, caches), per-device editor
  state (`.obsidian/workspace*`, SilverBullet's index/`.db`), OS junk, `*.bak`.
- **`.gitattributes`** normalises line endings to LF, so editing one file on
  several OSes doesn't produce phantom "everything changed" diffs.

**One-writer discipline** is the real failsafe. Keep publish-bound Markdown
portable — SilverBullet `[[wikilinks]]` and `#inline-tags` render as literal text
on the site, so keep them to notes that stay in `_drafts/`.

---

## Automated tooling (`.github/`)

Two Actions look after quality and longevity. Both are standard-library Python
(no dependencies to rot) and readable from the GitHub web UI.

### Integrity gate — `integrity.yml` (every push)

Two severities, deliberately:

- **Errors (blocking)** — things that *silently break publishing*: a bad
  filename, a missing title, a date without a timezone offset, a work file Jekyll
  won't process. Not matters of taste; the post simply won't appear.
- **Warnings (non-blocking)** — chiefly an unrecognised or missing `type:`, or an
  unknown work `format:`. A vocabulary in flux must never block a publish: you
  may be mid-migration or trying a new form. The warning is a nudge, not a gate.

That split is the design. Blocking on genuine breakage is protection; blocking on
a judgement call punishes the work you were in the middle of.

It *validates*; it does not deploy. A failed check flags the commit but does not
take the live site down.

**When you add a new `type:` or `format:`, update the vocabulary sets at the top
of `check_integrity.py` and add the matching CSS rule** — the checker is the
enforcement, the CSS is the rendering, this README is the record.

### Maintenance reports — `maintenance.yml` (weekly, non-blocking)

Monday 06:00 UTC and on demand. These inform, never gate. Results appear in the
run's Step Summary (readable from mobile).

- **`tag_report.py`** — frequency table, style inconsistencies, near-duplicates,
  tags duplicating the `type:` field, single-use tags.
- **`link_check.py`** — dead, moved, and bot-hostile outbound links.

Scheduled Actions only fire from the default branch.

### The one maintenance habit worth keeping

Everything above runs itself. The single thing that needs a human is an
occasional audit of `philosophy` and of the deliberately thin tags (`life`,
`neurodivergence`, `craft`) — the first for re-bloat, the others because they
were kept as anchors for writing yet to come. If a thin tag is still thin after a
couple of years, merge or retire it. That one discipline keeps the taxonomy
honest at near-zero cost.

---

## Hard-won gotchas

- **Never paste `style.css` through a size-limited field.** It has been silently
  truncated at exactly 20,000 characters — the file ended mid-declaration, and
  every rule after that point (tag groups, the browse hub, works composition,
  backlinks) simply vanished from the live site while the page still loaded.
  Commit the file directly. If styling disappears wholesale, check the tail of
  the file and the brace balance before debugging anything else.
- **`white-space` is inherited and applies to the whitespace *between* child
  elements**, not just to text. This is why `pre-wrap` belongs on `p`/`li` and
  never on a container. It is the most counterintuitive rule in the stylesheet
  and the one most likely to be "tidied up" by a future self.
- **A blank line before block-level HTML in a `.md` file** makes kramdown treat
  it as markdown content and discard the structure — `browse.md`'s hub styling
  was lost exactly this way. Keep the markup flush against the Liquid.
- **Matching a post by slug in Liquid:** compare the last URL segment exactly
  (`p.url | split: '/' | last`). Using `contains` false-matches — `contains
  'love'` also hits `love-costs` and `run-love-run`.
- **Rendering a post inside a work:** pass `{{ ref.content }}` raw. Jekyll has
  already converted post markdown to HTML; running `markdownify` on it again
  mangles the output.
- A collection needs `output: true` for its items to have a `url` — without it,
  work pages don't exist and backlinks point nowhere.
- `{% feed_meta %}` can fail the build on GitHub Pages. Use a plain
  `<link rel="alternate" type="application/rss+xml">` in the head instead.
- `jekyll-paginate-v2` is not allowed on GitHub Pages. Use `jekyll-paginate`.
- `jekyll-paginate` only paginates an `.html` file (hence `index.html`).
- A filename with a space or capitals produces a broken URL.
- "Deployment failed, try again later" at `deploy-pages` is almost always a
  transient GitHub issue — re-run the job.
- Never hotlink images from a host you don't control — store them in `assets/`.
- Titles containing a colon must be quoted in YAML.

---

## Rebuild checklist (from zero)

1. New repo; enable GitHub Pages (Settings → Pages → branch, root).
2. `CNAME` + DNS CNAME → `USERNAME.github.io`; set `url` in `_config.yml`.
3. `_config.yml`: title, `author` (map: name / email / uri), nav, `paginate: 25`,
   the two plugins, the `works` collection (`output: true`), `social:`.
4. `_layouts/`: `default.html` (head with icons + RSS link + `rel="author"` +
   author/noai meta; nav; footer SVGs), `post.html` (adaptive + kicker +
   backlink), `work.html` (unified).
5. `assets/style.css` — the token system, the dark-mode override, and the poetry
   rules. Commit it as a file; do not paste it.
6. `_data/tags.yml` — the canonical tag descriptors.
7. `index.html`, `browse.md`, `tags.html`, `types.html`, `archive.html`,
   `about.md`, `books.md`, `blogroll.md`, `works.md`.
8. `robots.txt`, `humans.txt`, `404.html`, `LICENSE`, favicon +
   apple-touch-icon, `.gitignore`, `.gitattributes`, `Gemfile`.
9. `.github/workflows/` + `.github/scripts/`; `_drafts/` with its template.
10. Add posts to `_posts/`, works to `_works/`. Push. It builds itself.
