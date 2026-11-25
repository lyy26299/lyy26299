#!/usr/bin/env python3
"""Generate the SVG artwork the profile README shows.

    python3 build.py

Standard library only. Edit the texts and lists below, run it again and commit
what changes in assets/. The SVGs are shown through <img>, so they can load
nothing from outside: fonts are the viewer's own, taken from the stacks below,
and all motion is CSS inside each file.
"""

from __future__ import annotations

import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"

SANS = "'Helvetica Neue',Helvetica,'Arial Nova',Arial,'Liberation Sans',sans-serif"
SERIF = (
    "Didot,'Bodoni 72','Bodoni MT','Playfair Display','Sitka Banner',"
    "'Sitka Display',Georgia,'Noto Serif','DejaVu Serif',serif"
)
MONO = (
    "ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',Menlo,Consolas,"
    "'DejaVu Sans Mono',monospace"
)

# Coolest to hottest is top to bottom of a flame, so gradients run upward.
EMBER = ("#ffe29a", "#ffb347", "#ff6a1a", "#e0263a")

# The work rows, marquee and section labels have no background: one file per
# GitHub theme, picked in the README with <picture>.
THEMES = {
    "light": {"ink": "#191512", "accent": "#e2460b"},
    "dark": {"ink": "#f3ece2", "accent": "#ff8a3d"},
}

NAME = "LYY26299"
SINCE = "EST. 2022"
FIELD = "AGENTS · VISION · LLM INFRA"
TAGLINE = ("EXPLORING PERCEPTION, INTERACTION", "AND THE SYSTEMS BEHIND AI")

# The motto: two lines set in bold capitals, the last in italic.
MOTTO_BOLD = ("EXPLORE.", "BUILD.")
MOTTO_ITALIC = "contribute back."
# The same words as a tokenizer would cut them: text, column, row, seconds for
# one drift, seconds into it at the start. Chips that share a column are half
# a drift apart, so two never cross on the way up.
CHIPS = (
    ("Explore", 770, 290, 12, 0),
    ("<eos>", 770, 290, 12, 6),
    ("·Build", 882, 250, 13, 4),
    ("·contribute", 1006, 300, 14, 9),
    ("·back", 1112, 240, 11, 2),
)

# name: the project as written in the README. role and tags stay Latin, because
# CJK in an SVG falls back to a different font on every system; the Chinese
# description sits under each row in the README as ordinary text.
OPEN_SOURCE = [
    {"slug": "semantic-router", "mark": "CONTRIBUTOR", "name": "Semantic Router", "role": "systems behind LLM routing", "tags": "VLLM-PROJECT · GO · MCP"},
]
WORK = [
    {"slug": "vision-agent", "name": "Vision Agent", "role": "real-time AI fitness coach", "tags": "COMPUTER VISION · POSE · VOICE"},
    {"slug": "motion-relay", "name": "Motion Relay", "role": "realtime motion interaction", "tags": "PYTHON · VISION-AGENTS"},
    {"slug": "txt-epub", "name": "TXT → EPUB", "role": "a Kindle reading workflow", "tags": "PYTHON · EPUB"},
]

# An even number of entries, so that filled and outlined words still alternate
# where the loop joins.
STACK = ["GO", "PYTHON", "JAVASCRIPT", "YOLO", "GEMINI", "MCP", "LLM ROUTING", "COMPUTER VISION"]

# The width one pass of the marquee is set to, whatever font the viewer has, so
# that the loop joins without a jump. Close to its natural width in Arial Bold.
# After changing STACK, set this to 0, measure the text in a browser
# (getComputedTextLength) and put the number back.
MARQUEE_LENGTH = 2329

CARE = ("100% TOKENS · BURN AT HIGH TEMPERATURE", "DO NOT TRUNCATE")
CARE_MOTTO = ("Explore ideas. Build projects.", "Contribute back.")

