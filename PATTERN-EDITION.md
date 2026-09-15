# Le gabarit d'une édition · mode journal et mode vidéo

> Ce document décrit le fonctionnement des deux présentations d'une édition et
> toutes les règles à respecter pour en produire une nouvelle. Il complète
> `REPRISE-PROJET.md`, qui reste la fiche de reprise générale du projet.
>
> Établi sur le N°29, validé le 10 septembre 2026, à appliquer dès le N°30.

## 1. Deux présentations pour le même contenu

Chaque édition existe en deux pages autonomes, avec le même texte et les mêmes
liens. Elles ne se remplacent pas, elles se complètent.

| | Mode journal | Mode vidéo |
|---|---|---|
| Fichier | `editions/nXX.html` | `editions/nXX_video.html` |
| Gabarit | `editions/n00.html` | `editions/n00_video.html` |
| Lecture | tout est visible, on parcourt et on fait défiler | une brève à la fois, on navigue |
| Vidéos | des liens sortants avec une icône de source | des lecteurs jouables dans la page |
| Pour qui | ceux qui survolent, qui impriment, qui archivent | ceux qui veulent voir sans quitter la page |

**Le mode vidéo est la présentation par défaut**, celle qu'on partage. Le mode
journal reste accessible d'un clic pour ceux qui préfèrent lire d'une traite.

### La bascule
Un bouton en haut à droite, face au lien « Toutes les éditions », fait passer
de l'une à l'autre. Il porte une icône dessinée pour l'occasion : une page vue
de dessus, avec un filet de titre et deux colonnes de texte. Elle ne doit pas
être confondue avec l'icône « Les News », qui est un journal plié.

Les styles `.topbar` et `a.mode` vivent dans `style.css`. Chaque page pointe
vers son homologue :

```html
<!-- dans nXX_video.html -->
<a class="mode" href="nXX.html">…Mode journal</a>
<!-- dans nXX.html -->
<a class="mode" href="nXX_video.html">…Mode vidéo</a>
```

Le choix n'est pas mémorisé : c'est un aller-retour explicite. Rendre la
préférence persistante demanderait `localStorage`, bloqué tant que les pages
sont ouvertes en fichiers locaux depuis le partage réseau.

## 2. Structure du mode vidéo

La page tient dans un écran, **sans ascenseur**. `.sheet` occupe toute la
hauteur utile en colonne flex : l'en-tête, le menu, la navigation et le pied
sont figés, seule la scène centrale s'étire.

```
.sheet  (100dvh, flex column)
├── .topbar      ← retour + bouton de bascule
├── h1           ← titre de l'édition, une seule ligne
├── .bar         ← « Édition N°X · date » + le lecteur audio à droite
├── .menu        ← onglets des rubriques, centrés
├── .scene       ← flex:1, tout l'espace restant
│   └── .rub × 3 ← une par rubrique, une seule visible
│       ├── .fiche × n  ← une brève, une seule visible
│       └── .nav        ← flèches, pastilles, compteur
└── footer
```

### La fiche
C'est l'unité de lecture. Média à gauche, texte à droite, **sans filet entre
les deux**, le blanc suffit.

```html
<article class="fiche on">          <!-- « on » = fiche visible -->
  <div class="med"> … lecteur ou carte … </div>
  <div class="txt">
    <span class="kick">Surtitre</span>
    <h3>Titre de la brève</h3>
    <p>Le paragraphe éditorial.</p>
    <a class="go" href="…" target="_blank">…Voir sur Instagram</a>
  </div>
</article>
```

Règles de calage, toutes vérifiées à l'œil sur le N°29 :

- Le bloc entier est **centré horizontalement et verticalement** entre le menu
  et les flèches, via `justify-content:center` et `align-content:center`.
- La colonne de texte a une **largeur fixe de 450 px**. C'est délibéré : si
  elle s'adaptait au contenu, le lecteur se déplacerait à chaque changement de
  fiche. Largeur figée, donc bloc immobile quand on navigue.
