from src.utilities import *


def proximity_search(query, index_table, window, is_vb, is_gamma):
    for term in query:
        if not index_table.get_all_occurrences(term):
            print(term)
            return []
    term_lists = [index_table.get_all_occurrences(q) for q in query]
    term_lists_doc_ids = [term_list.get_doc_id() for term_list in term_lists]
    output_doc_ids = []
    while True:
        # print(term_lists_doc_ids)
        current_max = max(term_lists_doc_ids)
        check_not_equal = False
        for i in range(len(term_lists)):
            while term_lists_doc_ids[i] < current_max:
                term_lists[i] = term_lists[i].get_child()
                if term_lists[i] is None:
                    return output_doc_ids
                if is_vb or is_gamma:
                    term_lists_doc_ids[i] += term_lists[i].get_doc_id()
                else:
                    term_lists_doc_ids[i] = term_lists[i].get_doc_id()
            if term_lists_doc_ids[i] > current_max:
                check_not_equal = True
        if check_not_equal:
            continue
        if proximity_search_in_doc(term_lists, window, is_vb, is_gamma):
            output_doc_ids.append(current_max)
        if term_lists[0].get_child() is None:
            return output_doc_ids
        term_lists[0] = term_lists[0].get_child()
        if is_vb or is_gamma:
            term_lists_doc_ids[0] += term_lists[0].get_doc_id()
        else:
            term_lists_doc_ids[0] = term_lists[0].get_doc_id()


def proximity_search_in_doc(term_lists, window, is_vb, is_gamma):
    if is_gamma:
        all_positions = [gamma_decode(term_list.get_positions()) for term_list in term_lists]
    elif is_vb:
        all_positions = [variable_byte_decode(term_list.get_positions()) for term_list in term_lists]
    else:
        all_positions = [[p for p in term_list.get_positions()] for term_list in term_lists]
    current_positions = [positions[0] for positions in all_positions]
    while True:
        # print(current_positions)
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
