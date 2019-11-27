import codecs
import csv

from src.utilities import *


class TermList:
    def __init__(self, doc_id, position, parent, child, is_vb, is_gamma):
        self.doc_id = doc_id
        if is_vb:
            self.positions = variable_byte_encode(position)
        elif is_gamma:
            self.positions = binary_to_str(gamma_encode(position))
        else:
            self.positions = [position]
        self.parent = parent
        self.child = child
        self.last_position = position
        self.frequency = 1

    def get_child(self):
        return self.child

    def set_child(self, child):
        self.child = child

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_doc_id(self):
        return self.doc_id

    def set_doc_id(self, doc_id):
        self.doc_id = doc_id

    def get_positions(self):
        return self.positions

    def set_positions(self, positions):
        self.positions = positions

    def add_position(self, position, is_vb, is_gamma):
        if is_vb:
            self.positions += variable_byte_encode(position - self.last_position)
        elif is_gamma:
            numbers = gamma_decode(self.positions)
            numbers.append(position - self.last_position)
            p = []
            for num in numbers:
                p += gamma_encode(num)
            self.positions = binary_to_str(p)
        else:
            self.positions.append(position)
        self.last_position = position
        self.frequency += 1

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_frequency(self):
        return self.frequency


class IndexTable:
    def __init__(self, lines, is_vb, is_gamma):
        self.table = {}
        self.is_vb = is_vb
        self.is_gamma = is_gamma
        self.read_from_file(lines)

    def get_table(self):
        return self.table

    def get_is_vb(self):
        return self.is_vb

    def get_is_gamma(self):
        return self.is_gamma

    def read_from_file(self, lines):
        if self.is_vb:
            self.read_from_file_variable_byte(lines)
        elif self.is_gamma:
            self.read_from_file_gamma(lines)
        else:
            for line in lines:
                term = line[0]
                doc_id = line[1]
                counter = 2
                while counter < len(line):
                    if str(line[counter]) == "-1":
                        if counter + 1 < len(line):
                            doc_id = line[counter + 1]
                        counter += 2
                        continue
                    self.add_record(term, doc_id, int(line[counter]))
                    counter += 1

    def read_from_file_gamma(self, lines):
        for line in lines:
            term = line[0]
            doc_ids = gamma_decode(line[1])
            temp_term_list = self.create_term(term, doc_ids[0], line[2])
            counter = 3
            while counter < len(line):
                doc_id = doc_ids[counter - 2]
                positions = line[counter]
                temp_term_list = self.insert_all_doc_occurrences(term, doc_id, positions, temp_term_list)
                counter += 1

    def read_from_file_variable_byte(self, lines):
        for line in lines:
            term = line[0]
            doc_id = variable_byte_decode(line[1])
            temp_term_list = self.create_term(term, doc_id, line[2])
            counter = 3
            while counter < len(line):
                doc_id = variable_byte_decode(line[counter])
                positions = line[counter + 1]
                counter += 1
                temp_term_list = self.insert_all_doc_occurrences(term, doc_id, positions, temp_term_list)
                counter += 1

    # For case when no TermList for term exists in the dictionary. Creates a TermList and adds it to the dictionary.
    def create_term(self, term, doc_id, positions):
        new_term = TermList(doc_id, 0, None, None, self.is_vb, self.is_gamma)
        new_term.set_positions(positions)
        if self.is_vb:
            positions = variable_byte_decode(positions)
            new_term.set_frequency(len(positions))
        elif self.is_gamma:
            positions = gamma_decode(positions)
            new_term.set_frequency(len(positions))
        self.table[term] = [new_term]
        self.table[term].append(1)
        self.table[term].append(doc_id)
        self.table[term].append(new_term)
        return new_term

    # For case when term exists in the dictionary and this new term will be placed at the end of the linked list.
    # Gets a doc_id and the encoded representation of all the occurrences of that term in that doc.
    def insert_all_doc_occurrences(self, term, doc_id, positions, parent):
        new_term = TermList(doc_id, 0, parent, None, self.is_vb, self.is_gamma)
        new_term.set_positions(positions)
        parent.set_child(new_term)
        self.table[term][1] += 1
        self.table[term][2] += doc_id
        self.table[term][3] = new_term
        return new_term

    # For case when we have just one position of a term occurrence in a doc_id
    def insert_term_list_in_dictionary(self, term, doc_id, position, previous_term, previous_id):
        if not previous_term.get_child():
            self.table[term][2] = doc_id

        # case 1: another records from this doc exists. Suffices to add the position to the list of positions
        if previous_id == doc_id:
            previous_term.add_position(position, self.is_vb, self.is_gamma)
            return

        # case 2: this doc_id is lower than all other doc_ids. Should create a term list and add it to the head of
        # linked list
        if previous_id == self.table[term][0].get_doc_id() > doc_id:
            new_term = TermList(doc_id, position, None, previous_term, self.is_vb, self.is_gamma)
            self.table[term][1] += 1
            if self.is_vb or self.is_gamma:
                previous_term.set_doc_id(previous_id - doc_id)
            self.table[term][0] = new_term
            previous_term.set_parent(new_term)
            return

        # case 3: previous term has a doc id lower than doc_id
        child = previous_term.get_child()
        if self.is_vb or self.is_gamma:
            new_term = TermList(doc_id - previous_id, position, previous_term, child, self.is_vb, self.is_gamma)
            self.table[term][1] += 1
            if child:
                child.set_doc_id(child.get_doc_id() - (doc_id - previous_id))
        else:
            new_term = TermList(doc_id, position, previous_term, child, self.is_vb, self.is_gamma)
        if not child:
            self.table[term][3] = new_term
        else:
            child.set_parent(new_term)
        previous_term.set_child(new_term)

    def add_record(self, term, doc_id, position):
        if term not in self.table:
            if self.is_vb:
                position = variable_byte_encode(position)
            elif self.is_gamma:
                position = binary_to_str(gamma_encode(position))
            else:
                position = [position]
            self.create_term(term, doc_id, position)
        else:
            self.table[term][1] += 1
            previous_term, previous_doc_id = self.search_cell(term, doc_id)
            self.insert_term_list_in_dictionary(term, doc_id, position, previous_term, previous_doc_id)

    def delete_record(self, doc_id, term_list):
        for term in term_list:
            if term in self.table:
                record, record_doc_id = self.search_cell(term, doc_id)
                if record_doc_id == doc_id:
                    if record.get_parent():
                        record.get_parent().set_child(record.get_child())
                    else:
                        if not record.get_child():
                            del self.table[term]
                            continue
                        else:
                            self.table[term][0] = record.get_child()
                    if record.get_child():
                        record.get_child().set_parent(record.get_parent())
                    else:
                        self.table[term][3] = record.get_parent()
                self.table[term][1] -= 1

    def search_cell(self, term, doc_id):
        if self.is_vb or self.is_gamma:
            return self.search_cell_vb_gamma(term, doc_id)

        record = self.table[term][0]
        # check if doc_id of first record is higher than doc_id or doc_id the of the last record is lower than doc_id
        if record.get_doc_id() > doc_id:
            return record, record.get_doc_id()
        if self.table[term][3].get_doc_id() <= doc_id:
            return self.table[term][3], self.table[term][3].get_doc_id()

        while record:
            if record.get_child() and record.get_child().get_doc_id() > doc_id:
                return record, record.get_doc_id()
            if not record.get_child():
                return record, record.get_doc_id()
            record = record.get_child()

    def search_cell_vb_gamma(self, term, doc_id):
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
        return False

    def get_all_records(self):
        lines = []
        for term in self.table:
            current_cell = self.table[term][0]
            current_line = [term]
            if self.is_gamma:
                doc_ids = []
                current_line.append("")
                while current_cell:
                    doc_ids += gamma_encode(current_cell.get_doc_id())
                    current_line.append(current_cell.get_positions())
                    current_cell = current_cell.get_child()
                current_line[1] = binary_to_str(doc_ids)
                lines.append(current_line)
            else:
                while current_cell:
                    current_line.append(current_cell.get_doc_id())
                    if self.is_vb or self.is_gamma:
                        current_line.append(current_cell.get_positions())
                    else:
                        for i in current_cell.get_positions():
                            current_line.append(i)
                        current_line.append(-1)
                    current_cell = current_cell.get_child()
                lines.append(current_line)
        return lines

    def get_dictionary(self, term):
        if term not in self.table:
            return None
        term_list = self.table[term][0]
        output = {}
        doc_id = term_list.get_doc_id()
        output[doc_id] = [term_list.get_frequency()]
        term_list = term_list.get_child()
        while term_list:
            if self.is_gamma or self.is_vb:
                doc_id += term_list.get_doc_id()
            else:
                doc_id = term_list.get_doc_id()
            output[doc_id] = [term_list.get_frequency()]
            term_list = term_list.get_child()
        return output


def insert_index(index_table, doc_list, offset):
    for doc_id in range(len(doc_list)):
        print(doc_id)
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
    with open(filename, 'w+b') as f:
        writer = csv.writer(f, delimiter=',')
        for row in index_table.get_all_records():
            writer.writerow(row)


def read_from_file(filename, is_vb, is_gamma):
    reader = csv.reader(codecs.open(filename, 'rb', 'utf-8'), delimiter=',')
    lines = []
    for row in reader:
        if row:
            lines.append(row)
    return IndexTable(lines, is_vb, is_gamma)
