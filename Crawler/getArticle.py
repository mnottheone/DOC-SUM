import urllib
from bs4 import *
import nltk
import os
import re
import sys
import json
to = 15 #5s timeout
def IE ( soup ):
	'''Indian Express'''
	strings = soup.find('div', { 'itemprop' : 'articleBody' }).find_all('p')
	article = ""
	for par in strings:
		article = article  + '\n' + str(par)
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def Reuters ( soup ):
	'''Reuters'''
	strings = soup.find('span', { 'id' : 'articleText' }).find_all('p')
	article = ""
	for par in strings:
		article = article  + '\n' + str(par)
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def TOI ( soup ):
	'''Times of India'''
	strings = str(soup.find('div', { 'class' : 'Normal' }))
	sp2 = BeautifulSoup(strings,"lxml")
	return sp2.get_text()

def Hindu ( soup ):
	'''The Hindu'''
	strings = soup.find('div', { 'class' : 'article-text' }).find_all('p',{ 'class' : 'body' })
	article = ""
	for par in strings:
		article = article  + '\n' + str(par)
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def Repo ( soup ):
	'''repository.inshorts'''
	strings = soup.find('script', { 'type' : 'text/javascript' }).string.split('=')[1].split(';\n')[0]
	js = json.loads(strings)
	article = ""
	for par in js['content']:
		article = article  + '\n' + str(par['property_map']['TEXT_VALUE'])
	sp2 = BeautifulSoup(article,"lxml")
	return sp2.get_text()

def fetch( article ):
	site = article[2].strip().lower()
	n_attempt = 1 #In case thereis an exception
	tr = 0
	while(tr < n_attempt):
		try:
			if ('youtube' in site) or ('google' in site) or ('twitter' in site) :
				print('shit')
				return ""
			handle = urllib.request.urlopen(article[3],timeout = to)
			html_gunk =  handle.read()
			soup = BeautifulSoup(html_gunk,"lxml")
			if('repository.inshorts' in handle.geturl()):
				print('repo')
				return(Repo( soup ))
			if( 'times of india' in site ):
				print('toi')
				return(TOI(soup))
			if( 'the hindu' in site):
				print('hindu')
				return(Hindu(soup))
			if( 'reuters' in site):
				print('reuters')
				return Reuters(soup)
			if( 'indian express' in site ):
				print('ie')
				return IE(soup)
			return ""
		except Exception as e:
			print(e)
			tr = tr + 1
	print("Error!!!! [" + article[3] + "]")
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
	try:
		lis = []
		regex = re.compile(r'\d+')
		for fil in os.listdir(os.getcwd()+'/data'):
			tmp = int(regex.search(fil).group(0))
			lis.append(tmp)
		sorted_lis = sorted(lis)
		cnt = sorted_lis[-1] + 1
	except:
		cnt = 0
	print(cnt)
	already_crawled = {}
	for filename in os.listdir(os.getcwd()+'/data'):
		f = open('data/'+filename)
		txt = f.read()
		link = txt.split('||||\n')[3].strip()
		already_crawled[link] = 1
		f.close()
	for art in new:
		if(art[3].strip() not in already_crawled):
			text = fetch(art)
			if( text != ""):
				print(art[0] + ' [' + art[2] + ']' )
				f = open('data/article'+str(cnt)+'.txt','w')
				f.write(art[0] + '||||\n' + art[1] + '||||\n' + art[2] + '||||\n' + art[3] + '||||\n' + text +'\n' )
				f.close()
				cnt = cnt +1


getArticles( 'crawler_data.txt' )
#print( Hindu( 'http://m.thehindu.com/news/cities/Hyderabad/panel-to-resolve-differences-between-ap-ts-constituted/article7908950.ece?utm_source=inshorts&utm_medium=inshorts_full_article&utm_campaign=inshorts_full_article' ) )