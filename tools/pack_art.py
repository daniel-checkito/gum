"""Gezeichnetes GUMMIT-Stick-Pack als SVG: Vorderseite, offen, Rückseite.

Schwarzes Faltpack mit 8 Sticks, große Chrom-Zahl (mg Koffein), Farbgrafik pro Sorte.
Wird von build_site.py importiert. Entwurf, keine Druckvorlage.
"""
import math

FLAVORS = [
    {"id": "minze", "name": "Mint Condition", "taste": "Minze", "mg": 60,
     "color": "#19B6E8", "deep": "#0A5CFF", "light": "#9EE7FF", "art": "arcs",
     "line": "Eiskalt. Klar. Wie ein frisches Terminal."},
    {"id": "kirsche", "name": "Cherry Pick", "taste": "Kirsche", "mg": 52,
     "color": "#F0364A", "deep": "#9E0F2B", "light": "#FFB1BA", "art": "rays",
     "line": "Dunkel, saftig, ein bisschen frech."},
    {"id": "beere", "name": "Berry Important", "taste": "Beere", "mg": 52,
     "color": "#8B5CFF", "deep": "#4B1FCC", "light": "#D8C8FF", "art": "facets",
     "line": "Tief, süß und lila. Ohne Zucker."},
]
PIECES = 8
NET_G = 12  # vorläufig, siehe config.js
SANS = 'font-family="Geist, Helvetica, Arial, sans-serif"'


def mg100(mg):
    return f"{round(mg / (NET_G / PIECES) * 100):,}".replace(",", ".")


def _defs(u, f):
    return f'''<defs>
<linearGradient id="{u}-chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".28" stop-color="#B9BEC6"/><stop offset=".45" stop-color="#F7F8FA"/><stop offset=".62" stop-color="#6E747D"/><stop offset=".8" stop-color="#E4E7EB"/><stop offset="1" stop-color="#8A9099"/></linearGradient>
<linearGradient id="{u}-black" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2B2D31"/><stop offset=".55" stop-color="#121316"/><stop offset="1" stop-color="#050506"/></linearGradient>
<linearGradient id="{u}-gloss" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".35" stop-color="#fff" stop-opacity=".04"/><stop offset=".36" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="{u}-art" cx=".85" cy=".5" r=".75"><stop offset="0" stop-color="{f["light"]}"/><stop offset=".35" stop-color="{f["color"]}"/><stop offset="1" stop-color="{f["deep"]}"/></radialGradient>
<linearGradient id="{u}-foil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#D9DDE2"/><stop offset=".5" stop-color="#FFFFFF"/><stop offset="1" stop-color="#AEB4BC"/></linearGradient>
<clipPath id="{u}-clip"><rect x="40" y="50" width="320" height="200" rx="10"/></clipPath>
</defs>'''


def _art(f, u):
    """Farbgrafik rechts auf dem Pack, je Sorte ein anderes Motiv."""
    base = f'<path d="M232 50h128v200H196Z" fill="url(#{u}-art)"/>'
    if f["art"] == "arcs":
        lines = "".join(f'<circle cx="372" cy="150" r="{r}" fill="none" stroke="#fff" stroke-opacity="{.12 + (i % 3) * .1:.2f}" stroke-width="{2 if i % 2 else 5}"/>' for i, r in enumerate(range(30, 200, 16)))
        return base + f'<g clip-path="url(#{u}-artclip)">{lines}</g>'
    if f["art"] == "rays":
        rays = "".join(f'<path d="M372 150L{372 - 260 * math.cos(a / 10):.0f} {150 - 260 * math.sin(a / 10):.0f}" stroke="#fff" stroke-opacity="{.1 + (a % 3) * .1:.2f}" stroke-width="{3 if a % 2 else 8}"/>' for a in range(-14, 15, 2))
        seeds = "".join(f'<ellipse cx="{300 + (i * 23) % 56}" cy="{80 + (i * 37) % 150}" rx="2.5" ry="5" fill="#1A0006" opacity=".55"/>' for i in range(9))
        return base + f'<g clip-path="url(#{u}-artclip)">{rays}{seeds}</g>'
    pts = [(250, 60), (330, 90), (300, 160), (360, 210), (260, 240), (220, 170), (290, 110)]
    facets = "".join(f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}L372 150Z" fill="#fff" fill-opacity="{.05 + (i % 4) * .07:.2f}"/>' for i, (a, b) in enumerate(zip(pts, pts[1:] + pts[:1])))
    edges = "".join(f'<path d="M{x} {y}L372 150" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>' for x, y in pts)
    return base + f'<g clip-path="url(#{u}-artclip)">{facets}{edges}</g>'


