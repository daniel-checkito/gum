// Hier trägst du deine Daten ein. Leer lassen = Funktion aus.
window.GUMMIT_CONFIG = {
  // Formular-Endpunkt, der JSON per POST annimmt, z. B. von formspree.io:
  // "https://formspree.io/f/abcdwxyz"
  formEndpoint: "",

  // Fallback, solange kein Endpunkt da ist: Formular öffnet eine Mail an diese Adresse.
  contactEmail: "",

  // WhatsApp-Nummer für „Fragen? Schreib Daniel“, z. B. "+491701234567"
  whatsapp: "",

  // Shop: Preise pro Paket (Startpreise, anpassen). url = Stripe Payment Link pro Paket.
  // Ohne url reserviert der Button nur (Warteliste, keine Zahlung).
  packs: [
    { tins: 1, price: 4.99, url: "" },
    { tins: 3, price: 13.49, url: "" },
    { tins: 5, price: 21.49, url: "" },
    { tins: 10, price: 39.90, url: "" }
  ],

  // Bezahlte Vorbestellung, z. B. ein Stripe Payment Link: "https://buy.stripe.com/..."
  preorderUrl: "",
  preorderLabel: "Pre-order now",
  preorderNote: "Pay now, get the first batch. If it never ships, you get a full refund."
};
