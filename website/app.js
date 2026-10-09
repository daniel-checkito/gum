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
    var data = { email: email, type: fType.value, where: form.where.value.trim() };

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
      var body = "Email: " + data.email + "\nType: " + data.type + "\nWhere: " + data.where;
      location.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("GUMMIT waitlist") + "&body=" + encodeURIComponent(body);
      msg.textContent = "Your mail app is opening. Just hit send.";
    } else {
      msg.textContent = "Waitlist opens soon. Check back in a bit.";
    }
  });
})();
