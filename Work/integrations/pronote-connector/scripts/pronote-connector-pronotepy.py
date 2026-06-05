#!/usr/bin/env python3
"""
pronote-connector — pronotepy backend for OpenClaw.

Drop-in replacement for the Node.js pronote-connector.mjs.
Uses pronotepy (maintained, compatible with PRONOTE 2025).

Commands:
  test     - Test connection and show summary
  query    - Fetch timetable/homework as JSON context for OpenClaw
  sync     - Legacy vault write path, disabled by default
  download - Download one attachment from a JSON payload
  status   - Show configured profiles
  setup    - Create/update a profile (stores encrypted credentials)

Usage:
  python3 pronote-connector-pronotepy.py test --profile default [--json]
  python3 pronote-connector-pronotepy.py query --profile default --weeks 4 --mode full --json
  python3 pronote-connector-pronotepy.py query --profile default --mode communications --json
  python3 pronote-connector-pronotepy.py download --profile default --attachment '{"N":"...","L":"file.pdf","G":1}' --output-dir /tmp/pronote
"""

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    import pronotepy
except ImportError:
    print("❌ pronotepy not installed. Run: /root/.openclaw/pronote-connector/venv/bin/pip install pronotepy", file=sys.stderr)
    sys.exit(1)

# --- Config paths (same as Node connector) ---
CONFIG_DIR = Path.home() / ".openclaw" / "pronote-connector"
CONFIG_FILE = CONFIG_DIR / "profiles.json"
MASTER_KEY_FILE = CONFIG_DIR / "master.key"
LOG_FILE = CONFIG_DIR / "connector.log"

VAULT_DIRS = [
    Path.home() / ".openclaw" / "workspace" / "main" / "obsidian-vault" / "02 Projects" / "DSCG" / "00 Pilotage" / "Cours Pronote",
    Path("/root/.openclaw/workspace/main/obsidian-vault/02 Projects/DSCG/00 Pilotage/Cours Pronote"),
]
DEFAULT_VAULT_DIR = next((p for p in VAULT_DIRS if p.exists()), VAULT_DIRS[0])
HOMEWORK_DIR_NAME = "Homework"
COMMUNICATIONS_DIR_NAME = "Communications"
ATTACHMENTS_DIR_NAME = "Attachments"

DECRYPT_HELPER = Path(__file__).parent / "decrypt-password.mjs"