def _numeral(f, u, x=274, y=218, size=128):
    """Große Chrom-Zahl, schräg gestellt."""
    t = str(f["mg"])
    return (f'<g transform="translate({x} {y}) skewX(-14)">'
            f'<text x="6" y="6" text-anchor="middle" {SANS} font-weight="800" font-size="{size}" letter-spacing="-7" fill="#000" opacity=".55">{t}</text>'
            f'<text text-anchor="middle" {SANS} font-weight="800" font-size="{size}" letter-spacing="-7" fill="url(#{u}-chrome)" stroke="#3A3F46" stroke-width="1.5">{t}</text>'
            f'</g>')


def _body(u):
    return (f'<rect x="40" y="50" width="320" height="200" rx="10" fill="url(#{u}-black)"/>'
            f'<clipPath id="{u}-artclip"><path d="M232 50h128v200H196Z"/></clipPath>')


def front(f, u):
    return f'''<svg class="pack-svg" viewBox="0 0 400 300" role="img" aria-label="GUMMIT {f["name"]}, {f["taste"]}, {f["mg"]} mg Koffein pro Stick, Vorderseite">{_defs(u, f)}
<ellipse cx="200" cy="268" rx="170" ry="10" fill="#000" opacity=".22"/>
{_body(u)}
<g clip-path="url(#{u}-clip)">
  {_art(f, u)}
  <path d="M40 250 196 50h6L46 250Z" fill="#fff" opacity=".05"/>
  {_numeral(f, u)}
  <text x="62" y="84" font-family="Anton, Impact, sans-serif" font-size="22" letter-spacing="1" fill="#fff">GUMMIT</text>
  <text x="62" y="146" {SANS} font-weight="600" font-size="15" letter-spacing="3" fill="#fff">{f["taste"].upper()}</text>
  <text x="62" y="166" {SANS} font-weight="500" font-size="11" letter-spacing="1.8" fill="{f["color"]}">{f["name"].upper()}</text>
  <path d="M62 206h150" stroke="#fff" stroke-opacity=".25"/>
  <text x="62" y="226" {SANS} font-weight="600" font-size="12" letter-spacing="1.6" fill="#fff">{PIECES} STICKS</text>
  <text x="138" y="221" {SANS} font-size="7" letter-spacing=".8" fill="#fff" fill-opacity=".75">{f["mg"]} MG KOFFEIN</text>
  <text x="138" y="231" {SANS} font-size="7" letter-spacing=".8" fill="#fff" fill-opacity=".75">PRO STICK · ZUCKERFREI</text>
  <rect x="40" y="50" width="320" height="200" fill="url(#{u}-gloss)"/>
</g>
<rect x="40.5" y="50.5" width="319" height="199" rx="9.5" fill="none" stroke="#fff" stroke-opacity=".14"/>
</svg>'''


