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

  // Glaze-o-meter
  var glazes = [
    "{x}? YC is refreshing your Luma page right now.",
    "{x} is lowkey the next Notion. No notes.",
    "{x}. Sam Altman just followed you. Probably.",
    "Building {x}? Absolute cinema. Ship it.",
    "{x} has more aura than a Series A.",
    "{x}. The VCs at Factory are fighting in the hallway.",
    "{x}? You're absolutely right. Every single time.",
    "{x} is so clean it passed code review by itself.",
    "{x}. This is the demo day everybody talks about.",
    "{x}? That's not a side project. That's a unicorn in beta."
  ];
  var lastGlaze = -1;

  var colors = [
    { name: "Hotfix", bg: "#C6FF3D", fg: "#0B0A10" },
    { name: "Ship It", bg: "#FF3DA5", fg: "#0B0A10" },
    { name: "Demo Day", bg: "#7B5CFF", fg: "#F4F1EA" },
    { name: "Dark mode", bg: "#16141F", fg: "#C6FF3D" },
    { name: "Touch Grass", bg: "#F4F1EA", fg: "#0B0A10" }
  ];
  var current = colors[0];
  var idea = document.getElementById("gen-idea");
  var txt = document.getElementById("gen-text");
  var count = document.getElementById("gen-count");
  var lid = document.getElementById("lid");
  var lidText = document.getElementById("lid-text");
  var lidFlavor = document.getElementById("lid-flavor");
  var sw = document.getElementById("swatches");

  function render() {
    lidText.textContent = txt.value.trim() || "Works on my machine.";
    count.textContent = txt.value.length;
    lid.style.background = current.bg;
    lid.style.color = current.fg;
    lidFlavor.textContent = current.name;
  }

  colors.forEach(function (c, i) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "swatch";
    b.style.background = c.bg;
    b.setAttribute("aria-label", c.name);
    b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
    b.addEventListener("click", function () {
      current = c;
      sw.querySelectorAll(".swatch").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      render();
    });
    sw.appendChild(b);
  });

  function glaze() {
    var x = idea.value.trim() || "Your side project";
    var i;
    do { i = Math.floor(Math.random() * glazes.length); } while (i === lastGlaze && glazes.length > 1);
    lastGlaze = i;
    var out = glazes[i].replace("{x}", x);
    out = out.charAt(0).toUpperCase() + out.slice(1);
    txt.value = out.slice(0, 90);
    render();
  }
  document.getElementById("gen-glaze").addEventListener("click", glaze);
  idea.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); glaze(); } });
  txt.addEventListener("input", render);
  render();

  function wrapLines(ctx, text, maxWidth) {
    var words = text.split(/\s+/), out = [], line = "";
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (ctx.measureText(test).width > maxWidth && line) { out.push(line); line = w; }
      else line = test;
    });
    if (line) out.push(line);
    return out;
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
    ctx.fillStyle = "#0B0A10";
    ctx.fillRect(0, 0, W, H);
    var g = ctx.createRadialGradient(W * 0.8, H * 0.15, 0, W * 0.8, H * 0.15, 600);
    g.addColorStop(0, "rgba(123,92,255,.45)"); g.addColorStop(1, "rgba(123,92,255,0)");
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);

    var lw = 900, lh = Math.round(lw * 46 / 59), lx = (W - lw) / 2, ly = (H - lh) / 2 - 30;
    ctx.save();
    ctx.translate(W / 2, ly + lh / 2); ctx.rotate(-0.03); ctx.translate(-W / 2, -(ly + lh / 2));
    ctx.shadowColor = "rgba(0,0,0,.55)"; ctx.shadowBlur = 70; ctx.shadowOffsetY = 30;
    roundRect(ctx, lx, ly, lw, lh, 76);
    ctx.fillStyle = current.bg; ctx.fill();
    ctx.shadowColor = "transparent";
    ctx.lineWidth = 12; ctx.strokeStyle = "rgba(0,0,0,.12)";
    roundRect(ctx, lx + 6, ly + 6, lw - 12, lh - 12, 70); ctx.stroke();

    var pad = 70;
    ctx.fillStyle = current.fg;
    ctx.globalAlpha = 0.7;
    ctx.textBaseline = "top";
    ctx.font = "500 28px 'JetBrains Mono', monospace";
    ctx.fillText("git gummit -m", lx + pad, ly + pad - 6);
    ctx.globalAlpha = 1;

    var text = lidText.textContent, size = 72, ls;
    do {
      ctx.font = "800 " + size + "px 'Unbounded', sans-serif";
      ls = wrapLines(ctx, text, lw - pad * 2);
      size -= 3;
    } while (ls.length * (size + 3) * 1.15 > lh - pad * 2 - 140 && size > 30);
    var step = (size + 3) * 1.15;
    ls.forEach(function (l, i) { ctx.fillText(l, lx + pad, ly + pad + 54 + i * step); });

    ctx.textBaseline = "alphabetic";
    ctx.font = "900 50px 'Unbounded', sans-serif";
    ctx.fillText("GUMMIT", lx + pad, ly + lh - pad + 4);
    ctx.font = "500 28px 'JetBrains Mono', monospace";
    ctx.textAlign = "right";
    ctx.fillText(current.name, lx + lw - pad, ly + lh - pad);
    ctx.restore();

    ctx.textAlign = "center";
    ctx.fillStyle = "#C6FF3D";
    ctx.font = "500 28px 'JetBrains Mono', monospace";
    ctx.fillText("get glazed → " + location.host, W / 2, H - 60);
    return c;
  }

  document.getElementById("gen-download").addEventListener("click", function () {
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
      drawLid().toBlob(function (blob) {
        var file = new File([blob], "gummit-lid.png", { type: "image/png" });
        if (navigator.canShare && navigator.canShare({ files: [file] }) && /Mobi|Android/i.test(navigator.userAgent)) {
          navigator.share({ files: [file], title: "My GUMMIT lid" }).catch(function () {});
          return;
        }
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "gummit-lid.png";
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
      }, "image/png");
    });
  });

  var fLine = document.getElementById("f-line");
  var fType = document.getElementById("f-type");
  document.getElementById("gen-submit").addEventListener("click", function () {
    fLine.value = txt.value.trim();
    document.getElementById("waitlist").scrollIntoView({ behavior: "smooth" });
    setTimeout(function () { document.getElementById("f-email").focus({ preventScroll: true }); }, 600);
  });
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
    var data = { email: email, type: fType.value, where: form.where.value.trim(), line: fLine.value.trim() };

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
      var body = "Email: " + data.email + "\nType: " + data.type + "\nWhere: " + data.where + "\nLid line: " + data.line;
      location.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("GUMMIT waitlist") + "&body=" + encodeURIComponent(body);
      msg.textContent = "Your mail app is opening. Just hit send.";
    } else {
      msg.textContent = "Waitlist opens soon. Check back in a bit.";
    }
  });
})();
