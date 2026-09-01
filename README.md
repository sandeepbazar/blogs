<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# blogs

Long-form writing by [Sandeep Bazar](https://www.linkedin.com/in/sandeepbazar/), published at
**<https://sandeepbazar.github.io/blogs/>**.

The source of truth is markdown in [`posts/`](posts/). `build.py` renders it into
`_site/` and a GitHub Actions workflow publishes that to Pages. There is no CMS,
no database and no tracker.

## How posts are filed

Posts live in a folder named for the **project, repo or theme** they were
written about, so everything on one subject sits together:

| Folder | Subject |
|---|---|
| [`posts/ocm-mcp-server/`](posts/ocm-mcp-server/) | The guardrailed MCP control plane for Kubernetes fleets ([repo](https://github.com/ocm-mcp-server/ocm-mcp-server)) |
| [`posts/fusion-mcp/`](posts/fusion-mcp/) | Conversational and agentic ops on IBM Fusion — kubernetes-mcp, Fusion MCP, IBM BOB |
| [`posts/ibm-fusion/`](posts/ibm-fusion/) | The IBM Fusion platform — storage, virtualization, migration, GPUs |
| [`posts/research-and-life/`](posts/research-and-life/) | Qualitative research, and the writing that is not about infrastructure |

The folder is in the URL: a post is published at
`/blogs/<collection>/<slug>/`, so a reader can see which project a piece belongs
to before opening it, and can strip a segment to find its siblings.
[`posts/README.md`](posts/README.md) carries the full index.

Re-filing a post therefore changes its URL. The build leaves a redirect at the
old flat `/blogs/<slug>/` for every post, because links that are already shared
do not stop existing when a layout improves.

The build **rejects** a post loose in `posts/` or in a folder it does not know,
which is the only thing that keeps a scheme like this from decaying. Adding a
folder means adding it to `COLLECTIONS` in `build.py`.

## Adding a post

Create `posts/<collection>/YYYY-MM-DD-slug.md`:

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

`gen_covers.py` generates one animated SVG per post into
`assets/covers/<collection>/<slug>.svg` — art is filed the way posts are.
Each category has its own motif — orbits, a hexagon lattice, stacked planes, wave
bands — and the variation within a category is derived from a hash of the slug, so
a post always renders the same image but no two look alike. The animation is
declarative (it plays through an `<img>` tag) and switches off entirely under
`prefers-reduced-motion`.

Add `cover: assets/covers/<collection>/<slug>.svg` to a post's front matter to
use it. The workflow regenerates covers on every build, so a new post cannot
ship without one.

A post that deserves art of its own puts the file in
`assets/art/<collection>/` and points `cover:` (and `card:`) there.
`gen_covers.py` owns `assets/covers/` and touches nothing else, so drawn work is
never overwritten. [`assets/README.md`](assets/README.md) has the full layout and
the rules the build enforces — including that art must be filed under the same
collection as the post claiming it.

## Building locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py --serve   # http://localhost:8000/blogs/
```

The build **fails** rather than shipping a broken page. It rejects a missing
required field, an unknown category, a duplicate slug, a post filed outside a
known collection, a `cover` or `card` that does not resolve or is filed under
another collection, an SVG `card`, and any internal link pointing at a page that
was never generated.

## Announcement copy

[`social/<collection>/`](social/) holds the ready-to-paste announcement for a
post — the text, the first comment carrying the links, and which image to
attach — filed the same way posts and assets are. Nothing here posts anything
anywhere, but the build does check that a social file names a post that exists,
in its own collection, with an image that resolves: a dead link in a feed is not
something you find out about from your own machine.
[`social/README.md`](social/README.md) carries the front matter and the house
style.

## Canonical URLs

This site is canonical for everything hosted here. For a post that also exists
on Medium, set that story's canonical link to the `/blogs/` URL in Medium's
story settings — otherwise search engines split ranking across both copies.

## Related

- [ocm-mcp-server](https://ocm-mcp-server.github.io/) — AgentOps for Kubernetes fleets
- [365 Days of AI Mastery](https://ai-roadmap-365.github.io/) — the course
