"""Generates every themed SVG in assets/. Run: python scripts/gen_assets.py"""
import os
from xml.sax.saxutils import escape

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# palette, sampled from the banner's dusk sky
BG = "#0b0d11"
BORDER = "#1f242c"
TEXT = "#e9edf2"
SOFT = "#c3ccd6"
MUTED = "#8e98a6"
DIM = "#4a525e"
ACCENT = "#9fb3c8"
WARM = "#d9c9b0"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'Cascadia Code', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

# text measurement: real fonts when available, so pills and chips fit snugly
FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
FONT_FILES = {("sans", 300): "segoeuil.ttf", ("sans", 400): "segoeui.ttf",
              ("sans", 600): "seguisb.ttf", ("mono", 400): "CascadiaCode.ttf"}
_cache = {}
try:
    from PIL import ImageFont
except ImportError:
    ImageFont = None


def tw(s, size, family="sans", weight=400, spacing=0.0):
    """Text width in px, with a small margin for non-Windows fallback fonts."""
    key = (family, weight, size)
    font = _cache.get(key)
    if font is None and ImageFont:
        try:
            font = ImageFont.truetype(os.path.join(FONT_DIR, FONT_FILES[(family, weight)]), size)
        except (OSError, KeyError):
            font = False
        _cache[key] = font
    if font:
        base = font.getlength(s)
    else:
        base = len(s) * size * (0.6 if family == "mono" else 0.55)
    return base * 1.05 + spacing * max(len(s) - 1, 0)


def t(x, y, s, size, fill, family="sans", weight=400, spacing=0, anchor="start", extra=""):
    fam = MONO if family == "mono" else SANS
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    fw = f' font-weight="{weight}"' if weight != 400 else ""
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}"{fw}{ls}{an} '
            f'fill="{fill}" dominant-baseline="central"{extra}>{escape(s)}</text>')


DEFS = f'''<defs>
    <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="{WARM}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{WARM}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fadeline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glow" cx="0%" cy="0%" r="80%">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
  </defs>'''


def panel(w, h):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#glow)"/>'
            f'<rect x="28" y="0.5" width="140" height="1.5" fill="url(#hair)"/>')


def chip(x, y, label, h=22):
    w = 20 + tw(label, 11.5, "mono")
    return w, (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{ACCENT}" '
               f'fill-opacity="0.06" stroke="{ACCENT}" stroke-opacity="0.28"/>'
               + t(x + w / 2, y + h / 2, label, 11.5, ACCENT, "mono", anchor="middle"))


def save(name, w, h, body, label, style=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
           f'role="img" aria-label="{escape(label)}">\n  {DEFS}\n  {style}\n  {body}\n</svg>\n')
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def clear(prefix):
    for f in os.listdir(ROOT):
        if f.startswith(prefix) and f.endswith(".svg"):
            os.remove(os.path.join(ROOT, f))


# ---------- tagline: three phrases that fade in turn ----------
def tagline():
    w, h = 1200, 44
    phrases = ["building things for small screens",
               "currently: 3ds homebrew & tauri apps",
               "slow software, made with care"]
    n, step = len(phrases), 4
    total = n * step
    style = f'''<style>
    .p {{ opacity: 0; animation: cycle {total}s ease-in-out infinite; }}
    {"".join(f".p{i} {{ animation-delay: {i * step}s; }} " for i in range(n))}
    @keyframes cycle {{ 0% {{ opacity: 0; }} 4% {{ opacity: 1; }} {100 / n - 4:.1f}% {{ opacity: 1; }} {100 / n:.1f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .p {{ animation: none; }} .p0 {{ opacity: 1; }} }}
  </style>'''
    body = "".join(t(600, h / 2, p, 15, ACCENT, weight=300, spacing=1.2, anchor="middle",
                     extra=f' class="p p{i}"') for i, p in enumerate(phrases))
    half = max(tw(p, 15, weight=300, spacing=1.2) for p in phrases) / 2
    for side in (-1, 1):
        x = 600 + side * (half + 28)
        body += f'<rect x="{x - 14 if side > 0 else x - 14:.0f}" y="{h / 2}" width="28" height="1" fill="{DIM}"/>'
    save("tagline.svg", w, h, body, phrases[0], style)