def log_event(msg: str):
    """Append to connector log."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now().isoformat()} | {msg}\n")


def fail(msg: str):
    print(f"\n❌ {msg}", file=sys.stderr)
    sys.exit(1)


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {"version": 1, "profiles": {}}
    return json.loads(CONFIG_FILE.read_text())


def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")
    CONFIG_FILE.chmod(0o600)


def decrypt_password(profile_name: str = "default") -> str:
    """Decrypt password using the Node.js helper (shares the same encrypted store)."""
    if not DECRYPT_HELPER.exists():
        fail(f"decrypt-password.mjs not found at {DECRYPT_HELPER}")
    try:
        result = subprocess.run(
            ["node", str(DECRYPT_HELPER), profile_name],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        fail(f"Failed to decrypt password for profile {profile_name}: {e.stderr}")


def get_profile(name: str = "default") -> dict:
    config = load_config()
    profile = config.get("profiles", {}).get(name)
    if not profile:
        fail(f"Profile '{name}' not found. Run setup first.")
    password = decrypt_password(name)
    return {**profile, "password": password, "profileName": name}


def connect(profile: dict) -> pronotepy.Client:
    """Connect to Pronote using pronotepy."""
    url = profile["url"]
    if not url.endswith("eleve.html"):
        url = url.rstrip("/") + "/eleve.html"

    try:
        client = pronotepy.Client(
            url,
            username=profile["username"],
            password=profile["password"]
        )
    except pronotepy.exceptions.CryptoError:
        fail("Authentication failed (bad username/password). Re-run setup with correct credentials.")
    except Exception as e:
        fail(f"Connection failed: {type(e).__name__}: {e}")

    if not client.logged_in:
        fail("Login returned but client is not authenticated.")

    return client


# --- Data helpers ---

def to_local_iso(dt) -> str:
    """Convert datetime to local ISO string with timezone offset."""
    if dt is None:
        return None
    if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.combine(dt, datetime.time())
    # Use Paris timezone offset (simplified)
    return dt.strftime("%Y-%m-%dT%H:%M:%S+02:00")


def digest(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:8]


def slug(text: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize("NFKD", text or "cours")
    ascii_text = normalized.encode("ascii", "ignore").decode()
    clean = "".join(c if c.isalnum() or c in " ._-" else "" for c in ascii_text)
    return clean.strip().replace(" ", "-")[:70]


def safe_filename(name: str) -> str:
    """Return a local filename without path traversal or shell-hostile characters."""
    raw = Path(str(name or "attachment")).name.strip()
    clean = "".join("_" if c in '<>:"/\\|?*\n\r\t' else c for c in raw).strip(" .")
    if not clean:
        clean = f"attachment-{digest(str(name))}"
    return clean[:160]


def vault_relative_path(path: Path) -> str:
    """Return an Obsidian wikilink path relative to the vault when possible."""
    resolved = path.resolve()
    for parent in resolved.parents:
        if parent.name == "obsidian-vault":
            return resolved.relative_to(parent).as_posix()
    return path.as_posix()


def markdown_label(text: str) -> str:
    return str(text or "attachment").replace("|", "-").replace("]", "\\]")


UE_RULES = [
    (["ue2", "finance", "diagnostic"], "UE2 Finance"),
    (["ue3", "management", "controle", "control", "gestion"], "UE3 Management et contrôle de gestion"),
    (["ue4", "comptabil", "audit"], "UE4 Comptabilité et audit"),
    (["ue5", "si", "systeme", "informatique", "msi"], "UE5 MSI"),
    (["ue6", "anglais"], "UE6 Anglais"),
    (["ue7", "memoire"], "UE7 Mémoire"),
]

ACTIONABLE_KEYWORDS = [
    "annul",
    "apporter",
    "carte",
    "changement",
    "controle",
    "convocation",
    "devoir",
    "dossier",
    "echeance",
    "envoyer",
    "evaluation",
    "formulaire",
    "important",
    "intendance",
    "obligatoire",
    "paiement",
    "piece jointe",
    "rendu",
    "report",
    "salle",
    "urgent",
]

SCHEDULE_KEYWORDS = [
    "absence",
    "annul",
    "changement",
    "edt",
    "emploi du temps",
    "modification edt",
    "report",
    "salle",
]

HOMEWORK_KEYWORDS = [
    "apporter",
    "controle",
    "devoir",
    "dossier",
    "echeance",
    "envoyer",
    "evaluation",
    "piece jointe",
    "rendu",
]

ADMIN_IMPACT_KEYWORDS = [
    "carte",
    "demi-pension",
    "facture",
    "intendance",
    "paiement",
    "repas",
]


def detect_ue(subject: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize("NFKD", (subject or "").lower())
    for keys, label in UE_RULES:
        if any(k in normalized for k in keys):
            return label
    return "DSCG"


def format_lesson(lesson) -> dict:
    """Convert a pronotepy Lesson to our standard format."""
    subject_name = lesson.subject.name if lesson.subject else "Matière non désignée"
    teacher = lesson.teacher_name if hasattr(lesson, "teacher_name") and lesson.teacher_name else "Non spécifié"
    room = lesson.classroom if hasattr(lesson, "classroom") and lesson.classroom else ""
    start_iso = to_local_iso(lesson.start)
    end_iso = to_local_iso(lesson.end)
    duration = int((lesson.end - lesson.start).total_seconds() / 60) if lesson.start and lesson.end else 0

    key_seed = f"{start_iso}|{end_iso}|{subject_name}|{teacher}|{room}"
    uid = digest(key_seed)

    return {
        "uid": uid,
        "ue": detect_ue(subject_name),
        "subject": subject_name,
        "teacher": teacher,
        "room": room,
        "start_at": start_iso,
        "end_at": end_iso,
        "duration_min": duration,
        "cancelled": bool(lesson.canceled),
        "absent": bool(getattr(lesson, "absence", False)),
        "status": getattr(lesson, "status", None),
    }


def attachment_payload(att) -> dict:
    payload = {
        "N": getattr(att, "id", ""),
        "L": getattr(att, "name", ""),
        "G": getattr(att, "type", 1),
    }
    if payload["G"] == 0:
        payload["url"] = getattr(att, "url", "")
    return payload


def format_attachment(att) -> dict:
    att_type = getattr(att, "type", 1)
    name = getattr(att, "name", "attachment")
    return {
        "name": name,
        "file_name": safe_filename(name),
        "url": getattr(att, "url", ""),
        "type": att_type,
        "id": getattr(att, "id", ""),
        "downloadable": att_type == 1,
        "payload": attachment_payload(att),
    }


def get_attachment_payload(att_data: dict) -> dict:
    payload = att_data.get("payload", att_data)
    if isinstance(payload, str):
        payload = json.loads(payload)
    return payload


def attachment_note_line(att_data: dict, attachment_dir: Path) -> str:
    name = att_data.get("name") or att_data.get("file_name") or "Pièce jointe"
    if int(att_data.get("type", 1)) == 0:
        url = att_data.get("url") or get_attachment_payload(att_data).get("url", "")
        return f"- [{markdown_label(name)}]({url})\n" if url else f"- {name}\n"

    file_name = att_data.get("file_name") or safe_filename(name)
    link_path = vault_relative_path(attachment_dir / file_name)
    return f"- ![[{link_path}|{markdown_label(name)}]]\n"


def communication_text(item: dict) -> str:
    chunks = [
        item.get("subject", ""),
        item.get("title", ""),
        item.get("creator", ""),
        item.get("author", ""),
        item.get("content", ""),
    ]
    for message in item.get("messages", []):
        chunks.extend([message.get("author", ""), message.get("content", "")])
    return "\n".join(str(c or "") for c in chunks).lower()


def attention_kind(item: dict) -> str:
    text = communication_text(item)
    has_attachments = bool(item.get("attachments"))

    if any(keyword in text for keyword in SCHEDULE_KEYWORDS):
        return "schedule_change"
    if has_attachments or any(keyword in text for keyword in HOMEWORK_KEYWORDS):
        return "work_action"
    if any(keyword in text for keyword in ADMIN_IMPACT_KEYWORDS):
        return "admin_impact"
    if "urgent" in text or "important" in text or "obligatoire" in text:
        return "attention"
    return "none"


def is_actionable_communication(item: dict) -> bool:
    return attention_kind(item) != "none"


def is_unread_communication(item: dict) -> bool:
    if "messages" in item:
        return int(item.get("unread") or 0) > 0
    if "read" in item:
        return item.get("read") is False
    return False


def item_date(item: dict) -> datetime.datetime:
    value = item.get("last_message_at") or item.get("date")
    if not value:
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


def filter_communications(items: list, args) -> list:
    filtered = list(items)

    if getattr(args, "unread_only", False):
        filtered = [item for item in filtered if is_unread_communication(item)]

    if getattr(args, "actionable_only", False):
        filtered = [item for item in filtered if item.get("actionable")]

    if getattr(args, "with_attachments_only", False):
        filtered = [item for item in filtered if item.get("attachments")]

    since_days = getattr(args, "since_days", None)
    if since_days:
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=since_days)
        filtered = [item for item in filtered if item_date(item).astimezone(datetime.timezone.utc) >= cutoff]

    filtered.sort(key=item_date, reverse=True)

    limit = getattr(args, "limit", 10)
    if limit and limit > 0:
        filtered = filtered[:limit]

    return filtered


def format_discussion(disc) -> dict:
    messages = []
    for m in disc.messages:
        messages.append({
            "author": m.author,
            "date": to_local_iso(m.date),
            "content": m.content,
            "seen": m.seen
        })
    uid = digest(f"{disc.subject}|{disc.creator}|{len(messages)}")
    data = {
        "uid": uid,
        "subject": disc.subject,
        "creator": disc.creator,
        "closed": getattr(disc, "closed", False),
        "unread": getattr(disc, "unread", 0),
        "last_message_at": messages[-1]["date"] if messages else None,
        "messages": messages,
    }
    data["attention_kind"] = attention_kind(data)
    data["actionable"] = is_actionable_communication(data)
    return data


def format_information(info) -> dict:
    uid = digest(f"{info.title}|{info.author}|{info.creation_date}")
    data = {
        "uid": uid,
        "title": info.title,
        "author": info.author,
        "date": to_local_iso(info.creation_date),
        "start_date": to_local_iso(getattr(info, "start_date", None)),
        "end_date": to_local_iso(getattr(info, "end_date", None)),
        "read": getattr(info, "read", None),
        "category": getattr(info, "category", None),
        "survey": getattr(info, "survey", False),
        "content": info.content,
        "attachments": [format_attachment(a) for a in getattr(info, "attachments", [])]
    }
    data["attention_kind"] = attention_kind(data)
    data["actionable"] = is_actionable_communication(data)
    return data


def format_homework(hw) -> dict:
    """Convert a pronotepy Homework to our standard format."""
    subject_name = hw.subject.name if hw.subject else "Cours"
    due = to_local_iso(hw.date) if hw.date else None
    content = hw.description or ""

    uid = digest(f"{subject_name}|{due}|{content[:100]}")

    return {
        "uid": uid,
        "ue": detect_ue(subject_name),
        "subject": subject_name,
        "due": due,
        "done": bool(hw.done),
        "content_preview": content[:240],
        "content_full": content,
        "attachments": [format_attachment(a) for a in getattr(hw, "files", [])]
    }


# --- Note writing (Obsidian) ---

def write_lesson_note(lesson_data: dict, profile: dict, output_dir: Path):
    """Write a single lesson as an Obsidian markdown note."""
    date_prefix = (lesson_data["start_at"] or "no-date")[:10]
    hour_prefix = (lesson_data["start_at"] or "no-hour")[11:16].replace(":", "-")
    file_slug = f"{slug(lesson_data['subject'])}-{lesson_data['uid']}"
    filename = f"{date_prefix} {hour_prefix} - {file_slug}.md"
    filepath = output_dir / filename

    state = "Cours annulé" if lesson_data["cancelled"] else "Cours prévu"
    ue = lesson_data["ue"]

    frontmatter = f"""---
