(function () {
  var cfg = window.GUMMIT_CONFIG || {};
  var $ = function (id) { return document.getElementById(id); };
  var $$ = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };
  var eur = function (n) { return n.toFixed(2).replace(".", ",") + " €"; };
  var put = function (id, text) { var el = $(id); if (el) el.textContent = text; };
  var tins = function (n) { return n + (n === 1 ? " Pack" : " Packs"); };

  var flavors = [
    { id: "minze", name: "Mint Condition", taste: "Minze", mg: 60, color: "#19B6E8" },
    { id: "kirsche", name: "Cherry Pick", taste: "Kirsche", mg: 52, color: "#F0364A" },
    { id: "beere", name: "Berry Important", taste: "Beere", mg: 52, color: "#8B5CFF" }
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

  // ---------- Hintergrund-Videos: erst laden, wenn sichtbar ----------
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var vids = $$("video[data-src]");
  if (!still && vids.length && "IntersectionObserver" in window) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) {
          if (!v.src) v.src = v.dataset.src;
          var pr = v.play(); if (pr && pr.catch) pr.catch(function () {});
        } else if (v.src) v.pause();
      });
    }, { rootMargin: "200px" });
    vids.forEach(function (v) { vio.observe(v); });
  }

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
      return radio($("shop-packs"), "<span>" + tins(p.tins) + "</span><small>" + eur(p.price) + "</small><small>" + eur(p.price / p.tins) + " pro Pack</small>" + (save > 0 ? "<span class=\"tag\">−" + save + " %</span>" : ""),
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
      if ($("shop-ph")) $("shop-ph").hidden = sel.view !== "ph";
      if ($("stage")) $("stage").style.setProperty("--stage", f.color);
      put("pdp-flavor", f.name);
      put("lede-mg", f.mg);
      if ($("shop-stack")) { $("shop-stack").hidden = p.tins === 1; $("shop-stack").textContent = "×" + p.tins; }

      var mg100 = Math.round(f.mg / (netG / 8) * 100).toLocaleString("de-DE");
      put("shop-mg100", mg100);
      put("nut-mg100", mg100 + " mg");
      put("nut-mg", f.mg + " mg");
      put("net-weight", netG.toString().replace(".", ","));

      put("shop-price", eur(p.price));
      put("shop-per", eur(p.price / p.tins) + " / Pack");
      put("shop-unit", "Grundpreis " + eur(p.price / (p.tins * netG) * 1000) + " / kg (vorläufig)");
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
      if ($("pdp-flavor") && history.replaceState) history.replaceState(null, "", "?sorte=" + f.id + location.hash);
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
    rows.push({ name: "GUMMIT 60 mg, 1 Pack", label: eur(single) + " / Stück", mg: 60, sugar: "0 g", per100: single / 60 * 100, own: true });
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

  // ---------- Koffein-Timeline ----------
  if ($("tl-chart")) {
    var doses = [];
    $$(".tl-chips").forEach(function (box) {
      var on = box.dataset.on.split(",");
      box.dataset.hours.split(",").forEach(function (h) {
        var b = document.createElement("button");
        b.type = "button"; b.textContent = (h.length < 2 ? "0" : "") + h + ":00";
        var d = { h: +h, mg: +box.dataset.mg, kind: box.dataset.kind, on: on.indexOf(h) > -1 };
        b.setAttribute("aria-pressed", d.on ? "true" : "false");
        b.addEventListener("click", function () { d.on = !d.on; b.setAttribute("aria-pressed", d.on ? "true" : "false"); draw(); });
        doses.push(d); box.appendChild(b);
      });
    });
    // Bateman-Kurve: Aufnahme ca. 45 min, Halbwertszeit 5 h
    var ka = 3, ke = Math.LN2 / 5;
    var level = function (t) {
      return doses.reduce(function (sum, d) {
        var dt = t - d.h;
        return !d.on || dt <= 0 ? sum : sum + d.mg * ka / (ka - ke) * (Math.exp(-ke * dt) - Math.exp(-ka * dt));
      }, 0);
    };
    var W = 720, H = 260, L = 44, R = 26, T = 14, B = 34, t0 = 6, t1 = 24;
    var x = function (t) { return L + (t - t0) / (t1 - t0) * (W - L - R); };
    var draw = function () {
      var pts = [], peak = 0;
      for (var t = t0; t <= t1 + 1e-9; t += 0.1) { var v = level(t); peak = Math.max(peak, v); pts.push([t, v]); }
      var top = Math.max(200, Math.ceil(peak / 50) * 50);
      var y = function (v) { return T + (1 - v / top) * (H - T - B); };
      var grid = "";
      for (var g = 0; g <= top; g += 50) grid += "<line x1=\"" + L + "\" x2=\"" + (W - R) + "\" y1=\"" + y(g) + "\" y2=\"" + y(g) + "\" stroke=\"#E8E8ED\"/><text x=\"" + (L - 8) + "\" y=\"" + (y(g) + 4) + "\" text-anchor=\"end\" font-size=\"11\" fill=\"#6E6E73\">" + g + "</text>";
      for (var h = t0; h <= t1; h += 3) grid += "<text x=\"" + x(h) + "\" y=\"" + (H - 10) + "\" text-anchor=\"middle\" font-size=\"11\" fill=\"#6E6E73\">" + (h % 24 < 10 ? "0" : "") + (h % 24) + ":00</text>";
      var line = pts.map(function (p, i) { return (i ? "L" : "M") + x(p[0]).toFixed(1) + " " + y(p[1]).toFixed(1); }).join("");
      var area = line + "L" + x(t1) + " " + y(0) + "L" + x(t0) + " " + y(0) + "Z";
      var marks = doses.filter(function (d) { return d.on; }).map(function (d) {
        return "<circle cx=\"" + x(d.h) + "\" cy=\"" + y(0) + "\" r=\"5\" fill=\"" + (d.kind === "stick" ? "#0A5CFF" : "#1D1D1F") + "\"/>";
      }).join("");
      $("tl-chart").innerHTML = "<defs><linearGradient id=\"tlg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\"><stop offset=\"0\" stop-color=\"#0A5CFF\"/><stop offset=\".5\" stop-color=\"#8B5CFF\"/><stop offset=\"1\" stop-color=\"#F0364A\"/></linearGradient>" +
        "<linearGradient id=\"tla\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\"><stop offset=\"0\" stop-color=\"#8B5CFF\" stop-opacity=\".22\"/><stop offset=\"1\" stop-color=\"#8B5CFF\" stop-opacity=\"0\"/></linearGradient></defs>" +
        grid + "<path d=\"" + area + "\" fill=\"url(#tla)\"/><path d=\"" + line + "\" fill=\"none\" stroke=\"url(#tlg)\" stroke-width=\"3\" stroke-linejoin=\"round\"/>" + marks +
        "<text x=\"" + (L + 4) + "\" y=\"" + (T + 10) + "\" font-size=\"11\" fill=\"#6E6E73\">mg im Körper</text>";
      var total = doses.reduce(function (s, d) { return s + (d.on ? d.mg : 0); }, 0);
      $("tl-total").textContent = total;
      $("tl-peak").textContent = Math.round(peak);
      $("tl-night").textContent = Math.round(level(23));
      $("tl-total").parentNode.classList.toggle("tl-over", total > 400);
      $("tl-note").textContent = total > 400 ? "Mehr als 400 mg am Tag. Das liegt über der EFSA-Empfehlung für gesunde Erwachsene." : "";
    };
    draw();
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