# ---------- intro ----------
def intro():
    w, h = 1200, 268
    rows = [("focus", "3ds homebrew"),
            ("also", "desktop apps · extensions · web"),
            ("stack", "c · c++ · rust · python · ts"),
            ("since", "2024 · 50+ repositories")]
    facts = "".join(t(808, 78 + i * 38, k.upper(), 11, MUTED, spacing=3) + t(900, 78 + i * 38, v, 14.5, SOFT)
                    for i, (k, v) in enumerate(rows))
    style = f'''<style>
    .pulse {{ animation: pulse 3.2s ease-in-out infinite; transform-origin: 54px 64px; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 0.25; transform: scale(1); }} 50% {{ opacity: 0; transform: scale(2.6); }} }}
    @media (prefers-reduced-motion: reduce) {{ .pulse {{ animation: none; opacity: 0; }} }}
  </style>'''
    body = f'''{panel(w, h)}
  <circle class="pulse" cx="54" cy="64" r="4" fill="{WARM}"/>
  <circle cx="54" cy="64" r="3.5" fill="{WARM}"/>
  {t(68, 64, "HELLO, I'M P0MPURIN", 12, ACCENT, spacing=4)}
  {t(48, 112, "I make homebrew, desktop apps", 31, TEXT, weight=300)}
  <text x="48" y="152" font-family="{SANS}" font-size="31" font-weight="300" fill="{TEXT}" dominant-baseline="central">and <tspan fill="{WARM}">small things</tspan> for the web.</text>
  {t(48, 204, "old hardware, simple interfaces, software that stays out of the way.", 15, MUTED)}
  <rect x="764" y="52" width="1" height="164" fill="{BORDER}"/>
  {facts}
  {t(808, 230, "~/p0mpurin $ ls ./projects", 11.5, DIM, "mono")}'''
    save("intro.svg", w, h, body, "hello, i'm p0mpurin", style)


# ---------- section headers ----------
def section(slug, idx, label, note):
    w, h = 1200, 48
    x2 = 44 + tw(label.upper(), 13, spacing=4) + 20
    x3 = 1198 - tw(note, 12) - 20
    body = (t(2, 24, idx, 12, WARM, "mono") + t(44, 24, label.upper(), 13, SOFT, spacing=4)
            + f'<rect x="{x2:.0f}" y="24" width="{x3 - x2:.0f}" height="1" fill="url(#fadeline)"/>'
            + t(1198, 24, note, 12, MUTED, anchor="end"))
    save(f"section-{slug}.svg", w, h, body, f"{idx} {label}")


# ---------- project cards ----------
CARDS = [
    ("rune3ds", "Rune3DS", "#f34b7d", "C++",
     ["A modern 3hs fork for the 3DS: wallpaper theming,", "faster downloads, live speed and ETA."],
     ["3ds", "homebrew"]),
    ("kuroaria", "KuroAria DL", "#dea584", "Rust",
     ["Desktop download manager on Tauri, React and aria2,", "with a browser extension bridge."],
     ["tauri", "desktop"]),
    ("japw", "JAPW", "#3572A5", "Python",
     ["Just A Pinterest Wrapper. Feed, boards and downloads", "in its own quiet window."],
     ["flask", "desktop"]),
    ("kasumi", "Kasumi", "#8a8f98", "C",
     ["Cloud gaming client for the New 3DS, with", "hardware video decoding."],
     ["3ds", "streaming"]),
    ("maki", "maki", "#8a8f98", "C",
     ["Anime streaming on the 3DS through a tiny", "Node proxy that transcodes for the hardware."],
     ["3ds", "node"]),
    ("jumptosb", "jumptosb", "#f1e05a", "JavaScript",
     ["Browser extension: jump to the search bar", "on any site with a single key."],
     ["extension", "web"]),
]


def cards():
    clear("card-")
    w, h = 600, 200
    for i, (slug, title, color, lang, lines, tags) in enumerate(CARDS, 1):
        desc = "".join(t(28, 100 + j * 21, l, 14, MUTED) for j, l in enumerate(lines))
        x, chips = 28, ""
        for tag in tags:
            cw, c = chip(x, 152, tag)
            chips += c
            x += cw + 8
        lang_w = tw(lang, 12.5)
        body = f'''{panel(w, h)}
  {t(28, 38, f"{i:02d}", 11.5, WARM, "mono")}
  {t(572, 38, "↗", 15, MUTED, anchor="end")}
  {t(28, 70, title, 21, TEXT, weight=600, spacing=0.4)}
  {desc}
  {chips}
  <circle cx="{572 - lang_w - 10:.1f}" cy="163" r="4" fill="{color}"/>
  {t(572, 163, lang, 12.5, MUTED, anchor="end")}'''
        save(f"card-{slug}.svg", w, h, body, title)


