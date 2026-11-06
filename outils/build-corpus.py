# -*- coding: utf-8 -*-
"""
Construit api/corpus.json : le texte brut de chaque édition, lu par la
recherche IA (api/recherche.js). À relancer après chaque nouvelle édition :
    python3 outils/build-corpus.py
"""
import os, re, json, html

RACINE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITIONS = os.path.join(RACINE, "editions")
SORTIE   = os.path.join(RACINE, "api", "corpus.json")

def texte(chemin):
    s = open(chemin, encoding="utf-8").read()
    titre = re.search(r"<title>(.*?)</title>", s, re.S)
    corps = re.sub(r"(?is)<(script|style|svg|head)\b.*?</\1>", " ", s)
    corps = re.sub(r"<[^>]+>", " ", corps)
    corps = re.sub(r"\s+", " ", html.unescape(corps)).strip()
    return (html.unescape(titre.group(1)).strip() if titre else ""), corps

eds = []
for f in os.listdir(EDITIONS):
    m = re.fullmatch(r"n(\d+)\.html", f)
    if not m:
        continue
    t, c = texte(os.path.join(EDITIONS, f))
    eds.append({"n": int(m.group(1)), "url": "editions/" + f, "titre": t, "texte": c})
eds.sort(key=lambda e: e["n"])

os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
json.dump(eds, open(SORTIE, "w", encoding="utf-8"), ensure_ascii=False)
print(len(eds), "éditions,", sum(len(e["texte"]) for e in eds), "caractères")
