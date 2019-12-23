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
    total = [0, 0, 0, 0]
    correctly_classified_each = [[0, 0, 0, 0] for _ in range(len(ks))]
    classified_each = [[0, 0, 0, 0] for _ in range(len(ks))]
    for i in range(len(tokens_test)):
        cs = knn(tokens_test[i], index_table, docs_number, ks, documents)
        for j in range(len(ks)):
            c = cs[j]
            classified_each[j][int(c) - 1] += 1
            if str(c) == str(documents.get_doc_type(i + offset)):
                correctly_classified[j] += 1
                correctly_classified_each[j][int(c) - 1] += 1
                print(i, correctly_classified_each)
        total[int(documents.get_doc_type(i + offset)) - 1] += 1
    for j in range(len(ks)):
        print("k: ", ks[j])
        print("number of correctly classified: " + str(correctly_classified[j]))
        print("accuracy: " + str(correctly_classified[j]/len(tokens_test)))
        print("recall class 1: " + str(correctly_classified_each[j][0]/total[0]))
        print("precision class 1: " + str(correctly_classified_each[j][0] / classified_each[j][0]))
        print("recall class 2: " + str(correctly_classified_each[j][1] / total[1]))
        print("precision class 2: " + str(correctly_classified_each[j][1] / classified_each[j][1]))
        print("recall class 3: " + str(correctly_classified_each[j][2] / total[2]))
        print("precision class 3: " + str(correctly_classified_each[j][2] / classified_each[j][2]))
        print("recall class 4: " + str(correctly_classified_each[j][3] / total[3]))
        print("precision class 4: " + str(correctly_classified_each[j][3] / classified_each[j][3]))


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