# ---------- toolkit ----------
def toolkit():
    cols = [("languages", ["c", "c++", "rust", "python", "typescript", "javascript", "gdscript"]),
            ("frameworks", ["react", "tauri", "flask", "node", "tailwind", "pywebview"]),
            ("platforms", ["3ds / luma3ds", "windows", "browser extensions", "vercel", "github actions"])]
    parts, rows = [], 1
    for ci, (label, items) in enumerate(cols):
        x0 = 48 + ci * 384
        parts.append(t(x0, 52, label.upper(), 11, MUTED, spacing=3))
        x, y, r = x0, 74, 1
        for it in items:
            cw = 20 + tw(it, 11.5, "mono")
            if x + cw > x0 + 336:
                x, y, r = x0, y + 32, r + 1
            parts.append(chip(x, y, it)[1])
            x += cw + 8
        rows = max(rows, r)
    h = 74 + rows * 32 + 30
    for ci in (1, 2):
        parts.insert(0, f'<rect x="{48 + ci * 384 - 24}" y="40" width="1" height="{h - 80}" fill="{BORDER}"/>')
    save("toolkit.svg", 1200, h, panel(1200, h) + "".join(parts), "toolkit")


# ---------- link pills ----------
def pill(name, label, w, h, fs, dot, color):
    r = h / 2
    body = (f'<rect x="0.5" y="0.5" width="{w - 1:.0f}" height="{h - 1}" rx="{r - 0.5}" fill="{BG}" stroke="{BORDER}"/>'
            f'<rect x="1" y="1" width="{w - 2:.0f}" height="{h - 2}" rx="{r - 1}" fill="url(#glow)"/>'
            f'<circle cx="{r}" cy="{r}" r="{h / 12:.1f}" fill="{dot}"/>'
            + t(r + 12, r, label, fs, color)
            + t(w - r + 4, r, "↗", fs - 1, DIM if color == MUTED else MUTED, anchor="end"))
    save(name, w, h, body, label)


LINKS = [("site", "purinpage"), ("kofi", "ko-fi"), ("repos", "all repos")]
MORE = [("runefetch", "RuneFetch"), ("nightreign", "Nightreign launcher"), ("vitapapers", "vitapapers"),
        ("discord-css", "discord-css"), ("yt", "yt_downloader")]


def pills():
    clear("link-")
    clear("more-")
    h = 38
    w = max(tw(l, 13.5) for _, l in LINKS) + h / 2 + 12 + 34   # same width for all three
    for slug, label in LINKS:
        pill(f"link-{slug}.svg", label, w, h, 13.5, WARM, SOFT)
    for slug, label in MORE:
        h2 = 28
        pill(f"more-{slug}.svg", label, tw(label, 12) + h2 / 2 + 12 + 26, h2, 12, ACCENT, MUTED)


# ---------- footer ----------
def footer():
    w, h = 1200, 96
    body = f'''<rect x="300" y="20" width="300" height="1" fill="url(#fadeline)" transform="rotate(180 450 20.5)"/>
  <rect x="600" y="20" width="300" height="1" fill="url(#fadeline)"/>
  <circle cx="600" cy="20.5" r="3" fill="{WARM}"/>
  {t(600, 54, "THANKS FOR STOPPING BY", 13, MUTED, spacing=5, anchor="middle")}
  {t(600, 78, "p0mpurin · made slowly, with care", 11, DIM, "mono", anchor="middle")}'''
    save("footer.svg", w, h, body, "thanks for stopping by")


if __name__ == "__main__":
    tagline()
    intro()
    section("works", "01", "works", "selected projects")
    section("toolkit", "02", "toolkit", "what i build with")
    section("activity", "03", "activity", "updated daily")
    cards()
    toolkit()
    pills()
    footer()
    print("ok")
