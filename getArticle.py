import urllib
from bs4 import *
import nltk

to = 10 #10s timeout
def IE ( url ):
	'''Indian Express'''
	handle = urllib.request.urlopen(url,timeout = to)
	html_gunk =  handle.read()
	soup = BeautifulSoup(html_gunk,"lxml")
	strings = soup.find('div', { 'itemprop' : 'articleBody' }).find_all('p')
	article = ""
	for par in strings:
		article = article  + '\n' + str(par)
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def Reuters ( url ):
	'''Reuters'''
	handle = urllib.request.urlopen(url,timeout = to)
	html_gunk =  handle.read()
	soup = BeautifulSoup(html_gunk,"lxml")
	strings = soup.find('span', { 'id' : 'articleText' }).find_all('p')
	article = ""
	for par in strings:
		article = article  + '\n' + str(par)
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def TOI ( url ):
	'''Times of India'''
	handle = urllib.request.urlopen(url,timeout = to)
	html_gunk =  handle.read()
	soup = BeautifulSoup(html_gunk,"lxml")
	strings = str(soup.find('div', { 'class' : 'Normal' }))
	sp2 = BeautifulSoup(strings,"lxml")
	return sp2.get_text()

def Hindu ( url ):
	'''The Hindu'''
	handle = urllib.request.urlopen(url,timeout = to)
	html_gunk =  handle.read()
	soup = BeautifulSoup(html_gunk,"lxml")
	strings = soup.find('div', { 'class' : 'article-text' }).find_all('p',{ 'class' : 'body' })
	article = ""
	for par in strings:
		article = article  + '\n' + str(par)
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def fetch( article ):
	site = article[2].strip().lower()
	n_attempt = 3 #In case thereis an exception
	tr = 0
	while(tr < n_attempt):
		try:
			if( site.find('times of india') != -1):
				return(TOI(article[3]))
			if( site.find('the hindu') != -1):
				return(Hindu(article[3]))
			if( site.find('reuters') != -1):
				return Reuters(article[3])
			if( site.find('indian express') != -1):
				return IE(article[3])
			return ""
		except:
			tr = tr + 1
	print("Error!!!!")
	return ""

def getArticles( filename ):
	f = open(filename)
	data = f.read()
	sp = data.split('\n')
	new = []
	for art in sp:
		sp2 = art.split('|')
		if(len(sp2) < 4 ):
			prev = prev + art
			sp3 = prev.split('|')
			if(len(sp3) == 4):
				new.append(sp3)
				prev = ""
		else:
			prev = ""
			new.append(sp2)
	cnt = 0
	for art in new:
		text = fetch(art)

		if( text != ""):
			print(art[0] + ' [' + art[2] + ']' )
			f = open('data/article'+str(cnt)+'.txt','w')
			f.write(art[0] + '||||\n' + art[1] + '||||\n' + art[2] + '||||\n' + art[3] + '||||\n' + text +'\n' )
			f.close()
			cnt = cnt +1


#getArticles( 'crawler_data.txt' )
#print( Hindu( 'http://m.thehindu.com/news/cities/Hyderabad/panel-to-resolve-differences-between-ap-ts-constituted/article7908950.ece?utm_source=inshorts&utm_medium=inshorts_full_article&utm_campaign=inshorts_full_article' ) )