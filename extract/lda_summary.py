# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import sys
from time import sleep
from kl_div import get_topic_count
    
def get_split_lines(texts, line):
	tags = nltk.pos_tag(texts)
	connectors = []
	for tag in tags:
		if tag[1] == 'CC':
			connectors.append(tag[0])
	connectors = list(set(connectors))
	old_split = line.split(".") 
	for delim in connectors:
		split = []
		for ele in old_split:
			new_split = ele.split(delim)
			for e in new_split:
				split.append(e)
			del new_split[:]
		del old_split[:]
		old_split = split
	return split

def preprocess(doc):
	new_doc = re.sub('[\[\()](.*?)[\]\)]','',doc)
	return new_doc

def summarize(line):
	tokenizer = RegexpTokenizer(r'\w+')
	en_stop = get_stop_words('en')
	p_stemmer = PorterStemmer()
	
	doc_a = preprocess(line)
	doc_set = [doc_a]
	texts = []

	for i in doc_set:
	    
	    raw = i.lower()
	    tokens = tokenizer.tokenize(raw)

	    stopped_tokens = [i for i in tokens if not i in en_stop]
	    
	    stemmed_tokens = []
	    for i in stopped_tokens:
	    	try:
	    		stemmed_tokens.append(p_stemmer.stem(i))
	    	except:
	    		i = i[:-1]
	    		stemmed_tokens.append(p_stemmer.stem(i))
	    
	    texts.append(stemmed_tokens)

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	num_topics = get_topic_count(corpus, dictionary)
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)

	topical_words= ldamodel.print_topics(num_topics=num_topics, num_words=10)

	long_top_sentences = {}
	short_top_sentences = {}
	test = get_split_lines(tokens, doc_a)
	line_count = 0
	for line in test:
		
		raw = line.lower()
		tokens = tokenizer.tokenize(raw)
		
		stopped_tokens = [i for i in tokens if not i in en_stop]
		
		stemmed_tokens = []
		for i in stopped_tokens:
			try:
				stemmed_tokens.append(p_stemmer.stem(i))
			except:
				i = i[:-1]
				stemmed_tokens.append(p_stemmer.stem(i))

		similarity = ldamodel[dictionary.doc2bow(stemmed_tokens)]
		if len(similarity)==1:
			line_count += 1
			continue

		max_similar = -1
		for similar in similarity:
			if similar[1] > max_similar:
				max_similar = similar[1]

		key = max_similar
		long_top_sentences[key] = int(line_count)
		if line.count(" ")<15:
			short_top_sentences[key] = int(line_count)

		line_count += 1


	line_count = 0
	ordered_sentences = []
	for key in sorted(long_top_sentences.keys(), reverse=True):
		if line_count == 3: 
			break
		order = long_top_sentences[key]
		ordered_sentences.append(order)
		line_count += 1

	line_count = 0
	for key in sorted(short_top_sentences.keys(), reverse=True):
		if line_count == 2: 
			break
		order = short_top_sentences[key]
		ordered_sentences.append(order)
		line_count += 1

	ordered_sentences = sorted(list(set(ordered_sentences)))

	line_count = 0
	j = 0
	summary = ''
	if len(ordered_sentences) >= 3:
		for line in test:
			req_count = ordered_sentences[j]
			if req_count == line_count:
				summary += line+'. '
				j += 1
				if j == len(ordered_sentences):
					break
			line_count += 1
	return (summary+'\n')
