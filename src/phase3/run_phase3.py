from src.phase3.input_reader import read_file
from src.phase3.vectorize_data import tf_idf_vector


def run_phase3():
    documents, index_table = read_file()
    vectors = tf_idf_vector(documents, index_table)
    print(vectors[0:3])


if __name__ == "__main__":
    run_phase3()
