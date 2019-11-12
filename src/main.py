import importlib
from input_reader import *
from preprocess import *
from indexing import *
import sys


def main():
    token_list_persian = []
    token_list_english = []
    persian_documents = read_xml(
        '../raw-database/Persian.xml', '{http://www.mediawiki.org/xml/export-0.10/}')
    english_documents = read_csv('../raw-database/English.csv')
    for i in range(len(persian_documents)):
        if i % 100 == 0:
            print(i)
        token_list_persian.append(persian_preprocess(persian_documents[i]))
    for i in range(len(english_documents)):
        #feed in the body of documents index 1
        token_list_english.append(english_preprocess(english_documents[i][1]))
    preprocessed_persian = stopwords(token_list_persian)
    preprocessed_english = stopwords(token_list_english)
    create_index(preprocessed_persian)


if __name__ == "__main__":
    main()
