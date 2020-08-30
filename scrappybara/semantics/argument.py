import scrappybara.config as cfg
from scrappybara.exceptions import ArgumentValueError
from scrappybara.semantics.argument_code import ArgCode


class Argument(object):
    """Contained by a SemanticTuple"""

    __codes = {code.value for code in ArgCode}
    __adj_codes = {ArgCode.ADJ.value, ArgCode.PP.value}
    __verb_codes = {ArgCode.INTR.value, ArgCode.REC.value, ArgCode.TRANS.value}

    def __init__(self, word, code, is_affirmative=True):
        if code not in self.__codes:
            raise ArgumentValueError('code', code, self.__codes)
        self.is_affirmative = is_affirmative
        self.word = word
        self.code = code

    def __str__(self):
        return self.flatten()

    def __repr__(self):
        return self.flatten()

    @property
    def tag(self):
        """Part-of-speech tag"""
        if self.code in self.__adj_codes:
            return 'ADJ'
        if self.code in self.__verb_codes:
            return 'VERB'
        return 'NOUN'

    def flatten(self, with_decorators=True):
        """Returns the string representation"""
        strs = []
        if with_decorators and not self.is_affirmative:
            strs.append(cfg.NEGATION)
        strs.append(self.word)
        return ' '.join(strs)
