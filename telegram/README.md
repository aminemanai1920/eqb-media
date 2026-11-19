# 🤖 Pilote automatique Telegram — EliteQBank

Poste **une Question du jour** (Reel vidéo) sur le canal Telegram **chaque matin**, tout seul,
via GitHub Actions. Aucun serveur, aucun abonnement.

## Ce que ça fait
- `queue.json` : la file de 184 posts (124 Facile FR/EN + 60 Niveau FR/EN), 1 par jour ≈ **6 mois**.
- `post_daily.py` : choisit le post du jour (par la date) et l'envoie au canal.
- `.github/workflows/telegram-daily.yml` : cron quotidien à **13:00 UTC** (= 08:00 Toronto l'hiver).
- Quand la file est finie, elle **recommence** (le contenu est evergreen).

## Mise en route (une seule fois) — 3 étapes

### 1. Créer le bot
1. Dans Telegram, ouvre **@BotFather** → `/newbot`.
2. Nom : `EliteQBank` · identifiant : `eliteqbank_bot` (ou autre finissant par `_bot`).
3. BotFather te donne un **token** du type `123456:ABC-...`. **Garde-le**, ne le partage jamais en clair.

### 2. Faire du bot un admin du canal
1. Canal `@eliteqbank` → **Gérer** → **Administrateurs** → **Ajouter**.
2. Cherche ton bot (`@eliteqbank_bot`) → ajoute-le avec le droit **Publier des messages**.

### 3. Donner les 2 secrets à GitHub
Dépôt **aminemanai1920/eqb-media** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** :
- `TELEGRAM_BOT_TOKEN` = le token de BotFather
- `TELEGRAM_CHAT_ID` = `@eliteqbank`

C'est tout. Le lendemain matin, le 1er post part tout seul.

## Tester tout de suite (sans attendre demain)
Onglet **Actions** du dépôt → **Telegram — Question du jour** → **Run workflow**.
→ Ça poste immédiatement le post du jour sur le canal.

## Régler / modifier
- **Changer l'heure** : édite la ligne `cron:` dans le workflow (format UTC).
- **Changer l'ordre / le contenu** : édite `queue.json` (ou relance `python telegram/build_queue.py` après avoir ajouté des vidéos).
- **2 posts par jour** : duplique l'étape dans le workflow avec un `DAY_OFFSET` différent, ou ajoute un 2e cron.
- **Pause** : désactive le workflow dans l'onglet Actions.

*Mis en place le 18 novembre 2026 · marketing EliteQBank.*
