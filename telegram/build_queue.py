#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit telegram/queue.json : la liste ordonnée des posts (1 par exécution).

RÉGLAGE ACTUEL (18 nov. 2026) : FRANÇAIS SEULEMENT, ordre Difficile -> Moyen -> Facile.
  1) Difficile FR : niv_fr_21..30  (10)
  2) Moyen FR     : niv_fr_01..20  (20)
  3) Facile FR    : qotd_FR_01..62 (62)
  => 92 posts FR (~3 mois). L'anglais sera ajouté plus tard.

Relance après avoir changé l'ordre ou ajouté des vidéos :  python telegram/build_queue.py
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIFFICILE = list(range(21, 31))   # 21..30
MOYEN = list(range(1, 21))        # 1..20
FACILE = list(range(1, 63))       # 1..62

CAP_NIV = (
    "🩺 <b>Question clinique — niveau {niv}</b>\n"
    "MCCQE Partie I &amp; NAC · saute en fin de vidéo pour la correction 👇\n\n"
    "🎯 La banque complète, 100% bilingue FR/EN → eliteqbank.com"
)
CAP_FACILE = (
    "🩺 <b>Question du jour</b> — MCCQE Partie I &amp; NAC\n"
    "Teste-toi 👇 la réponse est dans la vidéo.\n\n"
    "🎯 6000+ questions, 100% bilingue FR/EN → eliteqbank.com"
)

def add(items, media, caption):
    if os.path.exists(os.path.join(ROOT, media)):
        items.append({"media": media, "lang": "FR", "caption": caption})
    else:
        print("  (absent, ignoré) " + media)

queue = []
for n in DIFFICILE:
    add(queue, f"reels_niveau/niv_fr_{n:02d}.mp4", CAP_NIV.format(niv="Difficile"))
for n in MOYEN:
    add(queue, f"reels_niveau/niv_fr_{n:02d}.mp4", CAP_NIV.format(niv="Moyen"))
for n in FACILE:
    add(queue, f"reels/qotd_FR_{n:02d}.mp4", CAP_FACILE)

out = os.path.join(ROOT, "telegram", "queue.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=1)

print(f"queue.json : {len(queue)} posts FR "
      f"(Difficile {len(DIFFICILE)} + Moyen {len(MOYEN)} + Facile {len(FACILE)}) ≈ {len(queue)//30} mois")
