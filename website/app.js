(function () {
  var cfg = window.GUMMIT_CONFIG || {};

  // Ticker
  var lines = [
    "You're absolutely right! This gum has no sugar.",
    "Works on my machine.",
    "Context window full. Mouth empty.",
    "Shipped it on a Friday. Again.",
    "Not a productivity hack. Just gum.",
    "Prompted, not programmed.",
    "Tab. Tab. Tab. Chew.",
    "Lowkey goated, highkey sugar-free.",
    "Your demo will crash. Your breath won't.",
    "git push --force (your luck)",
    "Seen at every Luma event. Allegedly."
  ];
  var track = document.getElementById("marquee");
  if (track) {
    track.innerHTML = lines.concat(lines).map(function (s) { return "<span>" + s + "</span>"; }).join("");
  }

  // Shop
  var flavors = [
    { name: "Hotfix", taste: "mint", mg: 60, color: "#C6FF3D", fg: "#0B0A10" },
    { name: "Ship It", taste: "cherry", mg: 52, color: "#FF3DA5", fg: "#0B0A10" },
    { name: "Demo Day", taste: "berry", mg: 52, color: "#7B5CFF", fg: "#F4F1EA" }
  ];
  var packs = cfg.packs || [{ tins: 1, price: 4.99, url: "" }];
  var sel = { flavor: flavors[0], pack: packs[0] };
  var eur = function (n) { return "€" + n.toFixed(2); };

  function chip(parent, label, sub, active, onClick) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.setAttribute("aria-pressed", active ? "true" : "false");
    b.innerHTML = "<span>" + label + "</span>" + (sub ? "<small>" + sub + "</small>" : "");
    b.addEventListener("click", function () {
      parent.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      onClick();
    });
    parent.appendChild(b);
  }

  function renderShop() {
    var f = sel.flavor, p = sel.pack, base = packs[0].price;
    document.getElementById("shop-mg").textContent = f.mg + " mg";
    document.getElementById("shop-tinname").textContent = f.name;
    document.getElementById("shop-tintaste").textContent = f.taste + " · 8 pieces";
    var tf = document.getElementById("shop-tinflavor");
    tf.style.background = f.color; tf.style.color = f.fg;
    document.getElementById("shop-mg").style.color = f.color;
    document.getElementById("shop-stack").textContent = "×" + p.tins;
    document.getElementById("shop-price").textContent = eur(p.price);
    document.getElementById("shop-per").textContent = eur(p.price / p.tins) + " / tin";
    var save = Math.round((1 - p.price / (base * p.tins)) * 100);
    var sv = document.getElementById("shop-save");
    sv.hidden = save <= 0; sv.textContent = "save " + save + "%";
    var buy = document.getElementById("shop-buy");
    buy.textContent = p.url ? "Pre-order · " + eur(p.price) : "Reserve my tins";
    document.getElementById("shop-note").textContent = p.url
      ? "Secure checkout. Ships with the first batch, full refund if it doesn't."
      : "No payment yet. We email you when the first batch ships.";
  }

  var fWrap = document.getElementById("shop-flavors");
  flavors.forEach(function (f, i) {
    chip(fWrap, f.name, f.taste + " · " + f.mg + " mg", i === 0, function () { sel.flavor = f; renderShop(); });
  });
  var pWrap = document.getElementById("shop-packs");
  packs.forEach(function (p, i) {
    chip(pWrap, p.tins + (p.tins === 1 ? " tin" : " tins"), eur(p.price), i === 0, function () { sel.pack = p; renderShop(); });
  });
  renderShop();

  document.getElementById("shop-buy").addEventListener("click", function () {
    if (sel.pack.url) { location.href = sel.pack.url; return; }
    var picked = document.getElementById("f-picked");
    picked.hidden = false;
    picked.textContent = "Reserving: " + sel.pack.tins + "× " + sel.flavor.name + " (" + eur(sel.pack.price) + ")";
    document.getElementById("waitlist").scrollIntoView({ behavior: "smooth" });
    setTimeout(function () { document.getElementById("f-email").focus({ preventScroll: true }); }, 600);
  });

  var fType = document.getElementById("f-type");
  document.querySelectorAll("[data-type]").forEach(function (a) {
    a.addEventListener("click", function () { fType.value = a.getAttribute("data-type"); });
  });

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
