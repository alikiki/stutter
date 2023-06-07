import math
import operator as op

List = list
Env = dict
Number = (int, float)
Symbol = str


def eval(prog, env):
    if isinstance(prog, Symbol):
        return env.find(prog)[prog]
    elif not isinstance(prog, List):
        return prog

    op, *args = prog
    if op == "quote":
        return args[0]
    elif op == "if":
        test, conseq, alt = args
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)
    elif op == "define":
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op == "set!":
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == "lambda":
        (params, body) = args
        return Procedure(params, body, env)
    else:
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)


class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)


class Procedure:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.params, args, self.env))


def tokenize(chars):
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def parse_token(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF")

    token = tokens.pop(0)
    if token == "(":
        ast = []
        while tokens[0] != ")":
            ast.append(parse_token(tokens))
        tokens.pop(0)
        return ast
    elif token == ")":
        raise SyntaxError("Unexpected )")
    else:
        return atom(token)


def parse(prog):
    return parse_token(tokenize(prog))


def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        "+": op.add,
        "-": op.sub,
        "*": op.mul,
        "/": op.truediv,
        ">": op.gt,
        ">=": op.ge,
        "<": op.lt,
        "<=": op.le,
        "=": op.eq,
        "abs": abs,
        "apply": lambda proc, args: proc(*args),
        "begin": lambda *x: x[-1],  # get the last arg of a list of args
        "car": lambda x: x[0],
        "cdr": lambda x: x[1:],
        "cons": lambda x, y: [x] + y,
        "eq?": op.is_,
        "expt": math.pow,
        "equal?": op.eq,
        "length": len,
        "list": lambda *x: List(x),
        "list?": lambda x: isinstance(x, List),
        "map": map,
        "min": min,
        "max": max,
        "not": op.not_,
        "null?": lambda x: x == [],
        "number?": lambda x: isinstance(x, Number),
        "print": print,
        "procedure": callable,
        "round": round,
        "symbol?": lambda x: isinstance(x, Symbol)
    })

    return env


if __name__ == "__main__":
    global_env = standard_env()
    while True:
        try:
            x = input("stutter> ")
            print(eval(parse(x), env=global_env))
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)
        except KeyError as e:
            print(e)
        except AttributeError as e:
            print(e)
