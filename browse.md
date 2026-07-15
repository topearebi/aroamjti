---
layout: default
title: Browse
permalink: /browse/
description: Browse the archive by tag, by type, or by year.
---
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
