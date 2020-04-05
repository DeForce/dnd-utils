import json
from typing import Dict

from classes import MagicItem

with open('items.json', 'r') as item_file:
    items = json.loads(item_file.read())

item_dict: Dict[str, MagicItem] = {}
for item_name, item_data in items.items():
    item_dict[item_name] = MagicItem(**item_data)

# Filter by Type
with open('items_by_type.yaml', 'w') as type_file:
    types = set(item.type for item in item_dict.values())
pass
