import csv

import requests
from bs4 import BeautifulSoup
import json

emoji_class = 'Link_link-wrapper__C33u_ Emoji_emoji__6sYSR __variable_c30de8 EmojisList_emojis-list-item__MGP6t'
# URL de la página que contiene la lista de emojis
urls = {'https://emojipedia.org/es/smileys#list', 'https://emojipedia.org/es/personas#list', 'https://emojipedia.org/es/search?q=corazón'}

emoji_izenak = []

for url in urls:
    metodoa = "GET"
    goiburuak = goiburuak = {'Host': 'emojipedia.org'}
    erantzuna = requests.request(metodoa, url, headers=goiburuak, allow_redirects=False)

    html = erantzuna.content
    soup = BeautifulSoup(html, 'html.parser')

    script_tag = soup.find('script', id='__NEXT_DATA__')

    if script_tag:
        # Parse JSON content
        json_data = json.loads(script_tag.string)

        kategoriak = json_data['props']['pageProps']['dehydratedState']['queries']
        print(url)

        if url == 'https://emojipedia.org/es/search?q=corazón':
            kategoriak = json_data['props']['pageProps']['dehydratedState']['queries'][3]['state']['data']
            for i in kategoriak:
                izena = str(i['title']).lower()
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
                    print ('nop')


with open('emoji.txt', 'w', newline='', encoding='utf-8') as outfile:
    escritor = csv.writer(outfile)
    for emoji_name in emoji_izenak:
        if emoji_name != 'cara sonriendo':
            escritor.writerow([emoji_name])

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
                # Para cada celda, revisa cada emoji en el conjunto
                modified_cell = cell
                for emoji in emoji_set:
                    # Crear una expresión regular para encontrar la coincidencia exacta de la palabra/frase
                    # Esto evita reemplazos parciales en palabras que contienen las frases buscadas
                    regex_pattern = r'\b' + re.escape(emoji) + r'\b'
                    # Reemplaza la frase encontrada con su versión con guiones bajos
                    modified_cell = re.sub(regex_pattern, emoji.replace(' ', '_'), modified_cell)
                new_row.append(modified_cell)
            writer.writerow(new_row)

# Asume que las funciones read_emoji_file y las rutas de archivo están definidas como antes
modify_csv_with_phrases('Datuak/train.csv', emoji_izenak, 'Datuak/train_modified1.csv')
modify_csv_with_phrases('Datuak/train_modified1.csv', ['cara sonriendo'], 'Datuak/train_modified2.csv')
print(
    "El archivo CSV ha sido modificado para reemplazar frases que coinciden con 'emoji.txt', y guardado como 'test_modified.csv'.")
