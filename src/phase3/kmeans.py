from sklearn.cluster import KMeans
import numpy as np


def k_means(vectors, n, doc_ids):
    X = np.array(vectors)
    kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
    center_sentences = []
    for center in kmeans.cluster_centers_:
        max_score = 0
        doc = 0
        for i in range(len(vectors)):
            vector = vectors[i]
            score = 0
            for i in range(len(vector)):
                score += vector[i] * center[i]
            if score > max_score:
                max_score = score
                doc = doc_ids[i]
        center_sentences.append(doc)
    return center_sentences
