import numpy
import sys
import scipy.stats as stats
from gensim import corpora, models, similarities, matutils
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import re

def prepare_corpus(corpus, dictn):
    global my_corpus 
    global corpus_length_vector 
    global dictionary
    my_corpus = corpus
    dictionary = dictn
    corpus_length_vector = numpy.array(
        [sum(frequency for _, frequency in document) for document in my_corpus]
    )

def symmetric_kl_divergence(p, q):
    """ Caluculates symmetric Kullback-Leibler divergence.
    """
    return numpy.sum([stats.entropy(p, q), stats.entropy(q, p)])


def arun_metric(corpus, dictionary, min_topics=1, max_topics=1, iteration=1):
    """ Caluculates Arun et al metric..
    """
    result = [];
    for i in range(min_topics, max_topics, iteration):
        # Instanciates LDA.
        lda = models.ldamodel.LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=i
        )
        # Caluculates raw LDA matrix.
        matrix = lda.expElogbeta
        # Caluculates SVD for LDA matris.
        U, document_word_vector, V = numpy.linalg.svd(matrix)
        # Gets LDA topics.
        lda_topics = lda[my_corpus]
        # Caluculates document-topic matrix.
        term_document_matrix = matutils.corpus2dense(
            lda_topics, lda.num_topics
        ).transpose()
        document_topic_vector = corpus_length_vector.dot(term_document_matrix)
        document_topic_vector = document_topic_vector + 0.0001
        document_topic_norm   = numpy.linalg.norm(corpus_length_vector)
        document_topic_vector = document_topic_vector / document_topic_norm
        result.append(symmetric_kl_divergence(
            document_word_vector,
            document_topic_vector
        ))
    return result


def get_topic_count(corpus, dictn):
    prepare_corpus(corpus, dictn)
    # Caluculates symmetric KL divergence.
    kl_divergence = arun_metric(my_corpus, dictionary, max_topics=4);

    i = 0
    no_topics = None
    for topic_score in kl_divergence:
        if i == 1 :
            max_score = topic_score
        elif i > 1 and i < 4: 
            if max_score < topic_score:
                max_score = topic_score 
                no_topics = i

        elif i != 0:
            break
        i+=1

    if no_topics is None:
        no_topics = 2

    return no_topics
