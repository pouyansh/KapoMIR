from src.input_reader import *
from src.preprocess import *
from src.indexing import *
from src.search import *


def main():
    # token_list_persian = []
    # token_list_english = []
    # persian_documents = read_xml(
    #     '../raw-database/Persian.xml', '{http://www.mediawiki.org/xml/export-0.10/}')
    # english_documents = read_csv('../raw-database/English.csv')
    # for i in range(len(persian_documents)):
    #     token_list_persian.append(persian_preprocess(persian_documents[i]))
    # for i in range(len(english_documents)):
    #     # feed in the body of documents index 1
    #     token_list_english.append(english_preprocess(english_documents[i]))
    #
    # # removing stopwords from term lists
    # preprocessed_persian = stopwords(token_list_persian)
    # preprocessed_english = stopwords(token_list_english)
    #
    # # creating indexing tables
    # index_table = insert_index(IndexTable([], False, True), preprocessed_persian, 1)
    # index_table = insert_index(index_table, preprocessed_english, len(preprocessed_persian))
    # #
    # # creating bigram indexing tables
    # index_table = insert_bigram_index(index_table, preprocessed_persian, 1)
    # index_table = insert_bigram_index(index_table, preprocessed_english, len(preprocessed_persian))
    # save_to_file(index_table, "../output/gamma/index_table_gamma_words",
    #              "../output/gamma/index_table_gamma_indexes_")
    index_table = read_from_file("../../gamma/index_table_gamma_words",
                                 "../../gamma/index_table_gamma_indexes_", False, True)

    # get input and search the term
    # while True:
    #     term = input("Enter a word: ")
    #     term = english_preprocess(term)[0]
    #     element = index_table.get_all_occurrences(term)
    #     doc_id = 0
    #     while element:
    #         doc_id += gamma_decode(element.get_doc_id())[0]
    #         print("document id: ", doc_id, "\tpositions: ", gamma_decode(element.get_positions()))
    #         element = element.get_child()

    while True:
        term = input("Enter a query: ")
        # term = input("Enter a word: ")
        # element = index_table.get_all_occurrences(term)
        # if not element:
        #     print('not found')
        #     closest_words = find_closest_words(index_table, term)
        #     if len(closest_words) == 0:
        #         print('no close words found!')
        #     else:
        #         print('did you mean :')
        #         for word in closest_words:
        #             print(word)
        # else:
        #     doc_id = 0
        #     while element:
        #         print("document id: ", element.get_doc_id(), "\tpositions: ", element.get_positions())
        #         element = element.get_child()
        # search_english_query(term, index_table, 1001)
        search_english_query(term, index_table, 100)
        # 1572 persian docs


if __name__ == "__main__":
    main()