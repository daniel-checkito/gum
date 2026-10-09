#!/usr/bin/env python3
"""Baut die statischen Seiten in website/ aus gemeinsamen Bausteinen.

Aufruf: python3 tools/build_site.py
Danach liegen alle .html-Dateien in website/. Inhalte hier ändern, nicht in den HTML-Dateien.
"""
from pathlib import Path

from tin_art import FLAVORS, front, opened, back

OUT = Path(__file__).resolve().parent.parent / "website"

# ---------- Icons und Figuren (eigene Zeichnungen) ----------
S = 'stroke="#1D1D1B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'


def star(x, y, r):
    return f'<path d="M{x} {y-r}Q{x} {y} {x+r} {y}Q{x} {y} {x} {y+r}Q{x} {y} {x-r} {y}Q{x} {y} {x} {y-r}Z" fill="#1D1D1B"/>'


def heart(x, y, s=1.6):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M5 9C1 6 0 4 0 2.5 0 .5 2-.5 3.5.2 4.3.6 5 1.5 5 1.5S5.7.6 6.5.2C8-.5 10 .5 10 2.5 10 4 9 6 5 9Z" '
            'fill="#FF48B0" stroke="#1D1D1B" stroke-width="1.6" stroke-linejoin="round"/>')


CHEEK = "#FFB3D9"

M_GUM = f'''<svg viewBox="0 0 160 160" aria-hidden="true">{star(26,40,9)}{star(134,36,7)}{star(132,120,8)}
<path d="M36 82q-14-2-18-16M124 82q14-2 18-16M66 112v14h-8M94 112v14h8" fill="none" {S}/>
<rect x="36" y="46" width="88" height="66" rx="30" fill="#fff" {S}/>
<path d="M58 74q7-9 14 0M88 74q7-9 14 0" fill="none" {S}/>
<path d="M66 86q14 16 28 0Z" fill="#1D1D1B" {S}/>
<ellipse cx="53" cy="89" rx="7" ry="4.5" fill="{CHEEK}"/><ellipse cx="107" cy="89" rx="7" ry="4.5" fill="{CHEEK}"/>
</svg>'''

M_CUBE = f'''<svg viewBox="0 0 160 160" aria-hidden="true">
<path d="M12 72h18M8 88h22M14 104h14" fill="none" {S}/>
<path d="M60 104l-6 16h-8M98 110l8 14h8" fill="none" {S}/>
<path d="M44 56 80 40 116 56 80 72Z" fill="#fff" {S}/>
<path d="M44 56 80 72v44L44 100Z" fill="#F2F2F2" {S}/>
<path d="M80 72 116 56v44l-36 16Z" fill="#E2E2E2" {S}/>
<circle cx="56" cy="83" r="4.5" fill="#1D1D1B"/><circle cx="70" cy="89" r="4.5" fill="#1D1D1B"/>
<path d="M50 74l9 3M65 80l9 4M53 101q4-4 8 0t8 0" fill="none" stroke="#1D1D1B" stroke-width="3.5" stroke-linecap="round"/>
<path d="M126 32c-4 8-6 12 0 14 6-2 4-6 0-14Z" fill="#7FC4EE" stroke="#1D1D1B" stroke-width="3" stroke-linejoin="round"/>
<rect x="6" y="18" width="70" height="26" rx="13" fill="#fff" {S}/><text x="41" y="36" text-anchor="middle" font-family="Instrument Sans, sans-serif" font-weight="700" font-size="14" fill="#1D1D1B">tschüss!</text>
</svg>'''

M_TIN = f'''<svg viewBox="0 0 160 160" aria-hidden="true">{star(28,42,8)}{star(136,54,9)}{star(128,132,6)}
<rect x="40" y="38" width="80" height="92" rx="18" fill="#CFE6F5" {S}/>
<path d="M40 60h80" fill="none" {S}/>
<circle cx="66" cy="78" r="4.5" fill="#1D1D1B"/><path d="M87 78q6-6 12 0M70 88q10 9 20 0" fill="none" {S}/>
<ellipse cx="58" cy="90" rx="6" ry="4" fill="{CHEEK}"/><ellipse cx="102" cy="90" rx="6" ry="4" fill="{CHEEK}"/>
<text x="80" y="120" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="18" fill="#1D1D1B">60 MG</text>
</svg>'''

M_LAPTOP = f'''<svg viewBox="0 0 160 160" aria-hidden="true">{heart(20,30)}{heart(122,22,1.9)}{star(140,74,8)}{star(18,86,7)}
<rect x="40" y="40" width="80" height="58" rx="10" fill="#7FC4EE" {S}/>
<path d="M60 58l9 6-9 6M100 58l-9 6 9 6" fill="none" {S}/>
<path d="M68 78q12 13 24 0Z" fill="#1D1D1B" {S}/>
<ellipse cx="56" cy="80" rx="6" ry="4" fill="{CHEEK}"/><ellipse cx="104" cy="80" rx="6" ry="4" fill="{CHEEK}"/>
<path d="M26 104h108l-10 16H36Z" fill="#fff" {S}/>
</svg>'''

L = 'fill="none" stroke="#1D1D1B" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"'
I_TRUCK = f'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M6 18h32v24H6zM38 26h10l8 8v8H38z" {L}/><circle cx="18" cy="46" r="5" fill="#fff" stroke="#1D1D1B" stroke-width="3.5"/><circle cx="46" cy="46" r="5" fill="#fff" stroke="#1D1D1B" stroke-width="3.5"/></svg>'
I_CHAT = f'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M12 12h40a4 4 0 0 1 4 4v24a4 4 0 0 1-4 4H28l-10 8v-8h-6a4 4 0 0 1-4-4V16a4 4 0 0 1 4-4Z" {L}/><path d="M22 28h.1M32 28h.1M42 28h.1" fill="none" stroke="#1D1D1B" stroke-width="5" stroke-linecap="round"/></svg>'
I_CLOCK = f'<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="22" {L}/><path d="M32 18v14l9 6" {L}/></svg>'
I_SHIELD = f'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 6l22 8v16c0 14-10 22-22 28C20 52 10 44 10 30V14Z" {L}/><path d="M22 32l7 7 13-14" {L}/></svg>'
ARROW = '<svg class="arrow" viewBox="0 0 80 40" aria-hidden="true"><path d="M4 30C20 8 46 4 70 14M60 6l10 8-12 4" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def pack(f, view="front", uid=None):
    fn = {"front": front, "open": opened, "back": back}[view]
    return fn(f, uid or f"{f['id']}-{view}")


# ---------- Layout ----------
NAV = [("/produkt", "Produkt"), ("/mission", "Mission"), ("/teams", "Für Teams"), ("/story", "Story"), ("/faq", "FAQ")]

WARNING = ("Kaugummi mit Koffein, mit Süßungsmitteln. Enthält Koffein. Für Kinder und schwangere Frauen nicht empfohlen. "
           "Nicht mehr als 3 Stück pro Tag. Andere Koffeinquellen beachten. Kann bei übermäßigem Verzehr abführend wirken. "
           "Xylit ist für Hunde giftig.")


