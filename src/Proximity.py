from utilities import gamma_decode


def proximity_search(query, index_table, window):
    term_lists = [index_table.get_all_occurrences(q) for q in query]
    term_lists_doc_ids = [term_list.get_doc_id() for term_list in term_lists]
    output_doc_ids = []
    while True:
        current_max = max(term_lists_doc_ids)
        check_not_equal = False
        for i in range(len(term_lists)):
            while term_lists_doc_ids[i] < current_max:
                term_lists[i] = term_lists[i].get_child()
                if term_lists[i] is None:
                    return output_doc_ids
                term_lists_doc_ids[i] += term_lists[i].get_doc_id()
            if term_lists_doc_ids[i] > current_max:
                check_not_equal = True
        if check_not_equal:
            continue
        if proximity_search_in_doc(term_lists, window):
            output_doc_ids.append(current_max)
        if term_lists[0].get_child() is None:
            return output_doc_ids
        term_lists[0] = term_lists[0].get_child()
        term_lists_doc_ids[0] += term_lists[0].get_doc_id()


def proximity_search_in_doc(term_lists, window):
    all_positions = [gamma_decode(term_list.get_positions()) for term_list in term_lists]
    current_positions = [positions[0] for positions in all_positions]
    while True:
        min_position = min(current_positions)
        max_position = max(current_positions)
        if max_position - min_position <= window:
            return True
        for i in range(len(current_positions)):
            if current_positions[i] == min_position:
                if len(all_positions[i]) == 0:
                    return False
                current_positions[i] += all_positions[i][0]
                all_positions[i].pop(0)
