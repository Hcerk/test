

URL = 'https://www.ukrtb.ru/'
import requests as req
from lxml import html
import bs4, re

from flask import Flask, request, json, g
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/newsUKRTB', methods=['GET'])
@cross_origin()
def ukrtb():
    response = req.get('https://www.ukrtb.ru/').content
    path = html.fromstring(response)
    soup = bs4.BeautifulSoup(response)
    news_json = {'list': []}
    for news in soup.find_all('div', class_ = 'news-block'):
        news_json['list'].append({
            'image': URL + re.findall(r'url\((\S+)\)', str(news.find('a').find('div').get('style')))[0],
            'subtitle': news.find('div', class_ = 'news-category').text,
            'header': news.find('h2', class_ = 'truncate').text,
            'text': news.find('div', class_ = 'truncate').text,
            'caption': news.find('div', class_ = 'news-time').text,
            'url': URL + news.find('div', class_ = 'news-image-container').find('a').get('href')
        })
    return news_json


if __name__ == '__main__':
    app.run(debug = True)