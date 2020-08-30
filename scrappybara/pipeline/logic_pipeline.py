import multiprocessing

from scrappybara.normalization.canonicalizer import Canonicalizer
from scrappybara.normalization.lemmatizer import Lemmatizer
from scrappybara.normalization.standardizer import Standardizer
from scrappybara.semantics.semantic_tuple_extractor import SemanticTupleExtractor
from scrappybara.syntax.arg_finder import ArgFinder
from scrappybara.syntax.chunker import Chunker
from scrappybara.syntax.fixer import Fixer
from scrappybara.syntax.labelled_data import LabelledSentence
from scrappybara.syntax.nodifier import Nodifier
from scrappybara.utils.files import load_dict_from_txt_file, load_set_from_txt_file
from scrappybara.utils.multithreading import run_multithreads
from scrappybara.utils.mutables import reverse_dict


class LogicPipeline(object):
    """Contains all steps that don't require Machine Learning models.
    It's used for testing samples that are already labelled.
    """

    def __init__(self, language_model):
        # Irregular lemmatization/inflection
        preterits = load_dict_from_txt_file('english', 'irregular_preterits.txt')
        pps = load_dict_from_txt_file('english', 'irregular_past_participles.txt')
        plurals = load_dict_from_txt_file('english', 'irregular_plurals.txt')
        comparatives = load_dict_from_txt_file('english', 'irregular_comparatives.txt')
        superlatives = load_dict_from_txt_file('english', 'irregular_superlatives.txt')
        nouns = load_set_from_txt_file('english', 'nouns.txt')
        adjs = load_set_from_txt_file('english', 'adjectives.txt')
        reversed_pps = reverse_dict(pps)  # Lemma => past participle
        # Pipeline steps
        self.__nodify = Nodifier()
        self.__standardize = Standardizer(language_model)
        self.__lemmatize = Lemmatizer(language_model, adjs, preterits, pps, plurals, comparatives, superlatives,
                                      reversed_pps)
        self.__fix = Fixer(adjs, nouns)
        self.__chunk = Chunker()
        self.__canonicalize = Canonicalizer(self.__lemmatize)
        self.__find_arg = ArgFinder()
        self._extract_stuples = SemanticTupleExtractor(language_model, reversed_pps)

    def _logic_process(self, token_lists, tags, idx_trees, chunk_common_nouns,
                       nb_processes=multiprocessing.cpu_count()):
        """Processes many sentences"""
        sent_packs = list(zip(token_lists, tags, idx_trees, [chunk_common_nouns] * len(token_lists)))
        sent_results = run_multithreads(sent_packs, self.__logic_process, nb_processes)
        if len(sent_results):
            node_dicts, stuples = zip(*sent_results)
        else:
            return [], []
        return node_dicts, stuples

    def __logic_process(self, sentence_pack):
        """Processes single sentence"""
        tokens, tags, idx_tree, chunk_common_nouns = sentence_pack
        node_dict, node_tree = self.__nodify(tokens, tags, idx_tree)
        for node in node_dict.values():
            node.standard = self.__standardize(node.standard)
            node.lemma, node.suffix = self.__lemmatize(node.standard, node.tag)
        for node in node_dict.values():
            self.__fix(node, node_tree)
        if chunk_common_nouns:
            self.__chunk(node_dict.values(), node_tree)
        for node in node_dict.values():
            self.__canonicalize(node)
        self.__find_arg(node_dict.values(), node_tree)
        stuples = self._extract_stuples(node_dict.values())
        return node_dict, stuples

    # TESTING
    # -------------------------------------------------------------------------->

    def test_sample(self, token_tuples):
        sent = LabelledSentence(0, token_tuples)
        node_dicts, stuples = self._logic_process([sent.tokens], [sent.tags], [sent.tree], True)
        return stuples[0]
