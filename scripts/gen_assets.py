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
ACCENT = "#9fb3c8"
WARM = "#d9c9b0"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'Cascadia Code', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


def tw(s, size, k=0.56):
    """Rough text width for layout."""
    return len(s) * size * k


def defs(extra=""):
    return f'''<defs>
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
    {extra}
  </defs>'''


def panel(w, h):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#glow)"/>'
            f'<rect x="28" y="0.5" width="140" height="1.5" fill="url(#hair)"/>')


def chip(x, y, label, h=22):
    w = 16 + tw(label, 11.5, 0.6)
    return w, (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h // 2}" fill="{ACCENT}" fill-opacity="0.06" stroke="{ACCENT}" stroke-opacity="0.28"/>'
               f'<text x="{x + w / 2:.0f}" y="{y + 15}" font-family="{MONO}" font-size="11.5" fill="{ACCENT}" text-anchor="middle">{escape(label)}</text>')


def save(name, w, h, body, label):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{escape(label)}">\n  {defs()}\n  {body}\n</svg>\n')
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


# ---------- intro ----------
def intro():
    w, h = 1200, 260
    rows = [("focus", "3ds homebrew"),
            ("also", "desktop apps · extensions · web"),
            ("stack", "c · c++ · rust · python · ts"),
            ("since", "2024 · 50+ repositories")]
    facts = "".join(
        f'<text x="804" y="{82 + i * 38}" font-family="{SANS}" font-size="11" letter-spacing="3" fill="{MUTED}">{k.upper()}</text>'
        f'<text x="896" y="{82 + i * 38}" font-family="{SANS}" font-size="14.5" fill="{SOFT}">{escape(v)}</text>'
        for i, (k, v) in enumerate(rows))
    body = f'''{panel(w, h)}
  <circle cx="52" cy="62" r="3.5" fill="{WARM}"/>
  <text x="66" y="66" font-family="{SANS}" font-size="12" letter-spacing="4" fill="{ACCENT}">HELLO, I'M P0MPURIN</text>
  <text x="48" y="118" font-family="{SANS}" font-size="31" font-weight="300" fill="{TEXT}">I make homebrew, desktop apps</text>
  <text x="48" y="158" font-family="{SANS}" font-size="31" font-weight="300" fill="{TEXT}">and <tspan fill="{WARM}">small things</tspan> for the web.</text>
  <text x="48" y="206" font-family="{SANS}" font-size="15" fill="{MUTED}">old hardware, simple interfaces, software that stays out of the way.</text>
  <rect x="760" y="48" width="1" height="164" fill="{BORDER}"/>
  {facts}'''
    save("intro.svg", w, h, body, "hello, i'm p0mpurin")


# ---------- section headers ----------
def section(slug, idx, label, note):
    w, h = 1200, 48
    lw = tw(label, 13, 0.75)
    x2 = 44 + lw + 22
    nw = tw(note, 12, 0.55)
    body = f'''<text x="2" y="30" font-family="{MONO}" font-size="12" fill="{WARM}">{idx}</text>
  <text x="44" y="30" font-family="{SANS}" font-size="13" letter-spacing="4" fill="{SOFT}">{label.upper()}</text>
  <rect x="{x2:.0f}" y="25" width="{1200 - x2 - nw - 24:.0f}" height="1" fill="url(#fadeline)"/>
  <text x="1198" y="30" font-family="{SANS}" font-size="12" fill="{MUTED}" text-anchor="end">{escape(note)}</text>'''
    save(f"section-{slug}.svg", w, h, body, label)


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
    for f in os.listdir(ROOT):
        if f.startswith("card-"):
            os.remove(os.path.join(ROOT, f))
    w, h = 600, 200
    for i, (slug, title, color, lang, lines, tags) in enumerate(CARDS, 1):
        desc = "".join(f'<text x="28" y="{104 + j * 21}" font-family="{SANS}" font-size="14" fill="{MUTED}">{escape(l)}</text>'
                       for j, l in enumerate(lines))
        x, chips = 28, ""
        for t in tags:
            cw, c = chip(x, 152, t)
            chips += c
            x += cw + 8
        body = f'''{panel(w, h)}
  <text x="28" y="40" font-family="{MONO}" font-size="11.5" fill="{WARM}">{i:02d}</text>
  <text x="572" y="41" font-family="{SANS}" font-size="15" fill="{MUTED}" text-anchor="end">↗</text>
  <text x="28" y="74" font-family="{SANS}" font-size="21" font-weight="600" fill="{TEXT}" letter-spacing="0.4">{escape(title)}</text>
  {desc}
  {chips}
  <circle cx="{572 - tw(lang, 12.5, 0.56) - 11:.0f}" cy="163" r="4" fill="{color}"/>
  <text x="572" y="167.5" font-family="{SANS}" font-size="12.5" fill="{MUTED}" text-anchor="end">{escape(lang)}</text>'''
        save(f"card-{slug}.svg", w, h, body, title)


