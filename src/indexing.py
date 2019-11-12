class TermList:
    def __init__(self, doc_id, position, parent, child):
        self.doc_id = doc_id
        self.position = position
        self.parent = parent
        self.child = child

    def set_child(self, child):
        self.child = child

    def get_child(self):
        return self.child

    def get_doc_id(self):
        return self.doc_id

    def get_position(self):
        return self.position

    def get_parent(self):
        return self.parent


def create_index(doc_list):
    m_first = {}
    m_last = {}
    for doc_id in range(len(doc_list)):
        for item_position in range(len(doc_list[doc_id])):
            term = doc_list[doc_id][item_position]
            if term not in m_first:
                m_first[term] = [TermList(doc_id, item_position, None, None)]
                m_last[term] = [m_first[term][0]]
            else:
                m_last[term][0].set_child(TermList(doc_id, item_position, m_last[term][0], None))
                m_last[term][0] = m_last[term][0].get_child()

    counter = 0
    for i in m_first:
        counter += 1
        if counter % 1000 == 0 and counter < 10001:
            x = m_first[i][0]
            while x:
                print(i, x.doc_id, x.position)
                x = x.child
