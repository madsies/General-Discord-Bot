import json
from pathlib import Path

with open(Path(__file__).parent / "resources/data.json", "r", encoding="utf-8") as f:
    CONFIG_DATA = json.load(f)