# -*- coding: utf-8 -*-
"""
Supprime le créneau de la valeur barrée et recale le chiffre géant.

Deux corrections liées :

1. La valeur barrée (y=620) et son filet (y=604) disparaissent. Six jaquettes
   seulement en avaient une, et les vingt-trois autres réservaient la place
   pour rien : une bande vide sous le surtitre. L'information n'est pas perdue,
   la légende la porte déjà en toutes lettres.

2. Le chiffre géant n'est plus calé par sa ligne de base mais par le HAUT DE
   SES CAPITALES, fixé à y=648. C'est ce que l'œil voit en premier : avec une
   ligne de base commune, un « 3 » à 340 px et un « SeedDream » à 165 px
   commençaient à des hauteurs très différentes sous le surtitre. En Playfair
   Display, la hauteur de capitale vaut environ 0,70 cadratin, d'où :
        ligne de base = 648 + 0,70 x corps

La légende suit le chiffre à 78 px sous sa ligne de base : de quoi laisser
passer les jambages du signe dollar sans coller au texte.
"""
import glob, re, os

HAUT_CAP   = 648   # haut des capitales du chiffre, commun à toute la série
RAPPORT    = 0.70  # hauteur de capitale de Playfair Display, en cadratins
SOUS_LIGNE = 78    # distance ligne de base du chiffre -> ligne de base légende
PLAFOND    = 968   # la légende ne descend jamais sous cette valeur (filet à 1006)

faits = []
for f in sorted(glob.glob("editions/n*_Jaquette.svg"),
                key=lambda x: int(re.findall(r"n(\d+)_", x)[0])):
    n = int(re.findall(r"n(\d+)_", f)[0])
    s = open(f, encoding="utf-8").read()

    # --- 1. valeur barrée et son filet ---
    barre = re.search(r'<text class="serif mut" x="80" y="620"[^>]*>([^<]*)</text>', s)
    s = re.sub(r'<text class="serif mut" x="80" y="620".*?</text>\n', "", s, flags=re.S)
    s = re.sub(r'<line x1="80" y1="604".*?/>\n\n?', "", s)

    # --- 2. chiffre géant, calé par le haut des capitales ---
    m = re.search(r'(<text class="serif acc" x="80" y=")(\d+)(" font-size=")(\d+)(")', s)
    corps = int(m.group(4))
    base  = round(HAUT_CAP + RAPPORT * corps)
    s = s[:m.start(2)] + str(base) + s[m.end(2):]

    # --- 3. la légende suit ---
    leg = min(PLAFOND, base + SOUS_LIGNE)
    s = re.sub(r'(<text class="sans mut" x="80" y=")\d+(")', r"\g<1>%d\g<2>" % leg, s)

    # commentaire de section remis à jour
    s = s.replace("<!-- ============ le sujet du numéro, raconté par l'échelle ============ -->",
                  "<!-- ============ le sujet du numéro, raconté par l'échelle ============\n"
                  "     Le chiffre est calé par le haut de ses capitales (y=648), pas par sa\n"
                  "     ligne de base : c'est ce que l'œil aligne d'une couverture à l'autre.\n"
                  "     ligne de base = 648 + 0,70 x corps · légende = ligne de base + 78 -->")

    open(f, "w", encoding="utf-8").write(s)
    faits.append((n, corps, base, leg, (barre.group(1) if barre else "")))

for n, c, b, l, v in faits:
    print("N°%-3d corps %3d  base %3d  légende %3d %s"
          % (n, c, b, l, ("· barré « %s » retiré" % v) if v else ""))
