import ast

def set_bang(var, val, env):
    env.__setitem__(var.eval(env), val.eval(env))

def let(var_val_pairs, body, env):
    vars_and_vals = zip(var_val_pairs.items)
    vars = var.name for var in vars_and_vals[0]
    vals = val.eval(env) for val in vars_and_vals[1]
    new_lambda = Lambda(vars, body, env)
    new_lambda._apply_evaluated(vals)

def define():
    pass

def _and(*args, env):
    for arg in args:
        if arg.eval(env) == False:
            return ast.Bool("#f")
    return args[-1]

def _or(*args, env):
    for arg in args:
        if arg.eval(env) == True:
            return ast.Bool("#t")
    return ast.Bool("#f")

def _if(condition, true_case, false_case, env):
    if condition.eval(env).eval(env) != "#f":
        return true_case.eval(env)
    elif false_case is None:
        return None()
    else:
        return false_case.eval(env)
