import codecs
import json

with open('items.json', 'r') as item_file:
    json_data = json.loads(item_file.read())

clean_data = {}
if __name__ == '__main__':
    for name, item_data in json_data.items():
        notes = item_data['notes'].split(',')
        notes = [item.strip() for item in notes]

        item_data['notes'] = notes
        clean_data[name] = item_data

with open('items_clean.json', 'wb') as item_file:
    json.dump(clean_data, codecs.getwriter('utf-8')(item_file), ensure_ascii=False, indent=4, sort_keys=True)
