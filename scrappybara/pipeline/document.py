class Document(object):
    """Output of pipeline"""

    def __init__(self):
        self.sentences = []  # List of sentence objects

    def __iter__(self):
        return iter(self.sentences)

    @property
    def stuples(self):
        """Semantic tuples from every sentences"""
        return [stuple for sent in self.sentences for stuple in sent.stuples]
