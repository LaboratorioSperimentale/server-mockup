(function () {
  var urls = { home: "lab.it", corpora: "corpora.lab.it/#concordance", db: "progetto-alpha.lab.it/row/index", back: "progetto-alpha.lab.it/backend/user/login", annot: "progetto-beta.lab.it/query", form: "formazione.lab.it/Corsi/Python-per-la-linguistica", tei: "progetto-gamma.lab.it/works/canto1.xml", code: "git.lab.it/lab/tokenizer" };
  var tabs = document.querySelectorAll("#tabs button");
  function show(id) {
    document.querySelectorAll(".screen").forEach(function (s) { s.hidden = s.id !== id; });
    tabs.forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.s === id)); });
    document.getElementById("url").innerHTML = "<b>https://</b>" + urls[id];
    if (id === "back") { document.getElementById("login").hidden = false; document.getElementById("admin").hidden = true; }
  }
  tabs.forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.s); }); });
  // Nella demo locale ogni sito di esempio ha il suo indirizzo (progetto-alpha.localhost, ...) e mostra solo la sua schermata.
  var perHost = { "progetto-alpha": "db", "progetto-beta": "annot", "progetto-gamma": "tei" };
  var sito = new URLSearchParams(location.search).get("s") || perHost[location.hostname.split(".")[0]];
  if (sito && urls[sito]) { document.body.classList.add("solo"); show(sito); }
  document.querySelectorAll("[data-go]").forEach(function (t) { t.addEventListener("click", function () { show(t.dataset.go); }); });
  document.getElementById("lf").addEventListener("submit", function (e) {
    e.preventDefault();
    document.getElementById("login").hidden = true; document.getElementById("admin").hidden = false;
    document.getElementById("url").innerHTML = "<b>https://</b>progetto-alpha.lab.it/backend/row/index";
  });


  // ---- Progetto Beta (eXist-db): ricerca finta, i numeri sono inventati
  var $ = function (id) { return document.getElementById(id); };
  function schedaAltra(navId, mainId, altroId, testoId, nomePrincipale) {
    $(navId).addEventListener("click", function (e) {
      if (e.target.tagName !== "SPAN") return;
      $(navId).querySelectorAll("span").forEach(function (s) { s.classList.toggle("on", s === e.target); });
      var principale = e.target.textContent === nomePrincipale;
      $(mainId).hidden = !principale; $(altroId).hidden = principale;
      $(testoId).textContent = "«" + e.target.textContent + "»: pagina non inclusa nell'esempio.";
    });
  }
  schedaAltra("beta-nav", "beta-main", "beta-altro", "beta-altro-t", "Interroga il corpus");

  var BETA = {
    posse:  { n: [48, 74, 62, 35, 21], es: [["hoc fieri potest", "Possibilità", "I d.C."], ["nemo id facere potuit", "Possibilità", "II"], ["quantum potes, adiuva", "Permesso", "I a.C."]] },
    debere: { n: [20, 41, 38, 27, 12], es: [["debes id facere", "Possibilità", "I d.C."], ["quod debemus", "Permesso", "III"], ["debuit uenire", "Possibilità", "II"]] },
    uelle:  { n: [33, 52, 47, 30, 18], es: [["uolo uenire", "Permesso", "I d.C."], ["quid uis?", "Possibilità", "II"], ["nolebat loqui", "Permesso", "IV"]] }
  };
  var FATT = { "Tutti": 1, "Possibilità": 0.65, "Permesso": 0.35 };
  var PER = { "Tutti": [0, 1, 2, 3, 4], "I sec. a.C.": [0], "I–II sec. d.C.": [1, 2] };
  var SEC = ["I a.C.", "I d.C.", "II", "III", "IV"];
  function cercaBeta() {
    var lem = $("beta-lemma").value.trim().toLowerCase(), sig = $("beta-sig").value, per = $("beta-per").value;
    var d = BETA[lem], bars = $("beta-bars"), es = $("beta-esempi");
    if (!d) {
      bars.innerHTML = ""; bars.setAttribute("aria-label", "Nessun risultato");
      es.innerHTML = '<tr><td class="vuoto">Nessun risultato per «' + lem.replace(/[<>&]/g, "") + '». Prova con posse, debere o uelle.</td></tr>';
      $("beta-titolo").textContent = "Occorrenze per secolo"; return;
    }
    var v = d.n.map(function (n, i) { return PER[per].indexOf(i) >= 0 ? Math.round(n * FATT[sig]) : 0; });
    var max = Math.max.apply(null, v) || 1, tot = v.reduce(function (a, b) { return a + b; }, 0);
    bars.innerHTML = v.map(function (n) { return '<div style="height:' + Math.round(n / max * 100) + '%"><span>' + n + '</span></div>'; }).join("");
    bars.setAttribute("aria-label", "Occorrenze per secolo: " + v.map(function (n, i) { return SEC[i] + " " + n; }).join(", "));
    $("beta-titolo").textContent = "Occorrenze per secolo · " + tot + " in totale";
    var righe = d.es.filter(function (r) { return (sig === "Tutti" || r[1] === sig); });
    es.innerHTML = righe.length ? righe.map(function (r) { return "<tr><td><i>" + r[0] + '</i></td><td class="m">' + r[1] + '</td><td class="m">' + r[2] + "</td></tr>"; }).join("")
      : '<tr><td class="vuoto">Nessun esempio per questo significato.</td></tr>';
  }
  $("beta-form").addEventListener("submit", function (e) { e.preventDefault(); cercaBeta(); });
  ["beta-sig", "beta-per"].forEach(function (id) { $(id).addEventListener("change", cercaBeta); });
  cercaBeta();

  // ---- Progetto Gamma (TEI Publisher): note, ricerca e indici finti
  var GAMMA = [
    { v: "1–3", r: ["Nel mezzo del {1|cammin} di nostra vita", "mi ritrovai per una {2|selva oscura},", "ché la diritta via era smarrita."],
      n: { 1: ["cammin", "forma apocopata di «cammino»"], 2: ["selva oscura", "immagine allegorica"] } },
    { v: "4–6", r: ["Ahi quanto a dir qual era è cosa dura", "esta {1|selva selvaggia} e aspra e forte", "che nel pensier {2|rinova} la paura!"],
      n: { 1: ["selva selvaggia", "figura etimologica"], 2: ["rinova", "forma latineggiante per «rinnova»"] } },
    { v: "7–9", r: ["Tant'è amara che {1|poco è più morte};", "ma per trattar del ben ch'i' vi trovai,", "dirò de l'altre {2|cose} ch'i' v'ho scorte."],
      n: { 1: ["poco è più morte", "iperbole: la selva è quasi la morte"], 2: ["cose", "gli altri fatti incontrati nel viaggio"] } }
  ];
  var INDICI = {
    termini: "cammin (1) · selva (1, 4) · paura (6) · morte (7)",
    luoghi: "selva · colle · valle (nei versi successivi)",
    persone: "nessuna in questi versi"
  };
  var pag = 0, vista = "testo", cerca = "", sel = null;
  function esc(s) { return s.replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }
  function evidenzia(s) {
    if (!cerca) return s;
    return s.replace(new RegExp("(" + cerca.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi"), '<mark class="hit">$1</mark>');
  }
  function disegnaGamma() {
    var P = GAMMA[pag], doc = $("gamma-doc");
    $("gamma-pos").textContent = "Versi " + P.v + " · " + (pag + 1) + " di " + GAMMA.length;
    $("gamma-prec").disabled = pag === 0; $("gamma-succ").disabled = pag === GAMMA.length - 1;
    $("gamma-vista").querySelectorAll("button").forEach(function (b) { b.classList.toggle("ghost", b.dataset.v !== vista); });
    if (vista === "testo") {
      var html = P.r.map(function (riga) {
        return riga.split(/(\{\d\|[^}]+\})/).map(function (pz) {
          var m = pz.match(/^\{(\d)\|([^}]+)\}$/);
          if (m) return '<mark class="a' + m[1] + (sel === m[1] ? " sel" : "") + '" data-n="' + m[1] + '">' + evidenzia(esc(m[2])) + "</mark><sup>" + m[1] + "</sup>";
          return evidenzia(esc(pz));
        }).join("");
      });
      doc.innerHTML = '<p class="cap">Versi ' + P.v + "</p><p>" + html.join("<br>") + "</p>";
    } else if (vista === "facsimile") {
      doc.innerHTML = '<div class="facs">' + P.r.map(function (r) { return r.replace(/\{\d\|([^}]+)\}/g, "$1"); }).join("<br>") + "<br><br>(immagine del manoscritto, di esempio)</div>";
    } else {
      var n = 3 * pag;
      doc.innerHTML = '<pre class="xml">' + esc("<lg>\n" + P.r.map(function (r, i) { return '  <l n="' + (n + i + 1) + '">' + r.replace(/\{(\d)\|([^}]+)\}/g, function (m, k, w) { return '<term xml:id="t' + (n + +k) + '">' + w + "</term>"; }) + "</l>"; }).join("\n") + "\n</lg>") + "</pre>";
    }
    $("gamma-note").innerHTML = [1, 2].map(function (k) { return '<tr data-n="' + k + '"' + (sel === String(k) ? ' class="sel"' : "") + '><td><span class="chip c' + k + '"></span>' + k + " · " + esc(P.n[k][0]) + '</td><td class="m">' + esc(P.n[k][1]) + "</td></tr>"; }).join("");
  }
  function seleziona(e) {
    var el = e.target.closest("[data-n]"); if (!el) return;
    sel = sel === el.dataset.n ? null : el.dataset.n; disegnaGamma();
  }
  $("gamma-doc").addEventListener("click", seleziona);
  $("gamma-note").addEventListener("click", seleziona);
  $("gamma-prec").addEventListener("click", function () { pag = Math.max(0, pag - 1); sel = null; disegnaGamma(); });
  $("gamma-succ").addEventListener("click", function () { pag = Math.min(GAMMA.length - 1, pag + 1); sel = null; disegnaGamma(); });
  $("gamma-vista").addEventListener("click", function (e) { if (e.target.dataset.v) { vista = e.target.dataset.v; disegnaGamma(); } });
  $("gamma-cerca").addEventListener("input", function (e) { cerca = e.target.value.trim(); vista = "testo"; disegnaGamma(); });
  $("gamma-tag").addEventListener("click", function (e) {
    var k = e.target.dataset.i; if (!k) return;
    var acceso = e.target.classList.contains("on");
    $("gamma-tag").querySelectorAll("button").forEach(function (b) { b.classList.remove("on"); });
    if (!acceso) { e.target.classList.add("on"); $("gamma-indice").textContent = INDICI[k]; } else { $("gamma-indice").textContent = ""; }
  });
  schedaAltra("gamma-nav", "gamma-main", "gamma-altro", "gamma-altro-t", "Testi");
  disegnaGamma();
})();
