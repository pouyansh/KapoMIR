from Proximity import proximity_search
from indexing import *
from input_reader import *
from search import *


def main():
    token_list_persian = []
    token_list_english = []
    is_vb = True
    is_gamma = False
    persian_documents = read_xml(
        '../raw-database/Persian.xml', '{http://www.mediawiki.org/xml/export-0.10/}')
    english_documents = read_csv('../raw-database/English.csv')
    for i in range(len(persian_documents)):
        token_list_persian.append(persian_preprocess(persian_documents[i]))
    for i in range(len(english_documents)):
        # feed in the body of documents index 1
        token_list_english.append(english_preprocess(english_documents[i]))

    # removing stopwords from term lists
    preprocessed_persian, stopwords_list = stopwords(token_list_persian, False, [])
    preprocessed_english, stopwords_list = stopwords(token_list_english, False, stopwords_list)

    # creating indexing tables
    # index_table = insert_index(IndexTable([], is_vb, is_gamma), preprocessed_persian, 1)
    # index_table = insert_index(index_table, preprocessed_english, len(preprocessed_persian))
    # save_to_file(index_table, "../output/index_table_vb_words",
    #              "../output/index_table_vb_indexes", "../output/index_table_gamma_indexes_bigram")
    index_table = read_from_file("../output/index_table_vb_words", "../output/index_table_vb_indexes",
                                 "../output/index_table_gamma_indexes_bigram", is_vb, is_gamma)

    while True:
        print("1. show the posting list for the given word")
        print("2. show the position of the given word in each document")
        print("3. show the preprocessed query")
        print("4. show the list of relevant documents based on lnc-ltc")
        print("5. show the list of relevant documents based on proximity search")
        print("6. delete a document")
        print("7. add a document")
        try:
            choice = int(input("Which one do you want?"))
        except ValueError:
            continue

        if choice == 1:
            term = input("Enter the term: ")
            if is_english(term):
                term = english_preprocess(term)[0]
            else:
                term = persian_preprocess(term)[0]
            print(index_table.get_posting_list(term))
        elif choice == 2:
            term = input("Enter the term: ")
            if is_english(term):
                term = english_preprocess(term)[0]
            else:
                term = persian_preprocess(term)[0]
            element = index_table.get_all_occurrences(term)
            doc_id = 0
            while element:
                positions = element.get_positions()
                if index_table.get_is_gamma():
                    doc_id += element.get_doc_id()
                    positions = gamma_decode(binary_to_str(positions))
                elif index_table.get_is_vb():
                    doc_id += element.get_doc_id()
                    positions = variable_byte_decode(positions)
                else:
                    doc_id = element.get_doc_id()
                print("document id: ", doc_id, "\tpositions: ", positions)
                element = element.get_child()
        elif choice == 3:
            query = input("Enter the query: ")
            if is_english(query):
                query = english_preprocess(query)
            else:
                query = persian_preprocess(query)
            print(query)
        elif choice == 4:
            query = input("Enter a query: ")
            if is_english(query):
                search_english_query(query, index_table, 1000)
                # 1000 english documents
            else:
                search_persian_query(query, index_table, 1572)
                # 1572 persian docs
        elif choice == 5:
            query = input("Enter a query: ")
            window = int(input("Enter the window size: "))
            if is_english(query):
                temp_query = english_preprocess(query)
            else:
                temp_query = persian_preprocess(query)
            doc_ids = proximity_search(temp_query, index_table, window, is_vb, is_gamma)
            if is_english(query):
                search_english_query(query, index_table, 1000, True, doc_ids)
                # 1000 english documents
            else:
                search_persian_query(query, index_table, 1572, True, doc_ids)
                # 1572 persian docs
        elif choice == 6:
            doc_id = int(input("Document id: "))
            if doc_id >= 1572:
                delete_index(index_table, [preprocessed_english[doc_id - 1572]], doc_id)
            else:
                delete_index(index_table, [preprocessed_persian[doc_id - 1]], doc_id)
        elif choice == 7:
            doc_id = int(input("Document id: "))
            if doc_id >= 1572:
                insert_index(index_table, [preprocessed_english[doc_id - 1572]], doc_id)
            else:
                insert_index(index_table, [preprocessed_persian[doc_id - 1]], doc_id)


if __name__ == "__main__":
    main()
