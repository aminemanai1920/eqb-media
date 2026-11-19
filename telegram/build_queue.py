#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit telegram/queue.json : la liste ordonnée des posts (1 par jour).
Scanne reels/ (Facile, 62 FR + 62 EN) et reels_niveau/ (30 FR + 30 EN).
Ordre : Facile interleavé FR/EN, puis Niveau interleavé FR/EN.
Relance ce script si tu ajoutes des vidéos :  python telegram/build_queue.py
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAP = {
    ("facile", "FR"): (
        "🩺 <b>Question du jour</b> — MCCQE Partie I &amp; NAC\n"
        "Teste-toi 👇 la réponse est dans la vidéo.\n\n"
        "🎯 6000+ questions, 100% bilingue FR/EN → eliteqbank.com"
    ),
    ("facile", "EN"): (
        "🩺 <b>Question of the day</b> — MCCQE Part I &amp; NAC\n"
        "Test yourself 👇 the answer is in the video.\n\n"
        "🎯 6000+ questions, fully bilingual EN/FR → eliteqbank.com"
    ),
    ("niveau", "FR"): (
        "🩺 <b>Question clinique</b> — MCCQE Partie I &amp; NAC\n"
        "Niveau supérieur 👇 saute en fin de vidéo pour la correction.\n\n"
        "🎯 La banque complète, 100% bilingue → eliteqbank.com"
    ),
    ("niveau", "EN"): (
        "🩺 <b>Clinical question</b> — MCCQE Part I &amp; NAC\n"
        "Higher level 👇 the answer is at the end of the video.\n\n"
        "🎯 The full bank, fully bilingual → eliteqbank.com"
    ),
}

def nums(pattern):
    out = []
    for p in glob.glob(os.path.join(ROOT, pattern)):
        m = re.search(r"_(\d+)\.mp4$", os.path.basename(p))
        if m:
            out.append(m.group(1))
    return sorted(set(out), key=int)

def interleave(fr_rel, en_rel, kind):
    fr_n = nums(fr_rel.replace("{n}", "*"))
    en_n = nums(en_rel.replace("{n}", "*"))
    items = []
    for n in sorted(set(fr_n) | set(en_n), key=int):
        if n in fr_n:
            items.append({"media": fr_rel.replace("{n}", n), "lang": "FR",
                          "caption": CAP[(kind, "FR")]})
        if n in en_n:
            items.append({"media": en_rel.replace("{n}", n), "lang": "EN",
                          "caption": CAP[(kind, "EN")]})
    return items

queue = []
queue += interleave("reels/qotd_FR_{n}.mp4", "reels/qotd_EN_{n}.mp4", "facile")
queue += interleave("reels_niveau/niv_fr_{n}.mp4", "reels_niveau/niv_en_{n}.mp4", "niveau")

out = os.path.join(ROOT, "telegram", "queue.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=1)

print(f"queue.json écrit : {len(queue)} posts "
      f"({len(queue)} jours ≈ {len(queue)//30} mois de contenu quotidien)")
