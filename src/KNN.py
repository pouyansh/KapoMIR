from src.search import rate_english_doc


def knn(query, index_table, docs_number, k, documents):
    doc_scores, doc_ids = rate_english_doc(query, index_table, docs_number)
    docs = [[doc_scores[i], doc_ids[i]] for i in range(len(doc_scores))]
    docs = sorted(docs, key=lambda x: x[0])
    m = {1: 0, 2: 0, 3: 0, 4: 0}
    for i in range(k):
        doc_id = docs[i]
        doc_type = documents.get_doc_type(doc_id)
        if doc_type:
            m[doc_type] += 1
    majority = m[1]
    major_type = 1
    for i in range(2, 5):
        if majority < m[i]:
            majority = m[i]
            major_type = i
    return major_type
