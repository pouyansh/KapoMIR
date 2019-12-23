from search import rate_english_doc, csv
from indexing import insert_index, IndexTable, save_to_file
from sklearn import svm as svm_alg
from input_reader import read_csv_phase2, read_csv
from preprocess import english_preprocess
from math import log10

def docs_to_vector(index_table, docs_number):
    words_table = index_table.get_table()
    words_array = []
    docs_scores = []
    for i in range(docs_number):
        docs_scores.append([])
    for i in words_table:
        words_array.append(i)
        word_dictionary = index_table.get_dictionary(i)
        for j in docs_scores:
            j.append(0)
        term_doc_frequency = len(word_dictionary)
        # print(i)
        # print(term_doc_frequency)
        for j in word_dictionary:
            docs_scores[j - 1][len(docs_scores[0]) - 1] = word_dictionary.get(j)[0] * log10(docs_number/term_doc_frequency)
    # for i in range(len(docs_scores[0])):
    #     if(docs_scores[1][i] != 0):
    #         print(words_array[i])
    #         print(docs_scores[1][i])
    return docs_scores, words_array

def query_to_vector(query, index_table, words_array):
    score = []
    for i in range(len(words_array)):
        score.append(0)
    for i in query:
        if i in words_array:
            score[words_array.index(i)] += 1
    # for i in range(len(score)):
    #     if score[i] != 0:
    #         print(words_array[i])
    #         print(score[i])
    return score

def svm(train_list, test_list, documents, index_table, docs_number):
    # print("==================================================")
    # print(train_list)
    # print("==================================================")
    # print(test_list)
    # print("==================================================")
    # print(docs_number)
    # print("==================================================")
    doc_scores, words_array = docs_to_vector(index_table, docs_number)
    Cee = 2
    gamm = 0.001
    clf = svm_alg.SVC(gamma=gamm, C=Cee)
    
    print("gamma is " + str(gamm) + " and C is " + str(Cee))
    
    target = []
    #TODO why???? where is the first training data?
    for i in range(docs_number):
        target.append(documents.get_doc_type(i + 1))
    
    # for i in range(len(doc_scores[0])):
    #     if doc_scores[0][i] != 0 :
    #         print(words_array[i])
    
    x, y = doc_scores[:-1], target[:-1]
    
    print('fitting...')
    clf.fit(x, y)
    
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
    
    score_list = []
    
    for i in token_list:
        score_list.append(query_to_vector(i, index_table, words_array))
    
    # for i in range(len(score_list[0])):
    #     if score_list[0][i] != 0:
    #         print(words_array[i])
    # print('=======')
    # print(test_documents[0][0])
    # print('=======')
    
    predictions_list = clf.predict(score_list)
    
    true_positives = 0
    for i in range(len(predictions_list)):
        if int(predictions_list[i]) == int(test_documents[i][0]):
            true_positives += 1
    print("The acuracy is " + str((true_positives/len(predictions_list)) * 100))
    
    
    # print(len(x))
    # print(len(y))