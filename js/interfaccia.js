(function () {
  var urls = { home: "lab.it", corpora: "corpora.lab.it/#concordance", db: "costellazioni.lab.it/row/index", back: "costellazioni.lab.it/backend/user/login", annot: "palinsesto.lab.it/query", form: "formazione.lab.it/Corsi/Python-per-la-linguistica", tei: "testi.lab.it/works/canto1.xml", ann: "annotazione.lab.it/p/progetto-esempio/annotate", code: "git.lab.it/lab/tokenizer", stato: "stato.lab.it" };
  var tabs = document.querySelectorAll("#tabs button");
  function show(id) {
    document.querySelectorAll(".screen").forEach(function (s) { s.hidden = s.id !== id; });
    tabs.forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.s === id)); });
    document.getElementById("url").innerHTML = "<b>https://</b>" + urls[id];
    if (id === "back") { document.getElementById("login").hidden = false; document.getElementById("admin").hidden = true; }
  }
  tabs.forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.s); }); });
  document.querySelectorAll("[data-go]").forEach(function (t) { t.addEventListener("click", function () { show(t.dataset.go); }); });
  document.getElementById("lf").addEventListener("submit", function (e) {
    e.preventDefault();
    document.getElementById("login").hidden = true; document.getElementById("admin").hidden = false;
    document.getElementById("url").innerHTML = "<b>https://</b>costellazioni.lab.it/backend/row/index";
  });

  var data = [["NoSketchEngine", "99,95%", [11]], ["Costellazioni", "100%", []], ["Palinsesto", "99,91%", [8, 21]], ["TEI Publisher", "99,93%", [14]], ["INCEpTION", "99,97%", [26]],["Forgejo", "100%", []], ["Siti statici", "100%", []], ["Backup notturno", "ultimo: 03:12", [4]]];
  var out = "";
  data.forEach(function (r) {
    var bars = "";
    for (var i = 0; i < 30; i++) bars += '<i class="' + (r[2].indexOf(i) >= 0 ? "w" : "") + '"></i>';
    out += '<div class="svc"><strong>' + r[0] + '</strong><div class="hist">' + bars + '</div><div class="p">' + r[1] + '</div></div>';
  });
  document.getElementById("svcs").innerHTML = out;
})();
