import enum


@enum.unique
class ArgCode(enum.Enum):
    """Code of a SemanticTuple's Argument"""

    ADJ = 'A'  # Adjective that is not a past-participle: e.g. "big", "breaking"
    COP = 'C'  # Copula verb
    PP = 'L'  # Adjective that is a past participle
    INTR = 'I'  # Intransitive verb
    NOUN = 'N'  # Noun
    PRON = 'O'  # Pronoun
    PROPN = 'P'  # Proper noun
    REC = 'R'  # Verb with indirect object: the recipient of the action
    SYM = 'S'  # Symbolic noun: e.g. "mysite.com", "#OnSale"
    TRANS = 'T'  # Transitive Verb
    NUM = 'U'  # Numeral noun: e.g. "I bought 34"
