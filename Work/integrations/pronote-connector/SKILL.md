---
name: pronote-connector
description: Connecte Pronote à OpenClaw. Lit planning, devoirs, communications et pièces jointes DSCG depuis Pronote à la demande. Utilise exec pour invoquer la commande `pronote`.
license: MIT
author: Andrew (Nadrew-pgr)
license: MIT
author: Andrew (Nadrew-pgr)
---

# Pronote Connector

## Goal

Fournir le contexte DSCG en temps réel depuis Pronote, à la demande : planning, devoirs, messages, informations et pièces jointes. Quand Andrew demande son planning, ses prochains cours, ses devoirs, ses derniers messages Pronote ou le contenu d'une pièce jointe, utilise ce skill en lecture seule.

## Quand utiliser

- Andrew demande son planning de cours, de la semaine, du mois
- Andrew demande ses devoirs ou échéances DSCG
- Andrew demande ses messages, discussions, informations ou actualités Pronote
- Un agent a besoin du contexte DSCG pour orienter une décision
- Andrew demande ce que contient une pièce jointe Pronote précise

## Commandes

Toutes les commandes s'exécutent via `exec`. Le raccourci `pronote` est dans le PATH.

### Obtenir le contexte (recommandé)

```bash
pronote query --profile default --weeks 4 --mode full --limit 10 --json
```

Retourne un JSON borné avec le planning, les devoirs, les discussions, les informations et les métadonnées de pièces jointes. C'est la commande la plus utile pour alimenter ton contexte sans écrire dans le vault.

### Obtenir seulement les communications

```bash
pronote query --profile default --mode communications --limit 5 --json
```

Retourne les discussions et les informations Pronote sans écrire dans le vault.

### Obtenir les communications à traiter

```bash
pronote query --profile default --mode communications --unread-only --actionable-only --since-days 30 --limit 10 --json
```

À utiliser quand Andrew demande ce qui mérite son attention. Les communications pertinentes portent `actionable: true` et `attention_kind` (`schedule_change`, `work_action`, `admin_impact`, `attention`).

### Tester la connexion

```bash
pronote test --profile default --json
```

### Ne pas synchroniser le vault

`sync` est désactivé par défaut. Pour l'instant, OpenClaw doit consulter Pronote à la demande via `query`, pas remplir le workspace avec des notes Pronote.

### Télécharger une pièce jointe précise

```bash
pronote download --profile default --attachment '{"N":"...","L":"fichier.pdf","G":1}' --output-dir "/root/.openclaw/workspace/main/obsidian-vault/02 Projects/DSCG/00 Pilotage/Cours Pronote/Attachments"
```

À utiliser seulement si tu as déjà récupéré un `payload` de pièce jointe via `query --json`.

### Voir les profils configurés

```bash
pronote status
```

## Format de sortie

La commande `query --json` retourne :

```json
{
  "generated_at": "2026-05-07T13:58:28+02:00",
  "mode": "full",
  "weeks": 4,
  "filters": { "limit": 10, "unread_only": false, "actionable_only": false },
  "raw_counts": { "discussions": 6, "informations": 33 },
  "counts": { "timetable": 14, "homeworks": 0, "discussions": 2, "informations": 3 },
  "timetable": [
    {
      "uid": "b921a749",
      "ue": "UE5 MSI",
      "subject": "Matière non désignée",
      "teacher": "BABEAU F., MIRAT J.",
      "room": "C102",
      "start_at": "2026-05-07T13:00:00+02:00",
      "end_at": "2026-05-07T17:00:00+02:00",
      "duration_min": 240,
      "cancelled": true,
      "status": "Cours annulé"
    }
  ],
  "homeworks": [
    {
      "uid": "30fa3128",
      "subject": "UE4 Comptabilité",
      "due": "2026-05-18T00:00:00+02:00",
      "attachments": [
        {
          "name": "TD consolidation.pdf",
          "file_name": "TD consolidation.pdf",
          "type": 1,
          "downloadable": true,
          "payload": { "N": "...", "L": "TD consolidation.pdf", "G": 1 }
        }
      ]
    }
  ],
  "discussions": [],
  "informations": []
}
```

## Rules

1. Utiliser `query --json` comme source de vérité pour le planning, pas d'hypothèses.
2. Ne pas utiliser `sync` pour le moment. Le connecteur est une source de consultation à la demande, pas un miroir Obsidian.
3. Si la connexion échoue, le dire clairement et suggérer `pronote test --profile default --json` pour diagnostiquer.
4. Les heures sont en Europe/Paris (UTC+2). Les afficher en heure Paris.
5. Filtrer les cours annulés (`cancelled: true`) dans les résumés sauf si Andrew demande le planning complet.
6. Pour les messages Pronote, utiliser `pronote query --mode communications --limit 5 --json`.
7. Pour les communications à traiter, utiliser `--unread-only --actionable-only`.
8. Si `attention_kind: schedule_change`, envoyer un message à Andrew et lui demander de juger avant de modifier le plan. Ne pas déplacer automatiquement une session de rattrapage, car la décision dépend du prof, de l'UE et de la session prévue.
9. Si `attention_kind: work_action`, proposer ou créer une tâche/moment seulement si le contenu permet une action claire.
10. Si `attention_kind: admin_impact`, traiter seulement si cela impacte planning, obligations, paiement, accès, repas ou logistique concrète.
11. Pour les pièces jointes, `query` expose les métadonnées. Télécharger uniquement une pièce jointe précise si elle est utile pour répondre à Andrew. Télécharger d'abord dans `/tmp/pronote-attachments`; ne mettre dans le vault que si la PJ devient une preuve ou ressource durable.
12. Pour le setup du profil (changement de mot de passe), utiliser le script Node legacy :
   ```bash
   export PRONOTE_PASSWORD='...'
   node {baseDir}/scripts/pronote-connector.mjs setup \
     --profile default --username "APOUGARY" \
     --password-env PRONOTE_PASSWORD \
     --pronote-url "https://0332747g.index-education.net/pronote/" \
     --cas none
   ```

## Boundary

Ce skill lit Pronote à la demande. Il ne fait pas :
- de synchronisation globale du vault
- d'archivage automatique des communications
- d'envoi de rappels ou notifications
- de modification des données Pronote (lecture seule)

Si une communication implique une action réelle (devoir, changement d'emploi du temps, intendance, document à lire), l'agent peut ensuite utiliser les règles AI OS normales. Pour les changements d'emploi du temps, il notifie Andrew et demande jugement avant d'écrire. Pour les pièces jointes, il analyse en temporaire puis ne conserve durablement que ce qui sert vraiment.
