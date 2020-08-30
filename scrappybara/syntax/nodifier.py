"""The nodification process happens right after parsing.
It creates a new tree with syntactic node objects by flattening proper nouns & verbs with particles.
"""

import scrappybara.config as cfg
from scrappybara.syntax.dependencies import Dep, FUNCTIONAL_DEPS
from scrappybara.syntax.node import Node
from scrappybara.utils.tree import Tree


class Nodifier(object):

    def __call__(self, tokens, tags, idx_tree):
        # EDGE CASES
        # No node
        if idx_tree is None:
            return {}, None
        # Only root
        if len(idx_tree) == 1:
            root_node = Node(idx_tree.root, tokens[idx_tree.root], tags[idx_tree.root])
            return {idx_tree.root: root_node}, Tree(root_node)
        # STANDARD CASES
        node_dict = {}  # first_idx => (dep, node)
        bl_idxs = set()  # Black list of token indexes (flat, particles, NODEP)
        # Detect NODEPs
        for idx, _ in enumerate(tokens):
            if not idx_tree.has_node(idx):
                bl_idxs.add(idx)
        # Flatten tokens
        for idx, token in enumerate(tokens):
            if not idx_tree.children(idx):
                dep_idx = idx_tree.parent(idx)
                if dep_idx is not None:
                    dep, parent_idx = dep_idx
                    if dep == Dep.FLAT:
                        anc_branch = idx_tree.ancestors_via(idx, Dep.FLAT)
                        anc_idx = anc_branch[0]
                        bl_idxs |= set([idx] + anc_branch)
                        flat_tokens = [tokens[i] for i in anc_branch] + [token]
                        node_dict[anc_idx] = Node(idx, cfg.COMPOUND_JOIN.join(flat_tokens), tags[idx])
        # Make verb/adj with particles
        for idx, token in enumerate(tokens):
            particle_idxs = []
            for child_dep, child_idx in idx_tree.children(idx):
                if child_dep == Dep.PART:
                    particle_idxs.append(child_idx)
            if particle_idxs:
                bl_idxs |= set(particle_idxs)
                node = Node(idx, token, tags[idx])
                for i in sorted(particle_idxs):
                    if i > idx:
                        node.particles.append(tokens[i].lower())
                    elif tokens[i].lower() == 'to':
                        node.is_inf_to = True
                node_dict[idx] = node
        # Make remaining nodes
        for idx, token in enumerate(tokens):
            if idx not in node_dict and idx not in bl_idxs:
                node_dict[idx] = Node(idx, token, tags[idx])
        # Make new parse tree
        node_tree = Tree(node_dict[idx_tree.root])
        for idx, node in node_dict.items():
            for child_dep, child_idx in idx_tree.children(idx):
                if child_idx in node_dict:
                    node_tree.register_child(child_dep, node, node_dict[child_idx])
        # Delete functional nodes (only keep nodes that carry meaning)
        node_dict = {node.idx: node for node in node_dict.values() if
                     not node_tree.has_parent_via_set(node, FUNCTIONAL_DEPS)}
        return node_dict, node_tree
