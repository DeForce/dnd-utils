import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import concurrent.futures
import json
import codecs
import browser_cookie3
import functools

from classes import MagicItem

BEYOND_URL = 'https://www.dndbeyond.com/magic-items'


async def speedcrawl(a_pages):
    data = []
    for l_page in range(1, a_pages + 1):
        data.append({'page': l_page})

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(a_pages, 100)) as executor:
        async_loop = asyncio.get_event_loop()
        futures = [
            async_loop.run_in_executor(
                executor,
                functools.partial(
                    requests.get,
                    BEYOND_URL,
                    d_page,
                    cookies=cj
                )
            )
            for d_page in data
        ]
        for response in await asyncio.gather(*futures):
            pass
    return [f.result() for f in futures]


# Beyond hates automation at the moment, and there is no API available yet, so you need to be careful.
# They may block your account
cj = browser_cookie3.chrome(domain_name='www.dndbeyond.com')

ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}
url = BEYOND_URL
htmlContent = requests.get(url, headers=header, cookies=cj)
soup = BeautifulSoup(htmlContent.text, "html.parser")

uldiv = soup.find_all("a", class_="b-pagination-item")
pages = int(uldiv[-1].text)

# pages = 1

print('{} pages found.'.format(pages))

loop = asyncio.get_event_loop()
result = loop.run_until_complete(speedcrawl(pages))

item_dict = {
    'wondrousitem': 'https://media-waterdeep.cursecdn.com/attachments/2/665/wondrousitem.jpg',
    'armor': 'https://media-waterdeep.cursecdn.com/attachments/2/666/armor.jpg',
    'potion': 'https://media-waterdeep.cursecdn.com/attachments/2/667/potion.jpg',
    'ring': 'https://media-waterdeep.cursecdn.com/attachments/2/668/ring.jpg',
    'rod': 'https://media-waterdeep.cursecdn.com/attachments/2/669/rod.jpg',
    'scroll': 'https://media-waterdeep.cursecdn.com/attachments/2/661/scroll.jpg',
    'staff': 'https://media-waterdeep.cursecdn.com/attachments/2/662/staff.jpg',
    'wand': 'https://media-waterdeep.cursecdn.com/attachments/2/663/wand.jpg',
    'weapon': 'https://media-waterdeep.cursecdn.com/attachments/2/664/weapon.jpg',
}


magic_items = {}
for page in result:
    soup = BeautifulSoup(page.text, "html.parser")
    infos = soup.find_all('div', class_='info')
    # css_links = [link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]

    for info in infos:
        m_item = MagicItem()

        divs = info.find_all('div')
        for d in divs:
            c = d.get('class')
            if 'item-icon' in c:
                a = d.find('a')
                if a is None:
                    creature_type = d.find('div').get('class')[1]
                    img_url = item_dict[creature_type]
                else:
                    img_url = a.get('href')
                m_item.image = img_url
            elif 'item-name' in c:
                name = d.find('span').find('span').text
                m_item.name = name

                rarity = d.find('span').find('span').get('class')[0]
                m_item.rarity = rarity
            elif 'requires-attunement' in c:
                attunement = d.find('span').text.strip()
                if len(attunement) == 2:
                    m_item.attunement = False
                else:
                    m_item.attunement = True
            elif 'notes' in c:
                notes = d.find('span').text.strip()
                m_item.notes = notes
            elif 'item-type' in c:
                type_list = d.find_all('span')
                m_item.type = type_list[0].text.strip()
                m_item.subtype = type_list[1].text.strip()

        magic_items[m_item.name] = {
            'image': m_item.image,
            'type': m_item.type,
            'sub_type': m_item.subtype,
            'name': m_item.name,
            'attunement': m_item.attunement,
            'rarity': m_item.rarity,
            'notes': m_item.notes
        }

with open('items.json', 'wb') as f:
    json.dump(magic_items, codecs.getwriter('utf-8')(f), ensure_ascii=False, indent=4, sort_keys=True)
