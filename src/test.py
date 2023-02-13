from bs4 import BeautifulSoup
import requests

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
print("--------------------------------------------------------------------------------------------------------------")
print(" Buyback {}".format(buyback))
print("--------------------------------------------------------------------------------------------------------------")
print(" Bonus {}".format(bonus))
print("--------------------------------------------------------------------------------------------------------------")
print(" Split {}".format(split))
print("--------------------------------------------------------------------------------------------------------------")
