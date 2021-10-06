import requests
from bse.common_helper import get_current_script_price


def get_corporate_actions(start_date, end_date):
    bonus = []
    buyback = []
    dividend_list = []
    split = []

    corporate_actions = [
        {"name": "Bonus", "code": "P5"},
        {"name": "Buyback", "code": "P6"},
        {"name": "Split", "code": "P26"},
        {"name": "Dividend", "code": "P9"}
    ]

    for corporate_action in corporate_actions:
        url = "https://api.bseindia.com/BseIndiaAPI/api/DefaultData/w?" \
              "Fdate={}" \
              "&Purposecode={}" \
              "&TDate={}" \
              "&ddlcategorys=E" \
              "&ddlindustrys=" \
              "&scripcode=" \
              "&segment=0" \
              "&strSearch=S".format(start_date, corporate_action["code"], end_date)

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
            'accept-language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        results = response.json()
        for result in results:
            result["price"] = get_current_script_price(result["scrip_code"])
            if "Dividend" in corporate_action["name"]:
                if len(result["Purpose"].split('-')) >= 2:
                    dividend = float(result["Purpose"].split('-')[2].strip())
                    if get_current_script_price(result["scrip_code"]) != '':
                        dividend_yield = 100 * dividend / float(
                            get_current_script_price(result["scrip_code"]))
                        if dividend_yield > 2.5:
                            result['dy'] = dividend_yield
                            dividend_list.append([result])

            if "Bonus" in corporate_action["name"]:
                bonus.append([result])

            if "Buyback" in corporate_action["name"]:
                buyback.append([result])

            if "Split" in corporate_action["name"]:
                split.append([result])

    print(" Dividend {}".format(dividend_list))
    print(" Buyback {}".format(buyback))
    print(" Bonus {}".format(bonus))
    print(" Split {}".format(split))
    result = {"dividend": dividend_list, "bonus": bonus, "split": split, "buyback": buyback}
    return result
