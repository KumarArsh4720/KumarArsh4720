#!/usr/bin/env python3
"""Builds the self-hosted SVG banners for the GitHub profile README.

Warm palette, quiet geometry, drifting leaves.

GitHub's markdown sanitiser strips <style> blocks and style="" attributes from a
README, so CSS cannot live in the markdown. It *can* live inside an SVG that the
README embeds with <img>, and that CSS animates normally. Everything decorative
here therefore lives in the SVG files, not in README.md.

No dependencies, no web fonts, no network calls: `python3 gen_assets.py`.
"""

import random

# ---------------------------------------------------------------- palette ---
# warm near-black through to lamp-lit amber
BG0, BG1, BG2 = "#17110C", "#1F1710", "#271C13"
AMBER = "#E8A65D"
TERRA = "#D4785A"
SAND = "#F2D7A7"
TEXT = "#EDE3D6"
MUTED = "#A6907A"
DIM = "#6E5C49"

LEAF_TONES = ["#E8A65D", "#D4785A", "#C9955C", "#B87248", "#E5C089", "#A88A52"]

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
ADV = 0.60  # monospace advance width, in em


def tw(s, size):
    """approximate rendered width of monospace text"""
    return len(s) * size * ADV


# ------------------------------------------------------------------ defs ----
def defs(w, h):
    return f"""
    <linearGradient id="panel" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{BG0}"/>
      <stop offset=".55" stop-color="{BG1}"/>
      <stop offset="1" stop-color="{BG2}"/>
    </linearGradient>
    <linearGradient id="warm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{SAND}"/>
      <stop offset="1" stop-color="{AMBER}"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{AMBER}" stop-opacity=".75"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="lamp">
      <stop offset="0" stop-color="{AMBER}" stop-opacity=".22"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="ember">
      <stop offset="0" stop-color="{TERRA}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{TERRA}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1" fill="{AMBER}" fill-opacity=".07"/>
    </pattern>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath>"""


def backdrop(w, h):
    """warm panel, soft dot texture, two slow lamp glows"""
    return f"""
    <rect width="{w}" height="{h}" fill="url(#panel)"/>
    <rect width="{w}" height="{h}" fill="url(#dots)"/>
    <ellipse class="lampA" cx="{int(w*0.30)}" cy="{int(h*0.10)}" rx="{int(w*0.42)}" ry="{int(h*0.95)}" fill="url(#lamp)"/>
    <ellipse class="lampB" cx="{int(w*0.82)}" cy="{int(h*0.92)}" rx="{int(w*0.34)}" ry="{int(h*0.80)}" fill="url(#ember)"/>"""


def border(w, h):
    return (f'\n  <rect x=".9" y=".9" width="{w-1.8}" height="{h-1.8}" rx="17.1" '
            f'fill="none" stroke="{AMBER}" stroke-opacity=".20"/>')


def corners(w, h, arm=18, inset=14):
    s = f'fill="none" stroke="{AMBER}" stroke-opacity=".38" stroke-width="1.3" stroke-linecap="round"'
    x0, y0, x1, y1 = inset, inset, w - inset, h - inset
    return f"""
  <g class="hud">
    <path d="M{x0} {y0+arm}V{y0}H{x0+arm}" {s}/>
    <path d="M{x1-arm} {y0}H{x1}V{y0+arm}" {s}/>
    <path d="M{x1} {y1-arm}V{y1}H{x1-arm}" {s}/>
    <path d="M{x0+arm} {y1}H{x0}V{y1-arm}" {s}/>
  </g>"""


# ----------------------------------------------------------------- leaves ---
LEAF_D = "M6 0C9.7 3.3 12 6.6 6 14 0 6.6 2.3 3.3 6 0Z"
VEIN_D = "M6 1.8V12.2"


