# -*- coding: utf-8 -*-
"""
Met à jour le pied des jaquettes : compteur de sources à gauche, signature
et périodicité à droite.

Le compteur n'est pas saisi à la main, il est relu dans la page de l'édition
d'après l'icône de source de chaque brève :
    title="Instagram" ou title="YouTube"  -> une vidéo
    title="Lecture"                        -> une lecture
Un compteur à zéro n'est pas écrit : on n'affiche que ce qui existe. Les
éditions rédigées en texte suivi, sans aucun lien, n'ont donc rien à gauche.

Le script est idempotent : il retire le bloc précédent avant de le réécrire.
Relancer après toute modification des pages d'édition :
    python3 outils/maj-pied-jaquettes.py
"""
import os, re, glob

RACINE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITIONS = os.path.join(RACINE, "editions")

TAILLE_PIED = 15      # était 12 : trop discret une fois la jaquette en vignette
CHASSE      = ".22em" # l'interlettrage se resserre quand le corps grandit

def compte(n):
    """Nombre de vidéos et de lectures dans la page de l'édition.

    On lit en priorité la version « journal » (nXXold.html) quand elle
    existe : en mode vidéo, les lecteurs sont intégrés et les icônes de
    source disparaissent, il n'y aurait plus rien à compter.
    """
    p = os.path.join(EDITIONS, "n%dold.html" % n)
    if not os.path.exists(p):
        p = os.path.join(EDITIONS, "n%d.html" % n)
    if not os.path.exists(p):
        return 0, 0
    t = re.findall(r'title="(Instagram|YouTube|Lecture)"',
                   open(p, encoding="utf-8").read())
    return t.count("Instagram") + t.count("YouTube"), t.count("Lecture")

def libelle(v, l):
    """« 14 vidéos · 3 lectures », en omettant ce qui vaut zéro."""
    bouts = []
    if v: bouts.append('<tspan class="acc" font-weight="700">%d</tspan> vidéo%s'
                       % (v, "s" if v > 1 else ""))
    if l: bouts.append('<tspan class="acc" font-weight="700">%d</tspan> lecture%s'
                       % (l, "s" if l > 1 else ""))
    return " · ".join(bouts)

COMMENTAIRE = """<!-- Ce que contient l'édition, en face de la signature. Les liens sont
     comptés dans la page de l'édition d'après l'icône de source de chaque
     brève : Instagram et YouTube comptent comme vidéo, le livre ouvert
     comme lecture. Rien ne s'affiche quand un compteur vaut zéro.
     Bloc régénéré par outils/maj-pied-jaquettes.py -->"""

modifs = 0
for f in sorted(glob.glob(os.path.join(EDITIONS, "n[0-9]*_Jaquette.svg")),
                key=lambda x: int(re.findall(r"n(\d+)_", x)[0])):
    n = int(re.findall(r"n(\d+)_", f)[0])
    s = open(f, encoding="utf-8").read()

    # 1. on efface l'ancien pied, commentaire compris
    s = re.sub(r"<!-- Ce que contient l'édition.*?-->\s*", "", s, flags=re.S)
    s = re.sub(r'\n<text class="sans caps mut" x="80" y="1276".*?</text>\n', "\n", s, flags=re.S)

    # 2. corps du bloc de droite
    s = re.sub(r'(<text class="sans caps mut" x="920" y="1276" font-size=")\d+(" letter-spacing=")[^"]+(")',
               r"\g<1>%d\g<2>%s\g<3>" % (TAILLE_PIED, CHASSE), s)
    s = re.sub(r'(<text class="sans mut" x="920" y="1302" font-size=")\d+(")',
               r"\g<1>%d\g<2>" % (TAILLE_PIED - 1), s)

    # 3. compteur de sources à gauche
    v, l = compte(n)
    txt = libelle(v, l)
    if txt:
        bloc = ('%s\n<text class="sans caps mut" x="80" y="1276" font-size="%d" '
                'letter-spacing="%s">%s</text>\n\n' % (COMMENTAIRE, TAILLE_PIED, CHASSE, txt))
        s = s.replace('<text class="sans caps mut" x="920" y="1276"',
                      bloc + '<text class="sans caps mut" x="920" y="1276"', 1)

    open(f, "w", encoding="utf-8").write(s)
    modifs += 1
    print("N°%-3d %s" % (n, txt.replace('<tspan class="acc" font-weight="700">', '')
                                .replace("</tspan>", "") or "(aucun lien)"))

print("\n%d jaquettes mises à jour." % modifs)
