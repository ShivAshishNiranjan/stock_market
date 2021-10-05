import datetime

import requests

from bse.common_helper import get_current_script_price

start_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')
end_date = "20211231"

corporate_actions = [
    {"name": "Bonus", "code": "P5"},
    {"name": "Buyback", "code": "P6"},
    {"name": "Split", "code": "P26"},
    {"name": "Dividend", "code": "P9"}
]

bonus = []
buyback = []
dividend = []
split = []

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

        if "Dividend" in corporate_action["name"]:
            if len(result["Purpose"].split('-')) >= 2:
                dividend = float(result["Purpose"].split('-')[2].strip())
                if get_current_script_price(result["scrip_code"]) != '':
                    dividend_yield = 100 * dividend / float(
                        get_current_script_price(result["scrip_code"]))
                    if dividend_yield > 2.5:
                        print("---------------------------------------------------------------------------------")
                        print(
                            "Opportunity in {} \n dividend_yield {:.2f} \n dividend {} \n Price {} \n Ex-Date: {}".format(
                                result["long_name"],
                                dividend_yield,
                                dividend,
                                get_current_script_price(
                                    result[
                                        "scrip_code"]),
                                result["Ex_date"]

                            ))
                        print("---------------------------------------------------------------------------------")


        else:
            print(
                "Script Name: {} \n Script Price: {} \n Corporate Action: {} \n Ex-Date: {}".format(result["long_name"],
                                                                                                    get_current_script_price(
                                                                                                        result[
                                                                                                            "scrip_code"]),
                                                                                                    result["Purpose"],
                                                                                                    result["Ex_date"]))

            print("---------------------------------------------------------------------------------")
