def find_jaccard(first, second):
    return len(set(first).intersection(set(second))) / len(set(first).union(set(second)))


def find_closest_words(term, index_table):
    close_words = []
    edit_distance_with_words = []
    possible_words = index_table.bigram.get_terms(term)
    for i in possible_words:
        jaccard_distance = find_jaccard(i, term)
        if jaccard_distance >= 0.6:
            leven_distance = levenshtein_distance(i, term)
            close_words.append(i)
            edit_distance_with_words.append(leven_distance)
            # uncomment if you wanna see the progress and all the terms chosen by jaccard algorithm
            # print(i + " " + str(leven_distance) + " " + str(jaccard_distance))
    if len(close_words) == 0:
        return []
    else:
        min_leven_distance = edit_distance_with_words[0]
        for leven_distance in edit_distance_with_words:
            if leven_distance < min_leven_distance:
                min_leven_distance = leven_distance
        if min_leven_distance > 4:
            return []
        chosen_words = []
        for i in range(len(edit_distance_with_words)):
            if edit_distance_with_words[i] == min_leven_distance:
                chosen_words.append(close_words[i])
        return chosen_words


def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def edit_distance(s1, s2):
    m = len(s1) + 1
    n = len(s2) + 1

    tbl = {}
    for i in range(m):
        tbl[i, 0] = i
    for j in range(n):
        tbl[0, j] = j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            tbl[i, j] = min(tbl[i, j - 1] + 1, tbl[i - 1, j] + 1, tbl[i - 1, j - 1] + cost)

    return tbl[i, j]


def minimum_edit_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1],
                                              distances[index1 + 1],
                                              new_distances[-1])))
        distances = new_distances
    return distances[-1]
