import json
import pandas as pd
import matplotlib.pyplot as plt

RARITY_PRIORITY = {
    'varies': 'black',
    'common': 'black',
    'uncommon': 'green',
    'rare': 'lightblue',
    'very-rare': 'purple',
    'legendary': 'orange',
    'artifact': 'darksalmon'
}

with open('items.json', 'r') as item_file:
    items = json.loads(item_file.read())

data = []
for item_name, item_data in items.items():
    data.append(item_data)

main_df = pd.DataFrame(data)
ordered_df = main_df[['name', 'rarity', 'type', 'sub_type', 'attunement', 'notes', 'image']]

# Count Items by Rarity
rarity_df = ordered_df.groupby('rarity', as_index=False)['name'].count()
rarity_df['rarity'] = pd.Categorical(rarity_df['rarity'], RARITY_PRIORITY.keys())
rarity_sorted_df = rarity_df.sort_values('rarity')

plot = rarity_sorted_df.plot(kind='bar', color=[RARITY_PRIORITY.values()], legend=False)
plot.set_xticklabels(RARITY_PRIORITY.keys())
plt.show()
pass
