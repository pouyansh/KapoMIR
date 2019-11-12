class TermList:
    def __init__(self, doc_id, position, parent, child):
        self.doc_id = doc_id
        self.positions = [position]
        self.parent = parent
        self.child = child

    def set_child(self, child):
        self.child = child

    def set_parent(self, parent):
        self.parent = parent

    def get_child(self):
        return self.child

    def get_doc_id(self):
        return self.doc_id

    def get_positions(self):
        return self.positions

    def get_parent(self):
        return self.parent

    def add_position(self, position):
        self.positions.append(position)


class IndexTable:
    def __init__(self):
        self.table = {}

    def get_table(self):
        return self.table

    def add_record(self, term, doc_id, position):
        if term not in self.table:
            self.table[term] = [TermList(doc_id, position, None, None)]
            self.table[term].append(self.table[term][0])
        else:
            last_term = self.table[term][1]
            if last_term.get_doc_id() == doc_id:
                last_term.add_position(position)
            else:
                last_term.set_child(TermList(doc_id, position, self.table[term][1], None))
                self.table[term][1] = last_term.get_child()

    def delete_record(self, doc_id, term_list):
        for term in term_list:
            if term in self.table:
                record = self.table[term][0]
                while record:
                    if record.get_doc_id() == doc_id:
                        if record.get_parent():
                            record.get_parent().set_child(record.get_child())
                        else:
                            if not record.get_child():
                                del self.table[term]
                                break
                            else:
                                self.table[term][0] = record.get_parent()
                        if record.get_child():
                            record.get_child().set_parent(record.get_parent())
                        else:
                            self.table[term][1] = record.get_parent()
                    record = record.get_child()

    def get_all_occurrences(self, term):
        if term in self.table:
            return self.table[term]


def insert_index(index_table, doc_list, offset):
    for doc_id in range(len(doc_list)):
        for item_position in range(len(doc_list[doc_id])):
            term = doc_list[doc_id][item_position]
            index_table.add_record(term, doc_id + offset, item_position)
    return index_table


def delete_index(index_table, doc_list, offset):
    for doc_id in range(len(doc_list)):
        term_list = []
        for term in doc_list[doc_id]:
            if term not in term_list:
                term_list.append(term)
        index_table.delete_record(doc_id + offset, term_list)
    return index_table


def insert_bigram_index(index_table, doc_list, offset):
    for doc_id in range(len(doc_list)):
        for item_position in range(len(doc_list[doc_id]) - 1):
            term = doc_list[doc_id][item_position] + " " + doc_list[doc_id][item_position + 1]
            index_table.add_record(term, doc_id + offset, item_position)
    return index_table


def delete_bigram_index(index_table, doc_list, offset):
    for doc_id in range(len(doc_list)):
        term_list = []
        for term_index in range(len(doc_list[doc_id]) - 1):
            term = doc_list[doc_id][term_index] + " " + doc_list[doc_id][term_index + 1]
            if term not in term_list:
                term_list.append(term)
        index_table.delete_record(doc_id + offset, term_list)
    return index_table
