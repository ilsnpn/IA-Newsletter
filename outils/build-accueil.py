# -*- coding: utf-8 -*-
"""
Reconstruit index.html, la page d'accueil en vitrine de couvertures.

Pourquoi un script plutôt qu'un fichier écrit à la main : les jaquettes SVG
sont recopiées TELLES QUELLES à l'intérieur de la page, et non chargées par
<img> ou <object>. Trois raisons :
  · en <img>, le navigateur interdit au SVG d'aller chercher Playfair et
    Inter sur Google Fonts, et toutes les couvertures retombent sur Georgia ;
  · en <object>, ça fonctionne, mais rien ne garantit le chargement d'un
    fichier voisin quand la page est ouverte depuis un partage réseau, un
    SharePoint ou un Teams ;
  · intégré, il n'y a plus aucune ressource à charger : ça s'affiche partout.

La contrepartie est qu'index.html contient une copie des SVG. Dès qu'une
jaquette change, relancer ce script pour resynchroniser :
    python3 outils/build-accueil.py

Le bloc <style> interne de chaque SVG est retiré à l'intégration : les mêmes
règles sont déclarées une seule fois dans la page, sous le préfixe .jaq.
Les polices sont chargées par le <link> Google Fonts de la page.
"""
import os, re

RACINE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITIONS = os.path.join(RACINE, "editions")
SORTIE   = os.path.join(RACINE, "index.html")

# Numéro, date affichée sous la vignette, de la plus récente à la plus ancienne.
EDS = [
 (30,"22.09.2026"),(29,"08.09.2026"),(28,"31.08.2026"),(27,"17.08.2026"),(26,"03.08.2026"),
 (25,"20.07.2026"),(24,"04.07.2026"),(23,"23.06.2026"),(22,"08.06.2026"),
 (21,"26.05.2026"),(20,"11.05.2026"),(19,"27.04.2026"),(18,"13.04.2026"),
 (17,"09.04.2026"),(16,"13.03.2026"),(15,"02.03.2026"),(14,"16.02.2026"),
 (13,"02.02.2026"),(12,"19.01.2026"),(11,"05.01.2026"),(10,"11.12.2025"),
 ( 9,"24.11.2025"),( 8,"10.11.2025"),( 7,"27.10.2025"),( 6,"08.10.2025"),
 ( 5,"23.09.2025"),( 4,"08.09.2025"),( 3,"21.08.2025"),( 2,"17.08.2025"),
 ( 1,"29.07.2025"),
]

def integre(n):
    """Lit une jaquette et la prépare pour l'intégration dans la page."""
    src = open(os.path.join(EDITIONS, "n%d_Jaquette.svg" % n), encoding="utf-8").read()
    src = re.sub(r"<\?xml.*?\?>", "", src, flags=re.S)          # déclaration XML
    src = re.sub(r"<style>.*?</style>", "", src, flags=re.S)     # styles internes
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)             # commentaires
    src = re.sub(r'\s(?:width|height)="\d+"', "", src, count=2)  # laisse le viewBox piloter
    src = src.replace("<svg ", '<svg class="jaq" ', 1)
    return re.sub(r"\n{2,}", "\n", src).strip()

CARTE = '''    <li><a class="card" href="editions/n{n}.html">
      <span class="frame">{svg}<span class="hit"></span></span>
      <span class="leg"><span class="no">N°{n}</span><span class="d">{d}</span></span>
    </a></li>'''

PAGE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Newsletter IA · Les couvertures</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,500&family=Inter:wght@200;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<style>
/* ==================================================================
   Vitrine des couvertures. Page générée par outils/build-index-v2.py :
   ne pas la modifier à la main, les jaquettes y sont recopiées.
   outils/build-accueil.py la régénère.
   ================================================================== */
/* Fond plus clair que le crème des jaquettes : sans ça les couvertures
   se fondent dans la page et on ne voit plus où commence chaque objet. */
body{{background:#FCFAF5}}
.sheet.wide{{max-width:1440px}}

.gal{{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:44px 32px;margin-top:44px}}
@media(max-width:1180px){{ .gal{{grid-template-columns:repeat(3,1fr)}} }}
@media(max-width:860px) {{ .gal{{grid-template-columns:repeat(2,1fr);gap:34px 24px}} }}
@media(max-width:520px) {{ .gal{{grid-template-columns:1fr}} }}

/* display:block partout : ce sont des <span>, et un élément inline
   ignore aspect-ratio comme il ignore height. */
.card{{display:block;position:relative;text-decoration:none;color:inherit}}
.card .frame{{
  display:block;position:relative;overflow:hidden;
  border:1px solid var(--line);background:var(--bg);
  transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}}
.card .jaq{{display:block;width:100%;height:auto}}
.card .hit{{display:block;position:absolute;inset:0;z-index:2}}
.card:hover .frame,.card:focus-visible .frame{{
  transform:translateY(-4px);border-color:var(--accent);box-shadow:0 14px 34px #19161314;
}}

/* Légende : numéro et date seulement. Le titre est déjà en grand sur la
   couverture, le répéter dessous l'affaiblirait. */
.card .leg{{
  display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  margin-top:12px;padding-top:9px;border-top:1px solid var(--line);
  font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;
}}
.card .leg .no{{font-weight:700;color:var(--ink)}}
.card .leg .d{{color:var(--muted);letter-spacing:.12em}}
.card:hover .leg .no{{color:var(--accent)}}

/* Styles des jaquettes intégrées, déclarés une seule fois pour les 30.
   Ce sont exactement ceux du bloc <style> des fichiers SVG. */
.jaq .serif{{font-family:'Playfair Display',Georgia,'Times New Roman',serif}}
.jaq .sans {{font-family:'Inter','Helvetica Neue',Arial,sans-serif}}
.jaq .ink{{fill:#191613}}
.jaq .acc{{fill:#A9502F}}
.jaq .mut{{fill:#8a8378}}
.jaq .caps{{text-transform:uppercase;font-weight:700}}
.jaq .rule{{stroke:#191613}}
.jaq .hair{{stroke:#191613;opacity:.13}}

</style>
</head>
<body>
<div class="sheet wide">
  <div class="topbar end">
    <a class="mode" href="index-old.html" title="Basculer en sommaire texte, une ligne par édition"><svg viewBox="0 0 24 24" aria-hidden="true"><line x1="4" y1="6.5" x2="20" y2="6.5"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17.5" x2="20" y2="17.5"/></svg>Mode liste</a>
  </div>

  <h1>La Newsletter IA</h1>
  <div class="bar"><span class="ed">Les couvertures · {total} éditions</span><span>Par Nicolas Peytavin</span></div>

  <ul class="gal">
{cartes}
  </ul>

  <footer><div class="foot-row"><span>La Newsletter IA · Nicolas Peytavin</span><span>{total} éditions</span></div></footer>
</div>
</body>
</html>
'''

cartes = "\n".join(CARTE.format(n=n, d=d, svg=integre(n)) for n, d in EDS)
open(SORTIE, "w", encoding="utf-8").write(
    PAGE.format(cartes=cartes, total=len(EDS)))
print("index.html reconstruit ·", len(EDS), "couvertures intégrées ·",
      "%.0f Ko" % (os.path.getsize(SORTIE) / 1024))
