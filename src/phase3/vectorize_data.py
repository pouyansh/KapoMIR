from src.search import calculate_tf_idf


def tf_idf_vector(documents, index_table):
    all_words = []
    for document in documents:
        doc = document[1]
        for token in doc:
            if token not in all_words:
                all_words.append(token)
    doc_vectors, doc_ids = calculate_tf_idf(all_words, index_table, False)
    return doc_vectors


# def word2vec(documents):
#     return 
