from src.KNN import test_knn, predict_knn_and_save, read_results
from src.document import Documents
from src.indexing import insert_index, IndexTable, save_to_file
from src.input_reader import read_csv_phase2, read_csv
from src.preprocess import english_preprocess, stopwords
from src.search import search_english_query


def read_files(stopwords_list):
    token_list_train = []
    token_list_test = []
    train_documents = read_csv_phase2('../raw-database/phase2_train.csv')
    test_documents = read_csv_phase2('../raw-database/phase2_test.csv')
    documents = Documents()

    for i in range(len(train_documents)):
        token_list_train.append(english_preprocess(train_documents[i][1]))
        documents.add_document(i, train_documents[i][0])
    for i in range(len(test_documents)):
        token_list_test.append(english_preprocess(test_documents[i][1]))
        documents.add_document(i + len(train_documents), test_documents[i][0])

    token_list_train, stopwords_list = stopwords(token_list_train, False, stopwords_list)

    return token_list_train, test_documents, documents


def run_phase2():
    token_list_english = []
    is_vb = False
    is_gamma = False
    english_documents = read_csv('../raw-database/English.csv')
    for i in range(len(english_documents)):
        # feed in the body of documents index 1
        token_list_english.append(english_preprocess(english_documents[i]))

    # removing stopwords from term lists
    # preprocessed_english, stopwords_list = stopwords(token_list_english, False, [])

    # token_list_train, test_docs, documents = read_files(stopwords_list)
    # index_table = insert_index(IndexTable([], is_vb, is_gamma), token_list_train, 0)
    # save_to_file(index_table, "", "../output-phase2/index_table_indexes", "")

    # test_knn([test_docs[i][1] for i in range(len(test_docs))], index_table, documents, [1, 5, 9],
    #          len(token_list_train), len(token_list_train))

    # predicted_values = predict_knn_and_save(english_documents, index_table, documents, 9, len(token_list_train))
    predicted_values = read_results()
    index_table_english = insert_index(IndexTable([], is_vb, is_gamma), token_list_english, 0)

    while True:
        print("Lets start searching!")
        c = int(input("Please enter the class of the news: "))
        query = input("Please enter the query: ")
        doc_ids = []
        for i in range(len(predicted_values)):
            if int(predicted_values[i]) == c:
                doc_ids.append(i)
        search_english_query(query, index_table_english, 1000, True, True, doc_ids)


if __name__ == "__main__":
    run_phase2()
