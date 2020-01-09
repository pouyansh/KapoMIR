import csv

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture


def k_means(vectors, n, doc_ids, filename):
    kmeans = KMeans(n_clusters=n, random_state=0).fit_predict(vectors)
    with open('../output-phase3/' + filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(kmeans)):
            writer.writerow([doc_ids[i], kmeans[i]])
    center_sentences = []
    for center in kmeans.cluster_centers_:
        max_score = 0
        doc = 0
        for i in range(len(vectors)):
            vector = vectors[i]
            score = 0
            for j in range(len(vector)):
                score += vector[j] * center[j]
            if score > max_score:
                max_score = score
                doc = doc_ids[i]
        center_sentences.append(doc)
    return center_sentences


def gaussian_mixture_model(vectors, n, doc_ids, filename):
    gmm = GaussianMixture(n_components=n).fit_predict(vectors)
    with open('../output-phase3/' + filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(gmm)):
            writer.writerow([doc_ids[i], gmm[i]])


def hierarchical_clustering(vectors, n, doc_ids, filename):
    hc = AgglomerativeClustering(n_clusters=n).fit_predict(vectors)
    with open('../output-phase3/' + filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(hc)):
            writer.writerow([doc_ids[i], hc[i]])
