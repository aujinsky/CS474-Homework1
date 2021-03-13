import requests
import re
from konlpy.tag import Kkma

from bs4 import BeautifulSoup


for i in range(266): # Naver Newspaper Research has maximum 4000 < 267 * 15 results
    raw = requests.get("https://m.search.naver.com/search.naver?where=m_news&query=%ED%83%9C%ED%92%8D&sm=mtb_tnw&sort=1&photo=0&field=0&pd=3&ds=2001.03.14&de=2021.03.13&docid=&related=0&mynews=1&office_type=2&office_section_code=8&news_office_checked=1001&nso=so%3Add%2Cp%3Afrom20010314to20210313&start="+str(15*i+1))
    html = BeautifulSoup(raw.text, "html.parser")
    result = html.find_all('a', attrs={'class': 'news_tit'})
    urls = [a['href'] for a in result]
    for url in urls:
        article_raw = requests.get(url)
        article_html = BeautifulSoup(article_raw.text, "html.parser")
        title_tag = article_html.find('h2', attrs={'class': 'media_end_head_headline'})
        title = title_tag.contents
        content_tag = article_html.find('div', attrs={'class': 'go_trans _article_content'})
        content_text = content_tag.get_text()
        print(content_text)
        kkma = Kkma()
        Kkma.analyze(content_text)
        print(content_text)
        break
    break
    