def head(title, desc, path):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://gum-prototype.vercel.app/img/og.png">
<meta name="theme-color" content="#F4F0E8">
<link rel="canonical" href="https://gum-prototype.vercel.app{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/anton-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
'''


def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<div class="announce">Erste Charge: jetzt <b>unverbindlich reservieren</b> · Versand aus Berlin</div>
<header class="site-head">
  <div class="wrap nav">
    <a class="logo" href="/" aria-label="GUMMIT Startseite"><span>GUMMIT</span></a>
    <nav class="nav-links" aria-label="Hauptmenü">{links}</nav>
    <a class="btn small" href="/produkt#kaufen">Reservieren</a>
  </div>
</header>
<main id="inhalt">
'''


def footer():
    return f'''</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="logo" href="/"><span>GUMMIT</span></a>
        <p class="foot-claim"><b>Gummit. Push. Repeat.</b><br>Zuckerfreier Koffein-Kaugummi aus Berlin. Für alle, die Dinge bauen.</p>
      </div>
      <div><h4>Shop</h4><ul><li><a href="/produkt">Koffein-Kaugummi</a></li><li><a href="/teams">Team-Box</a></li><li><a href="/teams#host">Host-Box für Events</a></li><li><a href="/teams#coworking">Coworking-Display</a></li></ul></div>
      <div><h4>GUMMIT</h4><ul><li><a href="/mission">Mission</a></li><li><a href="/story">Story</a></li><li><a href="/faq">FAQ</a></li><li><a href="/kontakt">Kontakt</a></li></ul></div>
      <div><h4>Rechtliches</h4><ul><li><a href="/impressum">Impressum</a></li><li><a href="/datenschutz">Datenschutz</a></li><li><a href="/agb">AGB</a></li><li><a href="/widerruf">Widerruf</a></li><li><a href="/versand">Versand &amp; Zahlung</a></li></ul></div>
    </div>
    <p class="legal">{WARNING}</p>
  </div>
</footer>
<div class="sticky-buy" id="sticky-buy" hidden>
  <div><span id="sticky-name">Mint Condition · 1 Dose</span><b id="sticky-price">4,99 €</b></div>
  <a class="btn small" href="#kaufen">Reservieren</a>
</div>
<script src="/config.js"></script>
<script src="/app.js"></script>
</body>
</html>
'''


def section_label(n, text):
    return f'<p class="sec-label"><span>{n}</span>{text}</p>'


def page(path, title, desc, active, body):
    return head(title, desc, path) + header(active) + body + footer()


# ---------- Bausteine ----------
RESERVE_FORM = '''<section class="band blue" id="reservieren">
  <div class="wrap reserve">
    <div>
      <h2>Sichere dir die <em>erste</em> Charge</h2>
      <p class="lead">Unverbindlich und ohne Zahlung. Wir schreiben dir einmal, bevor die erste Charge verschickt wird. Dann entscheidest du, ob du bestellst.</p>
      <ul class="ticks"><li>Kein Kaufvertrag, keine Zahlung</li><li>Eine Mail vor dem Versand, kein Spam</li><li>Abmelden mit einem Klick</li></ul>
    </div>
    <form class="card form" data-lead="reserve" novalidate>
      <p class="picked" data-picked hidden></p>
      <div class="field"><label for="r-email">E-Mail</label><input id="r-email" name="email" type="email" autocomplete="email" placeholder="du@startup.de" required></div>
      <div class="row">
        <div class="field"><label for="r-type">Ich bin</label>
          <select id="r-type" name="type">
            <option value="builder">Builder / Vibe Coder</option>
            <option value="founder">Gründer:in</option>
            <option value="host">Event-Host</option>
            <option value="team">Startup-Team</option>
            <option value="coworking">Coworking</option>
          </select>
        </div>
        <div class="field"><label for="r-where">Wo baust du?</label><input id="r-where" name="where" type="text" placeholder="Factory, Zuhause, U8"></div>
      </div>
      <label class="check"><input type="checkbox" name="ok" required> <span>Ja, ihr dürft mir zu GUMMIT schreiben. Abmelden geht jederzeit. Mehr in der <a href="/datenschutz">Datenschutzerklärung</a>.</span></label>
      <button class="btn" type="submit">Unverbindlich reservieren</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''

MASCOTS = f'''<div class="mascots">
  <div>{M_GUM}<h3>Schmeckt nach Kaugummi</h3><p>Minze, Kirsche oder Beere. Nicht nach Apotheke.</p></div>
  <div>{M_CUBE}<h3>Null Zucker</h3><p>Gesüßt mit Xylit. Der Zucker ist schon weg.</p></div>
  <div>{M_TIN}<h3>Dosis vorne drauf</h3><p>52–60 mg pro Stück, groß gedruckt. Kein Rätselraten.</p></div>
  <div>{M_LAPTOP}<h3>Für Builder gemacht</h3><p>Hackathons, Demo Days, der 47. Tab in Cursor.</p></div>
</div>'''

COMPARE = '''<section class="band" id="vergleich">
  <div class="wrap">
    {label}
    <h2>Koffein pro <em>Euro</em></h2>
    <p class="lead">Was kosten 100 mg Koffein, wenn du sie unterwegs kaufst? GUMMIT liegt unter Coffee to go und Energy Drinks. Nur Kaffee zu Hause ist günstiger, das sagen wir ehrlich.</p>
    <div class="cmp-grid">
      <div class="cmp" id="cmp" role="img" aria-label="Balkendiagramm: Preis pro 100 mg Koffein"></div>
      <div class="calc card">
        <label for="calc-n">Wie oft kaufst du unterwegs Koffein pro Woche?</label>
        <div class="calc-row"><input type="range" id="calc-n" min="1" max="20" value="5"><output id="calc-n-out">5×</output></div>
        <label for="calc-what">Meistens</label>
        <select id="calc-what"></select>
        <p class="calc-big" id="calc-save">–</p>
        <p class="calc-detail" id="calc-detail">–</p>
      </div>
    </div>
    <details class="cmp-table">
      <summary>Zahlen, Annahmen und Quellen</summary>
      <div class="table-scroll"><table class="table">
        <thead><tr><th>Produkt</th><th>Preis</th><th>Koffein</th><th>Zucker</th><th>pro 100 mg</th></tr></thead>
        <tbody id="cmp-rows"></tbody>
      </table></div>
      <p class="fine">Stand Oktober 2026, Preise ohne Pfand. Koffein laut BfR (Espresso-Basis 80 mg, Energy Drink 250 ml 80 mg) und Herstellerangaben (Monster 32 mg/100 ml, Club-Mate 20 mg/100 ml). Cappuccino: Durchschnitt deutscher Großstädte laut Coffeefriend-Auswertung. Red Bull: REWE. Monster: EDEKA. Club-Mate und Kaffee zu Hause sind Schätzungen. GUMMIT: Startpreise. Zucker laut Etikett, gerundet. Quellen: <a href="https://www.bfr.bund.de/veroeffentlichung/fragen-und-antworten-zu-koffein-und-koffeinhaltigen-lebensmitteln-einschliesslich-energy-drinks/" rel="noopener">BfR</a>, <a href="https://www.meininger.de/gastronomie/trends/kaffee-index-bremen-ist-spitzenreiter-beim-teuersten-cappuccino" rel="noopener">Meininger</a>, <a href="https://www.supermarktcheck.de/rewe/sortiment/energy-drinks/" rel="noopener">Supermarktcheck</a>, <a href="https://wolt.com/de/deu/berlin/venue/edeka-gerstmann/items/gemusesafte-272" rel="noopener">EDEKA via Wolt</a>, <a href="https://en.wikipedia.org/wiki/Club-Mate" rel="noopener">Club-Mate</a>.</p>
    </details>
  </div>
