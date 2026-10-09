"""Gezeichnete GUMMIT-Dose als SVG: Vorderseite, offen, Rückseite.

Entwurf der echten Verpackung (Metall-Klappdose, 8 Stück). Wird von build_site.py importiert.
"""

INK = "#15172B"
PAPER = "#F3EFE6"
BLUE = "#2F3BFF"

FLAVORS = [
    {"id": "minze", "name": "Mint Condition", "taste": "Minze", "mg": 60, "color": "#A8DCC6", "deep": "#6FBF9E",
     "line": "Frisch wie ein leeres Repo."},
    {"id": "kirsche", "name": "Cherry Pick", "taste": "Kirsche", "mg": 52, "color": "#F7A8B8", "deep": "#E77F96",
     "line": "Nimm dir nur die guten Commits."},
    {"id": "beere", "name": "Berry Important", "taste": "Beere", "mg": 52, "color": "#C3B8EE", "deep": "#9A8BDB",
     "line": "Für den Pitch um 9&nbsp;Uhr."},
]
NET_G = 12  # vorläufig, siehe config.js


def mg100(mg):
    return f"{round(mg / (NET_G / 8) * 100):,}".replace(",", ".")


def _defs(u, f):
    return f'''<defs>
<linearGradient id="{u}-metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7F7F5"/><stop offset=".35" stop-color="#C9C9C5"/><stop offset=".6" stop-color="#EDEDEA"/><stop offset="1" stop-color="#9A9A96"/></linearGradient>
<linearGradient id="{u}-metal-h" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A9A9A5"/><stop offset=".25" stop-color="#EFEFEC"/><stop offset=".7" stop-color="#C4C4C0"/><stop offset="1" stop-color="#8E8E8A"/></linearGradient>
<linearGradient id="{u}-gloss" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".38" stop-color="#fff" stop-opacity=".08"/><stop offset=".39" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="{u}-piece" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E4E0D8"/></linearGradient>
<linearGradient id="{u}-side" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{f["deep"]}"/><stop offset="1" stop-color="{f["color"]}"/></linearGradient>
<clipPath id="{u}-face"><rect x="58" y="56" width="284" height="214" rx="22"/></clipPath>
</defs>'''


def _illu(fid, x, y):
    """Kleine Geschmacks-Illustration, Ursprung oben links."""
    s = f'stroke="{INK}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"'
    if fid == "minze":
        return f'''<g transform="translate({x} {y})">
<path d="M8 52C2 30 14 8 40 2c6 24-6 46-32 50Z" fill="#4DB384" {s}/><path d="M10 50C18 36 26 22 38 6" fill="none" {s}/>
<path d="M30 58c10-20 30-30 52-24-6 22-28 32-52 24Z" fill="#7FD0A8" {s}/><path d="M32 57c14-8 28-14 48-22" fill="none" {s}/>
</g>'''
    if fid == "kirsche":
        return f'''<g transform="translate({x} {y})">
<path d="M26 38C30 20 40 8 54 2M58 40C56 24 56 12 54 2" fill="none" {s}/>
<path d="M54 2c10-4 22 0 26 8-10 4-20 2-26-8Z" fill="#4DB384" {s}/>
<circle cx="24" cy="48" r="15" fill="#E8364F" {s}/><circle cx="58" cy="50" r="15" fill="#D42A45" {s}/>
<path d="M18 42a6 6 0 0 1 6-4M52 44a6 6 0 0 1 6-4" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
</g>'''
    return f'''<g transform="translate({x} {y})">
<circle cx="22" cy="42" r="14" fill="#5B4BC4" {s}/><circle cx="50" cy="44" r="14" fill="#7462D8" {s}/><circle cx="36" cy="20" r="14" fill="#4A3CA8" {s}/>
<path d="M30 14l6 4 6-4M16 36l6 4 6-4M44 38l6 4 6-4" fill="none" {s}/>
<path d="M58 8c8-6 18-4 22 2-8 6-16 4-22-2Z" fill="#4DB384" {s}/>
</g>'''


