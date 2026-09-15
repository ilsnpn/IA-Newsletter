# Fiche de reprise · Site « La Newsletter IA »

> À faire lire à Claude en début de conversation pour reprendre le projet là où
> il en était. Claude n'a aucune mémoire d'une conversation à l'autre : ce
> document EST la mémoire. Le tenir à jour après chaque séance de travail.
>
> Dernière mise à jour : 9 septembre 2026.

## 1. Contexte du projet
Nicolas Peytavin publie une **newsletter sur l'actualité de l'IA**, envoyée par
mail (sujet type : « N°23 - IA Fable V : le model IA, pas le jeu vidéo »). Le
« N° - IA » est un jeu de mots avec « Il y a », et chaque titre doit jouer
là-dessus.

Le projet transforme ces mails en un **mini-site web** : une page d'accueil qui
sert de sommaire, et une page HTML par édition. 29 éditions publiées à ce jour,
de juillet 2025 à septembre 2026.

**Changement de rythme en cours** : le format bimensuel s'arrête, l'actualité
va trop vite. Les éditions paraîtront les **10, 20 et 30 de chaque mois**. Le
cas de février reste à trancher avec Nicolas.

## 2. Où sont les fichiers

**Dossier de travail : `U:\SHARE\Nicolas Peytavin\IA Newsletter`**
Les anciens emplacements (OneDrive « IT_OT projects - Newsletter IA » et
`U:\DEPARTEMENTS\ENGINEERING\OT\Newsletter IA`) sont morts : **ne plus jamais
les utiliser**.

```
IA Newsletter/
├── index.html            ← page d'accueil, sommaire des 29 éditions
├── style.css             ← feuille de style COMMUNE, source de vérité du style
├── REPRISE-PROJET.md     ← ce fichier
├── audio/                ← un MP3 par édition (nXX.mp3) + LISEZ-MOI.md
├── img/                  ← images des éditions (n27-cursorbench.png)
├── newsletters/          ← archives markdown du contenu (voir § 7)
├── Exports PDF/          ← PDF envoyés par mail
└── editions/
    ├── n1.html … n29.html ← une page par édition (n5 existe bien)
    ├── n00.html           ← gabarit de test, bac à sable design
    ├── n00_Audio.html     ← gabarit AVEC lecteur audio, à copier
    └── n25_export.html    ← ancien export autonome, ne pas y toucher
```

Ne pas déplacer les fichiers séparément : bouger le dossier d'un bloc.

## 3. Ligne éditoriale et design (À RESPECTER)
- **Style** : minimal, éditorial, « magazine », inspiration presse de luxe.
- **Palette** : fond crème `#F3EFE6`, encre quasi noire `#191613`, accent
  terracotta `#A9502F`. Un seul accent, jamais criard.
- **Typo** : titres en **Playfair Display**, corps en **Inter**, chargées via
  Google Fonts dans chaque page. Sans connexion, la page bascule sur Georgia
  et Helvetica : la mise en page tient, elle perd son caractère.
- **Structure d'une édition** : titre serif géant, barre « Édition N°X · date »
  entre deux filets, « Par Nicolas Peytavin », puis les rubriques en colonnes
  séparées par des filets.
- **Rubriques** et leurs icônes SVG linéaires terracotta :
  - « À la une » → étoile
  - « Les News » → journal
  - « Bonus Insolite » → étincelle
- **Grilles flexibles** : classes `.cols c1 / c2 / c3`. On adapte la grille à
  la densité de l'édition, ce n'est pas figé. Cales `.spacer` (48 px) pour
  aligner les colonnes sans dupliquer l'en-tête. Filet noir pleine largeur
  entre deux blocs `.cols`.
- **Items cliquables** : chaque brève est un lien entier, avec une petite
  **icône de source** en fin d'item, jamais le mot « Vidéo » en toutes lettres :
  - Instagram → carré arrondi + cercle
  - YouTube → rectangle arrondi + triangle
  - Lecture (article) → petit livre ouvert
- **Navigation** : « ← Toutes les éditions » en haut, précédent / suivant en
  pied de page. Penser à compléter le lien « suivant » de l'édition précédente
  à chaque nouveau numéro.

## 4. Règles d'écriture imposées par Nicolas
- **JAMAIS de tiret cadratin (—)**. Deux-points, virgules ou point médian
  « · ». Règle absolue, y compris dans les archives markdown.
- Chaque brève = **titre accrocheur + vrai paragraphe** de 3 à 5 lignes, ton
  éditorial. L'icône de source sert de porte de sortie.
- Ne pas surinterpréter : les notes de Nicolas sont parfois télégraphiques, et
  beaucoup de sources sont des reels. Nuancer quand la source est faible
  (« mis en cause » plutôt que « a menti »).
- Signer « Nicolas Peytavin ».

## 4 bis. Les deux présentations d'une édition
Depuis le N°30, chaque édition existe en **mode journal** (`nXX.html`, tout
visible, on fait défiler) et en **mode vidéo** (`nXX_video.html`, une brève à
la fois, lecteurs Instagram et YouTube jouables dans la page). Un bouton en
haut à droite fait passer de l'un à l'autre.

