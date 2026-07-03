---
layout: default
title: Works
permalink: /works/
---
# Works

Longer, self-contained pieces — written collections meant to be read whole,
rather than the daily entries of the journal.

<ul class="works-list">
  {% assign works = site.works | sort: "order" %}
  {% for work in works %}
  <li class="work-item">
    <a class="work-link" href="{{ work.url | relative_url }}">{{ work.title }}</a>
    {% if work.subtitle %}<span class="work-subtitle">{{ work.subtitle }}</span>{% endif %}
    {% if work.year %}<span class="work-year">{{ work.year }}</span>{% endif %}
    {% if work.blurb %}<p class="work-blurb">{{ work.blurb }}</p>{% endif %}
  </li>
  {% endfor %}
</ul>
