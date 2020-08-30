import os

from scrappybara.syntax.charset import Charset
from scrappybara.syntax.models import PTagsModel
from scrappybara.syntax.tags import Tag
from scrappybara.syntax.training_samples import vectorize_sentence
from scrappybara.syntax.wordset import Wordset

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class Tagger(object):
    """Predicts part-of-speech tags for a batch of sentences"""

    def __init__(self):
        self.__charset = Charset().load()
        self.__wordset = Wordset().load()
        self.__ptags_model = PTagsModel(len(self.__charset)).load()

    def tag(self, token_lists):
        data_per_sentence = [vectorize_sentence(tokens, self.__charset, self.__wordset) for tokens in token_lists]
        seq_lengths, char_codes, word_vectors = zip(*data_per_sentence)
        tag_codes = self.__ptags_model.predict(char_codes, word_vectors)
        return [[Tag(code) for code in tag_codes[idx][1:sl + 1]] for idx, sl in enumerate(seq_lengths)]
