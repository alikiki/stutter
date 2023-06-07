import math
import operator as op

Number = (int, float)
Symbol = str
Env = dict


def tokenize(prg):
    return prg\
        .replace("(", " ( ")\
        .replace(")", " ) ")\
        .split()


def atom(token):
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return Symbol(token)


def parse_token(tokens):
    if not tokens:
        raise ValueError("Unexpected EOF")

    token = tokens.pop(0)
    if token == "(":
        ast = []
        while tokens[0] != ")":
            ast.append(parse_token(tokens))
        tokens.pop(0)
        return ast
    elif token == ")":
        raise ValueError("Unexpected EOF")
    else:
        return atom(token)


def parse(prog):
    return parse_token(tokenize(prog))


if __name__ == "__main__":
    while True:
        x = input("stutter> ")
        print(parse(x))
