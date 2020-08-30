"""This process attaches core dependents to syntactic nodes.
Aggregations are also detected here.
"""
from scrappybara.normalization.suffixes import Suffix
from scrappybara.syntax.dependencies import Dep, MARKER_DEPS
from scrappybara.syntax.tags import Tag, NOUN_TAGS


def _register_subjs(verb, subj, tree):
    verbs = [verb]
    for v in verb.cconjs:
        if not tree.has_child_via(v, Dep.SUBJ):
            verbs.append(v)
    for v in verbs:
        v.subjs.extend(subj.aggreg)


def _register_objs(verb, obj, tree):
    verbs = [verb]
    for v in verb.cconjs:
        if not tree.children(v):
            verbs.append(v)
    for v in verbs:
        v.objs.extend(obj.aggreg)


def _register_iobjs(verb, iobj):
    verb.iobjs.extend(iobj.aggreg)


def _register_exists(verb, exist):
    verb.exists.extend(exist.aggreg)


def _register_adjs(noun, adj):
    noun.adjs.extend(adj.aggreg)


def _register_props_via_pp(noun, pp, prop):
    for p in prop.aggreg:
        noun.pps_props.append((pp, p))


def _register_props_via_copula(subj, copula, prop, tree):
    for s, p in [(s, p) for s in subj.aggreg for p in prop.aggreg if not tree.has_child_via_set(p, MARKER_DEPS)]:
        s.copulas_props.append((copula, p))


def _register_iprops(verb, iprop, tree):
    # Register to verb
    verb.iprops.extend(iprop.aggreg)
    # Register to owner
    obj = tree.child_via(verb, Dep.OBJ)
    subj = tree.child_via(verb, Dep.SUBJ)
    if obj is not None:
        for o, ip in [(o, ip) for o in obj.aggreg for ip in iprop.aggreg]:
            o.subjs_verbs_iprops.append((subj, verb, ip))


def _register_agents(describee, cpl, marker, tree):
    """We distribute the complements to the describees only.
    We don't distribute the describees to the complements.
    """
    for cpl in cpl.aggreg:
        if marker.canon == 'by':
            dep_parent = tree.parent(describee)
            if dep_parent is not None:
                dep, _ = dep_parent
                if dep in {Dep.PROP, Dep.CPL}:
                    describee.agents.append(cpl)