</section>
'''

REVIEWS_EMPTY = '''<div class="reviews-empty card">
  <p class="stamp">Neu</p>
  <h3>Noch keine Bewertungen</h3>
  <p>GUMMIT startet gerade. Wir zeigen hier nur echte Stimmen von Leuten, die ihn probiert haben. Sei unter den Ersten und sag uns ehrlich, wie er schmeckt.</p>
  <a class="btn ghost small" href="/kontakt">Feedback schicken</a>
</div>'''

PHOTOS = '''<div class="gallery-ph">
  <div class="ph-tile tape"><span>Foto folgt</span><b>Hackathon</b></div>
  <div class="ph-tile tape"><span>Foto folgt</span><b>Demo Day</b></div>
  <div class="ph-tile tape"><span>Foto folgt</span><b>Coworking</b></div>
  <div class="ph-tile tape"><span>Foto folgt</span><b>Deine Dose</b></div>
</div>'''

SERVICE = f'''<section class="band service-band">
  <div class="wrap service">
    <div>{I_TRUCK}<h3>Versand aus Berlin</h3><p>Nach Deutschland, Österreich und in die Schweiz.</p></div>
    <div>{I_CHAT}<h3>Echte Menschen</h3><p>Fragen landen direkt bei Daniel.</p></div>
    <div>{I_CLOCK}<h3>Erst reservieren</h3><p>Keine Zahlung, bis die erste Charge rausgeht.</p></div>
    <div>{I_SHIELD}<h3>Ehrliche Dosis</h3><p>mg vorne, höchstens 3 am Tag.</p></div>
  </div>
</section>
'''

FLAVOR_CARDS = "".join(
    f'<a class="flavor card" href="/produkt?sorte={f["id"]}"><div class="flavor-pack">{pack(f, "front", "card-" + f["id"])}</div>'
    f'<h3>{f["name"]}</h3><p>{f["taste"]} · {f["mg"]} mg pro Stück. {f["line"]}</p><span class="more">Ansehen →</span></a>'
    for f in FLAVORS)

PDP_VIEWS = "".join(
    f'<div class="pack-view" data-f="{f["id"]}" data-v="{v}"{"" if (f["id"], v) == ("minze", "front") else " hidden"}>{pack(f, v, "pdp-" + f["id"] + "-" + v)}</div>'
    for f in FLAVORS for v in ("front", "open", "back"))

MISSION_BAND = '''<section class="mission-band" id="mission">
  <div class="wrap">
    <p class="sec-label light"><span>05</span>Mission</p>
    <h2>Projekt <em>Erster Commit</em></h2>
    <p class="lead">Mit jeder Dose bringst du GUMMIT zu Berliner Builder:innen, die gerade erst anfangen. Gratis auf Uni-Hackathons, Einsteiger-Meetups und Community-Events ohne Budget.</p>
    <div class="hero-cta"><a class="btn ghost" href="/mission">Mehr erfahren</a><a class="btn white-ghost" href="/teams#anfrage">Event vorschlagen</a></div>
    <p class="mission-stamp" aria-hidden="true">chew good,<br>ship good.</p>
  </div>
