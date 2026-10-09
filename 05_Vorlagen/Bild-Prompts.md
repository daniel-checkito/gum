# Bild-Prompts für die Website

Stil: **Keynote**. Hellgrau #F5F5F7, Weiß, Text #1D1D1F. Farbe kommt von den Sorten: Minze #19B6E8, Kirsche #F0364A, Beere #8B5CFF. Das Produkt ist ein schwarzes, flaches Stick-Pack mit großer Chrom-Zahl (wie Five Gum), 8 Sticks.

## So gehst du vor

1. **Stil-Block** unten vor jeden Prompt setzen.
2. **Pack:** KI kann Text auf Verpackungen schlecht. Lade eine Referenz aus `05_Vorlagen/Bild-Referenz/` als Bildvorlage hoch (z. B. `pack-minze-front.png`). Oder lass das Pack klein bzw. unscharf und ohne lesbaren Text.
3. **Speichern** als `website/img/slots/<Datei>.jpg` (oder .webp). Breite mindestens 1600 px. Danach `python3 tools/build_site.py` laufen lassen oder mir die Bilder schicken. Der Platzhalter wird automatisch ersetzt.
4. **Echte Menschen** (Daniel, Team) bitte echt fotografieren. Keine KI-Gesichter für Team oder Bewertungen. Für Szenen mit Leuten nur Menschen ohne erkennbare Gesichter oder von hinten, damit niemand glaubt, das seien echte Kunden.

## Stil-Block (immer davor)

```
Premium tech product photography in the style of an Apple keynote, clean and minimal, soft studio light with one crisp highlight, light gray (#F5F5F7) or white surfaces, glossy black slim gum stick pack with a large chrome number on the front, accent colors electric cyan (#19B6E8), cherry red (#F0364A) and violet (#8B5CFF), futuristic but warm, shallow depth of field, no readable text, no logos
```

Negativ (falls das Tool es kann): `text, letters, watermark, logo, brand names, faces looking into camera, stock photo smile, cyberpunk neon, dark moody, orange tones, round tin`

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
Over-the-shoulder shot of a young developer at a wooden desk at night, laptop screen glowing with blurred code editor, mechanical keyboard, a slim black gum stick pack with cyan graphic next to the keyboard, two silver-wrapped gum sticks beside it, cold coffee mug, charging cable, sticker-covered laptop lid edge, person seen from behind, Berlin altbau window in the background
```

### persona-gruender (4:3)
```
Young founder rehearsing a pitch in an empty Berlin coworking event space, seen from the side and slightly blurred, holding a clicker, slide deck projected softly on a white wall without readable text, a slim black gum stick pack with red graphic on a high table in the foreground in sharp focus, folding chairs, late evening
```

### persona-hackathon (4:3)
```
Top-down flatlay of a crowded hackathon table: three laptops, pizza box, post-its, tangled cables, lanyard badges without text, unlabeled glass bottles, in the center an open slim black gum stick pack with violet graphic, silver-wrapped sticks sliding out, hands reaching in from the edges, no faces
```

### mission-event (4:5)
```
Students at a beginner hackathon in a Berlin university room, seen from behind and the side, laptops, whiteboard with abstract doodles, one person holding up a slim black gum stick pack like a trophy, joyful candid moment, lime green paper cups, cobalt blue hoodie, no readable text
```

### community-hackathon (4:3)
```
Wide shot of a busy hackathon at night in a Berlin warehouse loft, long tables, warm string lights, people from behind working on laptops, a few slim black gum stick packs with cyan, red and violet graphics on the tables, energetic but tidy
```

### community-demoday (4:3)
```
Demo day stage in a Berlin startup venue, speaker silhouette on a small stage, audience heads from behind, big screen with an abstract cobalt blue slide without text, a slim black gum stick pack on the edge of the stage in the foreground
```

### community-coworking (4:3)
```
Coworking counter in Berlin with a small white display holding slim black gum stick packs with cyan, red and violet graphics, coffee machine in the background, plants, someone grabbing a pack, hand only, soft daylight
```

### community-tasche (4:3)
```
Close-up of an open laptop sleeve or backpack front pocket, a slim black gum stick pack with cyan graphic peeking out next to an earbuds case, USB-C cable and a Luma-style event badge without text, on a light gray background
```

### produkt-hand (1:1)
```
Close-up of a hand holding an open slim black gum stick pack with silver-wrapped sticks sliding out, pack slightly smaller than a phone, background electric cyan (#19B6E8) with thin concentric diamond line pattern, soft studio light, product clearly visible
```
Tipp: hier unbedingt `pack-minze-open.png` als Referenz hochladen.

### Extra: Sorten-Shots (optional, 4:5)
Für spätere Produktfotos, je eine Sorte auf ihrer Farbe:
```
Studio product photo of a glossy black slim gum stick pack floating slightly tilted, large chrome number on the front, colored graphic on the right side, background in [#19B6E8 | #F0364A | #8B5CFF] with thin concentric diamond line pattern, soft reflections, premium, like a Five gum ad
```
Referenz: `pack-<sorte>-front.png`.

## Echte Fotos (kein KI)

- **daniel / team-daniel:** Hochformat 4:5. Vor einer Wand in Hellgrau oder einer Sortenfarbe. Weiches Studiolicht. Pack in der Hand, ehrliches Grinsen.
- **team-2, team-3:** Gleicher Hintergrund und gleiches Licht wie bei Daniel, damit das Karussell einheitlich aussieht (wie "The Chew Crew" bei Forest Gum).
- **Namen und Rollen** in `tools/build_site.py` unter `CREW` eintragen.