# ---------- toolkit ----------
def toolkit():
    w, h = 1200, 156
    cols = [("languages", ["c", "c++", "rust", "python", "typescript", "javascript", "gdscript"]),
            ("frameworks", ["react", "tauri", "flask", "node", "tailwind", "pywebview"]),
            ("platforms", ["3ds / luma3ds", "windows", "browser extensions", "vercel", "github actions"])]
    body = panel(w, h)
    for ci, (label, items) in enumerate(cols):
        x0 = 48 + ci * 384
        body += f'<text x="{x0}" y="56" font-family="{SANS}" font-size="11" letter-spacing="3" fill="{MUTED}">{label.upper()}</text>'
        x, y = x0, 76
        for it in items:
            cw = 16 + tw(it, 11.5, 0.6)
            if x + cw > x0 + 340:
                x, y = x0, y + 32
            _, c = chip(x, y, it)
            body += c
            x += cw + 8
        if ci:
            body += f'<rect x="{x0 - 22}" y="44" width="1" height="{h - 88}" fill="{BORDER}"/>'
    save("toolkit.svg", w, h, body, "toolkit")


# ---------- link pills ----------
def pill(name, label, h=36, fs=13, dot=WARM, color=SOFT):
    r = h / 2
    w = int(r + 12 + tw(label, fs, 0.6) + 30)
    body = (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="{BG}" stroke="{BORDER}"/>'
            f'<circle cx="{r}" cy="{r}" r="{h / 12:.1f}" fill="{dot}"/>'
            f'<text x="{r + 12}" y="{r + fs * 0.36:.1f}" font-family="{SANS}" font-size="{fs}" fill="{color}">{escape(label)}</text>'
            f'<text x="{w - 14}" y="{r + fs * 0.36:.1f}" font-family="{SANS}" font-size="{fs - 1}" fill="{MUTED}" text-anchor="end">↗</text>')
    save(name, w, h, body, label)


MORE = [("runefetch", "RuneFetch"), ("nightreign", "Nightreign launcher"), ("vitapapers", "vitapapers"),
        ("discord-css", "discord-css"), ("yt", "yt_downloader")]


def pills():
    for f in os.listdir(ROOT):
        if f.startswith("link-") or f.startswith("more-"):
            os.remove(os.path.join(ROOT, f))
    for slug, label in [("site", "purinpage"), ("kofi", "ko-fi"), ("repos", "all repos")]:
        pill(f"link-{slug}.svg", label)
    for slug, label in MORE:
        pill(f"more-{slug}.svg", label, h=28, fs=12, dot=ACCENT, color=MUTED)


# ---------- footer ----------
def footer():
    w, h = 1200, 90
    body = f'''<rect x="300" y="20" width="600" height="1" fill="{BORDER}"/>
  <rect x="300" y="20" width="300" height="1" fill="url(#fadeline)" transform="rotate(180 450 20.5)"/>
  <rect x="600" y="20" width="300" height="1" fill="url(#fadeline)"/>
  <circle cx="600" cy="20.5" r="3" fill="{WARM}"/>
  <text x="600" y="56" font-family="{SANS}" font-size="13" letter-spacing="5" fill="{MUTED}" text-anchor="middle">THANKS FOR STOPPING BY</text>
  <text x="600" y="78" font-family="{MONO}" font-size="11" fill="#4a525e" text-anchor="middle">p0mpurin · made slowly, with care</text>'''
    save("footer.svg", w, h, body, "thanks for stopping by")


if __name__ == "__main__":
    intro()
    section("works", "01", "works", "selected projects")
    section("toolkit", "02", "toolkit", "what i build with")
    section("activity", "03", "activity", "updated daily")
    cards()
    toolkit()
    pills()
    footer()
    print("ok")