</section>
'''

FAQ = {
    "Produkt": [
        ("Was genau ist GUMMIT?", "Zuckerfreier Kaugummi mit Koffein. Jedes Stück hat je nach Sorte 52 bis 60 mg Koffein. 8 Stück stecken in einer Metall-Klappdose."),
        ("Wie schmeckt es?", "Mint Condition nach Minze, Cherry Pick nach Kirsche, Berry Important nach Beere. Koffein schmeckt leicht bitter. Minze überdeckt das am besten, deshalb ist Mint Condition unser Startpunkt."),
        ("Was ist drin?", "Kaugummi, Koffein und Xylit als Süße, dazu Aromen. Die vollständige Zutatenliste und die Nährwerte stehen auf der Produktseite, sobald der Hersteller sie final bestätigt hat, und immer auf der Dose."),
        ("Ist die Dose nachfüllbar?", "Ja, die Metall-Klappdose kannst du behalten und wiederverwenden. Ein Nachfüllpack ist geplant."),
    ],
    "Koffein und Sicherheit": [
        ("Wie viel Koffein ist in einem Stück?", "Mint Condition 60 mg, Cherry Pick und Berry Important je 52 mg. Zum Vergleich: Ein Espresso hat laut BfR etwa 80 mg."),
        ("Wie viele Stück pro Tag?", "Höchstens 3 Stück am Tag. Kaffee, Mate und Energy Drinks mitzählen. Das BfR nennt für gesunde Erwachsene bis zu 400 mg Koffein über den Tag verteilt als unbedenklich."),
        ("Wer sollte GUMMIT nicht kauen?", "Kinder und schwangere Frauen. Wenn du empfindlich auf Koffein reagierst, frag lieber vorher deine Ärztin oder deinen Arzt."),
        ("Worauf muss ich noch achten?", "Xylit kann bei übermäßigem Verzehr abführend wirken und ist für Hunde giftig. Dose also nicht in Reichweite vom Bürohund lassen."),
        ("Macht mich das 10x produktiver?", "Nein. Es ist Kaugummi mit Koffein. Die Zahl vorne drauf ist der ganze Pitch."),
    ],
    "Reservieren, Versand, Zahlung": [
        ("Wie funktioniert das Reservieren?", "Sorte und Menge wählen, Mail-Adresse eintragen. Das ist unverbindlich und kein Kaufvertrag. Wir schreiben dir einmal, bevor die erste Charge verschickt wird. Bestellen und zahlen kannst du dann separat."),
        ("Wohin liefert ihr?", "Aus Berlin nach Deutschland, Österreich und in die Schweiz. Kosten und Laufzeiten stehen unter Versand & Zahlung."),
        ("Welche Zahlungsarten gibt es?", "Sobald der Shop live ist: Karte, Apple Pay, Google Pay und weitere über Stripe. Aktuell zahlst du nichts."),
        ("Kann ich zurückgeben?", "Ja, bei Bestellungen gilt das gesetzliche Widerrufsrecht. Details stehen unter Widerruf."),
    ],
    "Teams und Events": [
        ("Gibt es GUMMIT für Firmen?", "Ja. Team-Boxen mit Rechnung, auf Wunsch mit eurem Logo, und ein Display für Coworkings. Mehr unter Für Teams."),
        ("Bringt ihr GUMMIT zu unserem Event?", "Für ausgewählte Hackathons und Meetups in Berlin gibt es Host-Boxen. Schreib uns über die Teams-Seite."),
        ("Was ist Projekt Erster Commit?", "Wir bringen GUMMIT gratis zu Berliner Events für Leute, die gerade anfangen zu bauen: Uni-Hackathons, Einsteiger-Meetups, Community-Events ohne Budget. Nur Events ab 18. Jedes unterstützte Event listen wir auf der Mission-Seite."),
    ],
}


def faq_html(groups=None, limit=None):
    out = []
    for g, items in FAQ.items():
        if groups and g not in groups:
            continue
        rows = items[:limit] if limit else items
        out.append(f'<div class="faq-group"><h3>{g}</h3>' + "".join(
            f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in rows) + "</div>")
    return '<div class="faq">' + "".join(out) + "</div>"


# ---------- Seiten ----------
def home():
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="sticker">Neu aus Berlin</span>
      <h1 class="riso">Gummit.<br>Push.<br>Repeat.</h1>
      <p class="lede">Zuckerfreier Kaugummi mit <b>52–60 mg Koffein</b> pro Stück. In der Metalldose, für <em>lange Build-Tage</em>, Hackathons und Demo Days.</p>
      <div class="hero-cta">
        <a class="btn" href="/produkt">Zum Produkt · ab <span data-from-price>3,99 €</span></a>
        <a class="btn ghost" href="/teams">Für Teams &amp; Events</a>
      </div>
      <ul class="hero-facts"><li><b>0 g</b> Zucker</li><li><b>8</b> Stück pro Dose</li><li><b>3</b> Sorten</li></ul>
    </div>
    <div class="hero-media">
      <div class="tin-fan">
        <a class="fan-l" href="/produkt?sorte=kirsche" aria-label="Cherry Pick ansehen">{pack(FLAVORS[1], "front", "hero-k")}</a>
        <a class="fan-r" href="/produkt?sorte=beere" aria-label="Berry Important ansehen">{pack(FLAVORS[2], "front", "hero-b")}</a>
        <a class="fan-c" href="/produkt?sorte=minze" aria-label="Mint Condition ansehen">{pack(FLAVORS[0], "front", "hero-m")}</a>
      </div>
      <p class="note">{ARROW}<span>die Zahl steht vorne drauf</span></p>
      <p class="render-note">Entwurf der Dose. Die echte Verpackung kann leicht abweichen.</p>
    </div>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">
  <span>0 g Zucker</span><span>52–60 mg Koffein pro Stück</span><span>Metall-Klappdose</span><span>Versand aus Berlin</span><span>Keine Wirkversprechen. Nur Kaugummi.</span>
  <span>0 g Zucker</span><span>52–60 mg Koffein pro Stück</span><span>Metall-Klappdose</span><span>Versand aus Berlin</span><span>Keine Wirkversprechen. Nur Kaugummi.</span>
</div></div>

<section class="band" id="fuer-wen">
  <div class="wrap">
    {section_label("01", "Für wen")}
    <h2>Gemacht für Berlins <em>Builder</em></h2>
    <p class="lead">Nicht für alle. Für Leute, die abends noch einen Prototyp fertig machen, am Wochenende auf Hackathons sitzen und Montag pitchen.</p>
    <div class="personas">
      <article class="card persona"><span class="num">A</span><h3>Vibe Coder</h3><p>Du baust mit Cursor, Claude und Kaffee. Der Kaffee ist kalt, der Build läuft noch. Die Dose liegt neben dem Ladekabel.</p></article>
      <article class="card persona"><span class="num">B</span><h3>Gründer:innen</h3><p>Pitch-Deck Version 14, Probelauf um 23 Uhr. Kein Zucker vor dem Auftritt, keine Dose Energy auf dem Tisch.</p></article>
      <article class="card persona"><span class="num">C</span><h3>Hackathon-Teams</h3><p>48 Stunden, ein Tisch, zu viel Pizza. Eine Dose in die Mitte, alle sehen, wie viel drin ist.</p></article>
    </div>
  </div>
</section>

<section class="band paper-2" id="warum">
  <div class="wrap">
    {section_label("02", "Warum GUMMIT")}
    <h2>Koffein ohne <em>Theater</em></h2>
    <p class="lead">Kein Zucker, kein Becher, kein Anstehen. Klein genug für die Hosentasche, ehrlich genug, um die Dosis groß aufs Etikett zu drucken.</p>
    {MASCOTS}
  </div>
</section>

<section class="band" id="sorten">
  <div class="wrap">
    {section_label("03", "Sorten")}
    <h2>Drei Sorten, <em>eine</em> Dose</h2>
    <div class="flavors">
      {FLAVOR_CARDS}
    </div>
  </div>
</section>

{COMPARE.format(label=section_label("04", "Rechnen wir mal"))}

{MISSION_BAND}

<section class="band paper-2" id="so-gehts">
  <div class="wrap split2">
    <div>
      {section_label("06", "So geht's")}
      <h2>Pop. Kau. <em>Ship.</em></h2>
      <ol class="steps">
        <li><b>Ein Stück nehmen,</b> wenn der nächste Arbeitsblock startet.</li>
        <li><b>Kauen</b> wie normalen Kaugummi. Der Geschmack hält.</li>
        <li><b>Mitzählen.</b> Höchstens 3 Stück am Tag, Kaffee mitgerechnet.</li>
      </ol>
    </div>
    <div>
      {section_label("07", "Community")}
      <h2>Bald hier: <em>ihr</em></h2>
      <p class="lead">Die erste Charge geht auf Berliner Events. Danach kommen hier eure Fotos hin.</p>
      {PHOTOS}
    </div>
  </div>
</section>

<section class="band" id="story-teaser">
  <div class="wrap teaser">
    <div class="teaser-photo ph-tile tape"><span>Foto folgt</span><b>Daniel</b></div>
    <div>
      {section_label("08", "Story")}
      <h2>Gebaut von einem, der <em>auch</em> nachts baut</h2>
      <p class="lead">Tagsüber Tech-Job, abends Side Projects und 3D-Drucker. Der Kaffee war kalt, der Automat hatte nur Zucker. Also hat Daniel GUMMIT gestartet.</p>
      <a class="btn ghost" href="/story">Ganze Story lesen</a>
    </div>
  </div>
</section>

<section class="band blue-soft" id="teams-teaser">
  <div class="wrap teams-teaser">
    <div>
      {section_label("09", "Für Teams")}
      <h2>Für Teams, Hosts <em>&amp;</em> Coworkings</h2>
      <p class="lead">Team-Boxen mit Rechnung, Host-Boxen für Hackathons und ein Display für eure Theke.</p>
    </div>
    <a class="btn" href="/teams">Angebote ansehen</a>
  </div>
</section>

<section class="band" id="faq-teaser">
  <div class="wrap">
    {section_label("10", "FAQ")}
    <h2>Kurz gefragt</h2>
    {faq_html(["Produkt", "Koffein und Sicherheit"], limit=2)}
    <p class="more-link"><a href="/faq">Alle Fragen ansehen →</a></p>
  </div>
</section>

{RESERVE_FORM}
{SERVICE}
'''
    return page("/", "GUMMIT – Koffein-Kaugummi für Berliner Builder",
                "Zuckerfreier Kaugummi mit 52 bis 60 mg Koffein pro Stück. Für alle, die in Berlin Dinge bauen: Hackathons, Demo Days, lange Abende im Coworking.",
                "/", body)


