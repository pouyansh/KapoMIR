import json


def calculate_page_rank(data, k):
    page_ranks = [1000/len(data) for _ in range(len(data))]
    for i in range(k):
        temp_page_ranks = [0 for _ in page_ranks]
        for d in range(len(data)):
            refs = []
            for r in data[d]["references_ids"]:
                if r < len(data):
                    refs.append(r)
            for ref in refs:
                temp_page_ranks[ref] += page_ranks[d] / len(refs)
        page_ranks = [pr for pr in temp_page_ranks]
    return page_ranks


def read_json():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    json_data = read_json()
    print(calculate_page_rank(json_data, 1))
