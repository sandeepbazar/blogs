#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sandeep Bazar
# SPDX-License-Identifier: Apache-2.0
"""Generate one cover image per post into assets/covers/<collection>/<slug>.svg.

The art is generated rather than drawn so a new post gets a cover for free and
every cover stays in the site's palette. Each category has its own motif; the
variation within a category is derived from a hash of the slug, so a given post
always renders the same image but no two posts look alike. Covers are filed in
the same collection folder as the post they belong to.

Animation lives inside the SVG (declarative, so it plays through an <img> tag)
and is switched off wholesale under prefers-reduced-motion.

Usage:  python3 gen_covers.py
"""

from __future__ import annotations

import hashlib
import math
import xml.etree.ElementTree as ET  # only ever parses strings this script just wrote
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.resolve()
POSTS = ROOT / "posts"
COVERS = ROOT / "assets" / "covers"

W, H = 1200, 630

# Each category gets a two-stop accent so covers are distinguishable at card
# size, where the motif itself is only a few dozen pixels tall.
PALETTES = {
    "Agentic AI": ("#6f6cf6", "#8ea2ff", "#38bdf8"),
    "Kubernetes & MCP": ("#38bdf8", "#7dd3fc", "#6f6cf6"),
    "IBM Fusion": ("#34d399", "#6ee7b7", "#38bdf8"),
    "Research & Life": ("#fb923c", "#fdba74", "#f472b6"),
}

BG = "#070b16"


class Rng:
    """Small deterministic PRNG seeded from the slug.

    random.Random would work, but seeding from a digest and stepping it by hand
    keeps the output stable across Python versions, which matters because these
    files are committed.
    """

    def __init__(self, seed: str):
        self.state = int(hashlib.sha256(seed.encode()).hexdigest()[:16], 16)

    def next(self) -> float:
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) % (2**64)
        return (self.state >> 11) / float(2**53)

    def between(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self.next()

    def pick(self, items):
        return items[int(self.next() * len(items)) % len(items)]


def head(slug: str, palette) -> str:
    a, b, c = palette
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{c}"/>
    </linearGradient>
    <radialGradient id="glow1" cx="50%" cy="50%">
      <stop offset="0" stop-color="{a}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{a}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="50%" cy="50%">
      <stop offset="0" stop-color="{c}" stop-opacity=".45"/>
      <stop offset="1" stop-color="{c}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" fill="none" stroke="#94a3b8" stroke-opacity=".07" stroke-width="1"/>
    </pattern>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  </defs>
  <style>
    .drift {{ animation: drift 14s ease-in-out infinite alternate; }}
    .drift2 {{ animation: drift 18s ease-in-out infinite alternate-reverse; }}
    .spin {{ animation: spin 44s linear infinite; transform-origin: {W/2}px {H/2}px; }}
    .spin-slow {{ animation: spin 72s linear infinite reverse; transform-origin: {W/2}px {H/2}px; }}
    .pulse {{ animation: pulse 3.6s ease-in-out infinite; }}
    @keyframes drift {{ from {{ transform: translate(-26px,-16px); }} to {{ transform: translate(26px,18px); }} }}
    @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .drift, .drift2, .spin, .spin-slow, .pulse {{ animation: none; }}
    }}
  </style>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)"/>
