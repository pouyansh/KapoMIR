import csv


class TermList:
    def __init__(self, doc_id, position, parent, child):
        self.doc_id = doc_id
        self.positions = [position]
        self.parent = parent
        self.child = child
        self.last_position = position

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

    def add_position(self, position, is_vb):
        if is_vb:
            self.positions.append(position - self.last_position)
        else:
            self.positions.append(position)
        self.last_position = position

    def set_doc_id(self, doc_id):
        self.doc_id = doc_id


class IndexTable:
    def __init__(self, lines, is_vb, is_gamma):
        self.table = {}
        self.is_vb = is_vb
        self.is_gamma = is_gamma
        for line in lines:
            term = line[0]
            doc_id = line[1]
            counter = 2
            while counter < len(line):
                if str(line[counter]) == "-1":
                    doc_id = line[counter + 1]
                    counter += 2
                self.add_record(term, doc_id, line[counter])
                counter += 1

    def get_table(self):
        return self.table

    def get_is_vb(self):
        return self.is_vb

    def get_is_gamma(self):
        return self.is_gamma

    def add_term_to_dictionary(self, term, doc_id, position):
        self.table[term] = [TermList(doc_id, position, None, None)]
        self.table[term].append(1)
        self.table[term].append(doc_id)
        self.table[term].append(self.table[term][0])

    def insert_term_list_in_dictionary(self, term, doc_id, position, previous_term, previous_id):
        if not previous_term.get_child():
            self.table[term][2] = doc_id

        # case 1: another records from this doc exists. Suffices to add the position to the list of positions
        if previous_id == doc_id:
            previous_term.add_position(position, self.is_vb)
            return

        # case 2: this doc_id is lower than all other doc_ids. Should create a term list and add it to the head of
        # linked list
        if previous_id == self.table[term][0].get_doc_id() > doc_id:
            new_term = TermList(doc_id, position, None, previous_term)
            if self.is_vb:
                previous_term.set_doc_id(previous_id - doc_id)
            self.table[term][0] = new_term
            previous_term.set_parent(new_term)
            return

        # case 3: previous term has a doc id lower than doc_id
        child = previous_term.get_child()
        if self.is_vb:
            new_term = TermList(doc_id - previous_id, position, previous_term, child)
            if child:
                child.set_doc_id(child.get_doc_id() - (doc_id - previous_id))
        else:
            new_term = TermList(doc_id, position, previous_term, child)
        if not child:
            self.table[term][3] = new_term
        else:
            child.set_parent(new_term)
        previous_term.set_child(new_term)

    def add_record(self, term, doc_id, position):
        if term not in self.table:
            self.add_term_to_dictionary(term, doc_id, position)
        else:
            self.table[term][1] += 1
            if self.is_vb:
                previous_term, previous_doc_id = self.search_cell_vb(term, doc_id)
                self.insert_term_list_in_dictionary(term, doc_id, position, previous_term, previous_doc_id)
            else:
                previous_term = self.search_cell(term, doc_id)
                self.insert_term_list_in_dictionary(term, doc_id, position, previous_term, previous_term.get_doc_id())

    def delete_record(self, doc_id, term_list):
        for term in term_list:
            if term in self.table:
                record = self.search_cell(term, doc_id)
                if record.get_doc_id() == doc_id:
                    if record.get_parent():
                        record.get_parent().set_child(record.get_child())
                    else:
                        if not record.get_child():
                            del self.table[term]
                            continue
                        else:
                            self.table[term][0] = record.get_parent()
                    if record.get_child():
                        record.get_child().set_parent(record.get_parent())
                    else:
                        self.table[term][1] = record.get_parent()
                self.table[term][1] -= 1

    def search_cell(self, term, doc_id):
        record = self.table[term][0]
        if record.get_doc_id() > doc_id:
            return record
        if self.table[term][3].get_doc_id() <= doc_id:
            return self.table[term][3]
        while record:
            if record.get_child() and record.get_child().get_doc_id() > doc_id:
                return record
            if not record.get_child():
                return record
            record = record.get_child()

    def search_cell_vb(self, term, doc_id):
        record = self.table[term][0]
        if record.get_doc_id() > doc_id:
            return record, record.get_doc_id()
        if self.table[term][2] <= doc_id:
            return self.table[term][3], self.table[term][2]
        sum_id = record.get_doc_id()
        while record:
            if record.get_child() and record.get_child().get_doc_id() + sum_id > doc_id:
                return record, sum_id
            if not record.get_child():
                return record, sum_id
            sum_id += record.get_doc_id()
            record = record.get_child()
        return record

    def get_all_occurrences(self, term):
        if term in self.table:
            return self.table[term][0]

    def get_all_records(self):
        lines = []
        for term in self.table:
            current_cell = self.table[term][0]
            current_line = [term]
            while current_cell:
                current_line.append(current_cell.get_doc_id())
                for i in current_cell.get_positions():
                    current_line.append(i)
                current_line.append(-1)
                current_cell = current_cell.get_child()
            lines.append(current_line)
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
        writer = csv.writer(f, delimiter=',')
        for row in index_table.get_all_records():
            writer.writerow(row)


def read_from_file(filename):
    with open(filename, 'r', newline='', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        lines = []
        for row in reader:
            lines.append(row)
        return IndexTable(lines, False, False)
