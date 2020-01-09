from src.indexing import IndexTable, insert_index
from src.search import calculate_tf_idf


def tf_idf_vector(documents):
    index_table = IndexTable([], False, False)
    index_table = insert_index(index_table, documents, 0)
    all_words = []
    for doc in documents:
        for token in doc:
            if token not in all_words:
                all_words.append(token)
    doc_vectors, doc_ids = calculate_tf_idf(all_words, index_table, False, len(documents))
    return doc_vectors


def word2vec(documents):
    all_words = []
    for doc in documents:
        for term in doc:
            if term not in all_words:
                all_words.append(term)
    vectors = []
    for doc in documents:
        vector = [0 for _ in range(len(all_words))]
        for term in doc:
            for i in range(len(all_words)):
                if term == all_words[i]:
                    vector[i] += 1
                    break
        vectors.append(vector)
    return vectors
