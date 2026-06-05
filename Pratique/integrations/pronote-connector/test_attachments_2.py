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

infos = client.information_and_surveys()
for i in infos:
    if i.attachments:
        print(f"Found info with {len(i.attachments)} attachments")
        for f in i.attachments:
            print(f"File: {f.name}")
            try:
                # _data is the json dictionary representing the attachment in pronotepy
                # We can serialize it and deserialize it to pass it around
                json_str = json.dumps(f._data)
                
                # Assume agent passes json_str
                passed_dict = json.loads(json_str)
                att = pronotepy.dataClasses.Attachment(client, passed_dict)
                print(f"Recreated: {att.name}, id: {att.id}")
                
                # Try saving it to /tmp
                tmp_path = Path("/tmp") / att.name
                # att.save(str(tmp_path)) # Wait, is save() defined for all attachments?
                # print(f"Saved to {tmp_path}")
            except Exception as e:
                print(f"Failed: {e}")
        break
