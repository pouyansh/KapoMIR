import csv


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
    def __init__(self, lines):
        self.table = {}
        for line in lines:
            for counter in range(2, len(line)):
                self.add_record(line[0], line[1], int(line[counter]))

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
            return self.table[term][0]

    def get_all_records(self):
        lines = []
        for term in self.table:
            current_cell = self.table[term][0]
            while current_cell:
                line = [term, current_cell.get_doc_id()]
                for i in current_cell.get_positions():
                    line.append(i)
                lines.append(line)
                current_cell = current_cell.get_child()
        return lines


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


def save_to_file(index_table, filename):
    with open(filename, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=' ')
        for row in index_table.get_all_records():
            writer.writerow(row)


def read_from_file(filename):
    with open(filename, 'r', newline='', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=' ')
        lines = []
        for row in reader:
            lines.append(row)
        return IndexTable(lines)