class ArgFinder(object):
    __reflexive_pronouns = {'myself', 'yourself', 'yourselves', 'himself', 'herself', 'itself', 'ourself', 'ourselves',
                            'theirself', 'themselves', 'oneself'}
    __relative_pronouns = {'that', 'which', 'who'}

    def __call__(self, nodes, tree):
        """Registers core dependents to each node"""
        # AGGREGATIONS
        for node in nodes:
            node.and_cconjs = tree.children_via(node, Dep.AND)
            node.or_cconjs = tree.children_via(node, Dep.OR)
        # DIRECT DEPENDENCIES
        naked_cpls = set()
        marked_cpls = set()
        for node in nodes:
            is_cpl = False
            # Analyze parent
            dep_parent = tree.parent(node)
            if dep_parent is not None:
                dep, parent = dep_parent
                if dep == Dep.SUBJ:
                    ref = self.__resolve_relative_pron(parent, node, tree) or \
                          self.__resolve_subj_reflexive_pron(parent, node, tree)
                    if ref:
                        _register_subjs(parent, ref, tree)
                    else:
                        _register_subjs(parent, node, tree)
                elif dep == Dep.OBJ:
                    ref = self.__resolve_relative_pron(parent, node, tree) or \
                          self.__resolve_obj_reflexive_pron(parent, node, tree)
                    if ref:
                        _register_objs(parent, ref, tree)
                    else:
                        _register_objs(parent, node, tree)
                elif dep == Dep.IOBJ:
                    _register_iobjs(parent, node)
                elif dep == Dep.EXIST:
                    _register_exists(parent, node)
                elif dep == Dep.PROP:
                    parent.props.extend(node.aggreg)
                    subj = tree.child_via(parent, Dep.SUBJ)
                    if subj:
                        ref = self.__resolve_relative_pron(parent, subj, tree)
                        if ref:
                            _register_props_via_copula(ref, parent, node, tree)
                        else:
                            _register_props_via_copula(subj, parent, node, tree)
                elif dep == Dep.IPROP:
                    _register_iprops(parent, node, tree)
                elif dep == Dep.CPL:
                    is_cpl = True
            # Analyze children
            mark = tree.child_via(node, Dep.MARK)
            cmark = tree.child_via(node, Dep.CMARK)
            imark = tree.child_via(node, Dep.IMARK)
            for dep, child in tree.children(node):
                if dep == Dep.NEG:
                    node.is_aff = False
            # Analyze node
            if is_cpl:
                parent = dep_parent[1]
                # Naked complement
                if not any([mark, imark, cmark]):
                    naked_cpls.add(node)
                # Marker
                if mark is None:
                    if node.tag == Tag.ADJ:
                        _register_adjs(parent, node)
                        if parent.tag in NOUN_TAGS:
                            prop = tree.child_via(node, Dep.PROP)
                            if prop is not None and node.suffix == Suffix.PAST:
                                _register_props_via_pp(parent, node, prop)
                else:
                    marked_cpls.add(node)
                    _register_agents(parent, node, mark, tree)
                # Comparative marker
                if cmark is not None and parent.tag == Tag.ADJ and node.tag in NOUN_TAGS:
                    _register_adjs(node, parent)
        # LONG-DISTANCE DEPENDENCIES
        for node in nodes:
            dep_parent = tree.parent(node)
            if dep_parent is not None:
                dep, parent = dep_parent
                if all([node in marked_cpls, node.tag == Tag.VERB, not tree.has_child_via(node, Dep.SUBJ),
                          parent.tag == Tag.VERB]):
                    subj = tree.child_via(parent, Dep.SUBJ)
                    if subj:
                        # Subject to marked complement: e.g. "I ate but didn't drink"
                        _register_subjs(node, subj, tree)
                elif all([node in naked_cpls, parent.tag in NOUN_TAGS, not tree.has_child_via(node, Dep.OBJ)]):
                    subj = tree.child_via(node, Dep.SUBJ)
                    if subj and subj.canon not in self.__relative_pronouns:
                        # Object of complement verb: e.g. "the apple I ate"
                        _register_objs(node, parent, tree)

    # PRONOUN RESOLUTION
    # -------------------------------------------------------------------------->

    def __resolve_relative_pron(self, verb, pron, tree):
        """Tries to find the referent node of a relative pronoun"""
        dep_parent = tree.parent(verb)
        if dep_parent is not None:
            dep, parent = dep_parent
            if all([pron.tag == Tag.PRON, pron.canon in self.__relative_pronouns, dep == Dep.CPL,
                    parent.tag in NOUN_TAGS,
                    not tree.has_child_via_set(verb, MARKER_DEPS)]):
                return parent
        return None

    def __resolve_obj_reflexive_pron(self, verb, pron, tree):
        """Tries to find the referent node of an object reflexive pronoun.
        e.g. 'You treat [yourself]'
        """
        if pron.canon in self.__reflexive_pronouns:
            subj = tree.child_via(verb, Dep.SUBJ)
            if subj:
                return subj
        return None

    def __resolve_subj_reflexive_pron(self, verb, pron, tree):
        """Tries to find the referent node of a subject reflexive pronoun.
        e.g. 'Parents found [themselves] doubting'
        """
        if pron.canon in self.__reflexive_pronouns:
            dep_parent = tree.parent(verb)
            if dep_parent:
                dep, parent = dep_parent
                if dep == Dep.OBJ and parent.tag == Tag.VERB:
                    subj = tree.child_via(parent, Dep.SUBJ)
                    if subj:
                        return subj
        return None
