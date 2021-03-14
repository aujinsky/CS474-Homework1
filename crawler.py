import requests
import re
import konlpy
import nltk
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import datetime
okt= konlpy.tag.Okt()
count = 0
count_vect = CountVectorizer()
article_list = []
pos_list = []
date_list = []
num_pages = 3
print("Evaluation and verification only done on keyword '태풍 사망'")
keyword = input("Search keyword: ")
keyword = keyword.replace(" ","+")
for i in range(num_pages):
    raw = requests.get("http://search.khan.co.kr/search.html?stb=khan&dm=5&q=" +keyword+"&pg="+str(i+1)+"&sort=1&d1=20010315~20210314")
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
        date = date.replace("-",".")
        date_list.append(date)
        content_text = ''.join([content_tag.getText() for content_tag in content_tags])
        content_text = re.sub('\t', '', content_text)
        # print(content_text)
        # hannanum = konlpy.tag.Hannanum()
        # hannanum.analyze(content_text)
        nouns = okt.nouns(content_text)
        counter = Counter(nouns)
        print(counter.most_common(20)) # change to word2vec approach
        article_list.append(' '.join(nouns)) # disgusting
        pos = okt.pos(content_text, stem=True)
        # print(pos)
        pos_list.append(pos)
        # posnum = [item for item in pos if item[1] == 'Number']

# print(article_list)
# article_list = ['인공지능 자연어 처리 자연어 처리', '자연어 열대어 열대어 열대어', '처리 소리 물리 구리']
article_vector = count_vect.fit_transform(article_list).toarray()
train_article_vector = article_vector[10:20,:]
if (num_pages > 2):
    Xtrain = train_article_vector
    Ytrain = np.array([0,1,0,0,1,1,1,1,1,1])
    clf = MultinomialNB()
    clf.fit(Xtrain, Ytrain)
    Ytest = clf.predict(article_vector)
    print("validity: "+ str(Ytest))
    print(date_list)
    for i in range(num_pages * 10):
	    pos = pos_list[i]
	    articletime = datetime.datetime.strptime(date_list[i], '%Y.%m.%d')
	    if [item for item in pos if item[0] == '어제']:
	    	realtime = articletime - timedelta(days=1)
	    	print(realtime)
	    if [item for item in pos if item[0] == '오늘' or item[0] == '오전' or item[0] == '오후' or item[0] == '올해']:
	    	realtime = articletime
	    	print(realtime)

