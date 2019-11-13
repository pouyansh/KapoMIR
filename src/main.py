import importlib
from src.input_reader import *
from src.preprocess import *
from src.indexing import *
import sys


def main():
    token_list_persian = []
    token_list_english = []
    persian_documents = read_xml(
        '../raw-database/Persian.xml', '{http://www.mediawiki.org/xml/export-0.10/}')
    english_documents = read_csv('../raw-database/English.csv')
    for i in range(len(persian_documents)):
        token_list_persian.append(persian_preprocess(persian_documents[i]))
    for i in range(len(english_documents)):
        # feed in the body of documents index 1
        token_list_english.append(english_preprocess(english_documents[i][1]))

    # removing stopwords from term lists
    preprocessed_persian = stopwords(token_list_persian)
    preprocessed_english = stopwords(token_list_english)

    # creating indexing tables
    index_table = insert_index(IndexTable(), preprocessed_persian, 0)
    index_table = insert_index(index_table, preprocessed_english, len(preprocessed_persian))

    # creating bigram indexing tables
    index_bigram_table = insert_bigram_index(IndexTable(), preprocessed_persian, 0)
    index_bigram_table = insert_bigram_index(index_bigram_table, preprocessed_english, len(preprocessed_persian))

    # get input and search the term
    while True:
        term = input("Enter a word: ")
        term = english_preprocess(term)[0]
        element = index_table.get_all_occurrences(term)
        while element:
            print("document id: ", element.get_doc_id(), "\tpositions: ", element.get_positions())
            element = element.get_child()


if __name__ == "__main__":
    main()