def leaves(w, h, count, seed, opacity=(0.28, 0.62), size=(8, 17)):
    """A drifting leaf layer.

    Three nested transforms per leaf so the motions stay independent:
      outer <g>  CSS  — falls top to bottom, slight horizontal drift
      mid   <g>  CSS  — sways side to side and tumbles
      inner <g>  attr — static scale (attribute transform, so CSS never fights it)

    Negative animation-delay seeds each leaf mid-flight, so the banner is already
    full of leaves on the first painted frame instead of starting empty.
    """
    rng = random.Random(seed)
    body, css = [], []

    for i in range(count):
        x = rng.uniform(-30, w + 10)
        drift = rng.uniform(-70, 70)
        dur = rng.uniform(11, 24)
        delay = -rng.uniform(0, dur)
        sway_dur = rng.uniform(2.6, 5.2)
        sway = rng.uniform(9, 22)
        rot0 = rng.uniform(-40, 20)
        rot1 = rot0 + rng.uniform(40, 150)
        sc = rng.uniform(*size) / 12.0
        op = rng.uniform(*opacity)
        col = rng.choice(LEAF_TONES)

        body.append(
            f'\n    <g class="fl f{i}"><g class="sw s{i}">'
            f'<g transform="scale({sc:.3f})" opacity="{op:.2f}">'
            f'<path d="{LEAF_D}" fill="{col}"/>'
            f'<path d="{VEIN_D}" stroke="{BG0}" stroke-opacity=".45" stroke-width=".8"/>'
            f'</g></g></g>'
        )
        css.append(
            ".f%d{animation:fall%d %.2fs linear %.2fs infinite}"
            "@keyframes fall%d{from{transform:translate(%.1fpx,-30px)}"
            "to{transform:translate(%.1fpx,%dpx)}}"
            ".s%d{animation:sway%d %.2fs ease-in-out %.2fs infinite alternate}"
            "@keyframes sway%d{from{transform:translateX(%.1fpx) rotate(%.0fdeg)}"
            "to{transform:translateX(%.1fpx) rotate(%.0fdeg)}}"
            % (i, i, dur, delay, i, x, x + drift, h + 30,
               i, i, sway_dur, delay, i, -sway / 2, rot0, sway / 2, rot1)
        )

    return "".join(body), "".join(css)


# ------------------------------------------------------------ shared css ----
AMBIENCE_CSS = """
    .lampA{animation:driftA 19s ease-in-out infinite}
    .lampB{animation:driftB 23s ease-in-out infinite}
    @keyframes driftA{0%,100%{opacity:.85;transform:translate(0,0)}50%{opacity:1;transform:translate(26px,10px)}}
    @keyframes driftB{0%,100%{opacity:.8;transform:translate(0,0)}50%{opacity:1;transform:translate(-22px,-8px)}}
    .hud{animation:breathe 6s ease-in-out infinite}
    @keyframes breathe{0%,100%{opacity:.9}50%{opacity:.55}}"""

REDUCED = """
    @media(prefers-reduced-motion:reduce){
      .lampA,.lampB,.hud,.fl,.sw,.dot,.name,.sub,.bar,.chip,.ttl{animation:none}
      .chip,.ttl{opacity:1}
    }"""


