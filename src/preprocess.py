from __future__ import unicode_literals
import hazm
import nltk
from nltk.stem import PorterStemmer

ps = PorterStemmer()


def persian_normalizer(text):
    hazm_normalizer = hazm.Normalizer()
    return hazm_normalizer.normalize(text)


def persian_tokenize(text):
    return hazm.word_tokenize(text)


def delete_persian_stop_words(list):
    stop_words = '،!?'
    output = []
    for token in list:
        if token in stop_words:
            continue
        else:
            output.append(token)
    return output


def persian_stemmer(list):
    hazm_stemmer = hazm.Stemmer()
    output = []
    for token in list:
        output.append(hazm_stemmer.stem(token))
    return output


def persian_preprocess(text):
    return persian_stemmer(delete_persian_stop_words(persian_tokenize(persian_normalizer(text))))


def english_normalizer(text):
    return text.lower()


def english_tokenize(text):
    return nltk.word_tokenize(text)


def delete_english_stop_words(list):
    stop_words = ',!?'
    output = []
    for token in list:
        if token in stop_words:
            continue
        else:
            output.append(token)
    return output


def english_stemmer(list):
    output = []
    for token in list:
        output.append(ps.stem(token))
    return output


def english_preprocess(text):
    return english_stemmer(delete_english_stop_words(english_tokenize(english_normalizer(text))))


def stopwords(terms_list):
    persian_stopwords = [']', '[', '.', 'و', 'در', '{', '}', '|', '=', ':', 'به', 'از', ')', '(', 'که', '*', 'اس',
                         'این', 'را', '==', '«', '»']
    english_stopwords = ['the', '.', 'a', 'of', 'to', 'in', 'and', '-', ';', 'on', 'it', 'for', ')', '(', "'s", '#',
                         'that', 'reuter', 'as', '39', 'with', 'at', 'by']
    deleted_terms = persian_stopwords + english_stopwords
    output = []
    for term in terms_list:
        if term in deleted_terms:
            continue
        else:
            output.append(term)
    # m = {}
    # for doc in terms_list:
    #     for item in doc:
    #         if item in m:
    #             m[item][0] += 1
    #         else:
    #             m[item] = [1]
    # m = nltk.OrderedDict(sorted(m.items(), key=lambda t: -t[1][0]))
    # terms_count = 0
    # for i in range(len(terms_list)):
    #     terms_count += len(terms_list[i])
    # deleted_terms = []
    # for item in m:
    # if m[item][0] >= 0.005 * terms_count:
    # print(item, m[item][0])
    # deleted_terms.append(item)
    # print(deleted_terms)
    # output = [list(filter(lambda a: a not in deleted_terms, terms_list[i])) for i in range(len(terms_list))]
    # terms_count = 0
    # for doc in output:
    #     terms_count += len(doc)
    return output
