import requests
import re
import konlpy
import nltk
from bs4 import BeautifulSoup

okt= konlpy.tag.Okt()
count = 0
for i in range(1): # Naver Newspaper Research has maximum 4000 < 267 * 15 results
    raw = requests.get("http://search.khan.co.kr/search.html?stb=khan&dm=5&q=%ED%83%9C%ED%92%8D+%ED%94%BC%ED%95%B4&pg="+str(4)+"&sort=1&d1=20010315~20210314")
    html = BeautifulSoup(raw.text, "html.parser")
    result = html.find_all('dl', attrs={'class': 'phArtc'})
    atag = [a.find('a') for a in result]
    urls = [a['href'] for a in atag]
    for url in urls:
        count = count + 1
        artid = re.compile(r"artid=\d+");
        url = "https://m.khan.co.kr/view.html?" + artid.search(url).group()
        article_raw = requests.get(url, headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)'}) 
        article_html = BeautifulSoup(article_raw.text, "html.parser")
        title_tag = article_html.find('h3', attrs={'class': 'tit_view'})
        if title_tag == None:	# if 
        	print("MISS")
        	continue
        title = title_tag.contents
        print(str(count) + ". " + title[0])
        content_tags = article_html.find_all('p', attrs={'class': 'art_txt'})
        content_text = ''.join([content_tag.getText() for content_tag in content_tags])
        content_text = re.sub('\t', '', content_text)
        # print(content_text)
        # hannanum = konlpy.tag.Hannanum()
        # hannanum.analyze(content_text)
        pos = okt.pos(content_text, stem=True)
        posnum = [item for item in pos if item[1] == 'Number']
        print(posnum)
