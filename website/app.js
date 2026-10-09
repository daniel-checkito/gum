(function () {
  var cfg = window.GUMMIT_CONFIG || {};

  // Shop
  var flavors = [
    { name: "Hotfix", taste: "mint", mg: 60, color: "#A8E6A1" },
    { name: "Ship It", taste: "cherry", mg: 52, color: "#F07A86" },
    { name: "Demo Day", taste: "berry", mg: 52, color: "#B7A8EA" }
  ];
  var packs = cfg.packs || [{ tins: 1, price: 4.99, url: "" }];
  var sel = { flavor: flavors[0], pack: packs[0] };
  var eur = function (n) { return "€" + n.toFixed(2); };
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
    return chip($("shop-packs"), "<span>" + p.tins + (p.tins === 1 ? " tin" : " tins") + "</span><small>" + eur(p.price) + "</small>",
      function () { sel.pack = p; render(); });
  });

  function render() {
    var f = sel.flavor, p = sel.pack, base = packs[0].price;
    fChips.forEach(function (c, i) { c.setAttribute("aria-pressed", flavors[i] === f ? "true" : "false"); });
    pChips.forEach(function (c, i) { c.setAttribute("aria-pressed", packs[i] === p ? "true" : "false"); });
    $("shop-tin").style.background = f.color;
    $("shop-mg").textContent = f.mg + " mg";
    $("shop-tinname").textContent = f.name;
    $("shop-tintaste").textContent = f.taste + " · 8 pcs";
    $("lede-mg").textContent = f.mg + " mg";
    $("shop-stack").hidden = p.tins === 1;
    $("shop-stack").textContent = "×" + p.tins;
    $("shop-price").textContent = eur(p.price);
    $("shop-per").textContent = eur(p.price / p.tins) + " / tin";
    var save = Math.round((1 - p.price / (base * p.tins)) * 100);
    $("shop-save").hidden = save <= 0;
    $("shop-save").textContent = "save " + save + "%";
    $("shop-buy").textContent = p.url ? "Pre-order · " + eur(p.price) : "Reserve my tins";
    $("shop-note").textContent = p.url ? "Secure checkout" : "No payment now";
    $("sticky-name").textContent = f.name + " · " + p.tins + (p.tins === 1 ? " tin" : " tins");
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
    $("f-picked").textContent = "Reserving: " + sel.pack.tins + "× " + sel.flavor.name + " (" + eur(sel.pack.price) + ")";
    $("waitlist").scrollIntoView({ behavior: "smooth" });
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

  // Pre-order
  if (cfg.preorderUrl) {
    document.getElementById("preorder").hidden = false;
    var pl = document.getElementById("preorder-link");
    pl.href = cfg.preorderUrl;
    pl.textContent = cfg.preorderLabel || "Pre-order now";
    document.getElementById("preorder-note").textContent = cfg.preorderNote || "";
  }

  // Waitlist form
  var form = document.getElementById("lead-form");
  var msg = document.getElementById("form-msg");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = form.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = "That email looks off. Try again?"; return; }
    if (!document.getElementById("f-ok").checked) { msg.textContent = "Tick the box and you're in."; return; }
    var picked = document.getElementById("f-picked");
    var data = { email: email, type: fType.value, where: form.where.value.trim(), reserve: picked.hidden ? "" : sel.pack.tins + "x " + sel.flavor.name };

    if (cfg.formEndpoint) {
      msg.textContent = "Pushing to main …";
      fetch(cfg.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error();
        form.reset();
        msg.textContent = "Merged. You're on the list.";
      }).catch(function () {
        msg.textContent = "Build failed. Try again in a sec.";
      });
    } else if (cfg.contactEmail) {
      var body = "Email: " + data.email + "\nType: " + data.type + "\nWhere: " + data.where + "\nReserve: " + data.reserve;
      location.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("GUMMIT waitlist") + "&body=" + encodeURIComponent(body);
      msg.textContent = "Your mail app is opening. Just hit send.";
    } else {
      msg.textContent = "Waitlist opens soon. Check back in a bit.";
    }
  });
})();