- Le texte et le lecteur partent tous les deux **du haut** de la fiche. Le
  surtitre affleure le bord supérieur de la vidéo · c'est pour ça que `.kick`
  a un `line-height:1`, sinon le blanc réservé au-dessus des capitales le
  décalerait de deux ou trois pixels.

### La navigation
Deux flèches rondes, des pastilles cliquables, un compteur « 3 / 5 ». Les
flèches du clavier fonctionnent aussi. Les onglets remettent la rubrique sur sa
première fiche.

**Les lecteurs se chargent à la demande** : l'iframe porte un `data-src`, et le
script ne pose le `src` que lorsque la fiche devient visible. En quittant une
fiche ou un onglet, le `src` est retiré, ce qui décharge le lecteur et **coupe
le son**. Sans ça, une vidéo continue de parler en fond.

## 3. Les cinq états d'un média

Toute brève a un lien. Selon ce qu'il y a au bout, la colonne de gauche prend
une forme différente. **Quand une vidéo ne peut pas être jouée, on dit
pourquoi**, précisément.

| Cas | Situation | Rendu |
|---|---|---|
| 1 | Reel Instagram jouable | lecteur recadré, `.tv` |
| 2 | Reel refusé par Instagram | carte `.hors`, avec le titre du morceau sous licence |
| 3 | Lien vers un article | carte `.hors.paysage`, avec le nom du média |
| 4 | Publication photo ou carrousel | lecteur `.tv.image`, cadre 4:5 |
| 5 | Vidéo YouTube non intégrable | carte `.hors.paysage` avec la vraie miniature |

### Pourquoi certains reels refusent la lecture
Quand la bande-son d'un reel utilise **un morceau de musique sous licence**,
Meta bloque la lecture en dehors d'Instagram. Les reels en « Audio d'origine »
passent presque toujours. Ce n'est pas une histoire de format de lien ni de
type de contenu, et ça se joue piste par piste : sur le N°29, trois reels sur
treize étaient bloqués, tous crédités d'un morceau connu, alors qu'un autre
utilisant M83 passait sans problème.

### Comment savoir avant de publier
Le test est mécanique et prend quelques secondes par lien. Ouvrir
`https://www.instagram.com/reel/CODE/embed/` et regarder :

- la page contient un vrai élément vidéo → **cas 1**, le lecteur marchera ;
- la page affiche « Jouer » et « Regarder sur Instagram » → **cas 2**, relever
  le nom du morceau crédité en haut et le citer dans la carte.

Pour YouTube, ouvrir `https://www.youtube.com/embed/ID`. Si la page renvoie
**erreur 153**, la chaîne a désactivé l'intégration : cas 5. La vignette reste
récupérable sur `https://i.ytimg.com/vi/ID/maxresdefault.jpg`, en 1280×720,
avec repli sur `mqdefault.jpg`.

## 4. Le recadrage des lecteurs Instagram

C'est la partie la plus délicate, et elle est entièrement réglée. Ne pas y
toucher sans refaire les mesures.

Ce qu'on a mesuré sur les embeds :

- le bandeau du compte fait **54 px, quelle que soit la largeur** ;
- le cadre du média est en **4:5** ;
- mais les reels sont en **9:16**, donc Instagram les centre lui-même dans son
  cadre, avec du vide de chaque côté ;
- une publication photo, elle, est servie déjà recadrée en 4:5 et remplit son
  cadre.

D'où le traitement :

```css
.tv        { aspect-ratio:9/16; overflow:hidden }
.tv iframe { top:-54px;                 /* supprime le bandeau du compte */
             width:142.22%;             /* la vidéo occupe toute la largeur */
             left:50%; transform:translateX(-50%) }
.tvz       { transform:scale(1.10) }    /* absorbe les arrondis du navigateur */
.tv.image  { aspect-ratio:4/5 }         /* photo : pas d'élargissement */
```

