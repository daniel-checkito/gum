(function () {
  var cfg = window.GUMMIT_CONFIG || {};
  var $ = function (id) { return document.getElementById(id); };
  var $$ = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };
  var eur = function (n) { return n.toFixed(2).replace(".", ",") + " €"; };
  var tins = function (n) { return n + (n === 1 ? " Dose" : " Dosen"); };

  var flavors = [
    { id: "minze", name: "Mint Condition", taste: "Minze", mg: 60, color: "#A8DCC6" },
    { id: "kirsche", name: "Cherry Pick", taste: "Kirsche", mg: 52, color: "#F7A8B8" },
    { id: "beere", name: "Berry Important", taste: "Beere", mg: 52, color: "#C3B8EE" }
  ];
  var packs = cfg.packs || [{ tins: 1, price: 4.99, url: "" }];
  var netG = cfg.netWeightGrams || 12;
  var best = packs.reduce(function (a, b) { return a.price / a.tins < b.price / b.tins ? a : b; });

  $$("[data-from-price]").forEach(function (el) { el.textContent = eur(best.price / best.tins); });
  $$("[data-launch]").forEach(function (el) { if (cfg.launch) el.textContent = cfg.launch; });

  // Kontaktwege
  $$("[data-chat]").forEach(function (a) {
    if (cfg.whatsapp) { a.href = "https://wa.me/" + cfg.whatsapp.replace(/\D/g, ""); a.target = "_blank"; a.rel = "noopener"; }
    else if (cfg.contactEmail) a.href = "mailto:" + cfg.contactEmail;
    else a.href = "/kontakt";
  });
  $$("[data-mail]").forEach(function (a) {
    if (cfg.contactEmail) { a.href = "mailto:" + cfg.contactEmail; a.textContent = cfg.contactEmail; }
  });

  // ---------- Produktseite ----------
  var sel = { flavor: flavors[0], pack: packs[0], view: "front" };
  if ($("shop-flavors")) {
    var q = new URLSearchParams(location.search).get("sorte");
    q = { hotfix: "minze", shipit: "kirsche", demoday: "beere" }[q] || q;
    flavors.forEach(function (f) { if (f.id === q) sel.flavor = f; });

    var radio = function (parent, html, onPick) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "chip"; b.setAttribute("role", "radio"); b.innerHTML = html;
      b.addEventListener("click", onPick);
      parent.appendChild(b);
      return b;
    };
    var fChips = flavors.map(function (f) {
      return radio($("shop-flavors"), "<span><i class=\"dot\" style=\"background:" + f.color + "\"></i>" + f.name + "</span><small>" + f.taste + " · " + f.mg + " mg</small>",
        function () { sel.flavor = f; if (sel.view === "ph") sel.view = "front"; render(); });
    });
    var base = packs[0].price;
    var pChips = packs.map(function (p) {
      var save = Math.round((1 - p.price / (base * p.tins)) * 100);
      return radio($("shop-packs"), "<span>" + tins(p.tins) + "</span><small>" + eur(p.price) + "</small><small>" + eur(p.price / p.tins) + " pro Dose</small>" + (save > 0 ? "<span class=\"tag\">−" + save + " %</span>" : ""),
        function () { sel.pack = p; render(); });
    });
    var thumbs = $$("#thumbs button");
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () { sel.view = t.dataset.view; render(); });
    });

    var render = function () {
      var f = sel.flavor, p = sel.pack;
      fChips.forEach(function (c, i) { c.setAttribute("aria-checked", flavors[i] === f ? "true" : "false"); });
      pChips.forEach(function (c, i) { c.setAttribute("aria-checked", packs[i] === p ? "true" : "false"); });
      thumbs.forEach(function (t) { t.setAttribute("aria-pressed", t.dataset.view === sel.view ? "true" : "false"); });
      $$(".pack-view").forEach(function (v) { v.hidden = !(v.dataset.f === f.id && v.dataset.v === sel.view); });
      $("shop-ph").hidden = sel.view !== "ph";
      $("pdp-flavor").textContent = f.name;
      $("lede-mg").textContent = f.mg;
      $("shop-stack").hidden = p.tins === 1;
      $("shop-stack").textContent = "×" + p.tins;

      var mg100 = Math.round(f.mg / (netG / 8) * 100);
      $("shop-mg100").textContent = mg100.toLocaleString("de-DE");
      $("nut-mg100").textContent = mg100.toLocaleString("de-DE") + " mg";
      $("nut-mg").textContent = f.mg + " mg";
      $("net-weight").textContent = netG.toString().replace(".", ",");

      $("shop-price").textContent = eur(p.price);
      $("shop-per").textContent = eur(p.price / p.tins) + " / Dose";
      $("shop-unit").textContent = "Grundpreis " + eur(p.price / (p.tins * netG) * 1000) + " / kg (vorläufig)";
      var save = Math.round((1 - p.price / (base * p.tins)) * 100);
      $("shop-save").hidden = save <= 0;
      $("shop-save").textContent = save + " % gespart";
      $("shop-buy").textContent = p.url ? "Zur Bestellung · " + eur(p.price) : "Unverbindlich reservieren";
      $("shop-note").textContent = p.url
        ? "Weiter zur Kasse bei Stripe. Dort bestellst du zahlungspflichtig."
        : "Unverbindlich, kein Kaufvertrag. Zahlung erst nach separater Bestellung.";
      if ($("sticky-name")) {
        $("sticky-name").textContent = f.name + " · " + tins(p.tins);
        $("sticky-price").textContent = eur(p.price);
      }
      if (history.replaceState) history.replaceState(null, "", "?sorte=" + f.id + location.hash);
    };
    render();

    $("shop-buy").addEventListener("click", function () {
      if (sel.pack.url) { location.href = sel.pack.url; return; }
      $$("[data-picked]").forEach(function (el) {
        el.hidden = false;
        el.textContent = "Du reservierst: " + sel.pack.tins + "× " + sel.flavor.name + " (" + eur(sel.pack.price) + ")";
      });
      $("reservieren").scrollIntoView({ behavior: "smooth" });
      setTimeout(function () { var i = $("r-email"); if (i) i.focus({ preventScroll: true }); }, 600);
    });

    if ("IntersectionObserver" in window && $("sticky-buy")) {
      new IntersectionObserver(function (entries) {
        var e = entries[0];
        $("sticky-buy").hidden = e.isIntersecting || e.boundingClientRect.top > 0;
      }).observe($("shop-buy"));
    }
  }

  // ---------- Koffein pro Euro ----------
  var drinks = [
    { name: "Cappuccino im Café", price: 3.30, mg: 80, sugar: "0 g zugesetzt" },
    { name: "Red Bull 250 ml", price: 1.89, mg: 80, sugar: "ca. 27 g" },
    { name: "Monster 500 ml", price: 2.48, mg: 160, sugar: "ca. 55 g" },
    { name: "Club-Mate 0,5 l", price: 1.20, mg: 100, sugar: "ca. 25 g", est: true },
    { name: "Kaffee zu Hause", price: 0.15, mg: 90, sugar: "0 g", est: true }
  ];
  if ($("cmp")) {
    var perPiece = best.price / best.tins / 8;
    var single = packs[0].price / 8;
    var rows = drinks.map(function (d) { return { name: d.name, label: eur(d.price), mg: d.mg, sugar: d.sugar, est: d.est, per100: d.price / d.mg * 100 }; });
    rows.push({ name: "GUMMIT 60 mg, 1 Dose", label: eur(single) + " / Stück", mg: 60, sugar: "0 g", per100: single / 60 * 100, own: true });
    rows.push({ name: "GUMMIT 60 mg, " + tins(best.tins), label: eur(perPiece) + " / Stück", mg: 60, sugar: "0 g", per100: perPiece / 60 * 100, own: true });
    rows.sort(function (a, b) { return b.per100 - a.per100; });
    var max = rows[0].per100;
    $("cmp").innerHTML = rows.map(function (r) {
      return "<div class=\"cmp-row" + (r.own ? " own" : "") + "\" title=\"" + r.name + ": " + eur(r.per100) + " pro 100 mg Koffein\">" +
        "<span class=\"cmp-name\">" + r.name + (r.est ? " *" : "") + "</span>" +
        "<span class=\"cmp-track\"><i style=\"width:" + Math.max(3, r.per100 / max * 100).toFixed(1) + "%\"></i></span>" +
        "<span class=\"cmp-val\">" + eur(r.per100) + "</span></div>";
    }).join("") + "<p class=\"fine\">Preis pro 100 mg Koffein. * Schätzung.</p>";
    $("cmp-rows").innerHTML = rows.map(function (r) {
      return "<tr><td>" + r.name + (r.est ? " *" : "") + "</td><td>" + r.label + "</td><td>" + r.mg + " mg</td><td>" + r.sugar + "</td><td>" + eur(r.per100) + "</td></tr>";
    }).join("");

    var what = $("calc-what");
    drinks.slice(0, 4).forEach(function (d, i) {
      var o = document.createElement("option"); o.value = i; o.textContent = d.name; what.appendChild(o);
    });
    var calc = function () {
      var n = +$("calc-n").value, d = drinks[+what.value];
      $("calc-n-out").textContent = n + "×";
      var perMonth = n * 52 / 12;
      var costDrink = perMonth * d.price;
      var costGum = perMonth * (d.mg / 60) * perPiece;
      var diff = costDrink - costGum;
      $("calc-save").textContent = diff > 0 ? "ca. " + eur(diff) + " gespart" : "kein Preisvorteil";
      $("calc-detail").textContent = "Pro Monat " + eur(costDrink) + " für " + d.name + " statt " + eur(costGum) + " mit GUMMIT (" + tins(best.tins) + "-Paket), gleiche Koffeinmenge.";
    };
    $("calc-n").addEventListener("input", calc);
    what.addEventListener("change", calc);
    calc();
  }

  // ---------- Formulare ----------
  $$("[data-type]").forEach(function (a) {
    a.addEventListener("click", function () {
      var s = $("b-type") || $("r-type");
      if (s) s.value = a.getAttribute("data-type");
    });
  });

  $$("form[data-lead]").forEach(function (form) {
    var msg = form.querySelector(".form-msg");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = { kind: form.dataset.lead };
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.type !== "checkbox") data[el.name] = el.value.trim();
      });
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email || "")) { msg.textContent = "Die Mail-Adresse sieht komisch aus. Nochmal?"; return; }
      var missing = Array.prototype.filter.call(form.querySelectorAll("[required]"), function (el) {
        return el.type === "checkbox" ? !el.checked : !el.value.trim();
      });
      if (missing.length) { msg.textContent = "Bitte noch alle Pflichtfelder ausfüllen und den Haken setzen."; return; }
      var picked = form.querySelector("[data-picked]");
      if (picked && !picked.hidden) data.reserve = sel.pack.tins + "x " + sel.flavor.name;

      if (cfg.formEndpoint) {
        msg.textContent = "Wird gesendet …";
        fetch(cfg.formEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify(data)
        }).then(function (r) {
          if (!r.ok) throw new Error();
          form.reset();
          msg.textContent = data.kind === "reserve" ? "Merged. Du stehst auf der Liste." : "Danke! Wir melden uns.";
        }).catch(function () { msg.textContent = "Build failed. Versuch es gleich nochmal."; });
      } else if (cfg.contactEmail) {
        var body = Object.keys(data).map(function (k) { return k + ": " + data[k]; }).join("\n");
        location.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("GUMMIT " + data.kind) + "&body=" + encodeURIComponent(body);
        msg.textContent = "Dein Mailprogramm öffnet sich. Einfach abschicken.";
      } else {
        msg.textContent = "Das Formular ist noch nicht verbunden. Schau bald wieder vorbei.";
      }
    });
  });
})();
