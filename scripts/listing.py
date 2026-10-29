"""Render the profile's App Listing artwork (header, project cards, section banners) as SVG.

Usage: python scripts/listing.py [output_dir]   (default: assets/listing)
Standard library only. Edit STATS / CARDS / SECTIONS below and rerun.
"""
import pathlib
import sys

# Midnight Tangerine
NAVY = "#14213d"
PANEL = "#1b2b4f"
ORANGE = "#fca311"
WHITE = "#ffffff"
MUTE = "#9fb0d0"
FONT = "'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"

STATS = [("4", "PRODUCTS SHIPPED"), ("2,893", "CONTRIBUTIONS / YR"), ("5", "APP LANGUAGES"), ("48h", "GAME JAM SHIP")]

CARDS = [
    ("day-loop", "Day Loop", "Voice-first habit tracker", "iOS · ANDROID"),
    ("portfolio-studio", "Portfolio Studio", "No-code portfolio builder", "WEB · NEXT.JS"),
    ("awesome-curator", "awesome-curator", "Self-curating lists", "PYTHON · CI"),
    ("masquerade-escape", "Masquerade Escape", "Global Game Jam 2026", "UNITY · 48H"),
]

SECTIONS = [
    ("day-loop", "FLAGSHIP · iOS · ANDROID", "Day Loop", "Talk to your habits."),
    ("portfolio-studio", "PRODUCT · WEB", "Portfolio Studio", "Thirteen cinematic worlds, zero code."),
    ("awesome-curator", "OPEN SOURCE · PYTHON", "awesome-curator", "Awesome lists that curate themselves."),
    ("masquerade-escape", "GAME JAM · UNITY", "Masquerade Escape", "Concept to playable in 48 hours."),
    ("stack", "TOOLKIT", "Tech Stack", "What I build with."),
    ("activity", "ACTIVITY", "On GitHub", "One building per day of contributions."),
]

STYLE = f"""<style>
.f{{font-family:{FONT}}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}}
.blink{{animation:blink 1.1s steps(1) infinite}}
.rise{{transform-box:fill-box;transform-origin:bottom;animation:rise 2.4s ease-in-out infinite alternate}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes rise{{from{{transform:scaleY(.55)}}}}
@media (prefers-reduced-motion:reduce){{.spin,.blink,.rise{{animation:none}}}}
</style>"""


