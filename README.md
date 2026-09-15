# La Newsletter IA

Mini-site statique qui archive 29 éditions d'une newsletter consacrée à
l'actualité de l'intelligence artificielle. Il est servi directement depuis
la racine, sans build ni dépendance.

## Organisation

- `index.html` : vitrine des couvertures.
- `index-old.html` : sommaire en liste.
- `editions/` : pages HTML des éditions et couvertures SVG.
- `audio/` et `img/` : ressources utilisées par les éditions.
- `outils/` : scripts Python de génération.
- `newsletters/` : archives Markdown de travail.

Le dossier local `Exports PDF/` contient les exports PDF et n'est pas versionné.

## Scripts

- `build-accueil.py` reconstruit `index.html` en intégrant les couvertures.
- `maj-pied-jaquettes.py` met à jour les compteurs de sources des couvertures.
- `recale-chiffre-jaquettes.py` recale le chiffre principal des couvertures.

## Règle éditoriale

Aucun tiret cadratin, jamais.
