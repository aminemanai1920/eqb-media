#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit telegram/queue.json : la liste ordonnée des posts (1 par exécution).

RÉGLAGE ACTUEL (23 nov. 2026) : BILINGUE, alterne EN / FR un jour sur deux.
  - Démarre en ANGLAIS (position 0 = EN), puis FR, puis EN, puis FR...
  - Une question différente chaque jour (pas de répétition de la réponse le lendemain).
  - Progression de difficulté conservée : Difficile -> Moyen -> Facile.
      Difficile : niv 21..30  (10)
      Moyen     : niv 01..20  (20)
      Facile    : qotd 01..62 (62)
  => 92 posts (~3 mois) puis la file reboucle. 92 est pair -> l'alternance
     reste cohérente au rebouclage (le post 0 et le post 92 sont tous deux EN).

Relance après un changement :  python telegram/build_queue.py
Les vidéos EN et FR existent toutes dans eqb-media (vérifié : 30/30 niveau, 62/62 facile).
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIFFICILE = list(range(21, 31))   # 21..30
MOYEN = list(range(1, 21))        # 1..20
FACILE = list(range(1, 63))       # 1..62

# --- Légendes FR ---
CAP_NIV_FR = (
    "🩺 <b>Question clinique — niveau {niv}</b>\n"
    "MCCQE Partie I &amp; NAC · saute en fin de vidéo pour la correction 👇\n\n"
    "🎯 La banque complète, 100% bilingue FR/EN → eliteqbank.com"
)
CAP_FACILE_FR = (
    "🩺 <b>Question du jour</b> — MCCQE Partie I &amp; NAC\n"
    "Teste-toi 👇 la réponse est dans la vidéo.\n\n"
    "🎯 6000+ questions, 100% bilingue FR/EN → eliteqbank.com"
)
# --- Légendes EN ---
CAP_NIV_EN = (
    "🩺 <b>Clinical question — {niv} level</b>\n"
    "MCCQE Part I &amp; NAC · skip to the end of the video for the answer 👇\n\n"
    "🎯 The full question bank, 100% bilingual EN/FR → eliteqbank.com"
)
CAP_FACILE_EN = (
    "🩺 <b>Question of the day</b> — MCCQE Part I &amp; NAC\n"
    "Test yourself 👇 the answer is in the video.\n\n"
    "🎯 6000+ questions, 100% bilingual EN/FR → eliteqbank.com"
)

NIV_FR = {"Difficile": "Difficile", "Moyen": "Moyen"}
NIV_EN = {"Difficile": "Hard", "Moyen": "Intermediate"}

# Progression de difficulté (une entrée par question, dans l'ordre)
# chaque entrée sait produire sa version FR ou EN
entries = []
for n in DIFFICILE:
    entries.append(("niveau", n, "Difficile"))
for n in MOYEN:
    entries.append(("niveau", n, "Moyen"))
for n in FACILE:
    entries.append(("facile", n, None))

def make(entry, lang):
    kind, n, niv = entry
    if kind == "niveau":
        media = f"reels_niveau/niv_{'en' if lang=='EN' else 'fr'}_{n:02d}.mp4"
        cap = (CAP_NIV_EN if lang == "EN" else CAP_NIV_FR).format(
            niv=(NIV_EN if lang == "EN" else NIV_FR)[niv])
    else:
        media = f"reels/qotd_{'EN' if lang=='EN' else 'FR'}_{n:02d}.mp4"
        cap = CAP_FACILE_EN if lang == "EN" else CAP_FACILE_FR
    return {"media": media, "lang": lang, "caption": cap}

# alterne la langue un jour sur deux ; position paire = EN (démarre en anglais)
queue = [make(e, "EN" if i % 2 == 0 else "FR") for i, e in enumerate(entries)]

out = os.path.join(ROOT, "telegram", "queue.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=1)

n_en = sum(1 for x in queue if x["lang"] == "EN")
print(f"queue.json : {len(queue)} posts — {n_en} EN + {len(queue)-n_en} FR, "
      f"alternance EN/FR à partir d'EN (Difficile {len(DIFFICILE)} + Moyen {len(MOYEN)} + Facile {len(FACILE)})")
print("1ers posts :", " · ".join(f"{x['lang']}:{x['media'].split('/')[-1]}" for x in queue[:6]))
