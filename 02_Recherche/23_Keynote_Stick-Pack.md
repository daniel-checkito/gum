# Richtung "Keynote": Stick-Pack im Five-Stil

Stand Oktober 2026. Wunsch von Daniel: futuristischer, moderner, näher an Five Gum ("Stimulate your senses"), Apple-Keynote, San Francisco, Claude.

## Was wir übernommen haben

**Verpackung wie Five Gum:** schwarzes, flaches Stick-Pack, große Chrom-Zahl vorne und rechts eine Farbgrafik pro Sorte. Bei uns ist die Zahl die mg Koffein.

| Sorte | Name | Farbe | Grafik |
|---|---|---|---|
| Minze | Mint Condition | #19B6E8 | Kreise |
| Kirsche | Cherry Pick | #F0364A | Strahlen |
| Beere | Berry Important | #8B5CFF | Facetten |

Gezeichnet in `tools/pack_art.py`.

**Bühnen mit Linienmuster:** Farbflächen mit konzentrischen Rauten (`website/img/lines.svg`) wie in den Five-Spots. Im Hero wechselt die Farbe mit der gewählten Sorte.

**Website wie eine Keynote:**
- Seite: hell (#F5F5F7), weiße Karten, große fette Headlines in Geist, Verlaufswörter Blau → Violett → Rot
- Bento-Kacheln und Eckdaten-Kacheln, ruhige Schatten
- Anton nur noch fürs Logo
- Dunkel sind nur das Pack und eine Kachel, die Seite selbst bleibt hell

**Biohacking-Ecke ohne Versprechen:** Die Koffein-Timeline zeigt, wie viel Koffein über den Tag im Körper ist. Grundlage ist ein vereinfachtes Modell mit 5 h Halbwertszeit und dem EFSA-Hinweis zu 400 mg pro Tag und 200 mg auf einmal. Die Zielgruppe bekommt damit Daten statt Wirkversprechen.

**KI-Zeitalter, San Francisco:** Kacheln "Du promptest. Claude coded. Du kaust." und "Gebaut in Kreuzberg. Im Tempo der Bay Area."

## Was wir bewusst nicht machen

- **Kein "Fokus", "Konzentration", "wach" oder "Biohacking" als Versprechen.** Unter 75 mg pro Portion ist der zugelassene Wach-Claim nicht drin. Andere Gesundheitsversprechen sind für Koffein nicht zugelassen (HCVO 1924/2006). Cognigum wirbt mit "Fokus". Das ist ein Risiko, das wir nicht kopieren.
- **"Stimulate your senses"** ist der Claim von Five (Wrigley). Wir sagen stattdessen "Drei Sorten. Alle Sinne." und "Präzise dosiert. Voll im Geschmack."
- **Apple- oder Claude-Branding** übernehmen wir nicht. Wir nehmen nur den Stil (hell, klar, groß). Claude wird nur als Werkzeug im Text erwähnt.

## Offen

- **Format beim Hersteller klären.** Stick-Gum statt Dragees in der Dose: Gibt es das mit Koffein, als White Label und mit MOQ ≤ 500? Die bisherigen Anfragen (Delica, siehe 02_Recherche/16) liefen auf Dragees bzw. Dosen.
- **Packgröße festlegen.** Wie viele Sticks pro Pack? Five hat 15. Die Website rechnet mit 8 Sticks und 12 g (`config.js`, `tools/pack_art.py`).
- **Druckvorlage** für das Faltpack von einem Designer anfertigen lassen. Chrom-Effekt geht z. B. mit Metallic-Folie oder Silberdruck.
