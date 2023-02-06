import os
import json
import sys

triplifier_location = os.getenv("TRIPLIFIER_LOCATION")

config = None
with open("/app/config.json") as f:
    config = json.load(f)

if config is None:
    print("No config file found at /app/config.json")
    sys.exit(1)

if triplifier_location:
    config["triplifier_service"] = triplifier_location

with open("/app/config.json", "w") as f:
    json.dump(config, f)