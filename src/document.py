class Documents:
    def __init__(self):
        self.documents = {}

    def add_document(self, doc_id, doc_type):
        if doc_id not in self.documents:
            self.documents[doc_id] = []
        self.documents[doc_id].append(doc_type)

    def get_doc_type(self, doc_id):
        if doc_id in self.documents:
            return self.documents[doc_id][0]
        return None