**Toutes les règles de ce gabarit sont dans `PATTERN-EDITION.md`** : structure
d'une fiche, cinq états possibles d'un média et comment les tester avant
publication, recadrage des lecteurs, contraintes d'écriture. Gabarits :
`editions/n00.html` et `editions/n00_video.html`.

## 5. Le lecteur audio
Chaque édition peut avoir une **version audio** enregistrée par Nicolas.

- **Gabarit** : `editions/n00_Audio.html`. Copier le bloc `<div class="audio">`
  juste sous la barre d'édition, et le `<script>` avant `</body>`. Seul le
  `data-src` change.
- **Fichiers** : `audio/nXX.mp3`, même numérotation que les pages.
- **Conversion** : les enregistrements arrivent en `.m4a` stéréo 256 kbit/s,
  soit quatre fois le poids utile pour de la voix. Commande :
  `ffmpeg -i source.m4a -ac 1 -b:a 64k audio/nXX.mp3`, plus les métadonnées
  titre, artiste et album.
- **Contrôles** : play/pause, curseur, durées, et un bouton de vitesse
  1× / 1,2× / 1,5× / 2×. **La lecture démarre à 1,2× par défaut**, réglé par
  la variable `VITESSE_DEFAUT` dans le script.
- **Si le MP3 manque**, le lecteur ne casse pas la page : il se grise et
  affiche « Version audio · Bientôt disponible pour cette édition ».
- Les styles sont dans `style.css`, section « lecteur audio ».

Éditions avec audio à ce jour : **N°27** et **N°29**.

## 6. CSS centralisé, et scellage à la demande
Le CSS est **centralisé dans `style.css`**, toutes les pages y pointent. C'est
l'état normal depuis que le site vit sur le partage réseau, où les fichiers
voisins sont accessibles.

Il a existé un script `sceller.py` qui intégrait `style.css`, les images et
l'audio directement dans le HTML, pour qu'une page partagée **seule** (Teams,
SharePoint, pièce jointe) s'affiche correctement. **Ce script a été perdu lors
d'une réorganisation de dossier.** Le réécrire si le besoin revient : il
remplaçait le `<link>` par un `<style>` marqué, et les images et sons par des
`data:` base64.

## 7. Archives markdown (état à vérifier)
Le dossier `newsletters/` contenait une archive markdown par édition. **Tout a
disparu lors de la même réorganisation, sauf `N29.md`.**

Piste retenue avec Nicolas : ne plus écrire ces archives à la main en parallèle
du HTML, ce qui créait deux vérités qui divergeaient, mais les **générer depuis
les pages HTML** avec un script d'extraction. Reste à faire.

## 8. Export PDF
Nicolas envoie aussi les éditions en PDF, rangées dans `Exports PDF/`.

- Imprimer depuis **Chrome ou Edge, Ctrl+P, destination « Enregistrer au format
  PDF »**, en cochant **« Graphismes d'arrière-plan »**.
- Ne PAS utiliser « Microsoft Print to PDF » : cette imprimante virtuelle
  aplatit la page et **détruit tous les liens cliquables**.
- Un PDF ne sait pas jouer de son de façon fiable. La version audio doit être
  jointe au mail ou hébergée à part, pas embarquée dans le PDF.

## 9. État d'avancement
- [x] 29 éditions en ligne (N°1 à N°29) + gabarits `n00` et `n00_Audio`
- [x] Sommaire au style magazine avec dates, navigation précédent / suivant
- [x] Lecteur audio maison, vitesse par défaut 1,2×
- [x] Graphique CursorBench intégré en image dans le N°27
- [x] Migration vers `U:\SHARE\Nicolas Peytavin\IA Newsletter`

### Reste à faire
- **Dates de publication des N°1 à ~15** : elles proviennent des sujets des
  mails, envoyés en rafale le même jour dans Gmail, et ne sont pas fiables.
  Nicolas doit fournir les vraies dates, à corriger dans `index.html` ET dans
  la barre « Édition N°X · date » de chaque page.
- **Deux liens manquants au N°5** (« Voir la vidéo » et « Exemple ici ») : les
  items correspondants sont sans icône en attendant les URL.
- **Régénérer les archives markdown** depuis le HTML (§ 7).
- **Trancher le cas de février** pour le rythme 10 / 20 / 30 (§ 1).
- **Réécrire `sceller.py`** si le besoin de partage à l'unité revient (§ 6).

## 10. Les cinq dernières éditions
| N° | Titre | Date |
|----|-------|------|
| 29 | Des mises à jour mineures, sauf une | 08.09.2026 |
| 28 | De l'innovation dans la compression | 31.08.2026 |
| 27 | Encore des autodafés en 2026 | 17.08.2026 |
| 26 | Trois prétendants pour un seul trône | 03.08.2026 |
| 25 | Une folle accélération en seulement 2 semaines | 20.07.2026 |

## 11. Comment reprendre
Ouvrir une conversation, donner accès au dossier
`U:\SHARE\Nicolas Peytavin\IA Newsletter`, et faire lire ce fichier. Par
exemple : « Reprends le projet Newsletter IA décrit dans REPRISE-PROJET.md,
voici mes notes pour le N°30 : … ».
