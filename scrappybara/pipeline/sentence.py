class Sentence(object):
    """Contained by a Document"""

    def __init__(self):
        self.stuples = []  # List of SemanticTuple objects

    def __iter__(self):
        return iter(self.stuples)
