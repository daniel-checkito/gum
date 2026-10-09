(function () {
  var cfg = window.BISS_CONFIG || {};

  // Laufband mit Sprüchen
  var sprueche = [
    "Zucker? Hamwa nich.",
    "Kamera aus, Kaugummi rein.",
    "Schmeckt besser als der Kaffee im 4. Stock.",
    "Hier könnte deine Ausrede stehen.",
    "Pfand gibt’s keins. Die Dose behältste.",
    "Ja, wir sind auch müde.",
    "Klein, rund, kein Drama.",
    "Dieses Meeting hätte eine Mail sein können.",
    "Kann man nicht auf Slack posten. Machste trotzdem."
  ];
  var track = document.getElementById("marquee");
  if (track) {
    var html = sprueche.concat(sprueche).map(function (s) { return "<span>" + s + "</span>"; }).join("");
    track.innerHTML = html;
  }

  // Deckel-Generator
  var sorten = [
    { name: "Deadline", bg: "#9FE3C8", fg: "#1F2C7A" },
    { name: "Standup", bg: "#E3A869", fg: "#1F2C7A" },
    { name: "Kundencall", bg: "#F2D23C", fg: "#1F2C7A" },
    { name: "Kobalt", bg: "#1F2C7A", fg: "#EDF1F2" },
    { name: "Signal", bg: "#FF6B1F", fg: "#1F2C7A" },
    { name: "Feierabend", bg: "#F8FAFB", fg: "#1F2C7A" }
  ];
  var current = sorten[0];
  var txt = document.getElementById("gen-text");
  var count = document.getElementById("gen-count");
  var lid = document.getElementById("lid");
  var lidText = document.getElementById("lid-text");
  var lidSorte = document.getElementById("lid-sorte");
  var sw = document.getElementById("swatches");

  function render() {
    var t = txt.value.trim() || "Hier könnte deine Ausrede stehen.";
    lidText.textContent = t;
    count.textContent = txt.value.length;
    lid.style.background = current.bg;
    lid.style.color = current.fg;
    lidSorte.textContent = current.name;
  }

  sorten.forEach(function (s, i) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "swatch";
    b.style.background = s.bg;
    b.setAttribute("aria-label", s.name);
    b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
    b.addEventListener("click", function () {
      current = s;
      sw.querySelectorAll(".swatch").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      render();
    });
    sw.appendChild(b);
  });
  txt.addEventListener("input", render);
  render();

  function wrapLines(ctx, text, maxWidth) {
    var words = text.split(/\s+/), lines = [], line = "";
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = w; }
      else line = test;
    });
    if (line) lines.push(line);
    return lines;
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function drawLid() {
    var W = 1080, H = 1080;
    var c = document.createElement("canvas");
    c.width = W; c.height = H;
    var ctx = c.getContext("2d");
    ctx.fillStyle = "#EDF1F2";
    ctx.fillRect(0, 0, W, H);

    var lw = 900, lh = Math.round(lw * 46 / 59), lx = (W - lw) / 2, ly = (H - lh) / 2 - 20;
    ctx.save();
    ctx.shadowColor = "rgba(31,44,122,.25)"; ctx.shadowBlur = 60; ctx.shadowOffsetY = 24;
    roundRect(ctx, lx, ly, lw, lh, 84);
    ctx.fillStyle = current.bg; ctx.fill();
    ctx.restore();
    ctx.lineWidth = 14; ctx.strokeStyle = "rgba(0,0,0,.08)";
    roundRect(ctx, lx + 7, ly + 7, lw - 14, lh - 14, 78); ctx.stroke();

    var pad = 72, text = lidText.textContent;
    ctx.fillStyle = current.fg;
    ctx.textBaseline = "top";
    var size = 84, lines;
    do {
      ctx.font = "800 " + size + "px 'Bricolage Grotesque', sans-serif";
      lines = wrapLines(ctx, text, lw - pad * 2);
      size -= 4;
    } while (lines.length * size * 1.05 > lh - pad * 2 - 90 && size > 36);
    var lh2 = (size + 4) * 1.04;
    lines.forEach(function (l, i) { ctx.fillText(l, lx + pad, ly + pad + i * lh2); });

    ctx.textBaseline = "alphabetic";
    ctx.font = "800 64px 'Bricolage Grotesque', sans-serif";
    ctx.fillText("BISS", lx + pad, ly + lh - pad + 6);
    ctx.font = "500 30px 'Instrument Sans', sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(current.name, lx + lw - pad, ly + lh - pad);
    ctx.textAlign = "left";

    ctx.fillStyle = "#4a5590";
    ctx.font = "500 28px 'Instrument Sans', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Mach deinen eigenen Deckel", W / 2, H - 56);
    return c;
  }

  document.getElementById("gen-download").addEventListener("click", function () {
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
      var c = drawLid();
      c.toBlob(function (blob) {
        var file = new File([blob], "biss-deckel.png", { type: "image/png" });
        if (navigator.canShare && navigator.canShare({ files: [file] }) && /Mobi|Android/i.test(navigator.userAgent)) {
          navigator.share({ files: [file], title: "Mein BISS-Deckel" }).catch(function () {});
          return;
        }
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "biss-deckel.png";
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
      }, "image/png");
    });
  });

  var fSpruch = document.getElementById("f-spruch");
  var fTyp = document.getElementById("f-typ");
  document.getElementById("gen-submit").addEventListener("click", function () {
    fSpruch.value = txt.value.trim();
    document.getElementById("vorbestellen").scrollIntoView({ behavior: "smooth" });
    setTimeout(function () { document.getElementById("f-email").focus({ preventScroll: true }); }, 600);
  });

  document.querySelectorAll("[data-typ]").forEach(function (a) {
    a.addEventListener("click", function () { fTyp.value = a.getAttribute("data-typ"); });
  });

  // Vorbestellung
  if (cfg.preorderUrl) {
    document.getElementById("preorder").hidden = false;
    var pl = document.getElementById("preorder-link");
    pl.href = cfg.preorderUrl;
    pl.textContent = cfg.preorderLabel || "Jetzt vorbestellen";
    document.getElementById("preorder-note").textContent = cfg.preorderNote || "";
  }

  // Formular
  var form = document.getElementById("lead-form");
  var msg = document.getElementById("form-msg");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = form.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = "Bitte gib eine gültige E-Mail-Adresse ein."; return; }
    if (!document.getElementById("f-ok").checked) { msg.textContent = "Bitte setz noch den Haken."; return; }
    var data = { email: email, typ: fTyp.value, ort: form.ort.value.trim(), spruch: fSpruch.value.trim() };

    if (cfg.formEndpoint) {
      msg.textContent = "Wird gesendet …";
      fetch(cfg.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error();
        form.reset();
        msg.textContent = "Danke, du stehst drauf. Wir melden uns.";
      }).catch(function () {
        msg.textContent = "Hat nicht geklappt. Versuch’s bitte gleich nochmal.";
      });
    } else if (cfg.contactEmail) {
      var body = "E-Mail: " + data.email + "\nIch bin: " + data.typ + "\nOrt: " + data.ort + "\nSpruch: " + data.spruch;
      location.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("BISS Liste") + "&body=" + encodeURIComponent(body);
      msg.textContent = "Dein Mailprogramm öffnet sich. Einfach abschicken.";
    } else {
      msg.textContent = "Die Liste ist noch nicht offen. Schau bald wieder vorbei.";
    }
  });
})();
