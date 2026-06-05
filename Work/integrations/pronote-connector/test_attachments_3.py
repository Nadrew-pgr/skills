import sys
import pronotepy
import json

sys.path.append("/root/.openclaw/workspace/skills/pronote-connector/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pronote", "/root/.openclaw/workspace/skills/pronote-connector/scripts/pronote-connector-pronotepy.py")
pronote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pronote)

profile = pronote.get_profile("default")
client = pronote.connect(profile)

infos = client.information_and_surveys()
for i in infos:
    if i.attachments:
        for f in i.attachments:
            if f.type == 1:
                # Reconstruct
                reconstructed = {"N": f.id, "L": f.name, "G": f.type}
                att = pronotepy.dataClasses.Attachment(client, reconstructed)
                print(f"Original URL: {f.url}")
                print(f"Recon URL:    {att.url}")
        break
