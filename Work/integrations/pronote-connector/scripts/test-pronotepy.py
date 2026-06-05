#!/usr/bin/env python3
"""Quick test script for pronotepy connection.
Gets the decrypted password from an env var set by the Node connector."""

import os
import sys
import json

try:
    import pronotepy
except ImportError:
    print("ERROR: pronotepy not installed. Run: pip install pronotepy")
    sys.exit(1)

PRONOTE_URL = "https://0332747g.index-education.net/pronote/eleve.html"
USERNAME = "APOUGARY"
PASSWORD = os.environ.get("PRONOTE_PASSWORD")

if not PASSWORD:
    print("ERROR: PRONOTE_PASSWORD env var not set")
    sys.exit(1)

print(f"pronotepy version: {pronotepy.__version__}")
print(f"URL: {PRONOTE_URL}")
print(f"Username: {USERNAME}")
print(f"Password length: {len(PASSWORD)}")
print()

# Try direct login (no CAS/ENT)
print("Attempting direct login (no CAS)...")
try:
    client = pronotepy.Client(
        PRONOTE_URL,
        username=USERNAME,
        password=PASSWORD
    )
    print(f"✅ SUCCESS - Connected as: {client.info.name}")
    print(f"   Class: {client.info.class_name}")
    print(f"   School: {client.info.establishment}")
    
    # Try getting timetable
    import datetime
    today = datetime.date.today()
    lessons = client.lessons(today, today + datetime.timedelta(days=14))
    print(f"   Lessons found (next 14 days): {len(lessons)}")
    
    if lessons:
        for lesson in lessons[:5]:
            status = "CANCELLED" if lesson.canceled else "OK"
            print(f"     - {lesson.start.strftime('%Y-%m-%d %H:%M')} {lesson.subject.name if lesson.subject else 'N/A'} ({status})")
    
    # Try getting homework
    homeworks = client.homework(today, today + datetime.timedelta(days=30))
    print(f"   Homework found (next 30 days): {len(homeworks)}")
    
    if homeworks:
        for hw in homeworks[:3]:
            print(f"     - Due {hw.date}: {hw.subject.name if hw.subject else 'N/A'} - {hw.description[:60]}...")
    
    print()
    print(json.dumps({
        "status": "ok",
        "name": client.info.name,
        "class": client.info.class_name,
        "lessons_count": len(lessons),
        "homework_count": len(homeworks)
    }, indent=2, ensure_ascii=False))

except pronotepy.ENTLoginError as e:
    print(f"❌ ENT Login Error: {e}")
    print("   This may require a CAS/ENT provider. Try with ent= parameter.")
except Exception as e:
    print(f"❌ Connection error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
