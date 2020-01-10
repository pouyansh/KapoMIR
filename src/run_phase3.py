from src.input_reader_phase3 import read_file
from src.clustering import k_means, gaussian_mixture_model, hierarchical_clustering
from src.vectorize_data import tf_idf_vector, word2vec


def run_phase3():
    doc_number = 1000
    cluster_numbers = 10
    documents, doc_ids = read_file(doc_number)

    # filename = "kmeans-tfidf"
    # filename = "kmeans-word2vec"
    filename = "gmm-tfidf"
    # filename = "gmm-word2vec"
    # filename = "hc-tfidf"
    # filename = "hc-word2vec"

    vectors, _ = tf_idf_vector(documents)
    # vectors = word2vec(documents)

    # k_means(vectors, cluster_numbers, doc_ids, filename)
    gaussian_mixture_model(vectors, cluster_numbers, doc_ids, filename)
    # hierarchical_clustering(vectors, doc_number)


if __name__ == "__main__":
    run_phase3()
