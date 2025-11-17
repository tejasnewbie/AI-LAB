import re
import itertools

VAR_RE = re.compile(r'^[a-z](_\d+)?$')   # single-letter variable optionally standardized (x_0, y_3)

def is_variable(token: str) -> bool:
    return bool(VAR_RE.fullmatch(token))

def parse_literal(text):
    text = text.strip()
    neg = False
    if text.startswith('¬') or text.startswith('~'):
        neg = True
        text = text[1:].strip()
    if '(' in text:
        pred = text[:text.index('(')].strip()
        args = [a.strip() for a in text[text.index('(')+1:-1].split(',')]
    else:
        pred = text
        args = []
    return {'neg': neg, 'pred': pred, 'args': args}

def clause_to_str(clause):
    if clause == []:
        return '⊥'
    parts = []
    for lit in clause:
        s = ('¬' if lit['neg'] else '') + (lit['pred'] + '(' + ', '.join(lit['args']) + ')' if lit['args'] else lit['pred'])
        parts.append(s)
    return ' ∨ '.join(parts)

def standardize_apart_clause(clause, idx):
    # only rename variables (single-letter) to var_index form
    mapping = {}
    new_clause = []
    for lit in clause:
        new_args = []
        for a in lit['args']:
            if is_variable(a):
                if a not in mapping:
                    mapping[a] = f"{a}_{idx}"
                new_args.append(mapping[a])
            else:
                new_args.append(a)
        new_clause.append({'neg': lit['neg'], 'pred': lit['pred'], 'args': new_args})
    return new_clause

# ----- Unification for flat args (no nested function terms) -----
def occurs_check(var, val, subs):
    # var and val are token strings
    if var == val:
        return True
    if is_variable(val) and val in subs:
        return occurs_check(var, subs[val], subs)
    return False

def apply_subs_token(tok, subs):
    if is_variable(tok):
        while tok in subs:
            tok = subs[tok]
        return tok
    return tok

def apply_subs_literal(lit, subs):
    new_args = [apply_subs_token(a, subs) for a in lit['args']]
    return {'neg': lit['neg'], 'pred': lit['pred'], 'args': new_args}

def unify_tokens(x, y, subs):
    # x,y are token strings (variables or constants)
    if x == y:
        return subs
    if is_variable(x):
        if x in subs:
            return unify_tokens(subs[x], y, subs)
        if occurs_check(x, y, subs):
            return None
        new = subs.copy()
        new[x] = y
        return new
    if is_variable(y):
        return unify_tokens(y, x, subs)
    # both constants and different => fail
    return None

def unify_arg_lists(a_list, b_list):
    if len(a_list) != len(b_list):
        return None
    subs = {}
    for a, b in zip(a_list, b_list):
        a_ap = a if not is_variable(a) else a
        b_ap = b if not is_variable(b) else b
        subs = unify_tokens(apply_subs_token(a_ap, subs), apply_subs_token(b_ap, subs), subs)
        if subs is None:
            return None
    return subs

# ----- Resolution -----
def is_tautology_clause(clause):
    # clause is a list of literals (after substitution). If it contains A and ¬A same args -> tautology
    seen = {}
    for lit in clause:
        key = (lit['pred'], tuple(lit['args']))
        if key in seen:
            if seen[key] != lit['neg']:
                return True
        else:
            seen[key] = lit['neg']
    return False

def resolve_pair(c1, c2):
    # c1, c2 are lists of literals (each literal dict)
    for i, l1 in enumerate(c1):
        for j, l2 in enumerate(c2):
            if l1['pred'] == l2['pred'] and l1['neg'] != l2['neg']:
                # try to unify their args
                subs = unify_arg_lists(l1['args'], l2['args'])
                if subs is None:
                    continue
                # apply substitution to the remainder of both clauses
                new_clause = []
                for k, lit in enumerate(c1):
                    if k == i: continue
                    new_clause.append(apply_subs_literal(lit, subs))
                for k, lit in enumerate(c2):
                    if k == j: continue
                    new_clause.append(apply_subs_literal(lit, subs))
                # remove duplicates (syntactic)
                uniq = []
                for lit in new_clause:
                    if not any(lit['pred']==u['pred'] and lit['neg']==u['neg'] and lit['args']==u['args'] for u in uniq):
                        uniq.append(lit)
                if is_tautology_clause(uniq):
                    continue
                return uniq, subs, (i, j)
    return None, None, None

