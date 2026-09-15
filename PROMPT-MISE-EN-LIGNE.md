# Prompt à donner à Claude Code

> Ouvrir le dossier dans VS Code, lancer Claude Code dedans, et coller le bloc
> ci-dessous. Tout ce qu'il y a avant ce bloc n'est qu'un mode d'emploi.

---

## À coller tel quel

```
Ce dossier est un site web statique : « La Newsletter IA », un mini-site qui
archive les éditions d'une newsletter sur l'actualité de l'IA. Je veux le
publier sur GitHub puis le mettre en ligne via Vercel.

CE QUE CONTIENT LE DOSSIER
  index.html            page d'accueil, vitrine des 29 couvertures
  index-old.html        même sommaire en liste, accessible par la bascule
  style.css             feuille de style commune à toutes les pages
  editions/             une page HTML par édition (n1 à n29) + n29old.html
                        (le N°29 en mode journal) + les gabarits n00*.html
                        + les 29 couvertures nXX_Jaquette.svg
  audio/                3 fichiers MP3 lus par le lecteur des éditions
  img/                  images utilisées dans les éditions
  outils/               3 scripts Python de génération, hors site
  newsletters/          archives markdown, hors site
  Exports PDF/          exports PDF, hors site, 3,6 Mo
  *.md                  notes de projet, hors site

Site 100 % statique : aucun build, aucune dépendance, aucun framework, aucune
variable d'environnement. Les polices viennent de Google Fonts par <link>.

CE QUE JE TE DEMANDE

1. Initialiser un dépôt git ici si ce n'est pas déjà fait.

2. Écrire un .gitignore qui exclut les fichiers système Windows et macOS
   (Thumbs.db, desktop.ini, .DS_Store) ainsi que les fichiers de conflit de
   synchronisation OneDrive s'il y en a.
   En revanche, versionne tout le reste, y compris les MP3, les PDF et les
   scripts Python : le dépôt fait environ 7 Mo, c'est négligeable, et je veux
   que le dossier de travail et le dépôt restent identiques.

3. Vérifier avant de publier, et me signaler tout problème plutôt que de le
   corriger en silence :
   - qu'aucun lien interne n'est cassé (href, src et data dans les .html) ;
   - que la casse des noms de fichiers dans les liens correspond exactement
     à la casse réelle sur le disque. C'est le piège classique : Windows ne
     fait pas la différence entre Style.css et style.css, les serveurs de
     Vercel si. Un lien qui marche chez moi peut renvoyer un 404 en ligne ;
   - que les noms de fichiers ne contiennent ni espace ni accent gênant.
     Le dossier « Exports PDF » en contient un : propose-moi de le renommer
     en « exports-pdf » plutôt que de le faire de ton propre chef.

4. Créer un README.md court : ce qu'est le site, comment il est organisé, à
   quoi servent les trois scripts de outils/, et la règle de rédaction que je
   tiens absolument, à savoir aucun tiret cadratin, jamais.

5. Créer un dépôt GitHub PUBLIC nommé « IA-Newsletter » sur mon compte, via
   la CLI gh. Si gh n'est pas installé ou pas authentifié, arrête-toi et
   dis-moi quoi faire, ne tente pas de contourner.

6. Faire le premier commit, message « Site La Newsletter IA, 29 éditions »,
   sur une branche main, et pousser.

7. Ne pas configurer Vercel toi-même. Dis-moi simplement, une fois le push
   fait, quoi cliquer sur vercel.com pour importer le dépôt. Le projet n'a
   ni build command ni output directory : c'est un site statique servi depuis
   la racine, et le preset à choisir est « Other ».

CONTRAINTES
  - Ne modifie aucun contenu éditorial, aucun HTML, aucun SVG, aucun CSS. Le
    site est fini, tu ne fais que l'empaqueter et le publier.
  - Ne crée pas de package.json, pas de vercel.json, pas de workflow GitHub
    Actions. Rien de tout ça n'est nécessaire pour un site statique et je ne
    veux pas de fichiers de configuration qui ne servent à rien.
  - Montre-moi le .gitignore et le README avant de committer.
  - Si tu hésites sur quoi que ce soit, demande plutôt que de supposer.
```

---

## Après le push, côté Vercel

1. Aller sur `vercel.com`, se connecter avec le compte GitHub.
2. **Add New → Project**, puis **Import** en face de `IA-Newsletter`.
3. Framework Preset : **Other**. Laisser Build Command, Output Directory et
   Install Command vides.
4. **Deploy**. Le site sort sur `ia-newsletter.vercel.app` en une trentaine
   de secondes.

Ensuite, chaque `git push` sur `main` redéploie tout seul.

## Un point à surveiller

Le site fonctionne aujourd'hui en ouvrant les fichiers directement depuis le
partage réseau, où la casse des noms n'a aucune importance. En ligne, elle en
a. C'est pour ça que la vérification de casse figure au point 3 du prompt :
c'est la seule chose qui peut casser au passage, et elle se voit uniquement
une fois déployée.
