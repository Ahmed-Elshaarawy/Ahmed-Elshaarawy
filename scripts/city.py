"""Render the last year of GitHub contributions as an isometric city skyline (SVG).

Usage: GITHUB_TOKEN=... python scripts/city.py <username> <output.svg>
Standard library only, so the workflow needs no installs.
"""
import json
import math
import os
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount contributionLevel weekday } }
      }
    }
  }
}
"""

LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]

# Top-face colour per level; side faces are shaded from it.
LIGHT = ["#e4e8ec", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
DARK = ["#2a313c", "#196c2e", "#2ea043", "#3fb950", "#56d364"]

U = (13.0, 0.5)    # one week to the right
V = (-4.0, 3.0)    # one weekday toward the viewer
FOOT = 0.78        # building footprint as a share of its cell
MAX_H = 120.0      # height of the busiest day
FLAT_H = 1.5       # height of a day with no contributions
PAD = 16.0


def fetch(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GitHub API error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def shade(hex_colour, factor):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c * factor))) for c in (r, g, b))


def point(w, d):
    return (w * U[0] + d * V[0], w * U[1] + d * V[1])


def render(calendar):
    days = [
        (w, day["weekday"], day["contributionCount"], LEVELS.index(day["contributionLevel"]))
        for w, week in enumerate(calendar["weeks"])
        for day in week["contributionDays"]
    ]
    peak = max((c for *_, c, _ in days), default=0) or 1
    inset = (1 - FOOT) / 2

    blocks = []
    for w, d, count, level in days:
        h = FLAT_H if count == 0 else 6 + math.sqrt(count / peak) * (MAX_H - 6)
        x0, x1, y0, y1 = w + inset, w + 1 - inset, d + inset, d + 1 - inset
        # Footprint corners: back, right, front, left (screen space).
        b, r, f, l = point(x0, y0), point(x1, y0), point(x1, y1), point(x0, y1)
        up = lambda p: (p[0], p[1] - h)
        faces = {
            "t": [up(b), up(r), up(f), up(l)],
            "l": [l, f, up(f), up(l)],
            "r": [f, r, up(r), up(f)],
        }
        blocks.append((w * U[1] + d * V[1], w, level, faces))
    blocks.sort(key=lambda blk: blk[0])  # paint back to front

    xs = [x for *_, faces in blocks for face in faces.values() for x, _ in face]
    ys = [y for *_, faces in blocks for face in faces.values() for _, y in face]
    min_x, min_y = min(xs) - PAD, min(ys) - PAD - 18
    width, height = max(xs) - min_x + PAD, max(ys) - min_y + PAD

    def fmt(face):
        return " ".join(f"{x - min_x:.1f},{y - min_y:.1f}" for x, y in face)

    def palette(colours):
        return "".join(
            f".t{i}{{fill:{c}}}.l{i}{{fill:{shade(c, 0.72)}}}.r{i}{{fill:{shade(c, 0.86)}}}"
            for i, c in enumerate(colours)
        )

    buildings = []
    for _, w, level, faces in blocks:
        polys = "".join(f'<polygon class="{k}{level}" points="{fmt(p)}"/>' for k, p in faces.items())
        buildings.append(f'<g class="b" style="animation-delay:{w * 22}ms">{polys}</g>')

    total = calendar["totalContributions"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" height="{height:.0f}" role="img" aria-label="{total} contributions in the last year, drawn as a city">
<style>
{palette(LIGHT)}
.cap{{fill:#59636e;font:500 12px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.cap b{{font-weight:700}}
.b{{transform-box:fill-box;transform-origin:50% 100%;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}}
@keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@media (prefers-color-scheme:dark){{{palette(DARK)}.cap{{fill:#9198a1}}}}
@media (prefers-reduced-motion:reduce){{.b{{animation:none}}}}
</style>
<text class="cap" x="{PAD}" y="{PAD + 4}">{total:,} contributions in the last year</text>
{"".join(buildings)}
</svg>
"""


def main():
    login, out = sys.argv[1], sys.argv[2]
    svg = render(fetch(login, os.environ["GITHUB_TOKEN"]))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
