import itertools
import multiprocessing
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf

import scrappybara.config as cfg
from scrappybara.langmodel.language_model import LanguageModel
from scrappybara.pipeline.document import Document
from scrappybara.pipeline.logic_pipeline import LogicPipeline
from scrappybara.pipeline.sentence import Sentence
from scrappybara.preprocessing.sentencizer import Sentencizer
from scrappybara.syntax.parser import Parser
from scrappybara.utils.multithreading import run_multithreads


class Pipeline(LogicPipeline):
    # Used to split sentences again after they've been sentencized once
    __splitters = {':', '"', ';', '(', ')', '[', ']', '{', '}', '-'}

    def __init__(self, sentencizer=Sentencizer(), nb_cores=multiprocessing.cpu_count(), batch_size=128,
                 use_gpu=True):
        self.__nb_processes = nb_cores
        self.__use_gpu = use_gpu
        self.__lm = LanguageModel(1, 1)
        super().__init__(self.__lm)
        self.__sentencize = sentencizer
        if use_gpu:
            self.__parse = Parser(nb_cores, batch_size)
        else:
            with tf.device('/CPU:0'):
                self.__parse = Parser(nb_cores, batch_size)

    def __call__(self, texts, chunk_common_nouns=True):
        """Processes all texts in memory & returns a list of documents"""
        # Text tokens is a list of list of list of tokens (tokens grouped by sentences for each text)
        tokens = run_multithreads(texts, self.__sentencize, self.__nb_processes)
        tokens = run_multithreads(tokens, self.__split_tokens, self.__nb_processes)
        # Remember the association text/sentences
        sent_ranges = []
        total_sents = 0
        for token_lists in tokens:
            new_total = total_sents + len(token_lists)
            sent_ranges.append((total_sents, new_total))
            total_sents = new_total
        # Flatten sentences
        tokens = [token_lists for group in tokens for token_lists in group]
        # Run pipeline on GPU or CPU
        if self.__use_gpu:
            _, _, _, stuple_lists = self.__process_tokens(tokens, chunk_common_nouns)
        else:
            with tf.device('/CPU:0'):
                _, _, _, stuple_lists = self.__process_tokens(tokens, chunk_common_nouns)
        # Regroup semantic tuples by documents
        docs = []
        for start, end in sent_ranges:
            doc = Document()
            for stuple_list in stuple_lists[start:end]:
                sentence = Sentence()
                sentence.stuples = stuple_list
                doc.sentences.append(sentence)
            docs.append(doc)
        return docs

    def __split_tokens(self, token_lists):
        """Resplit a text's sentences that are too long"""
        new_token_lists = []
        for tokens in token_lists:
            if len(tokens) > cfg.MAX_SENT_LENGTH:
                new_token_lists.extend(
                    [list(group) for b, group in itertools.groupby(tokens, lambda x: x in self.__splitters) if not b])
            else:
                new_token_lists.append(tokens)
        # Remove sentences that are still too long
        return [tokens for tokens in new_token_lists if len(tokens) <= cfg.MAX_SENT_LENGTH]

    def __process_tokens(self, token_lists, chunk_common_nouns):
        """Proxy for both production __call__ and testing"""
        tags, trees = self.__parse(token_lists)
        node_dicts, stuples = self._logic_process(token_lists, tags, trees, chunk_common_nouns, self.__nb_processes)
        return tags, trees, node_dicts, stuples

    # TESTING
    # -------------------------------------------------------------------------->

    def _test_parse(self, input_sentence):
        """Arg input_sentence can be a string or a list of tokens"""
        if isinstance(input_sentence, list):
            tokens = [input_sentence]
        else:
            tokens = self.__sentencize(input_sentence)
        tags, trees, node_dicts, _ = self.__process_tokens(tokens, True)
        return tokens[0], tags[0], trees[0], node_dicts[0]

    def _test_process(self, text):
        """To debug every step"""
        token_lists = self.__sentencize(text)
        tags, trees, node_dicts, _ = self.__process_tokens(token_lists, True)
        stuples = [self._extract_stuples(node_dict.values()) for node_dict in node_dicts]
        return token_lists[0], tags[0], trees[0], node_dicts[0], stuples[0]
