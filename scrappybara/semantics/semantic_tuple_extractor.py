import scrappybara.config as cfg
from scrappybara.normalization.inflector import Inflector
from scrappybara.semantics.argument import Argument
from scrappybara.semantics.argument_code import ArgCode
from scrappybara.semantics.semantic_tuple import SemanticTuple
from scrappybara.syntax.tags import Tag, NOUN_TAGS, PROP_TAGS
from scrappybara.utils.maths import xnor


def _noun_arg_code(noun):
    """Converts a NOUN tag to an argument code"""
    if noun.tag == Tag.PROPN:
        return ArgCode.PROPN.value
    if noun.tag == Tag.PRON:
        return ArgCode.PRON.value
    if noun.tag == Tag.NUM:
        return ArgCode.NUM.value
    if noun.tag == Tag.SYM:
        return ArgCode.SYM.value
    return ArgCode.NOUN.value


def _adj_arg_code(adj):
    """Converts an ADJ tag to an argument code"""
    if adj.active_verb:
        return ArgCode.PP.value
    return ArgCode.ADJ.value


def _prop_arg_code(prop):
    if prop.tag == Tag.ADJ:
        return _adj_arg_code(prop)
    return _noun_arg_code(prop)


class SemanticTupleExtractor(object):
    __not_passive = {'have', 'get'}
    __not_intransitive = {'have', 'get', 'be', 'do'}

    def __init__(self, language_model, lemma_pp):
        self.__inflector = Inflector(language_model, lemma_pp)

    def __call__(self, nodes):
        """Extracts semantic tuples from a list of nodes"""
        stuples = []
        # Greedy extraction
        blocked_for_round_2 = set()
        # First round
        for node in nodes:
            if node.tag == Tag.VERB and not any([node.is_inf_to, node.cannot_be_transitive]):
                stuples.extend(self.__make_stuples_from_verbs_subjs_objs(node, blocked_for_round_2))
        # Second round
        for node in [n for n in nodes if n not in blocked_for_round_2]:
            if node.tag == Tag.VERB and not any([node.is_inf_to, node.cannot_be_transitive]):
                stuples.extend(self.__make_stuples_from_subjs_objs(node))
                stuples.extend(self.__make_stuples_from_iobj(node))
            elif node.tag in NOUN_TAGS:
                stuples.extend(self.__make_stuples_from_iprops(node))
                stuples.extend(self.__make_stuples_from_copula_props(node))
                stuples.extend(self.__make_stuples_from_pp_props(node))
                stuples.extend(self.__make_stuples_from_naked_adjs(node))
        # Third round
        for node in nodes:
            if node.tag == Tag.VERB and not node.cannot_be_transitive:
                stuples.extend(self.__make_stuples_from_objs(node))
        return stuples

    def __make_stuples_from_verbs_subjs_objs(self, verb, blocked_for_next_round):
        """Make quadruples or quintuples when the object is a clause"""
        stuples = []
        for subj_1 in [s for s in verb.subjs if s.tag in NOUN_TAGS]:
            subj_1_arg = Argument(subj_1.canon, _noun_arg_code(subj_1))
            for obj_1 in [o for o in verb.objs if o.tag == Tag.VERB]:
                blocked_for_next_round.add(obj_1)
                if not obj_1.subjs:
                    subjs_2 = [subj_1]  # e.g. "I want to sing"
                else:
                    subjs_2 = [s for s in obj_1.subjs if s.tag in NOUN_TAGS]
                for subj_2 in subjs_2:
                    subj_2_arg = Argument(subj_2.canon, _noun_arg_code(subj_2))
                    if not obj_1.cannot_be_transitive:
                        if not obj_1.objs and obj_1.canon not in self.__not_intransitive:
                            is_aff = xnor(subj_1.is_aff, verb.is_aff, subj_2.is_aff, obj_1.is_aff)
                            verb_arg = Argument(verb.canon, ArgCode.TRANS.value, is_aff)
                            obj_1_arg = Argument(obj_1.canon, ArgCode.INTR.value)
                            stuples.append(SemanticTuple(subj_1_arg, verb_arg, subj_2_arg, obj_1_arg))
                        for obj_2 in [o for o in obj_1.objs if o.tag in NOUN_TAGS]:
                            is_aff = xnor(subj_1.is_aff, verb.is_aff, subj_2.is_aff, obj_1.is_aff, obj_2.is_aff)
                            verb_arg = Argument(verb.canon, ArgCode.TRANS.value, is_aff)
                            obj_1_arg = Argument(obj_1.canon, ArgCode.TRANS.value)
                            obj_2_arg = Argument(obj_2.canon, _noun_arg_code(obj_2))
                            stuples.append(SemanticTuple(subj_1_arg, verb_arg, subj_2_arg, obj_1_arg, obj_2_arg))
                    for prop in obj_1.props:
                        is_aff = xnor(subj_1.is_aff, verb.is_aff, subj_2.is_aff, obj_1.is_aff, prop.is_aff)
                        verb_arg = Argument(verb.canon, ArgCode.TRANS.value, is_aff)
                        obj_1_arg = Argument(obj_1.canon, ArgCode.COP.value)
                        prop_arg = Argument(prop.canon, _prop_arg_code(prop))
                        stuples.append(SemanticTuple(subj_1_arg, verb_arg, subj_2_arg, obj_1_arg, prop_arg))
        return stuples

    def __make_stuples_from_subjs_objs(self, verb):
        """Verb can have no subj, no obj"""
        stuples = []
        if not verb.objs and verb.canon not in self.__not_intransitive:
            # Intransitive forms
            for subj in [s for s in verb.subjs if s.tag in NOUN_TAGS]:
                subj_arg = Argument(subj.canon, _noun_arg_code(subj))
                verb_arg = Argument(verb.canon, ArgCode.INTR.value, xnor(subj.is_aff, verb.is_aff))
                stuples.append(SemanticTuple(subj_arg, verb_arg))
        for obj in [o for o in verb.objs if o.tag in NOUN_TAGS]:
            obj_arg = Argument(obj.canon, _noun_arg_code(obj))
            # Transitive forms
            for subj in [s for s in verb.subjs if s.tag in NOUN_TAGS]:
                subj_arg = Argument(subj.canon, _noun_arg_code(subj))
                verb_arg = Argument(verb.canon, ArgCode.TRANS.value, xnor(subj.is_aff, verb.is_aff, obj.is_aff))
                stuples.append(SemanticTuple(subj_arg, verb_arg, obj_arg))
        return stuples

    def __make_stuples_from_objs(self, verb):
        """Convert to passive form ADJ + NOUN"""
        stuples = []
        if verb.canon not in self.__not_passive:
            for obj in [o for o in verb.objs if o.tag in NOUN_TAGS]:
                obj_arg = Argument(obj.canon, _noun_arg_code(obj))
                if not verb.subjs:
                    is_aff = xnor(verb.is_aff, obj.is_aff)
                else:
                    is_aff = xnor(any([subj.is_aff for subj in verb.subjs]), verb.is_aff, obj.is_aff)
                copula_arg = Argument('be', ArgCode.COP.value, is_aff)
                pp = self.__inflector.past_participle(verb.lemma)
                if verb.particles:
                    pp = cfg.COMPOUND_JOIN.join([pp] + verb.particles)
                adj_arg = Argument(pp, ArgCode.PP.value)
                stuples.append(SemanticTuple(obj_arg, copula_arg, adj_arg))
        return stuples

    @staticmethod
    def __make_stuples_from_iobj(verb):
        stuples = []
        for iobj in [io for io in verb.iobjs if io.tag in NOUN_TAGS]:
            iobj_arg = Argument(iobj.canon, _noun_arg_code(iobj))
            for subj in [s for s in verb.subjs if s.tag in NOUN_TAGS]:
                subj_arg = Argument(subj.canon, _noun_arg_code(subj))
                verb_arg = Argument(verb.canon, ArgCode.REC.value, xnor(subj.is_aff, verb.is_aff, iobj.is_aff))
                stuples.append(SemanticTuple(subj_arg, verb_arg, iobj_arg))
        return stuples

    @staticmethod
    def __make_stuples_from_naked_adjs(noun):
        stuples = []
        noun_arg = Argument(noun.canon, _noun_arg_code(noun))
        for adj in noun.adjs:
            # Passive forms
            copula_arg = Argument('be', ArgCode.COP.value, xnor(adj.is_aff, noun.is_aff))
            adj_arg = Argument(adj.canon, _adj_arg_code(adj))
            stuples.append(SemanticTuple(noun_arg, copula_arg, adj_arg))
            # Active forms
            if adj.active_verb:
                for agent in [a for a in adj.agents if a.tag in NOUN_TAGS]:
                    is_aff = xnor(agent.is_aff, adj.is_aff, noun.is_aff)
                    verb_arg = Argument(adj.active_verb, ArgCode.TRANS.value, is_aff)
                    agent_arg = Argument(agent.canon, _noun_arg_code(agent))
                    stuples.append(SemanticTuple(agent_arg, verb_arg, noun_arg))
        return stuples

    @staticmethod
    def __make_stuples_from_pp_props(noun):
        stuples = []
        noun_arg = Argument(noun.canon, _noun_arg_code(noun))
        for pp, prop in [(pp, p) for pp, p in noun.pps_props if p.tag in PROP_TAGS]:
            is_aff = xnor(noun.is_aff, pp.is_aff, prop.is_aff)
            copula_arg = Argument(' '.join(['be', pp.canon]), ArgCode.COP.value, is_aff)
            prop_arg = Argument(prop.canon, _prop_arg_code(prop))
            stuples.append(SemanticTuple(noun_arg, copula_arg, prop_arg))
        return stuples

    @staticmethod
    def __make_stuples_from_copula_props(noun):
        stuples = []
        noun_arg = Argument(noun.canon, _noun_arg_code(noun))
        for copula, prop in [(c, p) for c, p in noun.copulas_props if p.tag in PROP_TAGS]:
            # Passive forms
            is_aff = xnor(noun.is_aff, copula.is_aff, prop.is_aff)
            copula_arg = Argument(copula.canon, ArgCode.COP.value, is_aff)
            prop_arg = Argument(prop.canon, _prop_arg_code(prop))
            stuples.append(SemanticTuple(noun_arg, copula_arg, prop_arg))
            # Active forms
            if prop.tag == Tag.ADJ and prop.active_verb:
                for agent in [a for a in prop.agents if a.tag in NOUN_TAGS]:
                    is_aff = xnor(agent.is_aff, prop.is_aff, noun.is_aff)
                    verb_arg = Argument(prop.active_verb, ArgCode.TRANS.value, is_aff)
                    agent_arg = Argument(agent.canon, _noun_arg_code(agent))
                    stuples.append(SemanticTuple(agent_arg, verb_arg, noun_arg))
        return stuples

    def __make_stuples_from_iprops(self, noun):
        stuples = []
        noun_arg = Argument(noun.canon, _noun_arg_code(noun))
        for subj, verb, iprop in [(s, v, i) for s, v, i in noun.subjs_verbs_iprops if i.tag in PROP_TAGS]:
            if subj is None:
                is_aff = xnor(verb.is_aff, noun.is_aff, iprop.is_aff)
            else:
                is_aff = xnor(subj.is_aff, verb.is_aff, noun.is_aff, iprop.is_aff)
            pp = self.__inflector.past_participle(verb.lemma)
            if verb.particles:
                pp = cfg.COMPOUND_JOIN.join([pp] + verb.particles)
            copula_arg = Argument(' '.join(['be', pp]), ArgCode.COP.value, is_aff)
            iprop_arg = Argument(iprop.canon, _prop_arg_code(iprop))
            stuples.append(SemanticTuple(noun_arg, copula_arg, iprop_arg))
        return stuples
