from search import rate_english_doc, csv


def knn(query, index_table, docs_number, ks, documents):
    doc_scores, doc_ids = rate_english_doc(query, index_table, docs_number)
    docs = [[doc_scores[i], doc_ids[i]] for i in range(len(doc_scores))]
    docs = sorted(docs, key=lambda x: -x[0])
    m = {'1': 0, '2': 0, '3': 0, '4': 0}
    outs = []
    for k in ks:
        for i in range(k):
            doc_id = docs[i][1]
            doc_type = documents.get_doc_type(doc_id)
            if doc_type:
                m[str(doc_type)] += 1
        majority = m['1']
        major_type = 1
        for i in range(2, 5):
            if majority < m[str(i)]:
                majority = m[str(i)]
                major_type = i
        outs.append(major_type)
    return outs


def test_knn(tokens_test, index_table, documents, ks, offset, docs_number):
    correctly_classified = [0 for _ in range(len(ks))]
    for i in range(len(tokens_test)):
        cs = knn(tokens_test[i], index_table, docs_number, ks, documents)
        for j in range(len(ks)):
            c = cs[j]
            if str(c) == str(documents.get_doc_type(i + offset)):
                correctly_classified[j] += 1
                print(i, correctly_classified)
    for j in range(len(ks)):
        print("k: ", ks[j])
        print("number of correctly classified: " + str(correctly_classified[j]))
        print("accuracy: " + str(correctly_classified[j]/len(tokens_test)))


def predict_knn_and_save(docs, index_table, documents, k, docs_number):
    output = []
    with open("../output-phase2/predicted_classes.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(docs)):
            if i % 50 == 0:
                print(i)
            doc = docs[i]
            c = knn(doc, index_table, docs_number, [k], documents)
            writer.writerow([i, c[0]])
            output.append(c[0])
    return output


def read_results():
    output = []
    with open("../output-phase2/predicted_classes.csv", 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row[1])
    return output
