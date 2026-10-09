# Bild-Prompts für die Website

Stil: **Cobalt Rush**. Cremepapier #F3EFE6, Kobalt #2F3BFF, Lime #D7F94A, Blau-Schwarz #15172B, Sortenfarben Mint #A8DCC6, Kirsche #F7A8B8, Beere #C9C2F5.

## So gehst du vor

1. **Stil-Block** unten vor jeden Prompt setzen.
2. **Dose:** KI kann Text auf Dosen schlecht. Lade eine Referenz aus `05_Vorlagen/Bild-Referenz/` als Bildvorlage hoch (z. B. `dose-minze-front.png`). Oder lass die Dose klein bzw. unscharf und ohne lesbaren Text.
3. **Speichern** als `website/img/slots/<Datei>.jpg` (oder .webp). Breite mindestens 1600 px. Danach `python3 tools/build_site.py` laufen lassen oder mir die Bilder schicken. Der Platzhalter wird automatisch ersetzt.
4. **Echte Menschen** (Daniel, Team) bitte echt fotografieren. Keine KI-Gesichter für Team oder Bewertungen. Für Szenen mit Leuten nur Menschen ohne erkennbare Gesichter oder von hinten, damit niemand glaubt, das seien echte Kunden.

## Stil-Block (immer davor)

```
Editorial lifestyle photo, Berlin tech scene, hard direct on-camera flash, crisp short shadows, slightly desaturated colors with warm midtones, 35mm, candid, clean composition, cream paper background tones (#F3EFE6), small accents in electric cobalt blue (#2F3BFF) and signal lime (#D7F94A), no text, no logos, no brand names
```

Negativ (falls das Tool es kann): `text, letters, watermark, logo, brand names, faces looking into camera, stock photo smile, neon cyberpunk, dark moody, orange tones`

## Slots

| Datei | Format | Wo |
|---|---|---|
| persona-vibecoder | 4:3 | Startseite, Für wen A |
| persona-gruender | 4:3 | Startseite, Für wen B |
| persona-hackathon | 4:3 | Startseite, Für wen C |
| mission-event | 4:5 | Mission-Band |
| community-hackathon | 4:3 | Community-Galerie |
| community-demoday | 4:3 | Community-Galerie |
| community-coworking | 4:3 | Community-Galerie |
| community-tasche | 4:3 | Community-Galerie |
| produkt-hand | 1:1 | Produktseite, Ansicht "Größe" |
| daniel | 4:5 | Story, Startseite (echtes Foto) |
| team-daniel, team-2, team-3 | 4:5 | Contributors (echte Fotos) |

### persona-vibecoder (4:3)
```
Over-the-shoulder shot of a young developer at a wooden desk at night, laptop screen glowing with blurred code editor, mechanical keyboard, a small metal flip-top gum tin in mint green open next to the keyboard with two white gum pieces, cold coffee mug, charging cable, sticker-covered laptop lid edge, person seen from behind, Berlin altbau window in the background
```

### persona-gruender (4:3)
```
Young founder rehearsing a pitch in an empty Berlin coworking event space, seen from the side and slightly blurred, holding a clicker, slide deck projected softly on a white wall without readable text, a small pink metal gum tin on a high table in the foreground in sharp focus, folding chairs, late evening
```

### persona-hackathon (4:3)
```
Top-down flatlay of a crowded hackathon table: three laptops, pizza box, post-its, tangled cables, lanyard badges without text, unlabeled glass bottles, in the center an open small metal flip-top gum tin in lilac with white gum pieces, hands reaching in from the edges, no faces
```

### mission-event (4:5)
```
Students at a beginner hackathon in a Berlin university room, seen from behind and the side, laptops, whiteboard with abstract doodles, one person holding up a small metal gum tin like a trophy, joyful candid moment, lime green paper cups, cobalt blue hoodie, no readable text
```

### community-hackathon (4:3)
```
Wide shot of a busy hackathon at night in a Berlin warehouse loft, long tables, warm string lights, people from behind working on laptops, a few small colorful metal gum tins scattered on the tables, energetic but tidy
```

### community-demoday (4:3)
```
Demo day stage in a Berlin startup venue, speaker silhouette on a small stage, audience heads from behind, big screen with an abstract cobalt blue slide without text, a small metal gum tin on the edge of the stage in the foreground
```

### community-coworking (4:3)
```
Coworking counter in Berlin with a small cardboard display holding colorful metal gum tins in mint, pink and lilac, coffee machine in the background, plants, someone grabbing a tin, hand only, daylight with flash fill
```

### community-tasche (4:3)
```
Close-up of an open laptop sleeve or backpack front pocket, a small mint green metal gum tin peeking out next to earbuds case, USB-C cable and a Luma-style event badge without text, on a cream paper background, playful
```

### produkt-hand (1:1)
```
Close-up of a hand holding a small open metal flip-top gum tin with 8 white rectangular gum pieces inside, tin about the size of a palm, seamless mint green (#A8DCC6) paper background, hard flash, crisp shadow, product clearly visible
```
Tipp: hier unbedingt `dose-minze-open.png` als Referenz hochladen.

### Extra: Sorten-Shots (optional, 4:5)
Für spätere Produktfotos, je eine Sorte auf ihrer Farbe:
```
Studio product photo of a small rectangular metal flip-top tin standing slightly tilted, lid closed, two white gum pieces in front, seamless [#A8DCC6 | #F7A8B8 | #C9C2F5] paper backdrop, hard direct flash, crisp short shadow, clean, playful
```
Referenz: `dose-<sorte>-front.png`.

## Echte Fotos (kein KI)

- **daniel / team-daniel:** Hochformat 4:5. Vor einer Wand in Kobalt, Lime oder Creme. Direkter Blitz, leicht von unten. Dose in der Hand, ehrliches Grinsen.
- **team-2, team-3:** Gleicher Hintergrund und gleiches Licht wie bei Daniel, damit das Karussell einheitlich aussieht (wie "The Chew Crew" bei Forest Gum).
- **Namen und Rollen** in `tools/build_site.py` unter `CREW` eintragen.
