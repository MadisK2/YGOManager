import requests
import json


def downloadallcardsjson():
    # api-endpoint
    URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

    # sending get request and saving the response as response object
    r = requests.get(url = URL)

    # extracting data in json format
    data = r.json()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__=='__main__':
    downloadallcardsjson()