import csv

from src.preprocess import stopwords, english_preprocess


def read_file(doc_number):
    data = []
    doc_ids = []
    documents = []
    with open('../raw-database/Data.csv', 'r', encoding="ansi") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if counter > doc_number:
                break
            if counter > 0:
                documents.append(row[1])
                tokens, _ = stopwords(english_preprocess(row[1]), True, [], "../output/stopwords.csv")
                doc_ids.append(row[0])
                data.append(tokens)
            counter += 1
    return data, doc_ids
