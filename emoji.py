import csv
import sys

import requests
from bs4 import BeautifulSoup
import json

csvPath = sys.argv[0]
outputPath1 = sys.argv[1]
outputPath2 = sys.argv[2]

# Beharrezkoak diren emojiak dituzten url-en lista
urls = {'https://emojipedia.org/es/smileys#list', 'https://emojipedia.org/es/personas#list', 'https://emojipedia.org/es/search?q=corazón'}

emoji_izenak = []

for url in urls: # URL bakoitzeko Web Scraping bat egin emoji lista lortzeko
    metodoa = "GET"
    goiburuak = goiburuak = {'Host': 'emojipedia.org'}
    erantzuna = requests.request(metodoa, url, headers=goiburuak, allow_redirects=False)

    html = erantzuna.content
    soup = BeautifulSoup(html, 'html.parser')

    script_tag = soup.find('script', id='__NEXT_DATA__')

    if script_tag:
        # DAtuak dituen JSON-etik datuak erauzi
        json_data = json.loads(script_tag.string)

        kategoriak = json_data['props']['pageProps']['dehydratedState']['queries']
        print(url)

        if url == 'https://emojipedia.org/es/search?q=corazón': # URL hau kasu berezi bat denez era ezberdin batean egingo da
            kategoriak = json_data['props']['pageProps']['dehydratedState']['queries'][3]['state']['data']
            for emoji in kategoriak:
                izena = str(emoji['title']).lower()
                emoji_izenak.append(izena)
        else:
            for idx in range(len(kategoriak)):
                try:
                    kategoriak = json_data['props']['pageProps']['dehydratedState']['queries'][idx]['state']['data']['subCategories']
                    for kategoria in kategoriak:
                        for emoji in kategoria['emoji']:
                            izena = str(emoji['title']).lower()
                            if izena != 'cara sonriendo':
                                emoji_izenak.append(izena)
                    pass
                except Exception as e:
                    pass


# Gorde emojien lista emoji.txt artxiboan
with open('emoji.txt', 'w', newline='', encoding='utf-8') as outfile:
    escritor = csv.writer(outfile)
    for emoji_name in emoji_izenak:
        if emoji_name != 'cara sonriendo':
            escritor.writerow([emoji_name])

# csv-artxiboa aldatuko duen metodoa emojiak gu nahi dugun eran agertzeko adb.: 'cara_sonriendo'
def modify_csv_with_phrases(csv_path, emoji_set, output_path):
    import csv
    import re

    with open(csv_path, 'r', encoding='utf-8') as infile, \
            open(output_path, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            new_row = []
            for cell in row:
                modified_cell = cell
                for emoji in emoji_set:
                    # Expresio erregular bat sortu emojiak lortzeko
                    regex_pattern = r'\b' + re.escape(emoji) + r'\b'
                    # Aurkitutako esaldia ordezten du, bere bertsioarekin, gidoi baxuekin
                    modified_cell = re.sub(regex_pattern, emoji.replace(' ', '_'), modified_cell)
                new_row.append(modified_cell)
            writer.writerow(new_row)

# Modifikazioak egin
modify_csv_with_phrases(csvPath, emoji_izenak, outputPath1)
# Cara Sonriendo kasu berezia da beraz beste batean procesatuko dugu
modify_csv_with_phrases(outputPath1, ['cara sonriendo'], outputPath2)
print(
    "El archivo CSV ha sido modificado para reemplazar frases que coinciden con 'emoji.txt', y guardado como 'test_modified.csv'.")
