import csv
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import dendrogram, linkage


def k_means(vectors, n, doc_ids, filename):
    sse = []
    list_k = [50*i+25 for i in range(5)]

    x = np.array(vectors)
    for k in list_k:
        print(k)
        km = KMeans(n_clusters=k)
        km.fit(x)
        sse.append(km.inertia_)
        print(sse)
        kmeans = km.predict(x)
        with open('../output-phase3/' + filename + "-" + str(k) + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(len(kmeans)):
                writer.writerow([doc_ids[i], kmeans[i]])

    # Plot sse against k
    plt.figure(figsize=(6, 6))
    plt.plot(list_k, sse, '-o')
    plt.xlabel(r'Number of clusters *k*')
    plt.ylabel('Sum of squared distance')
    plt.show()
    print(sse)


def gaussian_mixture_model(vectors, n, doc_ids, filename):
    sse = []
    list_k = [2 * i + 1 for i in range(5)]

    x = np.array(vectors)
    for k in list_k:
        print(k)
        gmm = GaussianMixture(n_components=k)
        gmm.fit(x)
        sse.append(gmm.bic(x))
        print(sse)
        g = gmm.predict(x)
        with open('../output-phase3/' + filename + "-" + str(k) + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(len(g)):
                writer.writerow([doc_ids[i], g[i]])

    # Plot sse against k
    plt.figure(figsize=(6, 6))
    plt.plot(list_k, sse, '-o')
    plt.xlabel(r'Number of clusters *k*')
    plt.ylabel('Sum of squared distance')
    plt.show()
    print(sse)


def hierarchical_clustering(vectors, n):
    x = np.array(vectors)

    label_list = np.array(range(len(vectors)))

    linked = linkage(x, 'ward')
    dendrogram(linked,
               orientation='top',
               labels=label_list,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.xlabel(r'hierarchical clustering - tf-idf - ward - ' + str(n))
    plt.show()

    plt.clf()
    linked = linkage(x, 'complete')
    dendrogram(linked,
               orientation='top',
               labels=label_list,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.xlabel(r'hierarchical clustering - tf-idf - complete - ' + str(n))
    plt.show()

    plt.clf()
    linked = linkage(x, 'average')
    dendrogram(linked,
               orientation='top',
               labels=label_list,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.xlabel(r'hierarchical clustering - tf-idf - average - ' + str(n))
    plt.show()

    plt.clf()
    linked = linkage(x, 'single')
    dendrogram(linked,
               orientation='top',
               labels=label_list,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.xlabel(r'hierarchical clustering - tf-idf - single - ' + str(n))
    plt.show()
