#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poste le contenu du jour sur le canal Telegram EliteQBank.
Sans dépendance externe (stdlib only). Lancé chaque jour par GitHub Actions.

L'index du jour est calculé par la DATE (déterministe, sans état) :
  idx = (aujourd'hui - START).days  ->  queue[idx % len(queue)]
Un jour manqué est simplement sauté ; le lendemain reprend normalement.

Variables d'environnement :
  TELEGRAM_BOT_TOKEN  (obligatoire)  le token @BotFather
  TELEGRAM_CHAT_ID    (obligatoire)  ex. @eliteqbank
  DRY_RUN=1           (optionnel)    n'envoie rien, affiche seulement
  DAY_OFFSET=<n>      (optionnel)    décale l'index (test manuel)
"""
import os, sys, json, datetime, urllib.request, urllib.parse

BASE = "https://raw.githubusercontent.com/aminemanai1920/eqb-media/main/"
START = datetime.date(2026, 11, 18)   # jour index 0 — 1re publication

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "queue.json"), encoding="utf-8") as f:
        queue = json.load(f)
    if not queue:
        print("queue.json vide"); return

    dry = os.environ.get("DRY_RUN") == "1"
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")

    offset = int(os.environ.get("DAY_OFFSET", "0"))
    today = datetime.date.today()
    idx = (today - START).days + offset
    if idx < 0:
        print(f"[{today}] Pas encore commencé (START={START}).")
        return

    item = queue[idx % len(queue)]
    media = item["media"]
    caption = item["caption"]
    url = BASE + media
    method = "sendVideo" if media.endswith(".mp4") else "sendPhoto"
    field = "video" if method == "sendVideo" else "photo"

    print(f"[{today}] idx={idx} ({idx % len(queue)+1}/{len(queue)}) "
          f"-> {method} {media} [{item.get('lang','')}]")

    if dry or not token or not chat:
        if not dry:
            print("⚠️  TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID manquants -> mode DRY.")
        print("URL média :", url)
        print("Légende :\n" + caption)
        return

    params = {"chat_id": chat, field: url, "caption": caption, "parse_mode": "HTML"}
    api = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(api, data=data), timeout=90) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode("utf-8", "replace")); sys.exit(1)
    if resp.get("ok"):
        print("✅ Publié (message_id =", resp["result"].get("message_id"), ")")
    else:
        print("❌", resp); sys.exit(1)

if __name__ == "__main__":
    main()