Le facteur 1,4222 vient du calcul : dans un cadre 4:5, une vidéo 9:16 ajustée
en hauteur n'occupe que 70,3 % de la largeur, et 1 ÷ 0,703 = 1,4222.

Le `scale(1.10)` est le seul réglage à ajuster si un liseré noir ou blanc
réapparaît sur un écran particulier. On perd 5 % sur chaque bord, ce qui ne
coûte rien sur un reel.

**Attention** : ce recadrage suppose un reel en 9:16, le format standard. Une
vidéo publiée en 4:5 ou en carré serait rognée sur les côtés · lui donner la
classe `image`, comme les publications photo.

## 5. Le lecteur audio

Il est logé **dans la barre d'édition**, à droite du numéro et de la date, sur
une seule ligne : bouton, mention « Écouter », curseur, durées, vitesse. La
mention « Par Nicolas Peytavin » n'apparaît plus en haut, elle est déjà en pied
de page.

- Fichier : `audio/nXX.mp3`, même numérotation que la page.
- Conversion depuis l'enregistrement brut :
  `ffmpeg -i source.m4a -ac 1 -b:a 64k audio/nXX.mp3`
- Vitesse par défaut **1,2×**, réglée par `VITESSE_DEFAUT` dans le script.
- Si le MP3 manque, le lecteur se grise au lieu de casser la page.

## 6. Écriture et contenu

Les règles du projet s'appliquent telles quelles, voir `REPRISE-PROJET.md` :

- **jamais de tiret cadratin**, deux-points, virgules ou point médian « · » ;
- chaque brève = un titre accrocheur et un vrai paragraphe de 3 à 5 lignes ;
- ne pas surinterpréter une source faible · préférer « mis en cause » à
  « a menti » quand la source est un reel ;
- signer « Nicolas Peytavin ».

Propres au mode vidéo :

- **Un surtitre par fiche**, court, en capitales : l'acteur (« Google · 2
  septembre »), la nature (« Comparatif ») ou le rattachement (« Démonstration
  ASTRA 6 »).
- Le paragraphe doit tenir dans la colonne de 450 px sans faire défiler, soit
  **environ 500 signes au maximum**.
- Une série de vidéos sur un même sujet fait autant de fiches, reliées par un
  surtitre commun, plutôt qu'une liste de liens.

## 7. Produire une nouvelle édition

1. Rédiger le contenu à partir des notes, en respectant les règles ci-dessus.
2. **Tester chaque lien vidéo** selon la méthode du § 3 et noter son cas.
3. Copier `editions/n00_video.html` en `editions/nXX_video.html`. Le gabarit
   contient un exemple commenté de chacun des cinq cas.
4. Adapter : titre, barre d'édition, `data-src` de l'audio, lien du bouton
   « Mode journal », fiches.
5. Produire aussi la version journal à partir de `editions/n00.html`.
6. Mettre à jour `index.html` : ligne du sommaire, compteur d'éditions.
7. Compléter le lien « suivant » en pied de l'édition précédente.
8. Vérifier : aucun tiret cadratin, aucun lien mort, balises équilibrées, et la
   page tient dans un écran sans ascenseur.

## 8. Ce qui est prévu et ce qui ne l'est pas

- **Petits écrans** : sous 900 px de large ou 620 px de haut, l'ascenseur
  revient, les colonnes se replient et le texte repasse au-dessus du lecteur.
- **Impression et PDF** : le menu, la navigation, les lecteurs et le bloc audio
  disparaissent, et toutes les fiches se déplient. Le PDF reste donc lisible et
  proche de la version journal. Rappel : imprimer depuis Chrome ou Edge avec
  « Enregistrer au format PDF », jamais « Microsoft Print to PDF ».
- **Réseau d'entreprise** : si `instagram.com` est bloqué, les lecteurs
  deviennent des cadres vides. Le mode journal reste alors le recours.
- **Polices** : chargées depuis Google Fonts. Sans connexion, la page bascule
  sur Georgia et Helvetica · la mise en page tient, elle perd son caractère.
