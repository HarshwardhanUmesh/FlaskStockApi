import os
import requests
from flask import Flask,jsonify
from bs4 import BeautifulSoup

import json

app = Flask(__name__)
f = open('stock.json','r')
proxies={
    'https' : '107.170.164.50:3128'
}
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
            url = data[stockname]
            response = requests.get(url=url)
            print(response)
            soup = BeautifulSoup(response.content, 'html.parser')
            Stock = soup.find(class_="inid_name").find('h1').text
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
            jsonfile = {
                "Stock" : Stock,
                "Open" : opens.text,
                "Previous Close" : prev_close.text.split('\n')[0],
                "Volume" : volume.text,
                "High" : high.text,
                "low" : low.text,
                "52 Week High" : yearly_high.text,
                "52 Week Low" : yearly_low.text,
                "Market Capital" : Market_Cap.text,
                "Dividend_yield" : dividend_yield.text,
                "Related News" : newsList
            }
            return jsonify(jsonfile)
        else:
            return "stock not found"
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
