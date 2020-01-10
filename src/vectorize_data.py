from src.indexing import IndexTable, insert_index
from src.search import calculate_tf_idf

from gensim.models import Word2Vec


def tf_idf_vector(documents):
    index_table = IndexTable([], False, False)
    index_table = insert_index(index_table, documents, 0)
    all_words = []
    for doc in documents:
        for token in doc:
            if token not in all_words:
                all_words.append(token)
    doc_vectors, doc_ids = calculate_tf_idf(all_words, index_table, False, len(documents))
    return doc_vectors, all_words


def word2vec(documents):
    w2v = Word2Vec(documents, min_count=1)
    tf_idf_vectors, all_words = tf_idf_vector(documents)
    vectors = []
    for k in range(len(documents)):
        doc = documents[k]
        vector = [0 for _ in range(len(w2v.wv['great']))]
        for i in range(len(doc)):
            term = doc[i]
            if term in w2v.wv:
                temp_vec = w2v.wv[term]
                index = all_words.index(term)
                for j in range(len(temp_vec)):
                    vector[j] += temp_vec[j] * tf_idf_vectors[k][index]
        # print(vector)
        vectors.append(vector)
    return vectors
