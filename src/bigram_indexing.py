import csv


class BigramIndex:
    def __init__(self):
        self.dictionary = {}

    def get_dictionary(self):
        return self.dictionary

    def add_term(self, term):
        new_term = '$' + term + '$'
        for i in range(len(new_term) - 1):
            bigram = new_term[i] + new_term[i + 1]
            if bigram in self.dictionary:
                if term not in self.dictionary[bigram]:
                    self.dictionary[bigram].append(term)
            else:
                self.dictionary[bigram] = [term]

    def get_terms(self, term):
        terms = []
        new_term = '$' + term + '$'
        for i in range(len(new_term) - 1):
            bigram = new_term[i] + new_term[i + 1]
            if bigram in self.dictionary:
                terms += self.dictionary[bigram]
        return list(set(terms))

    def delete_term(self, term):
        new_term = '$' + term + '$'
        for i in range(len(new_term) - 1):
            bigram = new_term[i] + new_term[i + 1]
            if bigram in self.dictionary:
                if term in self.dictionary[bigram]:
                    self.dictionary[bigram].remove(term)

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for term in self.dictionary:
                row = [term] + self.dictionary[term]
                writer.writerow(row)

    def read_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] not in self.dictionary:
                    self.dictionary[row[0]] = [row[1]]
                else:
                    self.dictionary[row[0]].append(row[1])
                for i in range(2, len(row)):
                    self.dictionary[row[0]].append(row[i])
