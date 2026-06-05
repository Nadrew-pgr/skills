#!/usr/bin/env python3
"""Test pronotepy with Bordeaux ENT variants."""

import os
import sys
import json

try:
    import pronotepy
    from pronotepy import ent
except ImportError:
    print("ERROR: pronotepy not installed")
    sys.exit(1)

PRONOTE_URL = "https://0332747g.index-education.net/pronote/eleve.html"
USERNAME = os.environ.get("PRONOTE_USERNAME", "APOUGARY")
PASSWORD = os.environ.get("PRONOTE_PASSWORD")

if not PASSWORD:
    print("ERROR: PRONOTE_PASSWORD env var not set")
    sys.exit(1)

# List of ENT functions to try for Bordeaux/Aquitaine
ent_candidates = [
    ("lyceeconnecte_edu", ent.lyceeconnecte_edu),
    ("lyceeconnecte_aquitaine", ent.lyceeconnecte_aquitaine),
    ("bordeaux", ent.bordeaux),
]

print(f"pronotepy version: {pronotepy.__version__}")
print(f"URL: {PRONOTE_URL}")
print(f"Username: {USERNAME}")
print(f"Password length: {len(PASSWORD)}")
print()

for ent_name, ent_func in ent_candidates:
    print(f"--- Trying ENT: {ent_name} ---")
    try:
        client = pronotepy.Client(
            PRONOTE_URL,
            username=USERNAME,
            password=PASSWORD,
            ent=ent_func
        )
        
        if client.logged_in:
            print(f"✅ SUCCESS with {ent_name}!")
            print(f"   Name: {client.info.name}")
            print(f"   Class: {client.info.class_name}")
            
            import datetime
            today = datetime.date.today()
            lessons = client.lessons(today, today + datetime.timedelta(days=14))
            print(f"   Lessons (next 14 days): {len(lessons)}")
            
            if lessons:
                for lesson in lessons[:5]:
                    status = "CANCELLED" if lesson.canceled else "OK"
                    subj = lesson.subject.name if lesson.subject else 'N/A'
                    print(f"     {lesson.start.strftime('%Y-%m-%d %H:%M')} | {subj} | {status}")
            
            homeworks = client.homework(today, today + datetime.timedelta(days=30))
            print(f"   Homework (next 30 days): {len(homeworks)}")
            
            print()
            print(json.dumps({
                "status": "ok",
                "ent": ent_name,
                "name": client.info.name,
                "class": client.info.class_name,
                "lessons_count": len(lessons),
                "homework_count": len(homeworks)
            }, indent=2, ensure_ascii=False))
            
            sys.exit(0)
        else:
            print(f"   ❌ logged_in=False with {ent_name}")
    except Exception as e:
        err_msg = str(e)
        # Keep it concise
        if len(err_msg) > 200:
            err_msg = err_msg[:200] + "..."
        print(f"   ❌ {type(e).__name__}: {err_msg}")
    print()

print("All ENT variants failed.")
sys.exit(1)
