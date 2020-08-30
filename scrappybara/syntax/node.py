from scrappybara.syntax.tags import Tag


class Node(object):
    """Belongs to a parse tree"""

    def __init__(self, token_idx, text, tag):
        self.idx = token_idx  # 0-index of the token in a sentence
        self.original = text  # Flat word found in the original sentence (cased)
        self.tag = tag
        # NODIFICATION
        self.particles = []  # Verb/adj particles (lower case)
        self.is_inf_to = False  # Verb seen as "TO + infinitive"
        # STANDARDIZATION
        self.standard = text.lower()  # Flat word with standardized orthography (lower case)
        # LEMMATIZATION
        self.lemma = self.standard
        self.suffix = None
        # CHUNKING
        self.chunk = None  # Common nouns chunked into a single string
        # CANONICALIZATION
        self.canon = self.standard  # Canonical representation
        self.active_verb = None  # Active verb from past participle
        # ARG REGISTRATION
        # Attached to any node
        self.and_cconjs = []
        self.or_cconjs = []
        self.is_aff = True  # Affirmative
        # Attached to verbs
        self.subjs = []  # 1st arguments (subjects)
        self.objs = []  # 2nd arguments (objects)
        self.exists = []  # 2nd arguments (existences)
        self.props = []  # 2nd arguments (properties)
        self.iprops = []  # 3rd arguments (indirect properties)
        self.iobjs = []  # 3rd arguments (indirect objects)
        # Attached to nouns
        self.adjs = []  # Adjectives
        self.subjs_verbs_iprops = []  # List of tuples (subj, verb, indirect property) where subj can be None
        self.copulas_props = []  # List of tuples (copula, property)
        self.pps_props = []  # List of tuples (past participle, property)
        # Attached to adjectives
        self.agents = []  # List of agents attached to an adj-ed when used in passive mode

    def __str__(self):
        return self.canon

    def __repr__(self):
        return self.canon

    @property
    def cconjs(self):
        return self.and_cconjs + self.or_cconjs

    @property
    def aggreg(self):
        return [self] + self.and_cconjs + self.or_cconjs

    @property
    def cannot_be_transitive(self):
        return any([self.props, self.iprops, self.exists])