def _logo(x, y, size):
    """GUMMIT in Anton mit Riso-Versatz in Blau."""
    return (f'<text x="{x + 3}" y="{y + 3}" font-family="Anton, Impact, sans-serif" font-size="{size}" fill="{BLUE}" opacity=".9">GUMMIT</text>'
            f'<text x="{x}" y="{y}" font-family="Anton, Impact, sans-serif" font-size="{size}" fill="{INK}">GUMMIT</text>')


def front(f, u):
    """Geschlossene Dose von vorne."""
    T = "font-family=\"Bricolage Grotesque, Arial, sans-serif\""
    return f'''<svg class="pack-svg" viewBox="0 0 400 320" role="img" aria-label="GUMMIT {f["name"]}, {f["taste"]}, {f["mg"]} mg Koffein pro Stück, Vorderseite der Dose">{_defs(u, f)}
<ellipse cx="200" cy="300" rx="158" ry="12" fill="{INK}" opacity=".14"/>
<rect x="48" y="60" width="304" height="230" rx="30" fill="url(#{u}-metal-h)" stroke="{INK}" stroke-width="2.5"/>
<rect x="46" y="44" width="308" height="234" rx="30" fill="url(#{u}-metal)" stroke="{INK}" stroke-width="2.5"/>
<rect x="58" y="56" width="284" height="214" rx="22" fill="{f["color"]}"/>
<g clip-path="url(#{u}-face)">
  <circle cx="320" cy="58" r="70" fill="{f["deep"]}" opacity=".35"/>
  {_logo(76, 124, 60)}
  <text x="78" y="146" {T} font-weight="700" font-size="11" letter-spacing="2.2" fill="{INK}">KAUGUMMI MIT KOFFEIN</text>
  <text x="76" y="226" font-family="Anton, Impact, sans-serif" font-size="78" fill="{INK}">{f["mg"]}</text>
  <text x="{76 + 42 * len(str(f["mg"]))}" y="196" font-family="Anton, Impact, sans-serif" font-size="26" fill="{INK}">MG</text>
  <text x="{76 + 42 * len(str(f["mg"]))}" y="211" {T} font-weight="700" font-size="9.5" fill="{INK}">KOFFEIN</text>
  <text x="{76 + 42 * len(str(f["mg"]))}" y="223" {T} font-weight="700" font-size="9.5" fill="{INK}">PRO STÜCK</text>
  {_illu(f["id"], 238, 150)}
  <g transform="translate(300 96) rotate(12)"><circle r="27" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/><text y="-2" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="17" fill="{INK}">0 G</text><text y="11" text-anchor="middle" {T} font-weight="700" font-size="7.5" letter-spacing="1" fill="{INK}">ZUCKER</text></g>
  <rect x="58" y="236" width="284" height="40" fill="{INK}"/>
  <text x="78" y="262" font-family="Instrument Serif, Georgia, serif" font-style="italic" font-size="22" fill="{PAPER}">{f["name"]}</text>
  <text x="322" y="261" text-anchor="end" {T} font-size="10" fill="{PAPER}">{f["taste"]} · 8 Stück · {NET_G} g ℮</text>
  <rect x="58" y="56" width="284" height="214" fill="url(#{u}-gloss)"/>
</g>
<rect x="58" y="56" width="284" height="214" rx="22" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1.5"/>
</svg>'''


