# 🛠️ LLM & Agentic Engineering Skills Vault

Bienvenue dans le dépôt centralisé de tes **skills d'agents**. Cette structure est conçue pour être directement consommable par des assistants IA (comme Claude, OpenClaw, ou Codex) ou utilisable au sein de ton coffre Obsidian.

Tous les skills sont organisés en deux grands domaines complémentaires : **Build** (conception, ingénierie et automatisation) et **Work** (cadrage, apprentissage, gestion de contenu et intégrations).

---

## 📂 Organisation du Dépôt

### 🚀 1. Domaine **Build/**
Regroupe les compétences liées à la création de logiciels, au dev workflow et aux aspects techniques/sécurité.
*   **`software-engineering/`** : Pratiques de développement, loops TDD, diagnostics de bugs, rédaction de PRD, génération de tickets et le pack **Codex Dev Workflow**.
*   **`agentic-ops/`** : Création de sous-agents, de règles, de nouveaux skills et configuration de l'IDE/CLI (Cursor/OpenClaw).
*   **`security/`** : Outils de scan de vulnérabilités, modélisation de menaces et rapports d'audit de sécurité (SecureCoder).
*   **`web-and-design/`** : Création d'interfaces premium, scrollytelling 3D et revues visuelles UI/UX.

### 💼 2. Domaine **Work/**
Regroupe les compétences de cadrage, de productivité personnelle, de connecteurs externes et de création de contenu.
*   **`thinking-and-scoping/`** : Méthodologies de cadrage (grill/interview), plans d'action, structuration de PRD et cadrage de projets.
*   **`learning/`** : Systèmes d'apprentissage continu (boucles d'apprentissage et deliberate practice).
*   **`notes-and-vault/`** : Capture d'informations, intégration de notes, gestion de l'Inbox Obsidian et outils d'extraction d'inbox YouTube.
*   **`media/`** : Traitement de la parole (Text-to-Speech, Transcription) et watcher YouTube.
*   **`content-creation/`** : Le **Content Lab** personnel pour le repurposing de contenu, le motion design (Creative Direction, Hyperframes) et les checklists de validation vidéo.
*   **`integrations/`** : Scripts et connecteurs externes (Pronote, navigateurs automatisés).

---

## ⚙️ Métadonnées & Licences

Chaque fichier `SKILL.md` intègre des métadonnées standardisées dans son frontmatter YAML pour assurer la traçabilité des licences et des auteurs :
```yaml
---
name: nom-du-skill
description: Cas d'usage pour les LLMs
license: MIT | Apache-2.0 | Proprietary
author: Matt Pocock | Google | Andrew (Nadrew-pgr)
scope: software-engineering | thinking-and-scoping (pour les doublons)
---
```

*   **MIT** : La majorité des skills d'ingénierie logicielle (provenant du dépôt original de Matt Pocock).
*   **Apache-2.0** : Utilisé pour les outils comme `agent-browser`.
*   **Propriétaire/Custom** : Tes connecteurs personnalisés, ton Content Lab et les outils internes.

---

## 🔄 Synchronisation OpenClaw & Obsidian

Ce dépôt est conçu pour être synchronisé en continu. Si tu utilises Obsidian-LiveSync ou CouchDB :
*   Les fichiers `SKILL.md` sont surveillés par le démon de synchronisation.
*   Chaque skill dispose d'une identité unique gérée par le script `openclaw-doc-identity.py`.
*   Les skills dupliqués dans plusieurs domaines possèdent un tag `scope:` unique pour éviter tout conflit de synchronisation dans la base de données.
