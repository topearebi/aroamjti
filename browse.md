---
layout: default
title: Browse
permalink: /browse/
description: Browse the archive by tag, by type, or by year.
---
{%- comment -%}
  The hub for the three discovery axes. Counts are computed at build time so
  this page cannot fall out of step with the archive — an earlier version
  hard-coded "Poetry, verse, prose", a vocabulary that had already been
  replaced. Nothing here needs editing when a tag, type, or year is added.

  NOTE: this is a .md file, so kramdown processes it. The markup below must sit
  flush against the Liquid with no blank lines between, or kramdown treats the
  block-level HTML as markdown content and the .browse-hub styling is lost.
{%- endcomment -%}
{%- assign all_tags = "" | split: "" -%}
{%- for post in site.posts -%}
  {%- for tag in post.tags -%}
    {%- assign all_tags = all_tags | push: tag -%}
  {%- endfor -%}
{%- endfor -%}
{%- assign tag_count = all_tags | uniq | size -%}
{%- assign years = site.posts | group_by_exp: "post", "post.date | date: '%Y'" | size -%}
<div class="browse-hub">
  <p class="browse-intro">Three ways into the archive.</p>
  <ul class="browse-hub-list">
    <li>
      <a class="browse-hub-link" href="{{ '/tags/' | relative_url }}">By tag</a>
      <span class="browse-hub-note">What a piece is about — {{ tag_count }} subjects, alphabetically.</span>
    </li>
    <li>
      <a class="browse-hub-link" href="{{ '/types/' | relative_url }}">By type</a>
      <span class="browse-hub-note">What kind of writing it is — journal, essay, poetry, fiction, fragments.</span>
    </li>
    <li>
      <a class="browse-hub-link" href="{{ '/archive/' | relative_url }}">By year</a>
      <span class="browse-hub-note">The whole record — {{ site.posts.size }} pieces across {{ years }} years, newest first.</span>
    </li>
  </ul>
</div>
