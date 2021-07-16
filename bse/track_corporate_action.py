import requests

start_date = "20210716"
end_date = "20210716"
corporate_actions = ["Board+Meeting", "Corp.+Action", "AGM/EGM"]
dividend = []
bonus = []
split = []
buyback = []


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


def format_corporate_action(data):
    data_to_read = ''
    if data["News_submission_dt"]:
        data_to_read += data["News_submission_dt"].split("T")[0] + "-->" + data["NEWSSUB"]
    else:
        data_to_read += data["DissemDT"].split("T")[0] + "-->" + data["NEWSSUB"]

    data_to_read += ("\n Stock Price: " + get_current_script_price(data["SCRIP_CD"]))

    if data["ATTACHMENTNAME"]:
        data_to_read += ("\n" + "https://www.bseindia.com/xml-data/corpfiling/AttachLive/" + data["ATTACHMENTNAME"])

    data_to_read += "\n##########################################################################################################################################################################\n"

    return data_to_read


for corporate_action in corporate_actions:
    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w" \
          "?strCat={}" \
          "&strPrevDate={}" \
          "&strScrip=" \
          "&strSearch=P" \
          "&strToDate={}" \
          "&strType=C" \
        .format(corporate_action, start_date, end_date)

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

print("----------------------- DIVIDEND -------------------------------")

print("\n".join(dividend))

print("----------------------- DIVIDEND -------------------------------")

print("----------------------- BONUS -------------------------------")

print("\n".join(bonus))
print("----------------------- BONUS -------------------------------")

print("----------------------- SPLIT -------------------------------")

print("\n".join(split))
print("----------------------- SPLIT -------------------------------")

print("----------------------- BUYBACK -------------------------------")

print("\n".join(buyback))

print("----------------------- BUYBACK -------------------------------")
