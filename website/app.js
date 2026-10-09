(function () {
  var cfg = window.GUMMIT_CONFIG || {};

  // Shop
  var flavors = [
    { name: "Hotfix", taste: "Minze", mg: 60, color: "#A8E6A1", img: "img/tin-hotfix" },
    { name: "Ship It", taste: "Kirsche", mg: 52, color: "#F07A86" },
    { name: "Demo Day", taste: "Beere", mg: 52, color: "#B7A8EA" }
  ];
  var packs = cfg.packs || [{ tins: 1, price: 4.99, url: "" }];
  var sel = { flavor: flavors[0], pack: packs[0] };
  var eur = function (n) { return n.toFixed(2).replace(".", ",") + " €"; };
  var tins = function (n) { return n + (n === 1 ? " Dose" : " Dosen"); };
  var $ = function (id) { return document.getElementById(id); };

  function chip(parent, html, onClick) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.innerHTML = html;
    b.addEventListener("click", onClick);
    parent.appendChild(b);
    return b;
  }

  var fChips = flavors.map(function (f) {
    return chip($("shop-flavors"), "<span><i class=\"dot\" style=\"background:" + f.color + "\"></i>" + f.name + "</span><small>" + f.taste + " · " + f.mg + " mg</small>",
      function () { sel.flavor = f; render(); });
  });
  var pChips = packs.map(function (p) {
    return chip($("shop-packs"), "<span>" + tins(p.tins) + "</span><small>" + eur(p.price) + "</small>",
      function () { sel.pack = p; render(); });
  });

  function render() {
    var f = sel.flavor, p = sel.pack, base = packs[0].price;
    fChips.forEach(function (c, i) { c.setAttribute("aria-pressed", flavors[i] === f ? "true" : "false"); });
    pChips.forEach(function (c, i) { c.setAttribute("aria-pressed", packs[i] === p ? "true" : "false"); });
    $("shop-tin").style.background = f.color;
    var hasPhoto = !!f.img;
    $("shop-photo").hidden = !hasPhoto;
    $("render-note").hidden = !hasPhoto;
    $("shop-tin").hidden = hasPhoto;
    $("shop-sun").hidden = hasPhoto;
    if (hasPhoto) {
      $("shop-photo-webp").srcset = "/" + f.img + ".webp";
      $("shop-photo-img").src = "/" + f.img + ".jpg";
      $("shop-photo-img").alt = "GUMMIT-Dose " + f.name + ", " + f.mg + " mg Koffein pro Stück";
    }
    $("shop-mg").textContent = f.mg + " mg";
    $("shop-tinname").textContent = f.name;
    $("shop-tintaste").textContent = f.taste + " · 8 Stk.";
    $("lede-mg").textContent = f.mg + " mg";
    $("shop-stack").hidden = p.tins === 1;
    $("shop-stack").textContent = "×" + p.tins;
    $("shop-price").textContent = eur(p.price);
    $("shop-per").textContent = eur(p.price / p.tins) + " / Dose";
    var save = Math.round((1 - p.price / (base * p.tins)) * 100);
    $("shop-save").hidden = save <= 0;
    $("shop-save").textContent = save + " % gespart";
    $("shop-buy").textContent = p.url ? "Vorbestellen · " + eur(p.price) : "Dosen reservieren";
    $("shop-note").textContent = p.url ? "Sicher bezahlen" : "Jetzt nichts zahlen";
    $("sticky-name").textContent = f.name + " · " + tins(p.tins);
    $("sticky-price").textContent = eur(p.price);
  }
  render();

  // Sticky buy bar once the buy button is out of view
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      $("sticky-buy").hidden = entries[0].isIntersecting || entries[0].boundingClientRect.top > 0;
    }).observe($("shop-buy"));
  }

  $("shop-buy").addEventListener("click", function () {
    if (sel.pack.url) { location.href = sel.pack.url; return; }
    $("f-picked").hidden = false;
    $("f-picked").textContent = "Du reservierst: " + sel.pack.tins + "× " + sel.flavor.name + " (" + eur(sel.pack.price) + ")";
    $("reservieren").scrollIntoView({ behavior: "smooth" });
    setTimeout(function () { $("f-email").focus({ preventScroll: true }); }, 600);
  });

  var fType = $("f-type");
  document.querySelectorAll("[data-type]").forEach(function (a) {
    a.addEventListener("click", function () { fType.value = a.getAttribute("data-type"); });
  });

  // Chat link: WhatsApp, else email, else FAQ
  var chat = $("chat-link");
  if (chat) {
    if (cfg.whatsapp) chat.href = "https://wa.me/" + cfg.whatsapp.replace(/\D/g, "");
    else if (cfg.contactEmail) chat.href = "mailto:" + cfg.contactEmail;
  }

  // Koffein pro Euro
  var drinks = [
    { name: "Cappuccino im Café", price: 3.30, mg: 80, sugar: "0 g zugesetzt" },
    { name: "Red Bull 250 ml", price: 1.89, mg: 80, sugar: "ca. 27 g" },
    { name: "Monster 500 ml", price: 2.48, mg: 160, sugar: "ca. 55 g" },
    { name: "Club-Mate 0,5 l", price: 1.20, mg: 100, sugar: "ca. 25 g", est: true },
    { name: "Kaffee zu Hause", price: 0.15, mg: 90, sugar: "0 g", est: true }
  ];
  if ($("cmp")) {
    var best = packs.reduce(function (a, b) { return a.price / a.tins < b.price / b.tins ? a : b; });
    var perPiece = best.price / best.tins / 8;
    var single = packs[0].price / 8;
    var rows = drinks.map(function (d) { return { name: d.name, label: eur(d.price), mg: d.mg, sugar: d.sugar, est: d.est, per100: d.price / d.mg * 100 }; });
    rows.push({ name: "GUMMIT Hotfix, 1 Dose", label: eur(single) + " / Stück", mg: 60, sugar: "0 g", per100: single / 60 * 100, own: true });
    rows.push({ name: "GUMMIT Hotfix, " + tins(best.tins), label: eur(perPiece) + " / Stück", mg: 60, sugar: "0 g", per100: perPiece / 60 * 100, own: true });
    rows.sort(function (a, b) { return b.per100 - a.per100; });
    var max = rows[0].per100;
    $("cmp").innerHTML = rows.map(function (r) {
      return "<div class=\"cmp-row" + (r.own ? " own" : "") + "\" title=\"" + r.name + ": " + eur(r.per100) + " pro 100 mg\">" +
        "<span class=\"cmp-name\">" + r.name + (r.est ? " *" : "") + "</span>" +
        "<span class=\"cmp-track\"><i style=\"width:" + Math.max(3, r.per100 / max * 100).toFixed(1) + "%\"></i></span>" +
        "<span class=\"cmp-val\">" + eur(r.per100) + "</span></div>";
    }).join("") + "<p class=\"fine\">Preis pro 100 mg Koffein. * Schätzung.</p>";
    $("cmp-rows").innerHTML = rows.map(function (r) {
      return "<tr><td>" + r.name + (r.est ? " *" : "") + "</td><td>" + r.label + "</td><td>" + r.mg + " mg</td><td>" + r.sugar + "</td><td>" + eur(r.per100) + "</td></tr>";
    }).join("");

    var sel2 = $("calc-what");
    drinks.slice(0, 4).forEach(function (d, i) {
      var o = document.createElement("option"); o.value = i; o.textContent = d.name; sel2.appendChild(o);
    });
    var calc = function () {
      var n = +$("calc-n").value, d = drinks[+sel2.value];
      $("calc-n-out").textContent = n + "×";
      var perMonth = n * 52 / 12;
      var costDrink = perMonth * d.price;
      var costGum = perMonth * (d.mg / 60) * perPiece;
      var diff = costDrink - costGum;
      $("calc-save").textContent = diff > 0 ? "ca. " + eur(diff) + " gespart" : "kein Preisvorteil";
      $("calc-detail").textContent = "Pro Monat " + eur(costDrink) + " für " + d.name + " statt " + eur(costGum) + " mit GUMMIT (" + tins(best.tins) + "-Paket) bei gleicher Koffeinmenge.";
    };
    $("calc-n").addEventListener("input", calc);
    sel2.addEventListener("change", calc);
    calc();
  }

  // Pre-order
  if (cfg.preorderUrl) {
    document.getElementById("preorder").hidden = false;
    var pl = document.getElementById("preorder-link");
    pl.href = cfg.preorderUrl;
    pl.textContent = cfg.preorderLabel || "Jetzt vorbestellen";
    document.getElementById("preorder-note").textContent = cfg.preorderNote || "";
  }

  // Waitlist form
  var form = document.getElementById("lead-form");
  var msg = document.getElementById("form-msg");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = form.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = "Die Mail-Adresse sieht komisch aus. Nochmal?"; return; }
    if (!document.getElementById("f-ok").checked) { msg.textContent = "Setz noch den Haken, dann bist du dabei."; return; }
    var picked = document.getElementById("f-picked");
    var data = { email: email, type: fType.value, where: form.where.value.trim(), reserve: picked.hidden ? "" : sel.pack.tins + "x " + sel.flavor.name };

    if (cfg.formEndpoint) {
      msg.textContent = "Wird gesendet …";
      fetch(cfg.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error();
        form.reset();
        msg.textContent = "Merged. Du stehst auf der Liste.";
      }).catch(function () {
        msg.textContent = "Build failed. Versuch es gleich nochmal.";
      });
    } else if (cfg.contactEmail) {
      var body = "E-Mail: " + data.email + "\nIch bin: " + data.type + "\nWo: " + data.where + "\nReservierung: " + data.reserve;
      location.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("GUMMIT Reservierung") + "&body=" + encodeURIComponent(body);
      msg.textContent = "Dein Mailprogramm öffnet sich. Einfach abschicken.";
    } else {
      msg.textContent = "Die Reservierung startet gleich. Schau bald wieder vorbei.";
    }
  });
})();
