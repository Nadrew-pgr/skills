import sys
import pronotepy
import json
import datetime
from pathlib import Path

# Need to import our connect logic
sys.path.append("/root/.openclaw/workspace/skills/pronote-connector/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pronote", "/root/.openclaw/workspace/skills/pronote-connector/scripts/pronote-connector-pronotepy.py")
pronote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pronote)

profile = pronote.get_profile("default")
client = pronote.connect(profile)

today = datetime.date.today()
hw = client.homework(today - datetime.timedelta(days=14), today + datetime.timedelta(days=14))

found = False
for h in hw:
    if h.files:
        print(f"Found homework with {len(h.files)} files: {h.subject.name}")
        for f in h.files:
            print(f"File: {f.name}, URL: {f.url}")
            print(f"Dict: {f._data if hasattr(f, '_data') else 'No _data'}")
            # Try to recreate and download
            try:
                att = pronotepy.dataClasses.Attachment(client, f._data)
                print(f"Recreated: {att.name}")
            except Exception as e:
                print(f"Recreate failed: {e}")
        found = True
        break

if not found:
    print("No attachments found in recent homework.")

# Also check information and discussions
infos = client.information_and_surveys()
for i in infos:
    if i.attachments:
        print(f"Found info with {len(i.attachments)} attachments")
        for f in i.attachments:
            print(f"File: {f.name}, url: {f.url}")
        break