# ----- Build derivation tree nodes -----
class Node:
    def __init__(self, clause, parents=None, label=None):
        self.clause = clause
        self.parents = parents if parents else []
        self.label = label

def resolution_with_tree(initial_clauses, goal_clause):
    # standardize apart initial clauses
    clauses_nodes = []
    for idx, c in enumerate(initial_clauses):
        std = standardize_apart_clause(c, idx)
        clauses_nodes.append(Node(std, parents=[] , label=f"C{idx}"))

    # add negated goal as a fresh clause (standardize apart too)
    neg_goal = []
    # goal_clause is a clause list (we take its first literal if single-literal goal)
    for lit in goal_clause:
        # negate each literal in goal clause (if goal is a single positive literal user passed)
        neg_goal.append({'neg': not lit['neg'], 'pred': lit['pred'], 'args': lit['args'][:]})
    neg_goal_std = standardize_apart_clause(neg_goal, len(clauses_nodes))
    goal_node = Node(neg_goal_std, parents=[], label="¬Goal")
    clauses_nodes.append(goal_node)

    # mapping from index -> Node
    idx = len(clauses_nodes)
    seen_clauses = {clause_to_str(n.clause): i for i, n in enumerate(clauses_nodes)}

    # perform breadth-first-ish resolution (pairwise), record parents as indices
    for a_index in range(len(clauses_nodes)):
        pass  # placeholder, we'll use dynamic loop below

    frontier_changed = True
    while True:
        new_added = False
        # iterate pairs over current clauses
        n = len(clauses_nodes)
        pairs = [(i,j) for i in range(n) for j in range(i+1, n)]
        for i,j in pairs:
            c1 = clauses_nodes[i].clause
            c2 = clauses_nodes[j].clause
            resolvent, subs, which = resolve_pair(c1, c2)
            if resolvent is None:
                continue
            s = clause_to_str(resolvent)
            if s in seen_clauses:
                continue
            # add node
            new_node = Node(resolvent, parents=[i, j], label=f"R{idx}")
            clauses_nodes.append(new_node)
            seen_clauses[s] = idx
            new_added = True
            idx += 1
            if resolvent == []:
                # build bottom-up tree node for ⊥
                root = new_node
                return clauses_nodes, seen_clauses, idx-1  # return nodes, map, index of empty clause node
        if not new_added:
            return clauses_nodes, seen_clauses, None

# ----- ASCII print bottom-up (root bottom) -----
def print_bottom_up_tree(nodes, root_index):
    # recursively print node; ensure parents printed above
    def recurse(node_index, prefix="", is_last=True):
        node = nodes[node_index]
        connector = "└── " if is_last else "├── "
        print(prefix + connector + clause_to_str(node.clause))
        # if this node has parents, print them above (parents as children in recursion so they appear above)
        parents = node.parents
        for k, pidx in enumerate(parents):
            recurse(pidx, prefix + ("    " if is_last else "│   "), k == len(parents)-1)
    recurse(root_index, "", True)

# ----- Runner -----
if __name__ == "__main__":
    print("="*70)
    print("FIRST-ORDER LOGIC RESOLUTION SYSTEM (FIXED)")
    print("="*70)
    print("Enter CNF clauses (one per line). End with a blank line.")
    raw = []
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if line == "":
            break
        raw.append(line)
    clauses = [ [parse_literal(tok.strip()) for tok in re.split(r"∨", line) ] for line in raw ]

    # read goal
    goal_line = input("\nEnter GOAL clause (single literal form): ").strip()
    goal_clause = [parse_literal(goal_line)]

    nodes, seen_map, root_idx = resolution_with_tree(clauses, goal_clause)
    if root_idx is None:
        print("\nNo empty clause could be derived — goal not entailed by KB.")
    else:
        print("\nDERIVATION TREE (bottom-up):")
        print_bottom_up_tree(nodes, root_idx)
        print("\nResolution complete — ⊥ derived.")

     
======================================================================
FIRST-ORDER LOGIC RESOLUTION SYSTEM (FIXED)
======================================================================
Enter CNF clauses (one per line). End with a blank line.
¬human(x) ∨ mortal(x)
human(Socrates)


Enter GOAL clause (single literal form): mortal(Socrates)

DERIVATION TREE (bottom-up):
└── ⊥
    ├── human(Socrates)
    └── ¬human(Socrates)
        ├── ¬human(x_0) ∨ mortal(x_0)
        └── ¬mortal(Socrates)

Resolution complete — ⊥ derived.
