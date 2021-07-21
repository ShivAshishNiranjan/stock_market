import requests


def get_current_script_price(script_code):
    url = "https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?Debtflag=&scripcode={}&seriesid=".format(
        script_code)

    payload = {}
    headers = {
        'authority': 'api.bseindia.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'origin': 'https://www.bseindia.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bseindia.com/',
        'accept-language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
        'if-modified-since': 'Thu, 15 Jul 2021 13:26:52 GMT'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["CurrRate"]["LTP"]
