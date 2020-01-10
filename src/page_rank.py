import csv
import json
import numpy as np


def calculate_page_rank(data, alpha, epsilon):
    ids = [e["id"] for e in data]
    page_ranks = np.array([1 / len(data) for _ in range(len(data))])
    b = np.array([(1 - alpha) * 1 / len(data) for _ in range(len(data))])
    a = [[0 for _ in range(len(data))] for _ in range(len(data))]
    for d in range(len(data)):
        refs = []
        for r in data[d]["references"]:
            if r in ids:
                refs.append(ids.index(r))
        if not refs:
            print(ids[d])
            refs = list(range(len(data)))
        for ref in refs:
            a[ref][d] += alpha / len(refs)
    a = np.array(a)
    difference = 1
    while difference > epsilon:
        temp_page_ranks = b + a.dot(page_ranks)
        sum_dif = 0
        for i in range(len(temp_page_ranks)):
            sum_dif += abs(temp_page_ranks[i] - page_ranks[i])
        print(sum_dif)
        difference = sum_dif
        page_ranks = temp_page_ranks
    print(page_ranks)
    return page_ranks


def read_json():
    with open('data2.json', 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    json_data = read_json()
    with open('../output-phase3/pageRank.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        prs = calculate_page_rank(json_data, 0.5, 0.0001)
        full_list = [[json_data[i]["id"], prs[i]] for i in range(len(prs))]
        for row in full_list:
            writer.writerow(row)
