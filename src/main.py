import importlib

from src.Proximity import proximity_search
from src.input_reader import *
from src.preprocess import *
from src.indexing import *
import sys

from src.utilities import variable_byte_decode, variable_byte_encode


def main():
    token_list_persian = []
    token_list_english = []
    persian_documents = read_xml(
        '../raw-database/Persian.xml', '{http://www.mediawiki.org/xml/export-0.10/}')
    english_documents = read_csv('../raw-database/English.csv')
    for i in range(100):
        token_list_persian.append(persian_preprocess(persian_documents[i]))
    for i in range(100):
        # feed in the body of documents index 1
        token_list_english.append(english_preprocess(english_documents[i][1]))

    # removing stopwords from term lists
    preprocessed_persian = stopwords(token_list_persian)
    preprocessed_english = stopwords(token_list_english)

    # creating indexing tables
    index_table = insert_index(IndexTable([], False, True), preprocessed_persian, 1)
    index_table = insert_index(index_table, preprocessed_english, len(preprocessed_persian))

    # creating bigram indexing tables
    index_table = insert_bigram_index(index_table, preprocessed_persian, 1)
    index_table = insert_bigram_index(index_table, preprocessed_english, len(preprocessed_persian))
    save_to_file(index_table, "../output/index_table_gamma_2.csv")
    # index_table = read_from_file("../output/index_table_gamma_2.csv", False, True)

    # get input and search the term
    while True:
        terms = input("Enter a word: ")
        query = english_preprocess(terms)
        window = int(input("Enter the window size: "))
        print(proximity_search(query, index_table, window))


if __name__ == "__main__":
    main()
