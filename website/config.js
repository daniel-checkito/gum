// Hier trägst du deine Daten ein. Leer lassen = Funktion aus.
window.GUMMIT_CONFIG = {
  // Formular-Endpunkt, der JSON per POST annimmt, z. B. von formspree.io:
  // "https://formspree.io/f/abcdwxyz"
  formEndpoint: "",

  // Fallback, solange kein Endpunkt da ist: Formular öffnet eine Mail an diese Adresse.
  contactEmail: "",

  // Bezahlte Vorbestellung, z. B. ein Stripe Payment Link: "https://buy.stripe.com/..."
  preorderUrl: "",
  preorderLabel: "Pre-order now",
  preorderNote: "Pay now, get the first batch. If it never ships, you get a full refund."
};