type: moment
status: planned
project: DSCG
workstream: rattrapage-niveau
casquette: Carrière & formation
priority: P1
moment_type: class_block
planned_for: {lesson_data['start_at']}
start_at: {lesson_data['start_at']}
due_at: {lesson_data['end_at']}
end_at: {lesson_data['end_at']}
duration_min: {lesson_data['duration_min']}
owner: Andrew
created_by: Sync
calendar_layer: dscg
source_profile: {profile['profileName']}
source_uid: {lesson_data['uid']}
proof_expected: capture_3_points_du_cours
rag: include
---"""

    body = f"""# Cours Pronote — {lesson_data['subject']}

## Infos

- UE : {ue}
- Enseignant : {lesson_data['teacher']}
- Salle : {lesson_data['room'] or 'Non précisée'}
- État : {state}
- Début : {lesson_data['start_at']}
- Fin : {lesson_data['end_at']}
- Durée : {lesson_data['duration_min']} min
- Source : {profile['url']}

## Checklist

- [ ] Extraire 2 questions essentielles
- [ ] Noter 1 point de confusion réel
- [ ] Créer 1 question dans questions-active-recall

Source profile: {profile['profileName']}
"""

    filepath.write_text(f"{frontmatter}\n\n{body}", encoding="utf-8")
    return filepath


def write_homework_note(hw_data: dict, profile: dict, homework_dir: Path, attachment_dir: Path = None):
    """Write a single homework as an Obsidian markdown note."""
    attachment_dir = attachment_dir or homework_dir.parent / ATTACHMENTS_DIR_NAME
    date_prefix = (hw_data["due"] or "no-date")[:10]
    file_slug = f"{slug(hw_data['subject'])}-{hw_data['uid']}"
    filename = f"{date_prefix}-{file_slug}.md"
    filepath = homework_dir / filename

    frontmatter = f"""---
