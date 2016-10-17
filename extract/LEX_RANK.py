
# coding: utf-8

# In[5]:

import nltk
import re
import pprint
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
import math
import numpy as np


# In[17]:
def test():
    f=open('/home/daivik/NLP/data/article2045.txt')
    txt = f.read()
    art = txt.split('||||')[4]
    nis_sum = txt.split('||||')[1]
    print('Article:')
    print(art)
    print('News In Shorts summary:')
    print(nis_sum)
    print('Lex Summary:')
    print(get_sum(art))


# In[18]:
def tokenize(art):
    sentences = nltk.sent_tokenize(art)
    #sentences  = art.split(['.','!','?'])
    #sentences = re.split('[.?!]+',art)
    #print(len(sentences))
    #print(sentences[0])
    stemmer = PorterStemmer()
    tokenized_sents = []
    for sen in sentences:
        tokenized_sents.append(word_tokenize(sen.lower()))
    stop = set(stopwords.words('english'))
    sss = []
    for sen in tokenized_sents:
        ss=[]
        for word in sen:
            if(word not in stop):
                ss.append(stemmer.stem(word))
        sss.append(ss)
    #word_tokenize(sentences[0].lower())
    #print(sss[0])
    return(sentences,sss)


# # Compute IDF

# In[20]:
#Supply tokenized sentences
def IDF(sss):
    idf = {}
    for sent in sss:
        for word in sent:
            if word not in idf:
                idf[word] = 0
    for word in idf:
        for sent in sss:
            if word in sent:
                idf[word] = idf[word] +1
    for word in idf:
        idf[word] = math.log(len(sss)/idf[word])
    return idf
#print(idf['friday'])


# # Compute TF-IDF

# In[21]:
#suply tokenized sentences and dictionary of idfs for each token
def TF_IDF(sss,idf):
    tfidf = []
    for sent in sss:
        dic = {}
        for word in sent:
            if word not in dic:
                dic[word] = 1
            else:
                dic[word] = dic[word] + 1
        for word in dic:
            dic[word] = math.log(1+dic[word]) * idf[word]
        tfidf.append(dic)
    return tfidf
    #print(tfidf[0])


# # Cosine Simillarity function

# In[22]:

def cosine_sim(sent1, sent2):
    dot = 0
    for word in sent1:
        if word in sent2:
            dot = dot + sent1[word] * sent2[word]
    for word in sent2:
        if word in sent1:
            dot = dot + sent1[word] * sent2[word]
    mag1 = 0
    for word in sent1:
        mag1 = mag1 + sent1[word] * sent1[word]
    mag1 = math.sqrt(mag1)
    mag2 = 0
    for word in sent2:
        mag2 = mag2 + sent2[word] * sent2[word]
    mag2 = math.sqrt(mag2)
    answer = dot/(mag1*mag2)
    return answer
#print(cosine_sim(tfidf[0],tfidf[1]))


# In[23]:
def get_adjacency_matrix(tfidf):
    cos_threshold = 0.15
    cnt = 0
    adj = np.zeros((len(tfidf),len(tfidf)))
    degree = np.zeros((len(tfidf)))
    for i in range(len(tfidf)):
        for j in range(len(tfidf)):
            if cosine_sim(tfidf[i],tfidf[j]) >= cos_threshold:
                adj[i][j]=1
                cnt = cnt +1
                degree[i] = degree[i]+1
            else:
                adj[i][j]=0
    # print(cnt)
    # print(len(tfidf))
    return(adj,degree)


# In[24]:take graph and return list of nodes with importance
#
def get_lexrank_scores(adj,degree,n_iter = 1000):
    n = adj.shape[0]
    B = np.zeros(adj.shape)
    for i in range(n):
        for j in range(n):
            B[i][j] = adj[i][j]/degree[j]


    # # Calculate Centrality score (eigenvector)

    # In[25]:

    eig = np.ones((n,1))/n
    for i in range(n_iter):
        eig = np.mat(B)*np.mat(eig)
    eig = np.array(eig)[:,0]
    #indices = np.argsort(eig)[::-1]
    #print(indices)
    return eig


# # Get summary

# In[26]:
# sorts sentences by score, returns tuple of sentence list,
# list of indices in order of decreasing importance
def get_scores(art):
    sentences,sss = tokenize(art)
    idf = IDF(sss)
    tfidf = TF_IDF(sss,idf)
    adj,degree = get_adjacency_matrix(tfidf)
    scores = get_lexrank_scores(adj,degree)
    return scores

def get_sorted_by_score(art):
    sentences,sss = tokenize(art)
    idf = IDF(sss)
    tfidf = TF_IDF(sss,idf)
    adj,degree = get_adjacency_matrix(tfidf)
    scores = get_lexrank_scores(adj,degree)
    indices = np.argsort(scores)[::-1]
    return sentences,indices


def get_sum(art, numsent=3):
    sentences,indices = get_sorted_by_score(art)
    relevant_sentences = indices[:numsent]
    relevant_sentences = np.sort(relevant_sentences)# put back in order
    summary = ''
    for i in relevant_sentences:
        summary = summary + sentences[i]
    #print(summary)
    return summary
    