def product():
    body = f'''
<div class="wrap crumbs"><a href="/">Start</a> / <span>Koffein-Kaugummi</span></div>
<section class="pdp wrap" id="kaufen">
  <div class="pdp-media">
    <div class="pdp-main card" id="pdp-main">
      {PDP_VIEWS}
      <div class="pdp-ph ph-tile" id="shop-ph" hidden><span>Foto folgt</span><b>In der Hand</b></div>
      <span class="stack-badge" id="shop-stack" hidden>×1</span>
    </div>
    <div class="thumbs" id="thumbs" role="group" aria-label="Ansichten">
      <button type="button" data-view="front" aria-pressed="true">Vorderseite</button>
      <button type="button" data-view="open" aria-pressed="false">Offen</button>
      <button type="button" data-view="back" aria-pressed="false">Rückseite</button>
      <button type="button" data-view="ph" aria-pressed="false">Größe</button>
    </div>
    <p class="render-note">Entwurf der Dose. Die echte Verpackung kann leicht abweichen.</p>
  </div>

  <div class="pdp-info">
    <p class="kicker">Kaugummi mit Koffein, mit Süßungsmitteln</p>
    <h1>GUMMIT <span id="pdp-flavor">Mint Condition</span></h1>
    <p class="lede">Zuckerfreier Kaugummi mit <b><span id="lede-mg">60</span> mg Koffein</b> pro Stück. 8 Stück in der Metall-Klappdose.</p>
    <div class="price-row"><span class="price" id="shop-price">4,99 €</span><span class="save" id="shop-save" hidden></span></div>
    <p class="price-meta"><span id="shop-per">4,99 € / Dose</span> · inkl. MwSt., zzgl. <a href="/versand">Versand</a> · <span id="shop-unit">Grundpreis folgt</span></p>

    <fieldset class="opt"><legend>Sorte</legend><div class="chips" id="shop-flavors" role="radiogroup"></div></fieldset>
    <fieldset class="opt"><legend>Menge</legend><div class="packs" id="shop-packs" role="radiogroup"></div></fieldset>

    <button class="btn buy" type="button" id="shop-buy">Unverbindlich reservieren</button>
    <p class="buy-note" id="shop-note">Unverbindlich, kein Kaufvertrag. Zahlung erst nach separater Bestellung.</p>
    <ul class="assure"><li>Erste Charge: <span data-launch>Termin folgt</span></li><li>Versand aus Berlin</li><li>14 Tage Widerruf bei Bestellung</li></ul>

    <p class="warn">Enthält Koffein (<span id="shop-mg100">–</span> mg/100 g). Für Kinder und schwangere Frauen nicht empfohlen.</p>

    <div class="acc">
      <details open><summary>Beschreibung</summary><p>GUMMIT ist Kaugummi mit Koffein und ohne Zucker, gesüßt mit Xylit. Jedes Stück hat eine feste Menge Koffein, die groß vorne auf der Dose steht. Gemacht für lange Build-Tage, Hackathons und Demo Days. Kein Wirkversprechen, nur Kaugummi mit einer ehrlichen Zahl.</p></details>
      <details><summary>Zutaten und Allergene</summary><p><span class="ph">Vollständige Zutatenliste folgt vom Hersteller.</span> Bekannt: Süßungsmittel Xylit, Kaumasse, Koffein, Aromen. Allergene werden hier hervorgehoben, sobald die Spezifikation vorliegt.</p></details>
      <details><summary>Nährwerte</summary><div class="table-scroll"><table class="table"><thead><tr><th></th><th>pro 100 g</th><th>pro Stück</th></tr></thead><tbody>
        <tr><td>Energie</td><td class="ph">folgt</td><td class="ph">folgt</td></tr>
        <tr><td>Fett</td><td class="ph">folgt</td><td class="ph">folgt</td></tr>
        <tr><td>Kohlenhydrate</td><td class="ph">folgt</td><td class="ph">folgt</td></tr>
        <tr><td>davon Zucker</td><td>0 g</td><td>0 g</td></tr>
        <tr><td>davon mehrwertige Alkohole</td><td class="ph">folgt</td><td class="ph">folgt</td></tr>
        <tr><td>Eiweiß</td><td class="ph">folgt</td><td class="ph">folgt</td></tr>
        <tr><td>Salz</td><td class="ph">folgt</td><td class="ph">folgt</td></tr>
        <tr><td>Koffein</td><td id="nut-mg100">–</td><td id="nut-mg">60 mg</td></tr>
      </tbody></table></div></details>
      <details><summary>Verzehrempfehlung</summary><p>Ein Stück kauen, wenn der nächste Arbeitsblock startet. Nicht mehr als 3 Stück pro Tag. Andere Koffeinquellen wie Kaffee, Mate oder Energy Drinks mitzählen.</p></details>
      <details><summary>Warnhinweise</summary><p>Enthält Koffein. Für Kinder und schwangere Frauen nicht empfohlen. Kann bei übermäßigem Verzehr abführend wirken. Xylit ist für Hunde giftig.</p></details>
      <details><summary>Füllmenge und Aufbewahrung</summary><p>8 Stück, Füllmenge <span id="net-weight">–</span> g (vorläufig). Trocken und unter 25 °C lagern. Mindesthaltbarkeit und Los stehen auf dem Dosenboden.</p></details>
      <details><summary>Lebensmittelunternehmer</summary><p><span class="ph">[Firmenname GbR, Anschrift, Berlin]</span></p></details>
      <details><summary>Versand und Rückgabe</summary><p>Versand aus Berlin nach Deutschland, Österreich und in die Schweiz. Kosten und Laufzeiten unter <a href="/versand">Versand &amp; Zahlung</a>. Bei Bestellungen gilt das <a href="/widerruf">Widerrufsrecht</a>.</p></details>
    </div>
  </div>
</section>

<section class="band paper-2">
  <div class="wrap">
    <h2>Warum GUMMIT</h2>
    {MASCOTS}
  </div>
</section>

{COMPARE.format(label="")}

<section class="band paper-2" id="bewertungen">
  <div class="wrap split2">
    <div>
      <h2>Bewertungen</h2>
      {REVIEWS_EMPTY}
    </div>
    <div>
      <h2>Für Teams?</h2>
      <div class="card cross">
        <h3>Team-Box</h3>
        <p>Gemischte Box für euer Büro oder Coworking. Mit Rechnung, auf Wunsch mit Logo.</p>
        <a class="btn ghost small" href="/teams">Team-Box ansehen</a>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Fragen zum Produkt</h2>
    {faq_html(["Koffein und Sicherheit", "Reservieren, Versand, Zahlung"])}
  </div>
</section>

{RESERVE_FORM}
'''
    return page("/produkt", "GUMMIT Koffein-Kaugummi – Mint Condition, Cherry Pick, Berry Important",
                "Zuckerfreier Kaugummi mit 52 bis 60 mg Koffein pro Stück, 8 Stück in der Metalldose. Drei Sorten, ab 3,99 € pro Dose. Jetzt unverbindlich reservieren.",
                "/produkt", body)