def motif(kind, c, bg):
    """Project glyph drawn in a 120x90 box at the origin."""
    if kind == "day-loop":
        return (f'<g class="spin"><circle cx="60" cy="45" r="40" fill="none" stroke="{c}" stroke-width="10" '
                f'stroke-dasharray="200 52" stroke-linecap="round"/></g>'
                f'<path d="M44 46 l11 11 l22 -24" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "portfolio-studio":
        return "".join(f'<rect x="{12 + k * 14}" y="{8 + k * 14}" width="80" height="54" rx="7" fill="{bg}" stroke="{c}" stroke-width="6"/>'
                       for k in range(3))
    if kind == "awesome-curator":
        return "".join(f'<circle cx="18" cy="{14 + k * 21}" r="7" fill="{c}"/>'
                       f'<rect x="34" y="{9 + k * 21}" width="{84 - k * 12}" height="10" rx="5" fill="{c}" opacity=".55"/>'
                       for k in range(4))
    if kind == "masquerade-escape":
        return (f'<path d="M8 32 q52 -40 104 0 q-8 44 -52 44 q-44 0 -52 -44z" fill="{c}"/>'
                f'<ellipse cx="38" cy="44" rx="13" ry="8" fill="{bg}"/><ellipse cx="82" cy="44" rx="13" ry="8" fill="{bg}"/>')
    if kind == "stack":
        return (f'<path d="M36 18 L10 45 L36 72 M84 18 L110 45 L84 72" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M68 12 L52 78" stroke="{c}" stroke-width="10" stroke-linecap="round"/>')
    if kind == "activity":
        return "".join(f'<rect class="rise" style="animation-delay:{k * .3}s" x="{8 + k * 22}" y="{82 - h}" width="16" height="{h}" rx="3" fill="{c}"/>'
                       for k, h in enumerate([30, 52, 40, 70, 58]))
    raise ValueError(kind)


def header():
    stats = ""
    for i, (big, small) in enumerate(STATS):
        x = 141 + i * 186
        stats += (f'<text x="{x}" y="276" text-anchor="middle" class="f" font-size="26" font-weight="800" fill="{WHITE}">{big}</text>'
                  f'<text x="{x}" y="300" text-anchor="middle" class="f" font-size="11" font-weight="600" fill="{MUTE}" letter-spacing="1.6">{small}</text>')
        if i < len(STATS) - 1:
            stats += f'<line x1="{x + 93}" y1="254" x2="{x + 93}" y2="304" stroke="{MUTE}" stroke-opacity=".35"/>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 330" width="840" height="330" role="img" aria-label="Ahmed Elshaarawy, Software Engineer and Machine Learning">
{STYLE}
<rect width="840" height="330" rx="28" fill="{NAVY}"/>
<rect x="48" y="48" width="140" height="140" rx="34" fill="{ORANGE}"/>
<g class="spin"><circle cx="118" cy="118" r="54" fill="none" stroke="{NAVY}" stroke-width="6" stroke-dasharray="250 90" stroke-linecap="round"/></g>
<text x="118" y="134" text-anchor="middle" class="f" font-size="44" font-weight="800" fill="{NAVY}" letter-spacing="-1">AE</text>
<text x="222" y="98" class="f" font-size="46" font-weight="800" fill="{WHITE}" letter-spacing="-1.5">Ahmed Elshaarawy</text>
<text x="224" y="134" class="f" font-size="21" font-weight="500" fill="{MUTE}">Software Engineer · Machine Learning<tspan class="blink" fill="{ORANGE}"> ▍</tspan></text>
<rect x="222" y="156" width="186" height="44" rx="22" fill="{ORANGE}"/>
<text x="315" y="185" text-anchor="middle" class="f" font-size="17" font-weight="800" fill="{NAVY}" letter-spacing="1">GET IN TOUCH</text>
<text x="428" y="184" class="f" font-size="15" fill="{MUTE}">Shipping on App Store · Google Play · Web</text>
<line x1="48" y1="232" x2="792" y2="232" stroke="{MUTE}" stroke-opacity=".35"/>
{stats}
</svg>"""


def card(kind, name, line, tag):
    # Long names wrap at the space or hyphen so every title keeps the same size.
    if len(name) > 12:
        cut = name.find(" ") + 1 or name.find("-") + 1
        lines = [name[:cut].strip(), name[cut:]]
    else:
        lines = [name]
    title = "".join(f'<tspan x="20" dy="{0 if i == 0 else 26}">{part}</tspan>' for i, part in enumerate(lines))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 360" width="200" height="360" role="img" aria-label="{name}: {line}">
{STYLE}
<rect width="200" height="360" rx="24" fill="{NAVY}"/>
<text x="20" y="44" class="f" font-size="12" font-weight="700" letter-spacing="1.6" fill="{MUTE}">{tag}</text>
<text x="20" y="74" class="f" font-size="22" font-weight="800" fill="{WHITE}" letter-spacing="-.5">{title}</text>
<g transform="translate(40 140)">{motif(kind, ORANGE, NAVY)}</g>
<text x="20" y="300" class="f" font-size="13" font-weight="500" fill="{WHITE}">{line}</text>
<rect x="20" y="316" width="64" height="24" rx="12" fill="{ORANGE}"/>
<text x="52" y="333" text-anchor="middle" class="f" font-size="11" font-weight="800" fill="{NAVY}">VIEW</text>
</svg>"""


def banner(kind, kicker, title, tagline):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 120" width="840" height="120" role="img" aria-label="{title}: {tagline}">
{STYLE}
<rect width="840" height="120" rx="22" fill="{NAVY}"/>
<rect x="20" y="16" width="88" height="88" rx="22" fill="{ORANGE}"/>
<g transform="translate(30 31) scale(.56)">{motif(kind, NAVY, ORANGE)}</g>
<text x="132" y="44" class="f" font-size="12" font-weight="700" letter-spacing="1.8" fill="{ORANGE}">{kicker}</text>
<text x="131" y="84" class="f" font-size="34" font-weight="800" fill="{WHITE}" letter-spacing="-1">{title}</text>
<text x="812" y="84" text-anchor="end" class="f" font-size="17" font-weight="500" fill="{MUTE}">{tagline}</text>
</svg>"""


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets/listing")
    out.mkdir(parents=True, exist_ok=True)
    (out / "header.svg").write_text(header(), encoding="utf-8")
    for kind, name, line, tag in CARDS:
        (out / f"card-{kind}.svg").write_text(card(kind, name, line, tag), encoding="utf-8")
    for kind, kicker, title, tagline in SECTIONS:
        (out / f"section-{kind}.svg").write_text(banner(kind, kicker, title, tagline), encoding="utf-8")
    print(f"wrote {1 + len(CARDS) + len(SECTIONS)} files to {out}")


if __name__ == "__main__":
    main()