type: task
status: planned
project: DSCG
workstream: pilotage
casquette: Carrière & formation
priority: P2
task_type: homework
due_at: {hw_data['due'] or 'non précisé'}
duration_min: 30
owner: Andrew
created_by: Sync
calendar_layer: dscg
source_profile: {profile['profileName']}
rag: include
---"""

    body = f"""# Devoir Pronote — {hw_data['subject']}

## Infos devoir

- UE : {hw_data['ue']}
- Réalisé pour : {hw_data['due'] or 'non précisé'}
- Fait : {'oui' if hw_data['done'] else 'non'}
- Source : {profile['url']}

## Contenu

{hw_data['content_full'] or 'Aucun contenu détaillé reçu.'}

## Pièces jointes

"""
    if hw_data.get("attachments"):
        for att in hw_data["attachments"]:
            body += attachment_note_line(att, attachment_dir)
    else:
        body += "Aucune pièce jointe.\n"

    body += f"""
## Actions

- [ ] Ajouter une piste d'action
- [ ] Relier à la session de révision correspondante

Profile utilisé : {profile['profileName']}
"""

    filepath.write_text(f"{frontmatter}\n\n{body}", encoding="utf-8")
    return filepath


def write_discussion_note(disc_data: dict, profile: dict, out_dir: Path):
    file_slug = f"{slug(disc_data['subject'])}-{disc_data['uid']}"
    filename = f"Discussion-{file_slug}.md"
    filepath = out_dir / filename
    
    frontmatter = f"""---
