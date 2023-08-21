import os
import requests
from flask import Flask,jsonify
from bs4 import BeautifulSoup

import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.json.sort_keys = False

f = open('stock.json','r')
port = int(os.environ.get('PORT', 80))

@app.route('/')
def home():
    return "STOCK API"

@app.route('/getStock/<stockname>')
def get(stockname):
    with open("stock.json", "r") as read_file:
        data = json.load(read_file)
        # data = json.loads(f.read())
        print(data)
        if stockname in data:
            print("ok")
            url = data[stockname]['url']
            response = requests.get(url=url)
            print(response)
            soup = BeautifulSoup(response.content, 'html.parser')
            Stock = soup.find(class_="inid_name").find('h1').text
            Market_value = soup.find(class_="pcstkspr nsestkcp bsestkcp futstkcp optstkcp").text
            fluctuation = soup.find(id="stick_ch_prch").text
            opens = soup.find(class_="nseopn bseopn")
            prev_close = soup.find(class_="nseprvclose bseprvclose")
            volume = soup.find(class_="nsevol bsevol")
            high = soup.find(class_="nseHP bseHP")
            low = soup.find(class_="nseLP bseLP")
            yearly_high = soup.find(class_="nseL52 bseL52")
            yearly_low = soup.find(class_="nseH52 bseH52")
            Market_Cap = soup.find(class_="nsemktcap bsemktcap")
            dividend_yield = soup.find(class_="nsedy bsedy")
            newsList = []
            news = soup.find(class_="news_list clearfix").findAll('a')
            news = news[1::2]
            for new in news:
                newsList.append(new.text)
                newsList.append(new.get('href'))
            today = datetime.now()
            from_timestamp = math.floor(today.timestamp() / 86400) * 86400
            to_stamp = from_timestamp - (86400 * 365)
            url="https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?"
            parameter = {
                "symbol" : data[stockname]['symbol'],
                "resolution" : "1D",
                "from" : from_timestamp,
                "to" : to_stamp,
                "countback" : 365,
                "currencyCode" : "INR"
            }
            header= {
                # ":authority:" : "priceapi.moneycontrol.com",
                # ":method:" : "GET",
                # ":path:" : "/techCharts/indianMarket/stock/history?symbol=RELIANCE&resolution=1D&from=1656288000&to=1692"
                #            "576000&countback=300&currencyCode=INR",
                # ":scheme:" : "https",
                "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                            "q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding" : "gzip, deflate, br",
                "Accept-Language" : "en-US,en;q=0.9",
                "Cache-Control" : "Cache-Control:",
                "Sec-Ch-Ua" : '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                "Sec-Ch-Ua-Mobile" : "?0",
                "Sec-Ch-Ua-Platform" : '"Windows"',
                "Sec-Fetch-Dest" : "document",
                "Sec-Fetch-Mode" : "navigate",
                "Sec-Fetch-Site" : "none",
                "Sec-Fetch-User" : "?1",
                "Upgrade-Insecure-Requests" : "1",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            response = requests.get(url=url,params=parameter,headers=header)
            print(response)
            jsonfile = {
                "Stock" : Stock,
                "Market Value" : Market_value,
                "fluctuation" : fluctuation,
                "Open" : opens.text,
                "Previous Close" : prev_close.text.split('\n')[0],
                "Volume" : volume.text,
                "High" : high.text,
                "low" : low.text,
                "52 Week High" : yearly_high.text,
                "52 Week Low" : yearly_low.text,
                "Market Capital" : Market_Cap.text,
                "Dividend_yield" : dividend_yield.text,
                "Related News" : newsList,
                "chart" : response.json()
            }
            return jsonify(jsonfile)
        else:
            return jsonify({"Stock" : "stock not found")
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