def teams():
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <span class="sticker">Für Teams</span>
    <h1 class="riso">Koffein für <br>euer Team.</h1>
    <p class="lede">Für Startups, Agenturen, Coworkings und alle, die Events für Builder machen. Mit Rechnung, ohne Zucker.</p>
  </div>
</section>

<section class="band">
  <div class="wrap offers">
    <article class="card offer" id="team"><span class="num">1</span><h3>Team-Box</h3><p>Gemischte Box mit allen drei Sorten für Büro, Meetingraum oder Offsite.</p><ul class="ticks"><li>ab 10 Dosen</li><li>Rechnung und Staffelpreise</li><li>Logo-Option auf Anfrage</li><li>Als Onboarding-Geschenk</li></ul><a class="btn small" href="#anfrage" data-type="team">Team-Box anfragen</a></article>
    <article class="card offer" id="host"><span class="num">2</span><h3>Host-Box</h3><p>Für Hackathons, Meetups und Demo Days in Berlin. Ihr organisiert, wir bringen die Dosen.</p><ul class="ticks"><li>Dosen für eure Gäste</li><li>Display für den Check-in</li><li>Für ausgewählte Events kostenlos in der Beta</li><li>Wir wollen nur ein Foto und eine Erwähnung</li></ul><a class="btn small" href="#anfrage" data-type="host">Host-Box anfragen</a></article>
    <article class="card offer" id="coworking"><span class="num">3</span><h3>Coworking-Display</h3><p>Ein kleines Display für eure Theke. Kein Automat, kein Vertrag.</p><ul class="ticks"><li>Wir füllen nach</li><li>Provision pro Dose, keine Miete</li><li>Jederzeit beendbar</li><li>Probier-Nachmittag um 14 Uhr</li></ul><a class="btn small" href="#anfrage" data-type="coworking">Display anfragen</a></article>
  </div>
</section>

<section class="band paper-2">
  <div class="wrap split2">
    <div>
      <h2>So läuft's</h2>
      <ol class="steps">
        <li><b>Anfrage schicken</b> mit Menge und Termin.</li>
        <li><b>Angebot bekommen</b> innerhalb von zwei Werktagen, netto mit Staffelpreisen.</li>
        <li><b>Lieferung</b> aus Berlin oder persönlich zum Event.</li>
      </ol>
    </div>
    <div>
      <h2>Fragen</h2>
      {faq_html(["Teams und Events"])}
    </div>
  </div>
</section>

<section class="band blue" id="anfrage">
  <div class="wrap reserve">
    <div>
      <h2>Anfrage <em>schicken</em></h2>
      <p class="lead">Sag uns kurz, was ihr braucht. Wir melden uns mit einem Angebot.</p>
    </div>
    <form class="card form" data-lead="b2b" novalidate>
      <div class="row">
        <div class="field"><label for="b-company">Firma oder Event</label><input id="b-company" name="company" type="text" required></div>
        <div class="field"><label for="b-name">Name</label><input id="b-name" name="name" type="text" autocomplete="name"></div>
      </div>
      <div class="field"><label for="b-email">E-Mail</label><input id="b-email" name="email" type="email" autocomplete="email" required></div>
      <div class="row">
        <div class="field"><label for="b-type">Was braucht ihr?</label>
          <select id="b-type" name="type"><option value="team">Team-Box</option><option value="host">Host-Box</option><option value="coworking">Coworking-Display</option><option value="other">Etwas anderes</option></select>
        </div>
        <div class="field"><label for="b-qty">Menge oder Gäste</label><input id="b-qty" name="qty" type="text" placeholder="z. B. 20 Dosen, 80 Gäste"></div>
      </div>
      <div class="field"><label for="b-date">Termin (optional)</label><input id="b-date" name="date" type="text" placeholder="z. B. Hackathon am 14.11."></div>
      <div class="field"><label for="b-msg">Nachricht</label><textarea id="b-msg" name="message" rows="3"></textarea></div>
      <label class="check"><input type="checkbox" name="ok" required> <span>Ihr dürft mich zu dieser Anfrage kontaktieren. Mehr in der <a href="/datenschutz">Datenschutzerklärung</a>.</span></label>
      <button class="btn" type="submit">Anfrage senden</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''
    return page("/teams", "GUMMIT für Teams, Events und Coworkings",
                "Team-Boxen mit Rechnung, Host-Boxen für Hackathons und Meetups, Displays für Coworkings. Zuckerfreier Koffein-Kaugummi aus Berlin.",
                "/teams", body)


def story():
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <span class="sticker">Story</span>
    <h1 class="riso">Warum es <br>GUMMIT gibt.</h1>
  </div>
</section>
<section class="band">
  <div class="wrap founder">
    <div class="founder-photo ph-tile tape"><span>Foto folgt</span><b>Daniel</b></div>
    <div class="prose">
      <p>Ich bin Daniel. Tagsüber habe ich einen Job in der Tech-Branche, abends baue ich Side Projects und drucke Dinge mit meinem 3D-Drucker. Die meisten guten Ideen kommen bei mir nach 21 Uhr.</p>
      <p>Und genau da war das Problem: Der Kaffee in der Küche ist kalt, der Automat im Coworking hat nur Zuckerdosen, und Energy Drinks fühlen sich nach Abiparty an. Ich wollte etwas Kleines, das in die Laptoptasche passt, keinen Zucker hat und ehrlich sagt, wie viel Koffein drin ist.</p>
      <p>Also habe ich angefangen, Koffein-Kaugummis zu testen. Die meisten schmecken nach Apotheke oder verstecken die Dosis im Kleingedruckten. Daraus wurde GUMMIT: Kaugummi mit Koffein, null Zucker, die Zahl groß vorne drauf.</p>
      <p>Die erste Charge bringe ich selbst zu den Events, auf denen ich eh bin: Hackathons, Luma-Meetups, Demo Days. Wenn du mich dort siehst, sag Hallo.</p>
      <p class="sig">– Daniel</p>
    </div>
  </div>
</section>
<section class="band paper-2">
  <div class="wrap">
    <h2>Woran wir <em>glauben</em></h2>
    <div class="values">
      <div class="card"><h3>Die Zahl zuerst</h3><p>Koffein in mg steht vorne auf der Dose. Nicht im Kleingedruckten.</p></div>
      <div class="card"><h3>Kein Zucker, kein Theater</h3><p>Keine Wundersätze, keine Hustle-Sprüche. Lange Tage sind lang, das reicht.</p></div>
      <div class="card"><h3>Aus der Szene</h3><p>Wir wachsen auf den Events, auf denen wir selbst sind. Nicht über Werbung.</p></div>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap split2">
    <div>
      <h2>Changelog</h2>
      <pre class="log"><b>$</b> git log --oneline
a1c3f02 erste Charge shippen
9e7b210 Sorte Kirsche hinzugefügt
4d2a8c1 Zucker entfernt
0b5e9f3 initial commit: Kaugummi</pre>
    </div>
    <div>
      <h2>Was als <em>Nächstes</em> kommt</h2>
      <ol class="steps">
        <li><b>Erste Charge</b> auf Berliner Hackathons und Meetups.</li>
        <li><b>Coworkings</b> mit Display an der Theke.</li>
        <li><b>Eigene Rezeptur,</b> wenn genug Leute mitmachen.</li>
      </ol>
    </div>
  </div>
