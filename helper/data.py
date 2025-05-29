import pandas as pd
import requests, re, os
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

def download_data(url):
    herose_pattern = '.*Zaehlstelle_Heros(e|é)_[0-9]{4}_(stuendlich|taeglich)_Wetter.*.csv'

    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True) if
             a["href"].lower().endswith(".csv")]

    for link in links:
        path = f"./data/{unquote(link.rsplit("/", 1)[-1])}"

        if re.match(herose_pattern, path) and not os.path.exists(path.replace('é', 'e')):
            path = path.replace('é', 'e')

            try:
                csv_data = requests.get(link)
                print(f'Downloading to {path}')
            except requests.RequestException as e:
                print(f"failed to fetch {url}: {e}")
                continue

            with open(path, 'wb') as file:
                file.write(csv_data.content)
        else:
            print(f'{path} alread downliaded.')

def get_daily(file):
    all_data_daily = pd.read_csv(file, sep=';', engine='python')

    all_data_daily.columns = all_data_daily.columns.str.replace(r' \([^)]*\)', '', regex=True)

    all_data_daily = all_data_daily.rename(columns={
        'Fahrradbruecke': 'anzahl',
        'Fahrradbruecke stadteinwaerts Fahrraeder': 'anzahl_stadteinwaerts',
        'Fahrradbruecke stadtauswaerts Fahrraeder': 'anzahl_stadtauswaerts'
    })

    all_data_daily[['date', 'time']] = all_data_daily['Zeit'].str.split(' ', expand=True)
    all_data_daily.drop('Quelle', axis=1, inplace=True)
    all_data_daily.drop('Zeit', axis=1, inplace=True)
    all_data_daily.drop('time', axis=1, inplace=True)
    all_data_daily.drop('Symbol Wetter', axis=1, inplace=True)

    return all_data_daily
