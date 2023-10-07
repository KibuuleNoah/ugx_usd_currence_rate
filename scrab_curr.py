from bs4 import BeautifulSoup

import requests

r = requests.get(
    "https://www.exchangerates.org.uk/Dollars-to-Ugandan-Shilling-currency-conversion-page.html"
)
# https://www.exchangerates.org.uk/graphs/USD-UGX-exchange-rate-today-medium2.png
# with open("ugx_to_usd.html", "wb") as f:
#     f.write(r.content)

API = {}
# with open("ugx_to_usd.html", "rb") as f:
# file = f.read()
print("status code: ", r.status_code)
print("loading.....")
soup = BeautifulSoup(r.content, "html.parser")
# print(soup.title.text)
curr_ex = {"curr_ex": soup.select(".p_conv30 #shd2a")[0].text}
chart = {"curr_chart": soup.select("#conversion-chart-today img")[0]["src"]}
curr_ex |= chart

charts = {"charts": [link["href"] for link in soup.select(".thumbs a")]}
his = soup.find_all("table", id="conversionpageb")[-1].find_all("td")
his = [i.text for i in his[1:] if i.text != ""]
his = {"history": [{his[i]: his[i + 1]} for i in range(0, len(his), 2)]}

API.update(curr_ex)
API.update(charts)
API.update(his)