</section>
'''
    return page("/story", "Story – GUMMIT", "Wie GUMMIT entstanden ist: kalter Kaffee, Zucker im Automaten und ein Kaugummi mit der Zahl vorne drauf.", "/story", body)


def mission():
    body = f'''
<section class="page-hero mission-hero">
  <div class="wrap">
    <span class="sticker">Mission</span>
    <h1 class="riso">Projekt <br>Erster Commit.</h1>
    <p class="lede">Jede Dose GUMMIT hilft Berliner Builder:innen, die gerade erst anfangen.</p>
  </div>
</section>
<section class="band">
  <div class="wrap split2">
    <div class="prose">
      <p>Die besten Projekte in Berlin starten selten im Büro. Sie starten auf Uni-Hackathons, in Einsteiger-Meetups und auf Community-Events, die mit null Budget laufen. Dort gibt es Pizza, Mate und Leute, die ihren ersten Prototyp bauen.</p>
      <p>Genau da wollen wir sein. Mit jeder Dose, die du kaufst, finanzierst du Dosen für diese Events. Wir bringen sie gratis vorbei und fragen nur nach einem Foto.</p>
      <p>Wir halten es ehrlich: Jedes Event, das wir unterstützen, steht unten mit Datum und Menge. Keine Prozent-Versprechen, die keiner prüfen kann.</p>
    </div>
    <div class="values one">
      <div class="card"><span class="num">1</span><h3>Gratis für Einsteiger-Events</h3><p>Uni-Hackathons, Coding-Meetups, Community-Events ohne Sponsor.</p></div>
      <div class="card"><span class="num">2</span><h3>Nur ab 18</h3><p>GUMMIT enthält Koffein. Deshalb unterstützen wir nur Events für Erwachsene.</p></div>
      <div class="card"><span class="num">3</span><h3>Offen gezählt</h3><p>Jedes Event steht hier. Du siehst, wohin die Dosen gehen.</p></div>
    </div>
  </div>
</section>
<section class="band paper-2">
  <div class="wrap">
    <h2>Bisher <em>unterstützt</em></h2>
    <div class="table-scroll"><table class="table">
      <thead><tr><th>Datum</th><th>Event</th><th>Dosen</th></tr></thead>
      <tbody><tr><td colspan="3" class="empty">Noch keine Events. Das erste kommt mit der ersten Charge.</td></tr></tbody>
    </table></div>
  </div>
</section>
<section class="mission-band">
  <div class="wrap">
    <h2>Du machst ein Event <em>für Einsteiger?</em></h2>
    <p class="lead">Erzähl uns davon. Wenn es passt, bringen wir GUMMIT vorbei.</p>
    <div class="hero-cta"><a class="btn ghost" href="/teams#anfrage">Event vorschlagen</a></div>
  </div>
</section>
'''
    return page("/mission", "Mission – Projekt Erster Commit – GUMMIT",
                "Mit jeder Dose GUMMIT unterstützt du Berliner Einsteiger-Events: Uni-Hackathons, Coding-Meetups, Community-Events ohne Budget.",
                "/mission", body)


def faq_page():
    body = f'''
<section class="page-hero"><div class="wrap"><span class="sticker">FAQ</span><h1 class="riso">Häufige <br>Fragen.</h1></div></section>
<section class="band"><div class="wrap">{faq_html()}<p class="more-link">Noch was offen? <a href="/kontakt">Schreib uns →</a></p></div></section>
'''
    return page("/faq", "FAQ – GUMMIT", "Antworten zu Koffein, Zutaten, Reservieren, Versand und Teams.", "/faq", body)


def contact():
    body = '''
<section class="page-hero"><div class="wrap"><span class="sticker">Kontakt</span><h1 class="riso">Sag <br>Hallo.</h1><p class="lede">Fragen, Feedback, Events, Presse. Wir antworten in der Regel innerhalb von zwei Werktagen.</p></div></section>
<section class="band">
  <div class="wrap split2">
    <div class="contact-ways">
      <div class="card"><h3>WhatsApp</h3><p>Am schnellsten. Direkt bei Daniel.</p><a class="btn small" href="#" data-chat>Chat starten</a></div>
      <div class="card"><h3>E-Mail</h3><p><a href="#" data-mail><span class="ph">[E-Mail-Adresse]</span></a></p></div>
      <div class="card"><h3>Anschrift</h3><p><span class="ph">[Firmenname GbR, Straße, PLZ Berlin]</span></p></div>
    </div>
    <form class="card form" data-lead="contact" novalidate>
      <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" type="text" autocomplete="name"></div>
      <div class="field"><label for="c-email">E-Mail</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="c-msg">Nachricht</label><textarea id="c-msg" name="message" rows="5" required></textarea></div>
      <label class="check"><input type="checkbox" name="ok" required> <span>Ihr dürft mich zu meiner Nachricht kontaktieren. Mehr in der <a href="/datenschutz">Datenschutzerklärung</a>.</span></label>
      <button class="btn" type="submit">Nachricht senden</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''
    return page("/kontakt", "Kontakt – GUMMIT", "Kontakt zu GUMMIT: WhatsApp, E-Mail und Formular.", "/kontakt", body)


DRAFT = '<p class="draft">Entwurf. Vor dem Verkaufsstart durch geprüfte Rechtstexte ersetzen (z. B. IT-Recht Kanzlei, Händlerbund oder Anwalt).</p>'


def legal(path, title, inner):
    body = f'<div class="page">{inner}</div>'
    return page(path, f"{title} – GUMMIT", f"{title} von GUMMIT.", "", body)


def versand():
    return legal("/versand", "Versand & Zahlung", f'''<h1>Versand &amp; Zahlung</h1>{DRAFT}
<p>Aktuell kannst du GUMMIT nur unverbindlich reservieren. Es fallen keine Kosten an. Sobald der Shop live ist, gelten diese Bedingungen.</p>
<h2>Liefergebiete und Versandkosten</h2>
<div class="table-scroll"><table class="table"><thead><tr><th>Land</th><th>Versandkosten</th><th>Versandkostenfrei ab</th><th>Lieferzeit</th></tr></thead><tbody>
<tr><td>Deutschland</td><td class="ph">[x,xx €]</td><td class="ph">[xx €]</td><td class="ph">[2–4 Werktage]</td></tr>
<tr><td>Österreich</td><td class="ph">[x,xx €]</td><td class="ph">[xx €]</td><td class="ph">[3–6 Werktage]</td></tr>
<tr><td>Schweiz</td><td class="ph">[x,xx CHF]</td><td class="ph">[–]</td><td class="ph">[4–8 Werktage]</td></tr>
</tbody></table></div>
<p>Bei Lieferungen in die Schweiz können Einfuhrumsatzsteuer und Zollgebühren anfallen. <span class="ph">[Wer zahlt sie?]</span></p>
<h2>Zahlungsarten</h2>
<p>Bezahlt wird über Stripe: <span class="ph">[Kreditkarte, Apple Pay, Google Pay, Klarna, SEPA]</span>. Alle Preise inklusive Mehrwertsteuer.</p>
<h2>Versand</h2>
<p>Wir verschicken aus Berlin mit <span class="ph">[Versanddienstleister]</span>. Du bekommst eine Mail mit Sendungsnummer.</p>''')


