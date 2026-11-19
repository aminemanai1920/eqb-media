# 🤖 Pilote automatique Telegram — EliteQBank

Poste **un Reel (Question du jour)** sur le canal Telegram **chaque matin**, tout seul,
via GitHub Actions. Aucun serveur, aucun abonnement.

## Réglage actuel (18 nov. 2026)
- **Français seulement** pour l'instant (l'anglais sera ajouté plus tard).
- **Ordre : Difficile → Moyen → Facile.**
- `queue.json` : **92 posts FR** (10 Difficile + 20 Moyen + 62 Facile) ≈ **3 mois**, puis ça recommence.
- **1 post / jour** à **13:00 UTC** (= 08:00 Toronto l'hiver).

## Comment ça marche
- `post_daily.py` : poste le **prochain** élément de la file, puis avance le compteur `state.json`.
  → Mode « compteur » : **chaque exécution = le suivant**, sans doublon ni saut, quel que soit le fuseau.
- `.github/workflows/telegram-daily.yml` : lance le script chaque jour + sauvegarde l'avancement.
- `build_queue.py` : régénère `queue.json` (après avoir changé l'ordre ou ajouté des vidéos).
- `state.json` : `{"next": N}` — le prochain post à envoyer (remettre à `0` pour repartir du début).

## Mise en route (une seule fois) — 3 étapes

### 1. Créer le bot
Telegram → **@BotFather** → `/newbot` → nom `EliteQBank`, identifiant `eliteqbank_bot`.
Il te donne un **token** `123456:ABC-...` → garde-le, ne le partage jamais en clair.

### 2. Faire du bot un admin du canal
Canal `@eliteqbank` → **Administrateurs** → **Ajouter** → ton bot → droit **Publier des messages**.

### 3. Donner les 2 secrets à GitHub
Dépôt **aminemanai1920/eqb-media** → **Settings → Secrets and variables → Actions** → **New repository secret** :
- `TELEGRAM_BOT_TOKEN` = le token de BotFather
- `TELEGRAM_CHAT_ID` = `@eliteqbank`

## Tester tout de suite
Onglet **Actions** → **Telegram — Question du jour** → **Run workflow**.
→ Poste le prochain Reel sur le canal (et avance le compteur).

## Régler / modifier
- **Passer au bilingue / changer l'ordre** : édite `build_queue.py` puis `python telegram/build_queue.py`.
- **Changer l'heure** : la ligne `cron:` du workflow (format UTC).
- **Repartir du début** : mets `{"next": 0}` dans `state.json`.
- **Pause** : désactive le workflow dans l'onglet Actions.

*Mis en place le 18 novembre 2026 · marketing EliteQBank.*
