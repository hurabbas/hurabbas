#!/usr/bin/env python3
"""Builds the profile infographic and contact buttons in GitHub's own (Primer) styling.

Outputs:
  assets/profile-{desktop,tablet,mobile}.svg   the infographic, one layout per screen size
  assets/btn-{email,linkedin}.svg              contact buttons, linked from README.md

Each SVG switches between GitHub's light and dark colours itself, with a prefers-color-scheme
media query inside the file. README.md's <picture> only chooses by screen width: GitHub's own
theme script rewrites any <source> that mentions prefers-color-scheme, which breaks width rules.

Edit CONTENT below, then run:  python3 scripts/build_profile.py
GitHub renders SVGs as images, so everything (including line wrapping) is laid out here,
once per screen size, so text stays at GitHub's own sizes on every screen.
The background is transparent so the image blends into the README page.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# Canvas width per screen size, close to the README's real width there so the image isn't scaled much.
# README.md switches at 543px and 1011px of viewport width (GitHub's own breakpoints).
SIZES = {"desktop": 880, "tablet": 620, "mobile": 380}
W = SIZES["desktop"]                 # set per size before each build

# ---------------------------------------------------------------- content
NAME = "Hur Abbas"
STATUS = "Open to senior & lead roles"
ROLES = ["Senior Full Stack Engineer", "Mobile Engineer · iOS & Android", "AI & LLM Engineer", "Team Lead & Mentor"]
CHIPS = ["8+ years", "Web · Mobile · Desktop · AI", "Lahore, Pakistan"]
HERO_STACK = "React Native · Flutter · Swift · Kotlin · Electron · Next.js"

STATS = [("8+", "years building", "production software"),
         ("6+", "years leading", "engineering teams"),
         ("4", "platforms", "web · iOS · Android · desktop"),
         ("0 → 1", "idea to launch", "MVPs to production scale")]

ABOUT = ("I'm a Senior Full Stack and Mobile Engineer and Team Lead. At Devsinc I lead cross-functional teams "
         "building TypeScript products for international clients, owning architecture, code review, mentoring, CI/CD "
         "and reliable releases. My products have shipped across many industries, from real estate and fintech to ride-hailing, data governance and Web3.")

BUILD = [
    ("web", "Full stack web", ["React, Next.js and Remix front ends", "Node.js, NestJS, Python and Go APIs", "PostgreSQL, REST and GraphQL, on AWS"]),
    ("mobile", "Mobile apps", ["React Native and Flutter for iOS and Android", "Native Swift/SwiftUI and Kotlin", "Live tracking, payments, push, store releases"]),
    ("desktop", "Desktop apps", ["Electron for Windows, macOS and Linux", "AI-assisted from planning to packaging", "Complete desktop apps, end to end"]),
    ("ai", "AI & LLM products", ["LangChain, LangGraph and RAG", "OpenAI and Claude APIs, tool calling", "pgvector, Pinecone and n8n automations"]),
]

EXPERIENCE = [
    ("May 2022 – Present", "Team Lead · Senior Software Engineer", "Devsinc",
     "Lead teams shipping web and mobile products: architecture, code reviews, mentoring, CI/CD and production incidents."),
    ("Mar 2020 – May 2022", "Team Lead · Senior Software Engineer", "KryptoMind LLC",
     "Led delivery of DApps with Solidity and Rust smart contracts, plus React and React Native apps."),
    ("Jan 2019 – Mar 2020", "Full Stack Developer", "Coding Pixel USA",
     "Built web and mobile apps, REST APIs and payment integrations for client products."),
]

STACK = [
    ("Languages", ["TypeScript", "JavaScript", "Python", "Go", "Java", "Kotlin", "Swift", "Dart", "Rust", "Solidity"]),
    ("Mobile & desktop", ["React Native", "Flutter", "SwiftUI", "Kotlin / Android", "Electron", "App Store", "Google Play"]),
    ("AI & automation", ["LangChain", "LangGraph", "OpenAI API", "Claude API", "Vercel AI SDK", "RAG", "pgvector", "Pinecone", "n8n", "Zapier"]),
    ("Frontend", ["React", "Next.js", "Remix", "Redux", "Tailwind CSS", "GraphQL"]),
    ("Backend", ["Node.js", "Express", "NestJS", "Django", "Flask", "Spring Boot", "Gin", "Fiber"]),
    ("Data", ["PostgreSQL", "MySQL", "MongoDB", "DynamoDB", "Neo4j", "Firebase", "SQLite"]),
    ("Cloud & DevOps", ["AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform", "GitHub Actions", "Linux"]),
    ("Web3", ["Solidity", "Ethereum", "Polygon", "Stellar", "Security tokens", "Wallets", "DApps"]),
]

HOW = [
    ("Own it end to end", "From the requirement to a reliable release, with decisions written down so nobody chases status."),
    ("Raise the bar", "Code reviews that lift team standards, and mentoring engineers along the way."),
    ("Async by default", "Comfortable across timezones with product, design and client teams."),
]

CONTACT = "Open to senior full stack, mobile, AI engineering and team lead roles. Email me or connect on LinkedIn."
BUTTONS = [("email", "Email me", "primary"), ("linkedin", "LinkedIn", "default")]

# ---------------------------------------------------------------- GitHub Primer tokens
THEMES = {
    "dark": dict(bg="#0d1117", muted_bg="#151b23", border="#3d444d", border_muted="#3d444db3",
                 fg="#f0f6fc", muted="#9198a1", accent="#4493f8", tag_bg="#388bfd1a",
                 success="#3fb950", done="#ab7df8", attention="#d29922", severe="#db6d28",
                 kw="#ff7b72", str="#a5d6ff", const="#79c0ff", ent="#d2a8ff", var="#ffa657",
                 btn_bg="#212830", btn_border="#3d444d", btn_fg="#f0f6fc", primary_bg="#238636", primary_border="#2ea043"),
    "light": dict(bg="#ffffff", muted_bg="#f6f8fa", border="#d1d9e0", border_muted="#d1d9e0b3",
                  fg="#1f2328", muted="#59636e", accent="#0969da", tag_bg="#ddf4ff",
                  success="#1a7f37", done="#8250df", attention="#9a6700", severe="#bc4c00",
                  kw="#cf222e", str="#0a3069", const="#0550ae", ent="#6639ba", var="#953800",
                  btn_bg="#f6f8fa", btn_border="#d1d9e0", btn_fg="#25292e", primary_bg="#1f883d", primary_border="#1a7f37"),
}

FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'

# ---------------------------------------------------------------- helpers
e = lambda s: escape(s, quote=True)


def text_w(s, size, bold=False, mono=False):
    return len(s) * size * (0.6 if mono else 0.53 if bold else 0.5)


def wrap(s, size, width, bold=False):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if text_w(trial, size, bold) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur] if cur else lines


def para(x, y, s, size, width, fill, lh=1.5, weight=400):
    lines = wrap(s, size, width, weight >= 600)
    out = "".join(f'<text x="{x:.0f}" y="{y + i * size * lh:.0f}" font-size="{size}" font-weight="{weight}" fill="{fill}">{e(l)}</text>'
                  for i, l in enumerate(lines))
    return out, len(lines) * size * lh


ICONS = {  # 16x16 outline icons in the spirit of Octicons
    "web": '<rect x="1.5" y="2.5" width="13" height="11" rx="1.5"/><path d="M1.5 5.5h13"/>',
    "mobile": '<rect x="4" y="1.5" width="8" height="13" rx="1.5"/><path d="M7 12h2"/>',
    "desktop": '<rect x="1.5" y="2" width="13" height="9" rx="1.5"/><path d="M5.5 14h5M8 11v3"/>',
    "ai": '<path d="M8 1.5l1.4 3.6L13 6.5 9.4 7.9 8 11.5 6.6 7.9 3 6.5l3.6-1.4z"/><path d="M12.5 11l.5 1.3 1.3.5-1.3.5-.5 1.2-.5-1.2-1.3-.5 1.3-.5z"/>',
    "own": '<circle cx="8" cy="8" r="6.5"/><path d="M5.5 8.2l1.7 1.7L10.6 6.4"/>',
    "bar": '<path d="M2 14.5h12M4 12V8M8 12V3.5M12 12V6"/>',
    "async": '<circle cx="8" cy="8" r="6.5"/><path d="M8 4.5V8l2.3 1.5"/>',
    "file": '<path d="M3.5 1.5h6l3 3v10h-9z"/><path d="M9.5 1.5v3h3"/>',
    "commit": '<circle cx="8" cy="8" r="3"/><path d="M1 8h4M11 8h4"/>',
    "email": '<rect x="1.5" y="3" width="13" height="10" rx="1.5"/><path d="M2 4l6 4.5L14 4"/>',
}


def icon(name, x, y, color, sw=1.5):
    return (f'<g transform="translate({x:.0f} {y:.0f})" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def h2(y, title, t, size=24):
    # matches a markdown ## heading: semibold with a bottom border
    return (f'<text x="0" y="{y + size + 6}" font-size="{size}" font-weight="600" fill="{t["fg"]}">{e(title)}</text>'
            f'<line x1="0" y1="{y + size + 20.5}" x2="{W}" y2="{y + size + 20.5}" stroke="{t["border_muted"]}"/>'), size + 40


def label(x, y, s, t):
    w = text_w(s, 12, bold=True) + 18
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.0f}" height="22" rx="11" fill="none" stroke="{t["border"]}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 15}" text-anchor="middle" font-size="12" font-weight="500" fill="{t["muted"]}">{e(s)}</text>'), w


def topic(x, y, s, t):
    w = text_w(s, 12, bold=True) + 18
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{t["tag_bg"]}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" font-size="12" font-weight="500" fill="{t["accent"]}">{e(s)}</text>'), w


def box(x, y, w, h, t, fill=None):
    return f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{w - 1:.0f}" height="{h - 1:.0f}" rx="6" fill="{fill or t["bg"]}" stroke="{t["border"]}"/>'


def fade(inner, delay):
    return f'<g class="in" style="animation-delay:{delay:.2f}s">{inner}</g>'


def flow(items, x0, y0, width, gap, row_h, make):
    """Lays out pill-shaped items left to right, wrapping to new rows. Returns (svg, rows)."""
    out, x, row = [], x0, 0
    for it in items:
        g, w = make(0, 0, it)
        if x + w > x0 + width and x > x0:
            x, row = x0, row + 1
        g, w = make(x, y0 + row * row_h, it)
        out.append(g)
        x += w + gap
    return "".join(out), row + 1


def grid(n, cols, gap=16):
    w = (W - (cols - 1) * gap) / cols
    return w, [((i % cols) * (w + gap), i // cols) for i in range(n)]


# ---------------------------------------------------------------- infographic
def build(t, size):
    wide, narrow = W >= 760, W < 500
    parts, d = [], 0.0

    # --- hero: intro, with a GitHub-style file view beside it (wide) or below it
    lw = 446 if wide else W
    name_size = 44 if wide else 40 if not narrow else 36
    role_size = 20 if not narrow else 18
    hero = [fade(
        f'<rect x="0.5" y="0.5" width="{text_w(STATUS, 12, True) + 36:.0f}" height="23" rx="11.5" fill="none" stroke="{t["success"]}" stroke-opacity=".6"/>'
        f'<circle class="live" cx="13" cy="12" r="4" fill="{t["success"]}"/><circle cx="13" cy="12" r="4" fill="{t["success"]}"/>'
        f'<text x="24" y="16" font-size="12" font-weight="500" fill="{t["success"]}">{e(STATUS)}</text>', .05)]
    hero.append(fade(f'<text x="-2" y="{30 + name_size + 4}" font-size="{name_size}" font-weight="600" letter-spacing="-.5" fill="{t["fg"]}">{e(NAME)}</text>', .15))
    ry = 30 + name_size + 4 + 36
    hero.append(fade(
        f'<text x="0" y="{ry}" font-size="{role_size}" fill="{t["accent"]}" style="font-family:{e(MONO)}">&gt;</text>'
        + "".join(f'<text class="role" style="animation-delay:{i * 3}s" x="{role_size + 2}" y="{ry}" font-size="{role_size}" fill="{t["muted"]}">{e(r)}</text>'
                  for i, r in enumerate(ROLES)), .3))
    chips, rows = flow(CHIPS, .5, ry + 26.5, lw, 6, 30, lambda x, y, c: label(x, y, c, t))
    sy = ry + 26 + rows * 30 + 26
    stack, sh = para(0, sy, HERO_STACK, 14, lw, t["muted"])
    hero.append(fade(chips + stack, .45))
    left_h = sy + sh - 14

    def arr(k, items):
        sep = f'<tspan fill="{t["fg"]}">, </tspan>'
        return (f'<tspan fill="{t["const"]}">{k}</tspan><tspan fill="{t["fg"]}">: [</tspan>'
                + sep.join(f'<tspan fill="{t["str"]}">"{i}"</tspan>' for i in items) + f'<tspan fill="{t["fg"]}">],</tspan>')
    pad = f'<tspan fill="{t["fg"]}">  </tspan>'
    code = [
        f'<tspan fill="{t["kw"]}">const</tspan><tspan fill="{t["var"]}"> hur</tspan><tspan fill="{t["kw"]}"> =</tspan><tspan fill="{t["fg"]}"> {{</tspan>',
        pad + f'<tspan fill="{t["const"]}">role</tspan><tspan fill="{t["fg"]}">: </tspan><tspan fill="{t["str"]}">"Team Lead"</tspan><tspan fill="{t["fg"]}">,</tspan>',
        pad + arr("web", ["TS", "React", "Node", "Go"]),
        pad + arr("apps", ["iOS", "Android", "Desktop"]),
        pad + arr("ai", ["LangGraph", "RAG", "Claude"]),
        pad + f'<tspan fill="{t["const"]}">ships</tspan><tspan fill="{t["fg"]}">: </tspan><tspan fill="{t["const"]}">true</tspan><tspan fill="{t["fg"]}">,</tspan>',
        f'<tspan fill="{t["fg"]}">}};</tspan><tspan class="caret" fill="{t["fg"]}">▍</tspan>',
    ]
    fx, fy = (466, 0) if wide else (0, left_h + 28)
    fw, fh = W - fx, 40 + len(code) * 20 + 24
    code_size = 13 if not narrow else 12
    rows = "".join(
        f'<text class="in" style="animation-delay:{.5 + i * .18:.2f}s;font-family:{e(MONO)}" x="{fx + 30}" y="{fy + 76 + i * 20}" font-size="12" text-anchor="end" fill="{t["muted"]}">{i + 1}</text>'
        f'<text class="in" style="animation-delay:{.5 + i * .18:.2f}s;font-family:{e(MONO)}" x="{fx + 44}" y="{fy + 76 + i * 20}" font-size="{code_size}" xml:space="preserve">{c}</text>'
        for i, c in enumerate(code))
    hero.append(fade(
        box(fx, fy, fw, fh, t)
        + f'<path d="M{fx + 6.5} {fy + .5}h{fw - 13}a6 6 0 0 1 6 6v33.5H{fx + .5}V{fy + 6.5}a6 6 0 0 1 6-6z" fill="{t["muted_bg"]}" stroke="{t["border"]}"/>'
        + icon("file", fx + 14, fy + 12, t["muted"])
        + f'<text x="{fx + 38}" y="{fy + 25}" font-size="14" font-weight="600" fill="{t["fg"]}">hur.ts</text>'
        + f'<text x="{W - 14}" y="{fy + 25}" font-size="12" text-anchor="end" fill="{t["muted"]}">{len(code)} lines · TypeScript</text>'
        + rows, .2))
    parts += hero
    y, d = (max(fh, left_h) if wide else fy + fh) + 32, .6

    # --- stats
    sw, cells = grid(len(STATS), 4 if wide else 2, 12 if not wide else 16)
    sh = 74 + max(len(wrap(b, 12, sw - 28)) for _, _, b in STATS) * 18
    for i, ((num, a, b), (x, r)) in enumerate(zip(STATS, cells)):
        sy = y + r * (sh + 12)
        sub, _ = para(x + 16, sy + 77, b, 12, sw - 28, t["muted"])
        parts.append(fade(box(x, sy, sw, sh, t)
                          + f'<text x="{x + 16:.0f}" y="{sy + 38}" font-size="26" font-weight="600" fill="{t["fg"]}">{e(num)}</text>'
                          + f'<text x="{x + 16:.0f}" y="{sy + 60}" font-size="14" font-weight="600" fill="{t["fg"]}">{e(a)}</text>'
                          + sub, d + i * .06))
    y += (cells[-1][1] + 1) * (sh + 12) - 12 + 24
    d += .3
    hs = 24 if not narrow else 22

    # --- about
    g, dh = h2(y, "Hi, I'm Hur 👋", t, hs)
    p, ph = para(0, y + dh + 16, ABOUT, 16, W - 6, t["fg"])
    parts.append(fade(g + p, d))
    y += dh + ph + 24
    d += .1

    # --- what I build
    g, dh = h2(y, "What I build", t, hs)
    parts.append(fade(g, d))
    y += dh + 16
    bw, cells = grid(len(BUILD), 2 if W >= 560 else 1)
    wrapped = [[wrap(it, 14, bw - 60) for it in items] for _, _, items in BUILD]
    bh = 52 + max(sum(len(w) * 20 + 4 for w in ws) for ws in wrapped) + 12
    colors = [t["accent"], t["success"], t["severe"], t["done"]]
    for i, ((ic, title, _), (x, r)) in enumerate(zip(BUILD, cells)):
        by, ly, lis = y + r * (bh + 16), y + r * (bh + 16) + 69, []
        for w in wrapped[i]:
            lis.append(f'<circle cx="{x + 22:.0f}" cy="{ly - 5}" r="2" fill="{t["muted"]}"/>')
            lis += [f'<text x="{x + 34:.0f}" y="{ly + k * 20}" font-size="14" fill="{t["fg"]}">{e(l)}</text>' for k, l in enumerate(w)]
            ly += len(w) * 20 + 4
        parts.append(fade(box(x, by, bw, bh, t) + icon(ic, x + 16, by + 18, colors[i])
                          + f'<text x="{x + 42:.0f}" y="{by + 31}" font-size="16" font-weight="600" fill="{t["fg"]}">{e(title)}</text>'
                          + "".join(lis), d + .05 + i * .06))
    y += (cells[-1][1] + 1) * (bh + 16) - 16 + 24
    d += .35

    # --- experience, as a GitHub timeline
    g, dh = h2(y, "Experience", t, hs)
    parts.append(fade(g, d))
    y += dh + 16
    top, items = y, []
    for i, (when, role, co, desc) in enumerate(EXPERIENCE):
        title, th = para(48, y + 21, role, 16, W - 52, t["fg"], lh=1.35, weight=600)
        meta_y = y + 21 + th - 16 * 1.35 + 22
        p, ph = para(48, meta_y + 23, desc, 14, W - 54, t["fg"])
        meta = (f'<text x="48" y="{meta_y:.0f}" font-size="14"><tspan font-weight="600" fill="{t["accent"]}">{e(co)}</tspan>'
                f'<tspan fill="{t["muted"]}">  ·  {e(when)}</tspan></text>')
        items.append(fade(
            f'<circle cx="16" cy="{y + 16}" r="16" fill="{t["muted_bg"]}" stroke="{t["border"]}"/>' + icon("commit", 8, y + 8, t["muted"])
            + title + meta + p, d + .1 + i * .1))
        y = meta_y + 23 + ph - 14 + 30
    parts.append(f'<line x1="16" y1="{top + 32}" x2="16" y2="{y - 40:.0f}" stroke="{t["border"]}" stroke-width="2"/>')
    parts += items
    y += 4
    d += .4

    # --- tech stack, as GitHub topic tags (label column when there's room, label above tags when narrow)
    g, dh = h2(y, "Tech stack", t, hs)
    parts.append(fade(g, d))
    y += dh + 16
    lx = 156 if W >= 560 else 0
    for gi, (name, tags) in enumerate(STACK):
        head = f'<text x="0" y="{y + 17}" font-size="14" font-weight="600" fill="{t["fg"]}">{e(name)}</text>'
        ty = y if lx else y + 26
        tags_svg, rows = flow(tags, lx, ty, W - lx, 6, 32, lambda x, yy, s: topic(x, yy, s, t))
        parts.append(fade(head + tags_svg, d + .05 + gi * .04))
        y = ty + rows * 32 + (8 if lx else 14)
    y += 16
    d += .4

    # --- how I work
    g, dh = h2(y, "How I work", t, hs)
    parts.append(fade(g, d))
    y += dh + 16
    hw, cells = grid(len(HOW), 3 if wide else 1, 16 if wide else 12)
    descs = [para(x + 16, 0, desc, 14, hw - 32, t["muted"])[1] for (_, desc), (x, _) in zip(HOW, cells)]
    # side by side, cards share the tallest height; stacked, each card fits its own text
    heights = [84 + (max(descs) if wide else ph) - 2 for ph in descs]
    hy = y
    for i, ((title, desc), (x, r)) in enumerate(zip(HOW, cells)):
        hh = heights[i]
        p, _ = para(x + 16, hy + 84, desc, 14, hw - 32, t["muted"])
        parts.append(fade(box(x, hy, hw, hh, t) + icon(["own", "bar", "async"][i], x + 16, hy + 18, [t["success"], t["attention"], t["accent"]][i])
                          + f'<text x="{x + 16:.0f}" y="{hy + 56}" font-size="16" font-weight="600" fill="{t["fg"]}">{e(title)}</text>' + p,
                          d + .05 + i * .06))
        if not wide:
            hy += hh + 12
    y = (y + heights[0] if wide else hy - 12) + 24
    d += .3

    # --- get in touch (the clickable buttons sit right below this image in README.md)
    g, dh = h2(y, "Get in touch", t, hs)
    p, ph = para(0, y + dh + 16, CONTACT, 16, W - 6, t["fg"])
    parts.append(fade(g + p, d))
    H = int(y + dh + ph + 4)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hur Abbas — Senior Full Stack, Mobile and AI Engineer and Team Lead with 8+ years.">
  <style>
    text {{ font-family: {FONT}; }}
    .in {{ opacity: 0; animation: rise .6s ease-out forwards; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    .live {{ animation: ping 2s ease-out infinite; transform-origin: 13px 12px; }}
    @keyframes ping {{ 0% {{ opacity: .6; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(2.4); }} }}
    .role {{ opacity: 0; animation: role {len(ROLES) * 3}s ease-in-out infinite; }}
    @keyframes role {{ 0% {{ opacity: 0; transform: translateY(6px); }} {100 / len(ROLES) * .12:.0f}%, {100 / len(ROLES) * .88:.0f}% {{ opacity: 1; transform: none; }} {100 / len(ROLES):.0f}%, 100% {{ opacity: 0; transform: translateY(-6px); }} }}
    .caret {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .in, .live, .caret {{ animation: none; opacity: 1; }}
      .role {{ animation: none; }} .role:first-of-type {{ opacity: 1; }}
    }}
  </style>
{"".join(parts)}
</svg>
'''


# ---------------------------------------------------------------- buttons (Primer "btn" and "btn-primary")
def button(kind, text, style, t):
    w = int(text_w(text, 14, bold=True) + 52)
    primary = style == "primary"
    bg, border, fg = (t["primary_bg"], t["primary_border"], "#ffffff") if primary else (t["btn_bg"], t["btn_border"], t["btn_fg"])
    mark = (icon("email", 12, 8, fg) if kind == "email" else
            f'<rect x="12" y="8" width="16" height="16" rx="3" fill="{fg}"/>'
            f'<text x="20" y="20.5" text-anchor="middle" font-size="11" font-weight="700" fill="{bg}">in</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="32" viewBox="0 0 {w} 32" role="img" aria-label="{e(text)}">'
            f'<style>text {{ font-family: {FONT}; }}</style>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="31" rx="6" fill="{bg}" stroke="{border}"/>{mark}'
            f'<text x="36" y="21" font-size="14" font-weight="500" fill="{fg}">{e(text)}</text></svg>\n')


def themed(svg, buttons=False):
    """Adds dark-mode overrides to an SVG drawn in light colours: each light token maps to its dark one.
    Buttons and the infographic share some light values, so each only maps its own tokens."""
    light, dark = THEMES["light"], THEMES["dark"]
    own = lambda k: k.startswith(("btn_", "primary_")) == buttons
    pairs = {light[k]: dark[k] for k in light if own(k) and light[k] != dark[k]}
    assert len(pairs) == len({light[k] for k in light if own(k) and light[k] != dark[k]})
    rules = " ".join(f'[fill="{a}"] {{ fill: {b}; }} [stroke="{a}"] {{ stroke: {b}; }}' for a, b in pairs.items())
    return svg.replace("</style>", f"@media (prefers-color-scheme: dark) {{ {rules} }}</style>", 1)


if __name__ == "__main__":
    light = THEMES["light"]
    for size, width in SIZES.items():
        W = width
        (OUT / f"profile-{size}.svg").write_text(themed(build(light, size)), encoding="utf-8")
    for kind, text, style in BUTTONS:
        (OUT / f"btn-{kind}.svg").write_text(themed(button(kind, text, style, light), buttons=True), encoding="utf-8")
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