def widerruf():
    return legal("/widerruf", "Widerruf", f'''<h1>Widerrufsbelehrung</h1>{DRAFT}
<p>Aktuell gibt es nur unverbindliche Reservierungen ohne Kaufvertrag. Ein Widerruf ist dafür nicht nötig. Für spätere Bestellungen gilt:</p>
<h2>Widerrufsrecht</h2>
<p>Du hast das Recht, binnen 14 Tagen ohne Angabe von Gründen deinen Vertrag zu widerrufen. Die Frist beginnt an dem Tag, an dem du oder ein von dir benannter Dritter die Ware in Besitz genommen hast.</p>
<p>Um dein Widerrufsrecht auszuüben, schick uns eine eindeutige Erklärung, zum Beispiel per E-Mail an <span class="ph">[E-Mail]</span> oder per Brief an <span class="ph">[Anschrift]</span>. Die Mitteilung, dass du widerrufst, vor Ablauf der Frist reicht.</p>
<h2>Folgen des Widerrufs</h2>
<p>Wir erstatten alle Zahlungen inklusive der Standard-Lieferkosten spätestens binnen 14 Tagen nach Eingang deines Widerrufs, mit demselben Zahlungsmittel. Wir können die Rückzahlung verweigern, bis die Ware wieder bei uns ist oder du den Rückversand nachgewiesen hast. Die Kosten der Rücksendung trägst <span class="ph">[du / wir]</span>.</p>
<h2>Muster-Widerrufsformular</h2>
<p class="ph">[Muster-Widerrufsformular nach Anlage 2 zu Art. 246a EGBGB einfügen]</p>
<h2>Vertrag widerrufen</h2>
<p>Sobald der Shop live ist, findest du hier den Button „Vertrag widerrufen“.</p>''')


def agb():
    sections = ["Geltungsbereich", "Vertragspartner", "Reservierung und Vertragsschluss", "Preise und Versandkosten", "Lieferung", "Zahlung", "Eigentumsvorbehalt", "Widerrufsrecht", "Gewährleistung", "Streitbeilegung"]
    inner = f'<h1>Allgemeine Geschäftsbedingungen</h1>{DRAFT}'
    inner += '<h2>Reservierung</h2><p>Eine Reservierung auf dieser Website ist unverbindlich. Sie ist kein Angebot zum Abschluss eines Kaufvertrags und verpflichtet weder dich noch uns. Ein Kaufvertrag entsteht erst durch eine separate Bestellung.</p>'
    inner += "".join(f'<h2>{s}</h2><p class="ph">[Text folgt]</p>' for s in sections)
    return legal("/agb", "AGB", inner)


def impressum():
    return legal("/impressum", "Impressum", '''<h1>Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p><span class="ph">[Name der GbR]</span><br><span class="ph">[Straße und Hausnummer]</span><br><span class="ph">[PLZ] Berlin</span></p>
<p>Vertreten durch: <span class="ph">[Namen der Gesellschafter]</span></p>
<h2>Kontakt</h2>
<p>E-Mail: <span class="ph">[E-Mail-Adresse]</span><br>Telefon oder WhatsApp: <span class="ph">[Nummer]</span></p>
<h2>Umsatzsteuer</h2>
<p>Umsatzsteuer-ID gemäß § 27a UStG: <span class="ph">[falls vorhanden, sonst Zeile löschen]</span></p>
<h2>Verantwortlich für den Inhalt</h2>
<p><span class="ph">[Name, Anschrift wie oben]</span></p>
<h2>Verbraucherstreitbeilegung</h2>
<p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>''')


def datenschutz():
    return legal("/datenschutz", "Datenschutz", '''<h1>Datenschutz</h1>
<h2>Wer verantwortlich ist</h2>
<p><span class="ph">[Name der GbR, Anschrift, E-Mail]</span> (siehe <a href="/impressum">Impressum</a>).</p>
<h2>Hosting</h2>
<p>Diese Website wird bei Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA gehostet. Beim Aufruf verarbeitet Vercel technisch nötige Daten wie IP-Adresse, Datum, Uhrzeit und aufgerufene Seite in Server-Logfiles. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (sicherer und stabiler Betrieb). Vercel ist unter dem EU-US Data Privacy Framework zertifiziert, zusätzlich gelten Standardvertragsklauseln.</p>
<h2>Schriften</h2>
<p>Die Schriften liegen auf unserem eigenen Server. Es werden keine Daten an Google oder andere Schriftanbieter übertragen.</p>
<h2>Cookies und Tracking</h2>
<p>Wir setzen keine Cookies und kein Tracking ein. Deine Auswahl im Shop wird nur im Browser verarbeitet.</p>
<h2>Reservierung, Anfragen und Kontakt</h2>
<p>Wenn du reservierst, eine Team-Anfrage schickst oder uns schreibst, verarbeiten wir deine Angaben (z. B. E-Mail, Name, Firma, Nachricht, gewählte Sorte und Menge), um dir zu antworten und dich vor dem Versand der ersten Charge zu informieren. Rechtsgrundlage ist deine Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) bzw. die Anbahnung eines Vertrags (lit. b). Du kannst die Einwilligung jederzeit per Mail widerrufen, dann löschen wir deine Daten. Für die Formulare nutzen wir <span class="ph">[Anbieter, z. B. Formspree Inc., USA]</span>.</p>
<h2>WhatsApp</h2>
<p>Wenn du uns über WhatsApp schreibst, verarbeitet WhatsApp Ireland Ltd. deine Daten nach deren Datenschutzhinweisen. Nutze lieber E-Mail oder das Formular, wenn du das nicht möchtest.</p>
<h2>Bestellung und Zahlung</h2>
<p>Für Bestellungen leiten wir dich zu <span class="ph">[Stripe Payments Europe Ltd., Irland]</span> weiter. Wir erhalten Name, E-Mail, Lieferadresse und Zahlungsstatus, um die Bestellung abzuwickeln (Art. 6 Abs. 1 lit. b DSGVO).</p>
<h2>Deine Rechte</h2>
<p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Außerdem kannst du dich bei einer Datenschutz-Aufsichtsbehörde beschweren, in Berlin bei der Berliner Beauftragten für Datenschutz und Informationsfreiheit.</p>
<p class="fine">Stand: <span class="ph">[Datum]</span></p>''')


def notfound():
    body = '''<section class="page-hero err"><div class="wrap"><span class="sticker">404</span><h1 class="riso">Diese Seite ist <br>im Meeting.</h1><p class="lede">Versuch's später. Oder geh zurück zum Kaugummi.</p><a class="btn" href="/">Zur Startseite</a></div></section>'''
    return page("/404", "404 – GUMMIT", "Seite nicht gefunden.", "", body)


PAGES = {
    "index.html": home, "produkt.html": product, "mission.html": mission, "teams.html": teams, "story.html": story,
    "faq.html": faq_page, "kontakt.html": contact, "versand.html": versand, "widerruf.html": widerruf,
    "agb.html": agb, "impressum.html": impressum, "datenschutz.html": datenschutz, "404.html": notfound,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
        print("wrote", name)
