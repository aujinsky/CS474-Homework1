import requests
import re
import konlpy
import nltk
from collections import Counter
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer


okt= konlpy.tag.Okt()
count = 0
count_vect = CountVectorizer()
article_list = []
date_list = []
for i in range(4):
    raw = requests.get("http://search.khan.co.kr/search.html?stb=khan&dm=5&q=태풍 사망&pg="+str(i+1)+"&sort=1&d1=20010315~20210314")
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
        em_tag = article_html.find('span', attrs={'class': 'txt_info'}).find('em')
        r = re.compile(r"20[012][0-9][.-][01][0-9][.-][0-9]{2}") # okay
        date = r.search(em_tag.contents[0]).group()
        date_list.append(date)
        content_text = ''.join([content_tag.getText() for content_tag in content_tags])
        content_text = re.sub('\t', '', content_text)
        # print(content_text)
        # hannanum = konlpy.tag.Hannanum()
        # hannanum.analyze(content_text)
        nouns = okt.nouns(content_text)
        counter = Counter(nouns)
        print(counter.most_common(20))
        article_list.append(' '.join(nouns)) # disgusting
        pos = okt.pos(content_text, stem=True)
        posnum = [item for item in pos if item[1] == 'Number']
# print(article_list)
# article_list = ['인공지능 자연어 처리 자연어 처리', '자연어 열대어 열대어 열대어', '처리 소리 물리 구리']
article_vector = count_vect.fit_transform(article_list)
print(date_list)
print(article_vector)

