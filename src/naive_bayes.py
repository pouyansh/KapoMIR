from input_reader import read_csv_phase2, read_csv
from indexing import insert_index, IndexTable, save_to_file
from document import Documents
from math import log10;
from preprocess import english_preprocess


def naive_bayes(words_table, index_table, documents, stopwords):
    Nc = [0, 0, 0, 0]
    train_documents = read_csv_phase2('../raw-database/phase2_train.csv') 
    for i in train_documents:
        Nc[int(i[0]) - 1] += 1
    N = 0
    for i in Nc:
        N += i
    B = len(words_table)
    TctP = [0, 0, 0, 0]
    Tct_table = {}
    for i in words_table:
        docs_table = index_table.get_dictionary(i)
        word_array = [0, 0, 0, 0]
        for j in docs_table:
            TctP[int(documents.get_doc_type(j)) - 1] += docs_table.get(j)[0]
            word_array[int(documents.get_doc_type(j)) - 1] += docs_table.get(j)[0]
        Tct_table[i] = word_array
    for i in Tct_table:
        for j in range(4):
            Tct_table.get(i)[j] = round(log10(int(Tct_table.get(i)[j]) + 1) - log10(int(TctP[j]) + int(B)), 4)
            # Tct_table.get(i)[j] = round(log10(int(Tct_table.get(i)[j]) + 1), 4)
    for i in range(4):
        Nc[i] = log10(Nc[i]/N)
    new_word_rate = [0, 0, 0, 0]
    for i in range(4):
        new_word_rate[i] += round(log10(1) - log10(int(TctP[i]) + int(B)), 4)
    label_test_docs(Nc, Tct_table, new_word_rate)

def label_test_docs(N, Tc_table, new_word_rate):
    stopwords = ['the', 'a', 'to', 'in', 'of', 's', 'and', 'on', 'for', 'it', '39', 'reuter', 'as', 'that', 'with', 'at', 'the', 'to', 'a', 'of', 'in', 'and', 's', 'on', 'for', '39', 'it', '&', 'that', 'with', 'at', 'as']
    test_documents = read_csv_phase2('../raw-database/phase2_test.csv')
    token_list = []
    for i in range(len(test_documents)):
        # feed in the body of documents index 1
        token_list.append(english_preprocess(test_documents[i][1]))
    for i in token_list:
        for j in i:
            if(j in stopwords):
                i.remove(j)
    true_positives = 0
    for i in range(len(token_list)):
        total_score = N.copy()
        for j in token_list[i]:
            if j in Tc_table:
                score = Tc_table.get(j)
            else:
                score = new_word_rate
            for k in range(4):
                total_score[k] += score[k]
        if (max_index(total_score) + 1) == int(test_documents[i][0]):
            true_positives += 1
    print("accuracy is " + str((true_positives * 100)/len(token_list)) + "%" )
            
        
def max_index(array):
    maximum = array[0]
    for i in array:
        if i > maximum:
            maximum = i
    for i in range(len(array)):
        if array[i] == maximum:
            return i
    return -1