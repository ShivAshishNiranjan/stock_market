import requests
from datetime import datetime

from bse.common_helper import get_current_script_price

start_date = "20210721"
end_date = "20210721"


def format_corporate_action(data):
    processed_data = {"NEWSSUB": data["NEWSSUB"],
                      "News_submission_dt": data["News_submission_dt"],
                      "DissemDT": data["DissemDT"],
                      "Price": get_current_script_price(data["SCRIP_CD"]),
                      "ATTACHMENTNAME": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/" + data[
                          "ATTACHMENTNAME"]}

    return processed_data


def get_live_announcement(corporate_action, start_date, end_date):
    print("Start Date {}".format(start_date))
    print("End Date {}".format(end_date))
    dividend = []
    bonus = []
    split = []
    buyback = []
    base_url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w" \
               "?strCat={}" \
               "&strPrevDate={}" \
               "&strScrip=" \
               "&strSearch=P" \
               "&strToDate={}" \
               "&strType=C" \
        .format(corporate_action, start_date, end_date)

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

    response = requests.request("GET", base_url, headers=headers)

    table_data = response.json()["Table"]

    print("total announcement {}".format(len(table_data)))

    for data in table_data:
        if "dividend" in data["NEWSSUB"].lower():
            dividend.append(format_corporate_action(data))

        if "bonus" in data["NEWSSUB"].lower():
            bonus.append(format_corporate_action(data))

        if "split" in data["NEWSSUB"].lower():
            split.append(format_corporate_action(data))

        if "buyback" in data["NEWSSUB"].lower():
            buyback.append(format_corporate_action(data))

    print(" Dividend {}".format(dividend))
    print(" Buyback {}".format(buyback))
    print(" Bonus {}".format(bonus))
    print(" Split {}".format(split))
    result = {"dividend": dividend, "bonus": bonus, "split": split, "buyback": buyback}

    return result


if __name__ == "__main__":
    get_live_announcement("Corp.+Action", datetime.today().strftime('%Y%m%d'), datetime.today().strftime('%Y%m%d'))
