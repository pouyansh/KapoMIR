import csv

from src.indexing import IndexTable, insert_index
from src.preprocess import stopwords, english_preprocess


def read_file():
    data = []
    doc_ids = []
    index_table = IndexTable([], False, False)
    with open('../../raw-database/Data.csv', 'r', encoding="ansi") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if counter % 200 == 0:
                print(counter)
            if counter > 0:
                tokens, _ = stopwords(english_preprocess(row[1]), True, [], "../../output/stopwords.csv")
                doc_ids.append(row[0])
                data.append(tokens)
            counter += 1
    index_table = insert_index(index_table, data, 0)
    return data, index_table, doc_ids
