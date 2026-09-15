# Dossier audio · La Newsletter IA

Un fichier audio par édition. Ce dossier fait partie du site : il se déplace
avec le dossier `site`, jamais séparément.

## Convention de nommage

```
audio/n1.mp3   ← version audio de l'édition N°1
audio/n27.mp3  ← version audio de l'édition N°27 (1 min 56)
audio/n29.mp3  ← version audio de l'édition N°29 (1 min 57)
audio/n00.mp3  ← fichier de démonstration du gabarit (42 s, bip de test)
```

Même numérotation que les pages : `editions/n27.html` écoute `audio/n27.mp3`.
Pas de zéro devant, pas d'espace, pas d'accent dans le nom.

## Format recommandé

- **MP3**, mono, 64 à 96 kbit/s. Une lecture de 10 minutes pèse environ 5 Mo.
- Le MP3 est lu nativement par tous les navigateurs. Éviter le WAV, dix fois
  plus lourd pour la même chose.
- Un enregistrement brut arrive souvent en `.m4a` stéréo à 256 kbit/s, soit
  quatre fois le poids nécessaire pour de la voix. Commande de conversion :

  ```
  ffmpeg -i source.m4a -ac 1 -b:a 64k audio/n27.mp3
  ```

## Brancher le lecteur sur une édition

Deux gestes dans la page de l'édition.

1. Coller le bloc du lecteur juste sous la barre « Édition N°X · date », en
   reprenant le gabarit `editions/n00_Audio.html`. Seul le `data-src` change :

   ```html
   <div class="audio" id="audio" data-src="../audio/n27.mp3">
   ```

2. Copier le bloc `<script>` situé en bas de `n00_Audio.html`, juste avant
   `</body>`.

Les styles vivent dans `style.css` (section « lecteur audio ») : rien à
recopier de ce côté.

La lecture démarre à **1,2×** par défaut, réglé dans le script par la variable
`VITESSE_DEFAUT`. Le menu propose 1×, 1,2×, 1,5× et 2×.

## Si le fichier est absent

Le lecteur ne casse pas la page. Il se met en veille et affiche « Version
audio · Bientôt disponible pour cette édition », bouton grisé. On peut donc
poser le bloc dans une édition avant d'avoir enregistré le son.