"""


def orbits(r: Rng, palette) -> str:
    """Agentic AI: a hub with orbiting satellites."""
    a, b, c = palette
    cx, cy = W / 2, H / 2
    out = [
        f'<ellipse class="drift" cx="{cx-180:.0f}" cy="{cy-90:.0f}" rx="330" ry="250" fill="url(#glow1)"/>',
        f'<ellipse class="drift2" cx="{cx+220:.0f}" cy="{cy+110:.0f}" rx="300" ry="230" fill="url(#glow2)"/>',
    ]
    for i in range(3):
        rx = 150 + i * 92 + r.between(-14, 14)
        ry = rx * r.between(0.52, 0.72)
        rot = r.between(-32, 32)
        cls = "spin" if i % 2 == 0 else "spin-slow"
        out.append(
            f'<g class="{cls}"><ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry:.0f}" '
            f'fill="none" stroke="{b}" stroke-opacity=".3" stroke-width="1.6" '
            f'transform="rotate({rot:.0f} {cx} {cy})"/>'
        )
        n = 3 + i
        for k in range(n):
            ang = r.between(0, math.tau) + k * math.tau / n
            px = cx + rx * math.cos(ang)
            py = cy + ry * math.sin(ang)
            # Undo the ellipse rotation for the node so it sits on the path.
            rr = math.radians(rot)
            qx = cx + (px - cx) * math.cos(rr) - (py - cy) * math.sin(rr)
            qy = cy + (px - cx) * math.sin(rr) + (py - cy) * math.cos(rr)
            out.append(
                f'<circle class="pulse" cx="{qx:.0f}" cy="{qy:.0f}" r="{r.between(4,8):.1f}" '
                f'fill="{c}" style="animation-delay:{r.between(0,3):.1f}s"/>'
            )
        out.append("</g>")
    out.append(
        f'<circle cx="{cx}" cy="{cy}" r="46" fill="url(#g1)" opacity=".9"/>'
        f'<circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="{a}" stroke-opacity=".5" stroke-width="2"/>'
    )
    return "\n  ".join(out)


def hexes(r: Rng, palette) -> str:
    """Kubernetes & MCP: a hexagon lattice behind a shield."""
    a, b, c = palette
    out = [
        f'<ellipse class="drift" cx="{r.between(200,420):.0f}" cy="{r.between(120,260):.0f}" rx="340" ry="260" fill="url(#glow1)"/>',
        f'<ellipse class="drift2" cx="{r.between(760,1000):.0f}" cy="{r.between(380,520):.0f}" rx="320" ry="250" fill="url(#glow2)"/>',
    ]

    def hexagon(cx, cy, rad):
        pts = " ".join(
            f"{cx + rad * math.cos(math.radians(60 * i - 30)):.1f},"
            f"{cy + rad * math.sin(math.radians(60 * i - 30)):.1f}"
            for i in range(6)
        )
        return pts

    # The lattice must overrun the canvas on every side; a partial fill reads
    # as a rendering bug rather than a design choice.
    rad = 42
    for row in range(-1, 11):
        for col in range(-1, 19):
            cx = 100 + col * rad * 1.74
            cy = 90 + row * rad * 1.5 + (col % 2) * rad * 0.75
            op = r.between(0.09, 0.26)
            out.append(
                f'<polygon points="{hexagon(cx, cy, rad)}" fill="none" '
                f'stroke="{b}" stroke-opacity="{op:.2f}" stroke-width="1.4"/>'
            )
    cx, cy = W / 2, H / 2
    out.append(
        f'<g class="pulse" style="animation-duration:5s">'
        f'<polygon points="{hexagon(cx, cy, 118)}" fill="url(#g1)" opacity=".22"/>'
        f'<polygon points="{hexagon(cx, cy, 118)}" fill="none" stroke="url(#g1)" stroke-width="3"/>'
        f"</g>"
        f'<path d="M{cx-42} {cy+4} l30 30 l56 -62" fill="none" stroke="{c}" '
        f'stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    return "\n  ".join(out)


def planes(r: Rng, palette) -> str:
    """IBM Fusion: stacked isometric layers."""
    a, b, c = palette
    out = [
        f'<ellipse class="drift" cx="{r.between(240,460):.0f}" cy="{r.between(140,280):.0f}" rx="340" ry="250" fill="url(#glow1)"/>',
        f'<ellipse class="drift2" cx="{r.between(740,980):.0f}" cy="{r.between(360,500):.0f}" rx="320" ry="240" fill="url(#glow2)"/>',
    ]
    cx, cy = W / 2, H / 2 + 60
    layers = 4
    for i in range(layers):
        y = cy - i * 74
        w = 300 - i * 8
        h = 78
        op = 0.16 + i * 0.13
        out.append(
            f'<g class="pulse" style="animation-delay:{i*0.5:.1f}s;animation-duration:{r.between(4,6):.1f}s">'
            f'<path d="M{cx} {y-h/2} L{cx+w} {y} L{cx} {y+h/2} L{cx-w} {y} Z" '
            f'fill="url(#g1)" opacity="{op:.2f}"/>'
            f'<path d="M{cx} {y-h/2} L{cx+w} {y} L{cx} {y+h/2} L{cx-w} {y} Z" '
            f'fill="none" stroke="{b}" stroke-opacity=".45" stroke-width="1.6"/></g>'
        )
    for i in range(int(r.between(5, 9))):
        px, py = r.between(120, W - 120), r.between(60, H - 60)
        out.append(
            f'<circle class="pulse" cx="{px:.0f}" cy="{py:.0f}" r="{r.between(2.5,5):.1f}" '
            f'fill="{c}" style="animation-delay:{r.between(0,3):.1f}s"/>'
        )
    return "\n  ".join(out)


def waves(r: Rng, palette) -> str:
    """Research & Life: soft overlapping wave bands."""
    a, b, c = palette
    out = [
        f'<ellipse class="drift" cx="{r.between(220,440):.0f}" cy="{r.between(120,240):.0f}" rx="360" ry="260" fill="url(#glow1)"/>',
        f'<ellipse class="drift2" cx="{r.between(760,1000):.0f}" cy="{r.between(400,540):.0f}" rx="330" ry="250" fill="url(#glow2)"/>',
    ]
    for i in range(6):
        y = 150 + i * 62 + r.between(-12, 12)
        amp = r.between(26, 58)
        op = 0.5 - i * 0.06
        d = f"M-40 {y:.0f}"
        for x in range(0, W + 120, 120):
            d += f" q60 {-amp:.0f} 120 0 t120 0"
        out.append(
            f'<path class="{"drift" if i % 2 else "drift2"}" d="{d}" fill="none" '
            f'stroke="{b}" stroke-opacity="{max(op,0.12):.2f}" stroke-width="2.2" '
            f'style="animation-duration:{r.between(12,22):.0f}s"/>'
        )
    for i in range(int(r.between(6, 11))):
        px, py = r.between(80, W - 80), r.between(60, H - 60)
        out.append(
            f'<circle class="pulse" cx="{px:.0f}" cy="{py:.0f}" r="{r.between(3,7):.1f}" '
            f'fill="{c}" style="animation-delay:{r.between(0,3):.1f}s"/>'
        )
    return "\n  ".join(out)


MOTIFS = {
    "Agentic AI": orbits,
    "Kubernetes & MCP": hexes,
    "IBM Fusion": planes,
    "Research & Life": waves,
}


def xml(text: str) -> str:
    """SVG is XML: a bare & in a category like "Kubernetes & MCP" is a parse
    error, and the browser stops rendering the document at that point."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def label(category: str, palette) -> str:
    a, b, c = palette
    category = xml(category)
    return f"""
  <rect x="56" y="{H-104}" width="{18 + len(category)*13.4:.0f}" height="46" rx="23"
        fill="#070b16" fill-opacity=".55" stroke="{b}" stroke-opacity=".45"/>
  <text x="{70:.0f}" y="{H-73}" fill="{b}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace"
        font-size="19" letter-spacing="1.2">{category}</text>
  <text x="{W-56}" y="{H-73}" fill="#7f8db5" text-anchor="end"
        font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="18">sandeepbazar</text>
"""