def opened(f, u):
    """Offene Dose von oben mit 8 Stück."""
    pieces = "".join(
        f'<g transform="translate({96 + c * 54} {196 + r * 44})"><rect x="2" y="3" width="46" height="34" rx="12" fill="{INK}" opacity=".12"/>'
        f'<rect width="46" height="34" rx="12" fill="url(#{u}-piece)" stroke="#BDB8AE" stroke-width="1.2"/>'
        f'<path d="M9 9q14-5 28 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></g>'
        for r in range(2) for c in range(4))
    hinge = "".join(f'<rect x="{112 + i * 36}" y="150" width="28" height="12" rx="5" fill="url(#{u}-metal)" stroke="{INK}" stroke-width="1.6"/>' for i in range(5))
    return f'''<svg class="pack-svg" viewBox="0 0 400 340" role="img" aria-label="Offene GUMMIT-Dose {f["name"]} mit 8 Kaugummistücken">{_defs(u, f)}
<ellipse cx="200" cy="322" rx="160" ry="12" fill="{INK}" opacity=".14"/>
<path d="M66 156 82 24q2-14 16-14h204q14 0 16 14l16 132Z" fill="url(#{u}-metal-h)" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M84 148 96 34q1-10 12-10h184q11 0 12 10l12 114Z" fill="#DADAD6" stroke="#A2A29E" stroke-width="1.4"/>
<text x="200" y="98" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="34" fill="#BDBDB8" stroke="#F4F4F2" stroke-width=".8">GUMMIT</text>
<text x="200" y="118" text-anchor="middle" font-family="Bricolage Grotesque, Arial, sans-serif" font-weight="700" font-size="9" letter-spacing="2" fill="#AFAFAA">BERLIN · 8 STÜCK</text>
<rect x="48" y="156" width="304" height="158" rx="28" fill="{f["color"]}" stroke="{INK}" stroke-width="2.5"/>
<rect x="64" y="170" width="272" height="128" rx="18" fill="url(#{u}-metal)" stroke="{INK}" stroke-width="2"/>
<rect x="74" y="180" width="252" height="108" rx="12" fill="#C9C9C4"/>
{pieces}
{hinge}
<rect x="48" y="156" width="304" height="158" rx="28" fill="url(#{u}-gloss)" opacity=".6"/>
</svg>'''


def back(f, u):
    """Rückseite mit Pflichtangaben (Entwurf)."""
    T = 'font-family="Bricolage Grotesque, Arial, sans-serif" fill="#15172B"'
    lines = [
        (10.5, 700, f"GUMMIT {f['name']} · {f['taste']}"),
        (9, 400, "Kaugummi mit Koffein, mit Süßungsmitteln. Zuckerfrei."),
        (9, 400, "Zutaten: Süßungsmittel Xylit, Kaumasse, Koffein, Aroma"),
        (9, 400, "[vollständige Liste folgt vom Hersteller]."),
        (9, 700, f"Enthält Koffein ({mg100(f['mg'])} mg/100 g, {f['mg']} mg pro Stück)."),
        (9, 700, "Für Kinder und schwangere Frauen nicht empfohlen."),
        (9, 400, "Nicht mehr als 3 Stück pro Tag. Kann bei übermäßigem"),
        (9, 400, "Verzehr abführend wirken. Xylit ist giftig für Hunde."),
        (9, 400, "Trocken und unter 25 °C lagern."),
    ]
    y, txt = 92, ""
    for size, w, t in lines:
        txt += f'<text x="80" y="{y}" {T} font-size="{size}" font-weight="{w}">{t}</text>'
        y += 14 if size < 10 else 18
    bars = "".join(f'<rect x="{262 + i * 3.1:.1f}" y="226" width="{1.2 if i % 3 else 2.2}" height="30" fill="{INK}"/>' for i in range(20))
    return f'''<svg class="pack-svg" viewBox="0 0 400 320" role="img" aria-label="Rückseite der GUMMIT-Dose {f["name"]} mit Zutaten und Warnhinweisen (Entwurf)">{_defs(u, f)}
<ellipse cx="200" cy="300" rx="158" ry="12" fill="{INK}" opacity=".14"/>
<rect x="48" y="60" width="304" height="230" rx="30" fill="url(#{u}-metal-h)" stroke="{INK}" stroke-width="2.5"/>
<rect x="46" y="44" width="308" height="234" rx="30" fill="url(#{u}-metal)" stroke="{INK}" stroke-width="2.5"/>
<rect x="58" y="56" width="284" height="214" rx="22" fill="{f["color"]}"/>
<g clip-path="url(#{u}-face)">
  <rect x="68" y="66" width="264" height="194" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>
  {txt}
  <text x="80" y="240" {T} font-size="9" font-weight="700">8 Stück · {NET_G} g ℮</text>
  <text x="80" y="254" {T} font-size="8.5">[Firma GbR, Anschrift] · Berlin</text>
  <text x="80" y="226" {T} font-size="8.5">MHD und Los: siehe Boden</text>
  {bars}
  <rect x="58" y="56" width="284" height="214" fill="url(#{u}-gloss)" opacity=".7"/>
</g>
</svg>'''
