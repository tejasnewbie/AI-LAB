import copy

def unify(x, y, subst):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif is_variable(x):
        return unify_var(x, y, subst)
    elif is_variable(y):
        return unify_var(y, x, subst)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return None
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    else:
        return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif occur_check(var, x, subst):
        return None
    else:
        new_subst = subst.copy()
        new_subst[var] = x
        return new_subst

def occur_check(var, x, subst):
    if var == x:
        return True
    elif isinstance(x, list):
        return any(occur_check(var, xi, subst) for xi in x)
    elif isinstance(x, str) and x in subst:
        return occur_check(var, subst[x], subst)
    return False

def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def negate(literal):
    return literal[1:] if literal[0] == '~' else '~' + literal

def apply_subst(clause, subst):
    new_clause = []
    for lit in clause:
        pred, args = parse_literal(lit)
        new_args = []
        for a in args:
            new_args.append(subst.get(a, a))
        new_clause.append(pred + "(" + ",".join(new_args) + ")")
    return new_clause

def parse_literal(literal):
    if literal[0] == '~':
        pred = "~" + literal[1:literal.index("(")]
    else:
        pred = literal[:literal.index("(")]
    args = literal[literal.index("(")+1:literal.index(")")].split(",")
    return pred, args

def resolve(ci, cj):
    resolvents = []
    for li in ci:
        for lj in cj:
            if negate(li.split("(")[0]) == lj.split("(")[0] or negate(lj.split("(")[0]) == li.split("(")[0]:
                pi, args_i = parse_literal(li)
                pj, args_j = parse_literal(lj)
                subst = unify(args_i, args_j, {})
                if subst is not None:
                    new_ci = [l for l in ci if l != li]
                    new_cj = [l for l in cj if l != lj]
                    resolvent = apply_subst(new_ci + new_cj, subst)
                    resolvent = list(set(resolvent))
                    resolvents.append(resolvent)
    return resolvents

def resolution(kb):
    clauses = copy.deepcopy(kb)
    new = []
    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1, len(clauses))]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if [] in resolvents:
                print("UNSAT")
                return True
            new.extend(resolvents)
        new_unique = [c for c in new if c not in clauses]
        if not new_unique:
            print("SAT")
            return False
        clauses.extend(new_unique)
