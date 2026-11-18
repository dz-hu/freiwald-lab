// Mobile menu
(function () {
  var btn = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", String(open));
  });
})();

// Publications: search box + "Selected only" filter
(function () {
  var search = document.getElementById("pub-search");
  var selected = document.getElementById("pub-selected");
  var count = document.getElementById("pub-count");
  if (!search) return;
  var pubs = Array.prototype.slice.call(document.querySelectorAll(".pub-year .pub"));
  var years = Array.prototype.slice.call(document.querySelectorAll(".pub-year"));
  var yearLinks = Array.prototype.slice.call(document.querySelectorAll(".year-nav a"));
  pubs.forEach(function (p) { p._text = p.textContent.toLowerCase(); });

  function apply() {
    var terms = search.value.toLowerCase().split(/\s+/).filter(Boolean);
    var onlySel = selected.checked;
    var shown = 0;
    pubs.forEach(function (p) {
      var ok = (!onlySel || p.dataset.highlight === "1") &&
        terms.every(function (t) { return p._text.indexOf(t) !== -1; });
      p.classList.toggle("hidden", !ok);
      if (ok) shown++;
    });
    years.forEach(function (y, i) {
      var any = y.querySelector(".pub:not(.hidden)");
      y.classList.toggle("hidden", !any);
      if (yearLinks[i]) yearLinks[i].classList.toggle("hidden", !any);
    });
    count.textContent = shown + " of " + pubs.length + " publications";
  }
  search.addEventListener("input", apply);
  selected.addEventListener("change", apply);
  apply();
})();