def opened(f, u):
    """Offenes Pack, Sticks schauen oben raus."""
    sticks = ""
    for i in range(PIECES):
        x = 62 + i * 36
        h = 70 + (i * 29) % 46
        sticks += (f'<g><rect x="{x}" y="{120 - h}" width="30" height="{h + 30}" rx="3" fill="url(#{u}-foil)" stroke="#9AA0A8" stroke-width=".8"/>'
                   f'<rect x="{x}" y="{132 - h}" width="30" height="9" fill="{f["color"]}"/>'
                   f'<text x="{x + 15}" y="{150 - h + 20}" text-anchor="middle" {SANS} font-weight="800" font-size="11" fill="#2B2D31" transform="rotate(-90 {x + 15} {150 - h + 20})">GUMMIT</text></g>')
    return f'''<svg class="pack-svg" viewBox="0 0 400 300" role="img" aria-label="Offenes GUMMIT-Pack {f["name"]} mit {PIECES} Sticks">{_defs(u, f)}
<ellipse cx="200" cy="268" rx="170" ry="10" fill="#000" opacity=".22"/>
<path d="M44 120 70 92h260l26 28Z" fill="#26282C"/>
{sticks}
<rect x="40" y="120" width="320" height="130" rx="8" fill="url(#{u}-black)"/>
<clipPath id="{u}-lowclip"><rect x="40" y="120" width="320" height="130" rx="8"/></clipPath>
<g clip-path="url(#{u}-lowclip)">
  <path d="M250 120h110v130H210Z" fill="url(#{u}-art)"/>
  {_numeral(f, u, 296, 236, 92)}
  <text x="62" y="160" {SANS} font-weight="600" font-size="13" letter-spacing="3" fill="#fff">{f["taste"].upper()}</text>
  <text x="62" y="178" {SANS} font-weight="500" font-size="11" letter-spacing="2" fill="{f["color"]}">{f["name"].upper()}</text>
  <text x="62" y="228" {SANS} font-weight="600" font-size="11" letter-spacing="1.6" fill="#fff">{PIECES} STICKS</text>
  <rect x="40" y="120" width="320" height="130" fill="url(#{u}-gloss)"/>
</g>
</svg>'''


def back(f, u):
    """Rückseite mit Pflichtangaben (Entwurf)."""
    T = f'{SANS} fill="#fff"'
    lines = [
        (10, 700, f"GUMMIT {f['name']} · {f['taste']}"),
        (8.5, 400, "Kaugummi mit Koffein, mit Süßungsmitteln. Zuckerfrei."),
        (8.5, 400, "Zutaten: Süßungsmittel Xylit, Kaumasse, Koffein, Aroma"),
        (8.5, 400, "[vollständige Liste folgt vom Hersteller]."),
        (8.5, 700, f"Enthält Koffein ({mg100(f['mg'])} mg/100 g, {f['mg']} mg pro Stick)."),
        (8.5, 700, "Für Kinder und schwangere Frauen nicht empfohlen."),
        (8.5, 400, "Nicht mehr als 3 Sticks pro Tag. Kann bei übermäßigem"),
        (8.5, 400, "Verzehr abführend wirken. Xylit ist giftig für Hunde."),
        (8.5, 400, "Trocken und unter 25 °C lagern."),
    ]
    y, txt = 82, ""
    for size, w, t in lines:
        txt += f'<text x="62" y="{y}" {T} font-size="{size}" font-weight="{w}" fill-opacity="{1 if w == 700 else .82}">{t}</text>'
        y += 13 if size < 10 else 17
    bars = "".join(f'<rect x="{278 + i * 3:.1f}" y="200" width="{1.1 if i % 3 else 2}" height="26" fill="#111"/>' for i, _ in enumerate(range(20)))
    return f'''<svg class="pack-svg" viewBox="0 0 400 300" role="img" aria-label="Rückseite des GUMMIT-Packs {f["name"]} mit Zutaten und Warnhinweisen (Entwurf)">{_defs(u, f)}
<ellipse cx="200" cy="268" rx="170" ry="10" fill="#000" opacity=".22"/>
{_body(u)}
<g clip-path="url(#{u}-clip)">
  <rect x="40" y="50" width="8" height="200" fill="{f["color"]}"/>
  {txt}
  <text x="62" y="210" {T} font-size="8.5" fill-opacity=".82">MHD und Los: siehe Lasche</text>
  <text x="62" y="223" {T} font-size="8.5" font-weight="700">{PIECES} Sticks · {NET_G} g ℮</text>
  <text x="62" y="236" {T} font-size="8" fill-opacity=".7">[Firma GbR, Anschrift] · Berlin</text>
  <rect x="270" y="192" width="74" height="44" rx="3" fill="#fff"/>
  {bars}
  <rect x="40" y="50" width="320" height="200" fill="url(#{u}-gloss)"/>
</g>
</svg>'''
