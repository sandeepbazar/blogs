<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# blogs

Long-form writing by [Sandeep Bazar](https://github.com/sandeepbazar), published at
**<https://sandeepbazar.github.io/blogs/>**.

The source of truth is markdown in [`posts/`](posts/). `build.py` renders it into
`_site/` and a GitHub Actions workflow publishes that to Pages. There is no CMS,
no database and no tracker.

## Adding a post

Create `posts/YYYY-MM-DD-slug.md`:

```markdown
---
title: "The title, as it should appear"
dek: "One sentence. It becomes the card subtitle and the meta description."
date: 2026-08-15
slug: the-url-segment
category: "Agentic AI"     # or Kubernetes & MCP | IBM Fusion | Research & Life
tags: [agentic-ai, kubernetes]
cover: assets/covers/example.png   # optional
medium: https://medium.com/...     # optional; rendered as a backlink
canonical: self
status: published          # published | link | draft
---

The body, in markdown.
```

Commit and push. The workflow rebuilds and redeploys.

### `status` values

| Value | Effect |
|---|---|
| `published` | Renders a full page at `/blogs/<slug>/` and a card on the index |
| `link` | Card only; it links out to `medium:`. Use for essays not yet migrated |
| `draft` | Excluded from the build entirely. Write in the open |

`reading_time` is computed from the body, never authored.

## Cover art

`gen_covers.py` generates one animated SVG per post into `assets/covers/<slug>.svg`.
Each category has its own motif — orbits, a hexagon lattice, stacked planes, wave
bands — and the variation within a category is derived from a hash of the slug, so
a post always renders the same image but no two look alike. The animation is
declarative (it plays through an `<img>` tag) and switches off entirely under
`prefers-reduced-motion`.

Add `cover: assets/covers/<slug>.svg` to a post's front matter to use it. The
workflow regenerates covers on every build, so a new post cannot ship without one.

## Building locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py --serve   # http://localhost:8000/blogs/
```

The build **fails** rather than shipping a broken page. It rejects a missing
required field, an unknown category, a duplicate slug, a `cover` that does not
resolve, and any internal link pointing at a page that was never generated.

## Canonical URLs

This site is canonical for everything hosted here. For a post that also exists
on Medium, set that story's canonical link to the `/blogs/` URL in Medium's
story settings — otherwise search engines split ranking across both copies.

## Related

- [ocm-mcp-server](https://sandeepbazar.github.io/ocm-mcp-server/) — AgentOps for Kubernetes fleets
- [365 Days of AI Mastery](https://sandeepbazar.github.io/ai-roadmap-365/) — the course
