<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# assets

Art is filed the way [posts](../posts/) are — by the project or theme it belongs
to — so a collection's writing and its artwork sit in the same place under two
different roots.

```
assets/
  covers/<collection>/<slug>.svg      generated cover art, one per post
  art/<collection>/<slug>.{svg,png}   drawn by hand for a specific post
  art/site-card.{svg,png}             the site-wide social card
```

## The two trees, and why they are separate

**`covers/` belongs to [`gen_covers.py`](../gen_covers.py).** It rewrites every
file in there on every build, so a new post always has a cover and a malformed
SVG fails CI rather than half-rendering in someone's browser. Do not put
anything in this tree by hand — it will be overwritten.

**`art/` is never touched by a script.** A post that deserves drawn artwork puts
it here and points `cover:` (and `card:`, if it has one) at it. `gen_covers.py`
skips any post whose cover lives outside `covers/`, which is what makes drawn
work safe to commit.

`art/site-card.png` sits at the root of `art/` rather than in a collection,
because it belongs to the site rather than to any one post. It is the `og:image`
for the home page and for every post that does not ship its own card.

## Rules the build enforces

- A `cover:` or `card:` that does not resolve fails the build.
- A `card:` must be a **PNG or JPEG**. LinkedIn, Slack and X do not rasterise
  SVG, so an SVG card renders as a blank box in the one place a card exists to
  be seen.
- Art inside `covers/` or `art/` must be filed under **the post's own
  collection**. Art filed under someone else's still renders correctly, which is
  exactly why it goes wrong quietly: the page looks fine and the folder is a
  lie.

Assets outside these two trees are unconstrained — a diagram shared by several
posts has no single collection to belong to, and the build does not pretend
otherwise.

## Adding drawn art to a post

```bash
mkdir -p assets/art/<collection>
# ... write assets/art/<collection>/<slug>.svg and, for social, <slug>.png
```

```yaml
cover: assets/art/<collection>/<slug>.svg
card:  assets/art/<collection>/<slug>.png
```

A card should be 1200×630. Draw it in SVG and rasterise it — but keep the
**bars, numbers and other data static**. Social previews screenshot a page at an
unpredictable moment, so anything that animates in from zero is blank in half
the captures. Background motion is fine.
