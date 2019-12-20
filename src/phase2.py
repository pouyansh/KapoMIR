from src.document import Documents
from src.input_reader import read_csv_phase2
from src.preprocess import english_preprocess, stopwords


def read_files():
    token_list_train = []
    token_list_test = []
    train_documents = read_csv_phase2('../raw-database/phase2_train.csv')
    test_documents = read_csv_phase2('../raw-database/phase2_test.csv')
    documents = Documents()

    for i in range(len(train_documents)):
        token_list_train.append(stopwords(english_preprocess(train_documents[i][1]), True))
        documents.add_document(i, train_documents[i][0])
    for i in range(len(test_documents)):
        token_list_test.append(stopwords(english_preprocess(test_documents[i][1]), True))
        documents.add_document(i + len(train_documents), test_documents[i][0])

    return token_list_train, token_list_test, documents