# ------------------------------------------------------------------ hero ----
def build_hero(name="ARSH KUMAR", role="SOFTWARE DEVELOPER", handle="~/KumarArsh4720"):
    W, H = 1000, 230
    leaf_body, leaf_css = leaves(W, H, count=16, seed=7)

    taglines = [
        "building backend systems and developer tooling",
        "python  ·  javascript  ·  mongodb  ·  node",
        "making hard things simple, one commit at a time",
    ]
    lines = ""
    for i, t in enumerate(taglines):
        lines += (
            f'\n  <text class="tag t{i+1}" x="{W//2}" y="196" text-anchor="middle" '
            f'font-family="{MONO}" font-size="13" fill="{MUTED}">'
            f'<tspan fill="{AMBER}">&#8250; </tspan>{t}</text>'
        )

    css = AMBIENCE_CSS + leaf_css + """
    .dot{animation:pulse 3.4s ease-in-out infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
    .name{animation:rise 1.2s cubic-bezier(.2,.7,.2,1) both}
    .sub{animation:rise 1.2s .16s cubic-bezier(.2,.7,.2,1) both}
    @keyframes rise{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
    .bar{animation:grow 1.1s .3s cubic-bezier(.2,.7,.2,1) both;transform-origin:500px 0}
    @keyframes grow{from{transform:scaleX(0);opacity:0}to{transform:scaleX(1);opacity:1}}
    .tag{opacity:0;animation:cyc 21s infinite}
    .t1{animation-delay:.7s}.t2{animation-delay:7.7s}.t3{animation-delay:14.7s}
    @keyframes cyc{0%{opacity:0;transform:translateY(4px)}
      4%{opacity:1;transform:translateY(0)}29%{opacity:1;transform:translateY(0)}
      33%{opacity:0;transform:translateY(-4px)}100%{opacity:0;transform:translateY(-4px)}}""" + REDUCED

    status = "OPEN TO COLLABORATE"
    status_w = tw(status, 11) + len(status) * 2

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img" aria-label="{name} — {role}">
  <defs>{defs(W, H)}
    <style>{css}
    </style>
  </defs>

  <g clip-path="url(#frame)">{backdrop(W, H)}{leaf_body}
  </g>{border(W, H)}{corners(W, H)}

  <text x="36" y="38" font-family="{MONO}" font-size="11" fill="{DIM}" letter-spacing="1">{handle}</text>
  <g transform="translate({W-36} 34)">
    <text x="0" y="4" text-anchor="end" font-family="{MONO}" font-size="11"
          fill="{MUTED}" letter-spacing="2">{status}</text>
    <circle class="dot" cx="{-status_w-12:.0f}" cy="0" r="3.2" fill="{AMBER}"/>
  </g>

  <text class="name" x="{W//2}" y="120" text-anchor="middle" font-family="{MONO}"
        font-size="50" font-weight="700" letter-spacing="8" fill="url(#warm)">{name}</text>
  <text class="sub" x="{W//2}" y="148" text-anchor="middle" font-family="{MONO}"
        font-size="11" letter-spacing="6" fill="{MUTED}">{role}</text>

  <g class="bar">
    <rect x="368" y="167" width="264" height="1.2" fill="url(#rule)"/>
    <path d="M500 163.4 503.2 168 500 172.6 496.8 168Z" fill="{AMBER}" fill-opacity=".85"/>
  </g>
{lines}
</svg>
"""


# ----------------------------------------------------------------- stack ----
def build_stack():
    W = 1000
    rows = [
        ("LANGUAGES", ["Python", "JavaScript", "HTML5", "CSS3"]),
        ("BACKEND · DATA", ["Node.js", "MongoDB", "PyMongo", "NumPy", "REST APIs"]),
        ("TOOLING", ["Git", "GitHub Actions", "VS Code", "Linux"]),
    ]

    pad_x, chip_h, gap, fs = 16, 32, 11, 13.5
    label_w, row_h, top = 150, 54, 46
    H = top + row_h * len(rows) + 16
    track_x0 = 34 + label_w

    leaf_body, leaf_css = leaves(W, H, count=9, seed=21,
                                 opacity=(0.18, 0.40), size=(7, 13))

    body, idx = "", 0
    for r, (label, chips) in enumerate(rows):
        cy = top + r * row_h
        body += (f'\n  <text x="34" y="{cy + chip_h/2 + 4.5}" font-family="{MONO}" '
                 f'font-size="11" letter-spacing="1.6" fill="{DIM}">{label}</text>')
        x = track_x0
        for c in chips:
            w = tw(c, fs) + pad_x * 2
            body += (
                f'\n  <g class="chip c{idx}">'
                f'<rect x="{x:.1f}" y="{cy}" width="{w:.1f}" height="{chip_h}" rx="10"'
                f' fill="#241A13" stroke="{AMBER}" stroke-opacity=".28"/>'
                f'<text x="{x + w/2:.1f}" y="{cy + chip_h/2 + 4.8:.1f}" text-anchor="middle"'
                f' font-family="{MONO}" font-size="{fs}" fill="{TEXT}">{c}</text></g>'
            )
            x += w + gap
            idx += 1

    delays = "".join(".c%d{animation-delay:%.2fs}" % (i, i * 0.06) for i in range(idx))
    css = AMBIENCE_CSS + leaf_css + """
    .chip{opacity:0;animation:pop .6s cubic-bezier(.2,.7,.2,1) both}
    .ttl{animation:pop .6s cubic-bezier(.2,.7,.2,1) both}
    @keyframes pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
    """ + delays + REDUCED

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
  <defs>{defs(W, H)}
    <style>{css}
    </style>
  </defs>

  <g clip-path="url(#frame)">{backdrop(W, H)}{leaf_body}
  </g>{border(W, H)}{corners(W, H)}

  <text class="ttl" x="34" y="30" font-family="{MONO}" font-size="11"
        letter-spacing="2.4" fill="{MUTED}"><tspan fill="{AMBER}">// </tspan>TECH STACK</text>{body}
</svg>
"""


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).parent / "assets"
    out.mkdir(exist_ok=True)
    (out / "hero.svg").write_text(build_hero(), encoding="utf-8")
    (out / "stack.svg").write_text(build_stack(), encoding="utf-8")
    for f in sorted(out.glob("*.svg")):
        print(f"{f.name:12} {f.stat().st_size:>7,} bytes")
