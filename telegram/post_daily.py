#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poste le prochain contenu de la file sur le canal Telegram EliteQBank.
Sans dépendance externe (stdlib only). Lancé chaque jour par GitHub Actions.

Mode COMPTEUR : chaque exécution poste l'élément `next` de la file, puis
incrémente `telegram/state.json`. Indépendant du fuseau horaire : pas de
doublon, pas de saut. En fin de file, ça recommence (modulo).

Variables d'environnement :
  TELEGRAM_BOT_TOKEN  (obligatoire)  le token @BotFather
  TELEGRAM_CHAT_ID    (obligatoire)  ex. @eliteqbank
  DRY_RUN=1           (optionnel)    n'envoie rien et n'avance pas le compteur
"""
import os, sys, json, datetime, urllib.request, urllib.parse, urllib.error

BASE = "https://raw.githubusercontent.com/aminemanai1920/eqb-media/main/"

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "queue.json"), encoding="utf-8") as f:
        queue = json.load(f)
    if not queue:
        print("queue.json vide"); return

    state_path = os.path.join(here, "state.json")
    try:
        nxt = int(json.load(open(state_path, encoding="utf-8"))["next"])
    except Exception:
        nxt = 0

    dry = os.environ.get("DRY_RUN") == "1"
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")

    i = nxt % len(queue)
    item = queue[i]
    media, caption = item["media"], item["caption"]
    url = BASE + media
    method = "sendVideo" if media.endswith(".mp4") else "sendPhoto"
    field = "video" if method == "sendVideo" else "photo"

    print(f"Post #{nxt+1} (file {i+1}/{len(queue)}) -> {method} {media} [{item.get('lang','')}]")

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
    if not resp.get("ok"):
        print("❌", resp); sys.exit(1)

    print("✅ Publié (message_id =", resp["result"].get("message_id"), ")")
    # avance le compteur SEULEMENT après succès
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump({"next": nxt + 1, "updated": str(datetime.date.today())}, f,
                  ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