REDUCED_MOTION = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def write(name: str, svg: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8", newline="\n")


def ember_stops() -> str:
    return "".join(
        f'<stop offset="{offset}" stop-color="{color}"/>'
        for offset, color in zip(("0", ".3", ".68", "1"), EMBER)
    )


def hero() -> str:
    rnd = random.Random(11)
    rules: list[str] = []
    embers: list[str] = []
    for i in range(30):
        x, y = rnd.uniform(520, 1190), rnd.uniform(430, 600)
        radius = rnd.choice((3, 4, 5, 6.5, 8))
        rise = rnd.choice(("riseA", "riseB", "riseC"))
        seconds = rnd.uniform(6, 13)
        sway = rnd.uniform(1.6, 3.2)
        rules.append(f".r{i}{{animation:{rise} {seconds:.1f}s linear -{rnd.uniform(0, seconds):.1f}s infinite}}")
        rules.append(f".s{i}{{animation:sway {sway:.1f}s ease-in-out -{rnd.uniform(0, sway):.1f}s infinite alternate}}")
        embers.append(
            f'<g class="r{i}"><circle class="s{i}" cx="{x:.0f}" cy="{y:.0f}" r="{radius}" fill="url(#spark)"/></g>'
        )

    chips: list[str] = []
    for i, (text, x, y, seconds, start) in enumerate(CHIPS):
        width = len(text) * 10 + 22
        rules.append(f".c{i}{{animation:drift {seconds}s ease-in-out -{start}s infinite}}")
        chips.append(
            f'<g transform="translate({x} {y})"><g class="c{i}">'
            f'<rect x="{-width / 2}" y="-15" width="{width}" height="30" rx="7" fill="#160d09" fill-opacity=".72" '
            f'stroke="#ffb98a" stroke-opacity=".42"/>'
            f'<text class="mono" y="5.5" font-size="16" text-anchor="middle" fill="#ffd9b0">{escape(text)}</text>'
            f"</g></g>"
        )

    style = (
        f".sans{{font-family:{SANS};font-weight:700}}"
        f".serif{{font-family:{SERIF};font-style:italic}}"
        f".mono{{font-family:{MONO}}}"
        "@keyframes riseA{0%{transform:translate(0,0);opacity:0}10%{opacity:.95}60%{opacity:.7}100%{transform:translate(-46px,-430px);opacity:0}}"
        "@keyframes riseB{0%{transform:translate(0,0);opacity:0}15%{opacity:.9}55%{opacity:.6}100%{transform:translate(38px,-360px);opacity:0}}"
        "@keyframes riseC{0%{transform:translate(0,0);opacity:0}8%{opacity:1}100%{transform:translate(-14px,-520px);opacity:0}}"
        "@keyframes sway{from{transform:translateX(-9px)}to{transform:translateX(9px)}}"
        "@keyframes drift{0%{transform:translateY(30px);opacity:0}16%{opacity:1}58%{opacity:1}100%{transform:translateY(-84px);opacity:0}}"
        "@keyframes breathe{from{opacity:.72}to{opacity:1}}"
        "@keyframes flicker{0%,100%{opacity:0}18%{opacity:.34}31%{opacity:.08}47%{opacity:.42}63%{opacity:.14}82%{opacity:.3}}"
        ".glow{animation:breathe 5.5s ease-in-out infinite alternate}"
        ".hot{opacity:0;animation:flicker 4.2s ease-in-out infinite}"
        + "".join(rules)
        + REDUCED_MOTION
    )

    bold = "".join(
        f'<text class="sans" x="56" y="{220 + 112 * i}" font-size="124" letter-spacing="-4.5" fill="#f6efe5">{escape(line)}</text>'
        for i, line in enumerate(MOTTO_BOLD)
    )
    italic = f'x="1134" y="474" font-size="132" text-anchor="end"'
    motto = " ".join(MOTTO_BOLD).title() + " " + MOTTO_ITALIC.capitalize()

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc">
<title id="title">{NAME.lower()}. {motto}</title>
<desc id="desc">The motto set large on black above a bed of embers, with the words rising out of it as tokens.</desc>
<defs>
<clipPath id="frame"><rect width="1200" height="600" rx="26"/></clipPath>
<linearGradient id="ember" x1="0" y1="1" x2="0" y2="0">{ember_stops()}</linearGradient>
<radialGradient id="fire" gradientUnits="userSpaceOnUse" cx="880" cy="690" r="720">
<stop offset="0" stop-color="#ff8a2a" stop-opacity=".9"/><stop offset=".3" stop-color="#e63a2e" stop-opacity=".42"/>
<stop offset=".62" stop-color="#8a1245" stop-opacity=".16"/><stop offset="1" stop-color="#8a1245" stop-opacity="0"/>
</radialGradient>
<radialGradient id="core" gradientUnits="userSpaceOnUse" cx="900" cy="650" r="310">
<stop offset="0" stop-color="#ffd27a" stop-opacity=".7"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/>
</radialGradient>
<radialGradient id="bed"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".85"/><stop offset=".5" stop-color="#ffb347" stop-opacity=".3"/>
<stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="spark"><stop offset="0" stop-color="#fff6d6"/><stop offset=".32" stop-color="#ffb347" stop-opacity=".9"/>
<stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="reach" gradientUnits="userSpaceOnUse" cx="900" cy="640" r="560">
<stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</radialGradient>
<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="#ffb98a"/></pattern>
<mask id="halftone"><rect width="1200" height="600" fill="url(#reach)"/></mask>
</defs>
<style>{style}</style>
<g clip-path="url(#frame)">
<rect width="1200" height="600" fill="#0b0908"/>
<g class="glow"><rect width="1200" height="600" fill="url(#fire)"/><rect width="1200" height="600" fill="url(#core)"/>
<ellipse cx="860" cy="606" rx="640" ry="40" fill="url(#bed)"/></g>
<rect width="1200" height="600" fill="url(#dots)" mask="url(#halftone)" opacity=".3"/>
<text class="sans" x="62" y="64" font-size="18" letter-spacing="6" fill="#f6efe5">{NAME}</text>
<text class="mono" x="600" y="63" font-size="15" letter-spacing="2" text-anchor="middle" fill="#9c8f82">{SINCE}</text>
<text class="mono" x="1138" y="63" font-size="15" letter-spacing="2" text-anchor="end" fill="#d8ccbf">{escape(FIELD)}</text>
<path d="M62 90H1138" stroke="#fff" stroke-opacity=".14"/>
{bold}
<text class="serif" {italic} fill="url(#ember)">{escape(MOTTO_ITALIC)}</text>
<text class="serif hot" {italic} fill="#fff6d6">{escape(MOTTO_ITALIC)}</text>
{"".join(embers)}
{"".join(chips)}
<text class="mono" x="62" y="532" font-size="16" letter-spacing="2" fill="#f6efe5">{escape(TAGLINE[0])}</text>
<text class="mono" x="62" y="558" font-size="16" letter-spacing="2" fill="#9c8f82">{escape(TAGLINE[1])}</text>
</g>
<rect x=".5" y=".5" width="1199" height="599" rx="25.5" fill="none" stroke="#fff" stroke-opacity=".1"/>
</svg>"""


def work_row(mark: str, item: dict[str, str], theme: dict[str, str]) -> str:
    ink, accent = theme["ink"], theme["accent"]
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 140" role="img" aria-label="{escape(item['name'])}: {escape(item['role'])}">
<style>.sans{{font-family:{SANS};font-weight:700}}.serif{{font-family:{SERIF};font-style:italic}}.mono{{font-family:{MONO}}}</style>
<path d="M0 .5H1200" stroke="{ink}" stroke-opacity=".18"/>
<text class="mono" x="2" y="38" font-size="16" letter-spacing="2" fill="{accent}">{escape(mark)}</text>
<text class="sans" x="-2" y="114" font-size="78" letter-spacing="-2.5" fill="{ink}">{escape(item['name'])}</text>
<text class="serif" x="1128" y="84" font-size="31" text-anchor="end" fill="{ink}" fill-opacity=".74">{escape(item['role'])}</text>
<text class="mono" x="1128" y="114" font-size="15" letter-spacing="2" text-anchor="end" fill="{ink}" fill-opacity=".5">{escape(item['tags'])}</text>
<g transform="translate(1174 92)" fill="none"><circle r="21" stroke="{ink}" stroke-opacity=".28"/>
<path d="M-6 6 6-6M-3-6H6V3" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>"""


def label(left: str, right: str, theme: dict[str, str]) -> str:
    ink = theme["ink"]
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 48" role="img" aria-label="{escape(left)}">
<style>.sans{{font-family:{SANS};font-weight:700}}.mono{{font-family:{MONO}}}</style>
<circle cx="6" cy="27" r="5" fill="{theme['accent']}"/>
<text class="sans" x="24" y="33" font-size="16" letter-spacing="5" fill="{ink}">{escape(left)}</text>
<text class="mono" x="1198" y="33" font-size="15" letter-spacing="2" text-anchor="end" fill="{ink}" fill-opacity=".5">{escape(right)}</text>
</svg>"""


def marquee(theme: dict[str, str]) -> str:
    ink, accent = theme["ink"], theme["accent"]
    # The gaps are no-break spaces, not dx: browsers disagree on whether dx
    # counts toward textLength, and squeeze the letters when it does not.
    spans = "".join(
        f'<tspan class="{"line" if i % 2 else "fill"}">{escape(word)}</tspan><tspan class="dot">  •  </tspan>'
        for i, word in enumerate(STACK)
    )
    length = f' textLength="{MARQUEE_LENGTH}" lengthAdjust="spacing"' if MARQUEE_LENGTH else ""
    run = f'<text class="sans" y="67" font-size="46" letter-spacing="1"{length}>{spans}</text>'
    period = MARQUEE_LENGTH
    style = (
        f".sans{{font-family:{SANS};font-weight:700}}"
        f".fill{{fill:{ink}}}.line{{fill:none;stroke:{ink};stroke-width:1.3}}.dot{{fill:{accent}}}"
        f"@keyframes run{{to{{transform:translateX(-{period}px)}}}}"
        ".run{animation:run 40s linear infinite}" + REDUCED_MOTION
    )
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 100" role="img" aria-label="{escape(', '.join(STACK))}">
<defs>
<linearGradient id="edges"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".09" stop-color="#fff"/>
<stop offset=".91" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="fade"><rect width="1200" height="100" fill="url(#edges)"/></mask>
</defs>
<style>{style}</style>
<path d="M0 .5H1200M0 99.5H1200" stroke="{ink}" stroke-opacity=".18"/>
<g mask="url(#fade)"><g class="run">{run}<g transform="translate({period} 0)">{run}</g></g></g>
</svg>"""


def care_label(paper: str, ink: str, motto_fill: str) -> str:
    """The sign-off: a garment care label. Its colours are the page's, inverted."""
    lines = [part.capitalize() for line in CARE for part in line.split(" · ")]
    spoken = f"{NAME.lower()}. {' '.join(CARE_MOTTO)} {'. '.join(lines)}."
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 320" role="img" aria-label="Care label: {escape(spoken)}">
<defs><linearGradient id="ember" x1="0" y1="1" x2="1" y2="0">{ember_stops()}</linearGradient></defs>
<style>.sans{{font-family:{SANS};font-weight:700}}.serif{{font-family:{SERIF};font-style:italic}}.mono{{font-family:{MONO}}}</style>
<rect width="560" height="320" rx="12" fill="{paper}"/>
<rect x="13" y="13" width="534" height="294" rx="5" fill="none" stroke="{ink}" stroke-opacity=".5" stroke-width="1.4" stroke-dasharray="7 5"/>
<text class="sans" x="284" y="62" font-size="20" letter-spacing="8" text-anchor="middle" fill="{ink}">{NAME}</text>
<text class="serif" x="280" y="104" font-size="30" text-anchor="middle" fill="{motto_fill}">{escape(CARE_MOTTO[0])}</text>
<text class="serif" x="280" y="140" font-size="30" text-anchor="middle" fill="{motto_fill}">{escape(CARE_MOTTO[1])}</text>
<path d="M200 162H360" stroke="{ink}" stroke-opacity=".35"/>
<g transform="translate(0 16)">
<g fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<g transform="translate(172 194)"><path d="M-22-11-16 16H16L22-11M-22-11q5.5-6 11 0t11 0 11 0 11 0"/></g>
<g transform="translate(244 194)"><path d="M0-18 20 16H-20ZM-18-16 18 16M18-16-18 16"/></g>
<g transform="translate(316 194)"><rect x="-18" y="-18" width="36" height="36"/><circle r="12"/></g>
<g transform="translate(388 194)"><path d="M-22 16-13-4H13q9 0 9 10v10ZM-7-4q2-12 13-12h9"/></g>
</g>
<text class="mono" x="172" y="207" font-size="12" text-anchor="middle" fill="{ink}">1.0</text>
<g fill="{ink}"><circle cx="311" cy="194" r="2"/><circle cx="321" cy="194" r="2"/>
<circle cx="381" cy="203" r="1.8"/><circle cx="388" cy="203" r="1.8"/><circle cx="395" cy="203" r="1.8"/></g>
<text class="mono" x="281" y="250" font-size="14" letter-spacing="2" text-anchor="middle" fill="{ink}">{escape(CARE[0])}</text>
<text class="mono" x="281" y="273" font-size="14" letter-spacing="2" text-anchor="middle" fill="{ink}" fill-opacity=".6">{escape(CARE[1])}</text>
</g>
</svg>"""


def main() -> None:
    write("hero.svg", hero())
    for name, theme in THEMES.items():
        write(f"label-open-source-{name}.svg", label("OPEN SOURCE", "UPSTREAM", theme))
        write(f"label-work-{name}.svg", label("SELECTED WORK", f"01 — {len(WORK):02d}", theme))
        write(f"marquee-{name}.svg", marquee(theme))
        for item in OPEN_SOURCE:
            write(f"work-{item['slug']}-{name}.svg", work_row(item["mark"], item, theme))
        for index, item in enumerate(WORK, start=1):
            write(f"work-{item['slug']}-{name}.svg", work_row(f"{index:02d}", item, theme))
    # A black label on GitHub's light page, a cream one on its dark page.
    write("care-label-light.svg", care_label("#12100e", "#efe7dc", "url(#ember)"))
    write("care-label-dark.svg", care_label("#f1eadf", "#191512", "#d63d0a"))
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
