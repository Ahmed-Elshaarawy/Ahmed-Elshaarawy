"""Render the profile's App Listing artwork (header, product banners, buttons) as SVG.

Palette: Obsidian & Electric Cyan / Ice Blue (Futuristic Linear/Vercel aesthetic)
Usage: python scripts/listing.py [output_dir]   (default: assets/listing)
"""
import pathlib
import sys

# Obsidian & Electric Cyan
BG = "#0b0f19"
SURFACE = "#111827"
BORDER = "#1e293b"
CYAN = "#00f0ff"
ICE = "#38bdf8"
WHITE = "#f8fafc"
MUTE = "#94a3b8"
FONT = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"

HEADER = (
    "Ahmed Elshaarawy",
    "Full-Stack & Applied AI Engineer",
    "Shipping Production Apps · Integrating AI & LLMs",
)

BANNERS = [
    ("day-loop", "LIVE  ·  iOS  ·  ANDROID", "Day Loop", "Talk to your habits. Shipped to real stores."),
    ("portfolio-studio", "LIVE  ·  WEB", "Portfolio Studio", "Thirteen cinematic worlds, zero code."),
]

# (file, label, primary?)
BUTTONS = [
    ("app-store", "App Store", True),
    ("google-play", "Google Play", True),
    ("try-portfolio-studio", "Try it live", True),
    ("linkedin", "Connect on LinkedIn", True),
    ("portfolio", "portfoliostudio.me", False),
]

STYLE = f"""<style>
.f{{font-family:{FONT}}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{.spin{{animation:none}}}}
</style>"""


def motif(kind, c, bg):
    """Product glyph drawn in a 120x90 box at the origin."""
    if kind == "day-loop":
        return (
            f'<g class="spin"><circle cx="60" cy="45" r="40" fill="none" stroke="{c}" stroke-width="8" '
            f'stroke-dasharray="190 60" stroke-linecap="round"/></g>'
            f'<path d="M44 46 l11 11 l22 -24" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if kind == "portfolio-studio":
        return "".join(
            f'<rect x="{12 + k * 14}" y="{8 + k * 14}" width="80" height="54" rx="7" fill="{bg}" stroke="{c}" stroke-width="5"/>'
            for k in range(3)
        )
    raise ValueError(kind)


def header():
    name, role, focus = HEADER
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 240" width="840" height="240" role="img" aria-label="{name}, {role}, {focus}">
{STYLE}
<rect width="840" height="240" rx="28" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
<rect x="40" y="40" width="160" height="160" rx="38" fill="{SURFACE}" stroke="{CYAN}" stroke-width="2"/>
<g class="spin"><circle cx="120" cy="120" r="62" fill="none" stroke="{CYAN}" stroke-width="6" stroke-dasharray="290 100" stroke-linecap="round"/></g>
<text x="120" y="139" text-anchor="middle" class="f" font-size="52" font-weight="700" fill="{CYAN}" letter-spacing="-1">AE</text>
<text x="236" y="110" class="f" font-size="58" font-weight="700" fill="{WHITE}" letter-spacing="-1.5">{name}</text>
<text x="238" y="158" class="f" font-size="30" font-weight="600" fill="{CYAN}">{role}</text>
<text x="238" y="196" class="f" font-size="26" font-weight="400" fill="{MUTE}">{focus}</text>
</svg>"""


def banner(kind, kicker, title, tagline):
    accent = CYAN if kind == "day-loop" else ICE
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 200" width="840" height="200" role="img" aria-label="{title}: {tagline}">
{STYLE}
<rect width="840" height="200" rx="26" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
<rect x="30" y="30" width="140" height="140" rx="34" fill="{SURFACE}" stroke="{accent}" stroke-width="2"/>
<g transform="translate(43 51) scale(.95)">{motif(kind, accent, SURFACE)}</g>
<text x="202" y="70" class="f" font-size="24" font-weight="700" letter-spacing="2" fill="{accent}">{kicker}</text>
<text x="200" y="124" class="f" font-size="50" font-weight="700" fill="{WHITE}" letter-spacing="-1">{title}</text>
<text x="202" y="162" class="f" font-size="28" font-weight="400" fill="{MUTE}">{tagline}</text>
</svg>"""


def button(label, primary):
    width = 40 + int(len(label) * 10.2) + 30
    fill = CYAN if primary else BG
    ink = "#080c14" if primary else WHITE
    stroke = CYAN if primary else BORDER
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 44" width="{width}" height="44" role="img" aria-label="{label}">
<rect x="1.5" y="1.5" width="{width - 3}" height="41" rx="20.5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
<text x="22" y="28" font-family="{FONT}" font-size="16" font-weight="700" fill="{ink}">{label} ↗</text>
</svg>"""


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets/listing")
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.svg"):
        old.unlink()
    (out / "header.svg").write_text(header(), encoding="utf-8")
    for kind, kicker, title, tagline in BANNERS:
        (out / f"banner-{kind}.svg").write_text(banner(kind, kicker, title, tagline), encoding="utf-8")
    for name, label, primary in BUTTONS:
        (out / f"button-{name}.svg").write_text(button(label, primary), encoding="utf-8")
    print(f"wrote {1 + len(BANNERS) + len(BUTTONS)} files to {out}")


if __name__ == "__main__":
    main()
