import sys
import pronotepy

sys.path.append("/root/.openclaw/workspace/skills/pronote-connector/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pronote", "/root/.openclaw/workspace/skills/pronote-connector/scripts/pronote-connector-pronotepy.py")
pronote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pronote)

profile = pronote.get_profile("default")
client = pronote.connect(profile)

discussions = client.discussions()
print(f"Got {len(discussions)} discussions.")
for d in discussions[:2]:
    print(f"Discussion: {d.subject}")
    print(f"Creator: {d.creator}")
    print(f"Messages: {len(d.messages)}")
    for m in d.messages:
        print(f" - [{m.date}] {m.author}: {m.content[:50]}...")

infos = client.information_and_surveys()
print(f"\nGot {len(infos)} infos.")
for i in infos[:2]:
    print(f"Info: {i.title}")
    print(f"Author: {i.author}")
    print(f"Content: {i.content[:50]}...")
    print(f"Attachments: {len(i.attachments)}")

