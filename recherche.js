// Champ « Retrouvez un ancien sujet par IA » de la page d'accueil.
(function () {
  const form = document.getElementById("rech");
  if (!form) return;
  const champ = form.querySelector("input");
  const zone = document.getElementById("rech-res");
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const q = champ.value.trim();
    if (!q) return;
    zone.hidden = false;
    zone.innerHTML = '<p class="rech-info">L’IA parcourt les éditions…</p>';
    try {
      const r = await fetch("/api/recherche", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ q }),
      });
      const d = await r.json();
      if (d.erreur) throw new Error(d.erreur);
      zone.innerHTML = d.resultats.length
        ? "<ul>" + d.resultats.map(x =>
            `<li><a href="${esc(x.url)}"><b>N°${x.n}</b> ${esc(x.titre)}</a><span>${esc(x.pourquoi)}</span></li>`
          ).join("") + "</ul>"
        : '<p class="rech-info">Aucune édition ne semble traiter ce sujet.</p>';
    } catch (err) {
      zone.innerHTML = `<p class="rech-info">${esc(err.message || "Recherche impossible.")}</p>`;
    }
  });
})();
