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
        if i % 100 == 0:
            print(i)
        token_list_persian.append(persian_preprocess(persian_documents[i]))
    for i in range(len(english_documents)):
        # feed in the body of documents index 1
        token_list_english.append(english_preprocess(english_documents[i][1]))
    preprocessed_persian = stopwords(token_list_persian)
    preprocessed_english = stopwords(token_list_english)
    index_table = insert_bigram_index(IndexTable(), preprocessed_persian, 0)
    index_table = insert_bigram_index(index_table, preprocessed_english, 1600)
    counter = 0
    m_first = index_table.get_table()
    for item in m_first:
        counter += 1
        if counter % 5000 == 1034:
            x = m_first[item][0]
            while x:
                print(item, x.get_doc_id(), x.get_positions())
                x = x.get_child()
    print("-----------------------")
    index_table = delete_bigram_index(index_table, preprocessed_persian, 0)
    counter = 0
    m_first = index_table.get_table()
    for item in m_first:
        counter += 1
        if counter % 2000 == 200:
            x = m_first[item][0]
            while x:
                print(item, x.get_doc_id(), x.get_positions())
                x = x.get_child()


if __name__ == "__main__":
    main()
