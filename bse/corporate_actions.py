import requests
from bse.common_helper import get_current_script_price
from bs4 import BeautifulSoup


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
        print(" Status Code {}".format(response.status_code))
        results = response.json()
        if response.status_code != 500:
            for result in results:
                print(" result {}".format(result))
                result["price"] = get_current_script_price(result["scrip_code"])

                if "Dividend" in corporate_action["name"]:
                    if len(result["Purpose"].split('-')) >= 2:
                        dividend = float(result["Purpose"].split('-')[2].strip())
                        if get_current_script_price(result["scrip_code"]) != '':
                            dividend_yield = 100 * dividend / float(
                                get_current_script_price(result["scrip_code"]))
                            if dividend_yield > 2:
                                result['dy'] = dividend_yield
                                dividend_list.append([result])

                if "Bonus" in corporate_action["name"]:
                    bonus.append([result])

                if "Buyback" in corporate_action["name"]:
                    buyback.append([result])

                if "Split" in corporate_action["name"]:
                    split.append([result])
        else:
            print("Status Code {}".format(response.status_code))

    print("Dividend {}".format(dividend_list))
    sorted_dividend_list = sorted(dividend_list, key=lambda x: x[0]['dy'])
    print("sorted_dividend_list {}".format(sorted_dividend_list))
    print(" Buyback {}".format(buyback))
    print(" Bonus {}".format(bonus))
    print(" Split {}".format(split))
    result = {"dividend": sorted_dividend_list, "bonus": bonus, "split": split, "buyback": buyback}
    return result


def get_upcoming_board_meetings():
    url = "https://www.moneycontrol.com/stocks/marketinfo/meetings.php?opttopic=brdmeeting"

    payload = {}
    headers = {
        'authority': 'www.moneycontrol.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    page_content = BeautifulSoup(response.content, "html.parser")

    input = page_content.find("input", value="brdmeeting")
    allCP = input.find("table").find_all("tr")
    bonus = []
    buyback = []
    dividend_list = []
    split = []

    for cp in allCP[1:]:
        if "dividend" in cp.find_all("td")[-1].text.lower():
            # print(cp.find("td").find("b").text)
            # print(cp.find_all("td")[-2].text)
            dividend_list.append([cp.find("td").find("b").text, cp.find_all("td")[-2].text])

        if "bonus" in cp.find_all("td")[-1].text.lower():
            # print(cp.find("td").find("b").text)
            # print(cp.find_all("td")[-2].text)
            bonus.append([cp.find("td").find("b").text, cp.find_all("td")[-2].text])

        if "buy back" in cp.find_all("td")[-1].text.lower():
            # print(cp.find("td").find("b").text)
            # print(cp.find_all("td")[-2].text)
            buyback.append([cp.find("td").find("b").text, cp.find_all("td")[-2].text])

        if "split" in cp.find_all("td")[-1].text.lower():
            # print(cp.find("td").find("b").text)
            # print(cp.find_all("td")[-2].text)
            split.append([cp.find("td").find("b").text, cp.find_all("td")[-2].text])

    print(" Dividend {}".format(dividend_list))
    print(
        "-------------------------------------------------------------------------------------------------------------")
    print(" Buyback {}".format(buyback))
    print(
        "-------------------------------------------------------------------------------------------------------------")
    print(" Bonus {}".format(bonus))
    print(
        "-------------------------------------------------------------------------------------------------------------")
    print(" Split {}".format(split))
    print(
        "-------------------------------------------------------------------------------------------------------------")
    result = {"dividend": dividend_list, "bonus": bonus, "split": split, "buyback": buyback}
    return result