def main() -> int:
    COVERS.mkdir(parents=True, exist_ok=True)
    made = 0
    skipped = 0

    for path in sorted(POSTS.rglob("*.md")):
        if path.name == "README.md":
            continue  # a folder index, not a post
        text = path.read_text(encoding="utf-8")
        meta = yaml.safe_load(text.split("---", 2)[1])
        if meta.get("status") == "draft":
            continue

        # This script owns assets/covers/ and nothing else. A post that points
        # its cover somewhere else - assets/art/, for drawn work - keeps that
        # file: generated covers are the default so no post ships without one,
        # not a rule that overwrites artwork on the next build.
        cover = meta.get("cover") or ""
        if cover and not cover.startswith("assets/covers/"):
            skipped += 1
            continue

        slug = meta["slug"]
        # Covers mirror how posts are filed, so a collection's art sits together.
        collection = path.parent.name
        category = meta["category"]
        palette = PALETTES[category]
        rng = Rng(slug)

        svg = (
            head(slug, palette)
            + "  "
            + MOTIFS[category](rng, palette)
            + label(category, palette)
            + f"  <title>{xml(category)} — cover art</title>\n</svg>\n"
        )
        # A browser stops rendering an SVG at the first XML error and shows a
        # half-drawn image, so catch it here instead of in production.
        try:
            ET.fromstring(svg)
        except ET.ParseError as exc:
            raise SystemExit(f"error: generated cover for {slug} is not valid XML: {exc}")

        target = COVERS / collection / f"{slug}.svg"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(svg, encoding="utf-8")
        made += 1

    note = f" ({skipped} post(s) ship their own cover)" if skipped else ""
    print(f"generated {made} covers -> {COVERS.relative_to(ROOT)}{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
