from src.preprocess import *
from src.edit_distance import *
import math


def search_persian_query(query, index_table, number_of_docs, similar_words=True, is_reading_from_window=False,
                         window_docs=None):
    if window_docs is None:
        window_docs = []
    processed_query, s = stopwords(persian_preprocess(query), True)
    if is_reading_from_window:
        search_query(processed_query, index_table, number_of_docs, similar_words, is_reading_from_window, window_docs)
    else:
        search_query(processed_query, index_table, number_of_docs, similar_words)


def search_english_query(query, index_table, number_of_docs, similar_words=True, is_reading_from_window=False,
                         window_docs=None):
    if window_docs is None:
        window_docs = []
    processed_query, s = stopwords(english_preprocess(query), True)
    if is_reading_from_window:
        search_query(processed_query, index_table, number_of_docs, similar_words, is_reading_from_window, window_docs)
    else:
        search_query(processed_query, index_table, number_of_docs, similar_words)


def rate_english_doc(query, index_table, number_of_docs):
    processed_query, s = stopwords(english_preprocess(query), True)
    return rate_docs(processed_query, index_table, number_of_docs, False, False, [], False)


def search_query(processed_query, index_table, number_of_docs, similar_words, is_reading_from_window=False,
                 window_docs=None):
    if window_docs is None:
        window_docs = []
    doc_scores, doc_ids = rate_docs(processed_query, index_table, number_of_docs, similar_words, is_reading_from_window,
                                    window_docs)

    best_docs = []
    best_docs_scores = []

    for i in range(10):
        if len(doc_scores) > 0:
            max_score = doc_scores[0]
        else:
            max_score = -1
        for score in doc_scores:
            if score > max_score:
                max_score = score
        if max_score < 0:
            continue
        for j in range(len(doc_scores)):
            if doc_scores[j] == max_score:
                best_docs.append(doc_ids[j])
                best_docs_scores.append(doc_scores[j])
                doc_scores[j] = -1

    if len(best_docs) > 0:
        for i in range(len(best_docs)):
            if i >= 10:
                break
            print("doc id : " + str(best_docs[i]) + " with score : " + str(best_docs_scores[i]))
    else:
        print('No Relevant Documents Found!')


def rate_docs(processed_query, index_table, number_of_docs, similar_words, is_reading_from_window=False,
              window_docs=None, normalization=True):
    query_term_vector = []
    query_vector_tf = []
    # deleting duplicates and making a frequency vector for query
    for term in processed_query:
        if term not in query_term_vector:
            query_term_vector.append(term)
            query_vector_tf.append(1)
        else:
            for i in range(len(query_term_vector)):
                if term == query_term_vector[i]:
                    query_vector_tf[i] += 1
    query_vector_idf = []
    for term in query_term_vector:
        if index_table.get_all_occurrences(term):
            term_frequency = index_table.get_table()[term][1]
            query_vector_idf.append(math.log10(number_of_docs / term_frequency))
        else:
            query_vector_idf.append(0)
    doc_vectors, doc_ids = calculate_tf_idf(query_term_vector, index_table, similar_words,
                                            is_reading_from_window,
                                            window_docs, normalization)
    doc_scores = []
    for vector in doc_vectors:
        score = 0
        for i in range(len(vector)):
            score += vector[i] * query_vector_tf[i] * query_vector_idf[i]
        doc_scores.append(score)
    return doc_scores, doc_ids


def check_for_similar_words(index_table, query_term_vector, i):
    element = index_table.get_all_occurrences(query_term_vector[i])
    if not element:
        print(str(query_term_vector[i]) + ' not found')
        closest_words = find_closest_words(query_term_vector[i], index_table)
        if len(closest_words) == 0:
            print('no close words found to ' + query_term_vector[i] + ' !')
        else:
            print('did you mean :')
            for word in closest_words:
                print(word)


def calculate_tf_idf(query_term_vector, index_table, similar_words, is_reading_from_window=False,
                     window_docs=None, normalization=True):
    if window_docs is None:
        window_docs = []

    doc_ids = []
    doc_vectors = []
    for i in range(len(query_term_vector)):
        dictionary = index_table.get_dictionary(query_term_vector[i])
        # in case of not finding a word in dictionary
        if dictionary is None:
            dictionary = []
            if similar_words:
                check_for_similar_words(index_table, query_term_vector, i)

        for doc in dictionary:
            if is_reading_from_window:
                if doc not in window_docs:
                    continue
            if doc in doc_ids:
                for j in range(len(doc_ids)):
                    if doc_ids[j] == doc:
                        doc_vectors[j].append(dictionary[doc][0])
                        break
            else:
                doc_ids.append(doc)
                new_vector = []
                for j in range(i):
                    new_vector.append(0)
                new_vector.append(dictionary[doc][0])
                doc_vectors.append(new_vector)
        for vector in doc_vectors:
            if len(vector) < i + 1:
                vector.append(0)

    if normalization:
        for vector in doc_vectors:
            vector_sum = 0
            for i in vector:
                vector_sum += i * i
            vector_sum = math.sqrt(vector_sum)
            for i in range(len(vector)):
                vector[i] = vector[i] / vector_sum
    return doc_vectors, doc_ids
