"""Render the profile's App Listing artwork (header, product banners, buttons) as SVG.

Usage: python scripts/listing.py [output_dir]   (default: assets/listing)
Standard library only. Edit HEADER / BANNERS / BUTTONS below and rerun.

Header and banners are 840 wide and render at ~0.37x in GitHub's 308px mobile
column, so no text in them goes below 26 units (~9.5px on a phone).
Buttons render at a fixed width that fits the mobile column unscaled.
"""
import pathlib
import sys

# Midnight Tangerine
NAVY = "#14213d"
ORANGE = "#fca311"
WHITE = "#ffffff"
MUTE = "#9fb0d0"
FONT = "'Segoe UI','Helvetica Neue',-apple-system,BlinkMacSystemFont,Arial,sans-serif"

HEADER = ("Ahmed Elshaarawy", "Software Engineer", "heading into Machine Learning")

BANNERS = [
    ("day-loop", "LIVE  ·  iOS  ·  ANDROID", "Day Loop", "Talk to your habits."),
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
        return (f'<g class="spin"><circle cx="60" cy="45" r="40" fill="none" stroke="{c}" stroke-width="10" '
                f'stroke-dasharray="200 52" stroke-linecap="round"/></g>'
                f'<path d="M44 46 l11 11 l22 -24" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "portfolio-studio":
        return "".join(f'<rect x="{12 + k * 14}" y="{8 + k * 14}" width="80" height="54" rx="7" fill="{bg}" stroke="{c}" stroke-width="6"/>'
                       for k in range(3))
    raise ValueError(kind)


def header():
    name, role, focus = HEADER
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 240" width="840" height="240" role="img" aria-label="{name}, {role}, {focus}">
{STYLE}
<rect width="840" height="240" rx="28" fill="{NAVY}"/>
<rect x="40" y="40" width="160" height="160" rx="38" fill="{ORANGE}"/>
<g class="spin"><circle cx="120" cy="120" r="62" fill="none" stroke="{NAVY}" stroke-width="7" stroke-dasharray="290 100" stroke-linecap="round"/></g>
<text x="120" y="139" text-anchor="middle" class="f" font-size="52" font-weight="700" fill="{NAVY}" letter-spacing="-1">AE</text>
<text x="236" y="112" class="f" font-size="60" font-weight="700" fill="{WHITE}" letter-spacing="-1.5">{name}</text>
<text x="238" y="160" class="f" font-size="32" font-weight="600" fill="{ORANGE}">{role}</text>
<text x="238" y="198" class="f" font-size="28" font-weight="400" fill="{MUTE}">{focus}</text>
</svg>"""


def banner(kind, kicker, title, tagline):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 200" width="840" height="200" role="img" aria-label="{title}: {tagline}">
{STYLE}
<rect width="840" height="200" rx="26" fill="{NAVY}"/>
<rect x="30" y="30" width="140" height="140" rx="34" fill="{ORANGE}"/>
<g transform="translate(43 51) scale(.95)">{motif(kind, NAVY, ORANGE)}</g>
<text x="202" y="72" class="f" font-size="26" font-weight="700" letter-spacing="2" fill="{ORANGE}">{kicker}</text>
<text x="200" y="126" class="f" font-size="52" font-weight="700" fill="{WHITE}" letter-spacing="-1">{title}</text>
<text x="202" y="164" class="f" font-size="30" font-weight="400" fill="{MUTE}">{tagline}</text>
</svg>"""


def button(label, primary):
    width = 40 + int(len(label) * 10.2) + 30
    fill, ink, stroke = (ORANGE, NAVY, ORANGE) if primary else (NAVY, WHITE, ORANGE)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 44" width="{width}" height="44" role="img" aria-label="{label}">
<rect x="1.5" y="1.5" width="{width - 3}" height="41" rx="20.5" fill="{fill}" stroke="{stroke}" stroke-width="3"/>
<text x="22" y="28" font-family="{FONT}" font-size="17" font-weight="700" fill="{ink}">{label} ↗</text>
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