type: pronote-discussion
project: DSCG
source_profile: {profile['profileName']}
uid: {disc_data['uid']}
closed: {disc_data['closed']}
---"""

    body = f"# {disc_data['subject']}\n\nCréée par : {disc_data['creator']}\n\n"
    for m in disc_data["messages"]:
        body += f"## {m['author']} ({m['date']})\n{m['content']}\n\n---\n"
        
    filepath.write_text(f"{frontmatter}\n\n{body}", encoding="utf-8")
    return filepath


def write_information_note(info_data: dict, profile: dict, out_dir: Path, attachment_dir: Path = None):
    attachment_dir = attachment_dir or out_dir.parent / ATTACHMENTS_DIR_NAME
    date_prefix = (info_data["date"] or "no-date")[:10]
    file_slug = f"{slug(info_data['title'])}-{info_data['uid']}"
    filename = f"{date_prefix}-{file_slug}.md"
    filepath = out_dir / filename
    
    frontmatter = f"""---
type: pronote-information
project: DSCG
source_profile: {profile['profileName']}
uid: {info_data['uid']}
---"""

    body = f"# {info_data['title']}\n\nAuteur : {info_data['author']} ({info_data['date']})\n\n{info_data['content']}\n\n"
    
    if info_data.get("attachments"):
        body += "## Pièces jointes\n"
        for att in info_data["attachments"]:
            body += attachment_note_line(att, attachment_dir)
            
    filepath.write_text(f"{frontmatter}\n\n{body}", encoding="utf-8")
    return filepath

def _download_attachments(client, attachments, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for att in attachments:
        if int(att.get("type", 1)) == 0:
            results.append({"status": "skipped", "reason": "external-link", "name": att.get("name", "")})
            continue

        try:
            a = pronotepy.dataClasses.Attachment(client, get_attachment_payload(att))
            out_path = out_dir / (att.get("file_name") or safe_filename(a.name))
            a.save(str(out_path))
            results.append({"status": "saved", "name": a.name, "file": str(out_path)})
        except Exception as e:
            results.append({"status": "error", "name": att.get("name", ""), "error": str(e)})
            log_event(f"Error downloading attachment {att.get('name', '')}: {e}")
    return results


def add_download_results(summary: dict, results: list):
    for result in results:
        status = result.get("status")
        if status == "saved":
            summary["downloads"]["saved"] += 1
        elif status == "skipped":
            summary["downloads"]["skipped"] += 1
        else:
            summary["downloads"]["errors"] += 1


# --- Commands ---

def cmd_status(args):
    config = load_config()
    profiles = config.get("profiles", {})
    if not profiles:
        print("Aucun profil Pronote configuré.")
        return
    print("Profiles Pronote configurés:")
    for name, p in profiles.items():
        print(f"- {name}")
        print(f"  username: {p.get('username')}")
        print(f"  url: {p.get('url')}")
        print(f"  cas: {p.get('cas', 'none')}")
        print(f"  output: {p.get('outputDir', str(DEFAULT_VAULT_DIR))}")


def cmd_test(args):
    profile = get_profile(args.profile)
    client = connect(profile)

    today = datetime.date.today()
    lessons = client.lessons(today, today + datetime.timedelta(days=7))

    msg = {
        "status": "ok",
        "profile": args.profile,
        "generated_at": to_local_iso(datetime.datetime.now()),
        "name": client.info.name,
        "class": client.info.class_name,
        "school": client.info.establishment,
        "timetable_count": len(lessons),
        "sample_lesson": format_lesson(lessons[0]) if lessons else None,
    }

    if args.json:
        print(json.dumps(msg, indent=2, ensure_ascii=False))
    else:
        print(f"✅ Connexion OK — {client.info.name} ({client.info.class_name})")
        print(f"   École : {client.info.establishment}")
        print(f"   Cours cette semaine : {len(lessons)}")

    log_event(f"test-success: {args.profile}")


def cmd_query(args):
    profile = get_profile(args.profile)
    client = connect(profile)

    today = datetime.date.today()
    end_date = today + datetime.timedelta(weeks=args.weeks)
    start_date = datetime.date.fromisoformat(args.start_from) if args.start_from else today

    timetable = []
    homeworks = []
    discussions = []
    informations = []
    raw_discussions_count = 0
    raw_informations_count = 0

    if args.mode in ("timetable", "full"):
        lessons = client.lessons(start_date, end_date)
        timetable = [format_lesson(l) for l in lessons]

    if args.mode in ("homework", "full"):
        hw = client.homework(start_date, end_date)
        homeworks = [format_homework(h) for h in hw]

    if args.mode in ("communications", "full"):
        discs = client.discussions()
        infos = client.information_and_surveys()
        raw_discussions_count = len(discs)
        raw_informations_count = len(infos)
        discussions = filter_communications([format_discussion(d) for d in discs], args)
        informations = filter_communications([format_information(i) for i in infos], args)

    payload = {
        "generated_at": to_local_iso(datetime.datetime.now()),
        "profile": {
            "name": profile["profileName"],
            "username": profile["username"],
            "url": profile["url"],
        },
        "mode": args.mode,
        "weeks": args.weeks,
        "start_from": start_date.isoformat(),
        "filters": {
            "limit": args.limit,
            "since_days": args.since_days,
            "unread_only": args.unread_only,
            "actionable_only": args.actionable_only,
            "with_attachments_only": args.with_attachments_only,
        },
        "raw_counts": {
            "discussions": raw_discussions_count,
            "informations": raw_informations_count,
        },
        "counts": {
            "timetable": len(timetable),
            "homeworks": len(homeworks),
            "discussions": len(discussions),
            "informations": len(informations),
        },
        "timetable": timetable,
        "homeworks": homeworks,
        "discussions": discussions,
        "informations": informations,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Connexion OK — mode {args.mode}")
        print(f"Timetable : {len(timetable)} événements")
        print(f"Devoirs : {len(homeworks)}")
        print(f"Discussions : {len(discussions)}")
        print(f"Informations : {len(informations)}")

    log_event(f"query-{args.mode}: {args.profile}")


def cmd_sync(args):
    if not args.allow_sync:
        fail("sync is disabled for now. Use `pronote query ... --json` for on-demand consultation. Re-run with --allow-sync only for an explicit manual vault write.")

    profile = get_profile(args.profile)
    client = connect(profile)

    today = datetime.date.today()
    end_date = today + datetime.timedelta(weeks=args.weeks)
    start_date = datetime.date.fromisoformat(args.start_from) if args.start_from else today

    timetable = []
    homeworks = []
    discussions = []
    informations = []

    if args.mode in ("timetable", "full"):
        lessons = client.lessons(start_date, end_date)
        timetable = [format_lesson(l) for l in lessons]

    if args.mode in ("homework", "full"):
        hw = client.homework(start_date, end_date)
        homeworks = [format_homework(h) for h in hw]

    if args.mode in ("communications", "full"):
        discs = client.discussions()
        infos = client.information_and_surveys()
        discussions = filter_communications([format_discussion(d) for d in discs], args)
        informations = filter_communications([format_information(i) for i in infos], args)

    summary = {
        "mode": args.mode,
        "weeks": args.weeks,
        "write_notes": args.write_notes,
        "counts": {
            "timetable": len(timetable),
            "homework": len(homeworks),
            "discussions": len(discussions),
            "informations": len(informations)
        },
        "writes": {"timetable": 0, "homework": 0, "discussions": 0, "informations": 0},
        "downloads": {"saved": 0, "skipped": 0, "errors": 0},
    }

    if args.write_notes:
        output_dir = Path(profile.get("outputDir", str(DEFAULT_VAULT_DIR)))
        output_dir.mkdir(parents=True, exist_ok=True)
        homework_dir = output_dir / HOMEWORK_DIR_NAME
        homework_dir.mkdir(parents=True, exist_ok=True)
        comm_dir = output_dir / COMMUNICATIONS_DIR_NAME
        attach_dir = output_dir / ATTACHMENTS_DIR_NAME

        for lesson_data in timetable:
            write_lesson_note(lesson_data, profile, output_dir)
            summary["writes"]["timetable"] += 1

        for hw_data in homeworks:
            write_homework_note(hw_data, profile, homework_dir, attach_dir)
            if hw_data.get("attachments"):
                add_download_results(summary, _download_attachments(client, hw_data["attachments"], attach_dir))
            summary["writes"]["homework"] += 1

        if args.mode in ("communications", "full"):
            comm_dir.mkdir(parents=True, exist_ok=True)
            for disc in discussions:
                write_discussion_note(disc, profile, comm_dir)
                summary["writes"]["discussions"] += 1
            for info in informations:
                write_information_note(info, profile, comm_dir, attach_dir)
                if info.get("attachments"):
                    add_download_results(summary, _download_attachments(client, info["attachments"], attach_dir))
                summary["writes"]["informations"] += 1

        if not args.json:
            print(f"Timetable: {summary['writes']['timetable']} notes -> {output_dir}")
            print(f"Homework: {summary['writes']['homework']} notes -> {homework_dir}")
            print(f"Communications: {summary['writes']['discussions'] + summary['writes']['informations']} notes -> {comm_dir}")
            print(f"Attachments: {summary['downloads']['saved']} saved, {summary['downloads']['skipped']} skipped, {summary['downloads']['errors']} errors -> {attach_dir}")

    if args.json:
        summary["timetable"] = timetable
        summary["homeworks"] = homeworks
        summary["discussions"] = discussions
        summary["informations"] = informations
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"Sync terminé ({args.mode})")

    log_event(f"sync-{args.mode}: {args.profile}")


def cmd_download(args):
    profile = get_profile(args.profile)
    client = connect(profile)
    
    attachment_arg = json.loads(args.attachment)
    if isinstance(attachment_arg, str):
        attachment_arg = json.loads(attachment_arg)
    payload_dict = get_attachment_payload(attachment_arg)
    att = pronotepy.dataClasses.Attachment(client, payload_dict)
    
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / safe_filename(att.name)
    
    try:
        if att.type == 0:
            raise ValueError(f"Attachment is an external link, not a downloadable file: {att.url}")
        att.save(str(out_path))
        if args.json:
            print(json.dumps({"status": "success", "file": str(out_path)}, ensure_ascii=False))
        else:
            print(f"✅ Téléchargé : {out_path}")
    except Exception as e:
        if args.json:
            print(json.dumps({"status": "error", "error": str(e)}))
        else:
            fail(f"Erreur lors du téléchargement de {att.name}: {e}")

# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Pronote connector for OpenClaw (pronotepy backend)")
    sub = parser.add_subparsers(dest="command")

    # status
    sub.add_parser("status", help="Show configured profiles")

    # test
    p_test = sub.add_parser("test", help="Test connection")
    p_test.add_argument("--profile", default="default")
    p_test.add_argument("--json", action="store_true")

    # query
    p_query = sub.add_parser("query", help="Fetch data as context (no file writes)")
    p_query.add_argument("--profile", default="default")
    p_query.add_argument("--weeks", type=int, default=4)
    p_query.add_argument("--mode", choices=["timetable", "homework", "communications", "full"], default="timetable")
    p_query.add_argument("--from", dest="start_from", default=None, help="Start date YYYY-MM-DD")
    p_query.add_argument("--limit", type=int, default=10, help="Limit communications per type. Use 0 for no limit.")
    p_query.add_argument("--since-days", type=int, default=None, help="Only keep communications newer than N days")
    p_query.add_argument("--unread-only", action="store_true", help="Only keep unread communications")
    p_query.add_argument("--actionable-only", action="store_true", help="Only keep communications that look actionable")
    p_query.add_argument("--with-attachments-only", action="store_true", help="Only keep communications with attachments")
    p_query.add_argument("--json", action="store_true")

    # sync
    p_sync = sub.add_parser("sync", help="Fetch and optionally write Obsidian notes")
    p_sync.add_argument("--profile", default="default")
    p_sync.add_argument("--weeks", type=int, default=4)
    p_sync.add_argument("--mode", choices=["timetable", "homework", "communications", "full"], default="timetable")
    p_sync.add_argument("--from", dest="start_from", default=None, help="Start date YYYY-MM-DD")
    p_sync.add_argument("--limit", type=int, default=10, help="Limit communications per type. Use 0 for no limit.")
    p_sync.add_argument("--since-days", type=int, default=None, help="Only keep communications newer than N days")
    p_sync.add_argument("--unread-only", action="store_true", help="Only keep unread communications")
    p_sync.add_argument("--actionable-only", action="store_true", help="Only keep communications that look actionable")
    p_sync.add_argument("--with-attachments-only", action="store_true", help="Only keep communications with attachments")
    p_sync.add_argument("--allow-sync", action="store_true", help="Explicitly allow vault writes; disabled by default")
    p_sync.add_argument("--write-notes", action="store_true")
    p_sync.add_argument("--json", action="store_true")

    # download
    p_dl = sub.add_parser("download", help="Download an attachment from a JSON payload")
    p_dl.add_argument("--profile", default="default")
    p_dl.add_argument("--attachment", required=True, help="JSON payload of the attachment")
    p_dl.add_argument("--output-dir", required=True, help="Directory to save the file")
    p_dl.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "status": cmd_status,
        "test": cmd_test,
        "query": cmd_query,
        "sync": cmd_sync,
        "download": cmd_download,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        fail(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
