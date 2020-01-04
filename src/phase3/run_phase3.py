from src.phase3.input_reader import read_file
from src.phase3.kmeans import k_means
from src.phase3.vectorize_data import tf_idf_vector


def run_phase3():
    documents, index_table, doc_ids = read_file()
    vectors = tf_idf_vector(documents, index_table)
    centers = k_means(vectors, 10, doc_ids)
    for j in centers:
        for i in range(len(doc_ids)):
            if doc_ids[i] == j:
                print(doc_ids[i], documents[i])


if __name__ == "__main__":
    run_phase3()
