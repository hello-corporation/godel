#!/usr/bin/env python

# =================================
# Gödel's Definition of Computation
#
# The built-in functions of μ-lang.
# =================================

def zero(n):
    """ zero is built-in """
    return 0

def incr(n):
    """ plus one is built-in """
    return n+1

def proj(i, *args):
    """ picking an arg is built-in """
    return args[i]

def comp(f, *hs):
    """ function composition is built-in """
    def g(*args):
        xs = (h(*args) for h in hs)
        return f(*xs)
    return g

def rec(f, g):
    """ recursion is built-in """
    def h(n, *xs):
        if n == 0:
            return f(*xs)
        return g(n-1, h(n-1, *xs), *xs)
    return h

def mu(p):
    """ unbounded while loops are built-in """
    def m(*xs):
        n = 0
        while True:
            if p(n, *xs) == 0:
                return n
            n += 1
    return m



# =========================
# Gödel's Standard Library
#
# Using the μ-lang builtins
# to implement a standard
# library of simple General
# Recursive Functions we'll
# need in order to write a
# compiler that translates
# the formal theory of first
# order (Peano) arithmetic
# into statements about the
# arithmetic of positive
# whole numbers which we can
# then re-express within,
# well, arithmetic. -K.G.
#
# P.S. This time we make
# sure to actually use the
# comp builtin instead of
# all those lambdas from
# before. -K.G.
# =========================

def const(k):
    return lambda *xs: k

# curried version of proj to make
# comp less of a pain to work with
mkproj = lambda i: (lambda *xs: proj(i, *xs))

zero = const(0)
one  = const(1)

id = lambda x: proj(0, x)

# predecessor
pred = rec(zero, lambda n, y: n)

add_base = id
add_step = comp(incr, mkproj(1))
add_raw  = rec(add_base, add_step)
add      = lambda x, y: add_raw(y, x)

mul_base = zero
mul_step = comp(add, mkproj(1), mkproj(2))
mul_raw  = rec(mul_base, mul_step)
mul      = lambda x, y: mul_raw(y, x)

exp_base = one
exp_step = comp(mul, mkproj(1), mkproj(2))
exp_raw  = rec(exp_base, exp_step)
exp      = lambda x, y: exp_raw(y, x)

sub_base = id
sub_step = comp(pred, mkproj(1))
sub_raw  = rec(sub_base, sub_step)
sub      = lambda x, y: sub_raw(y, x)

is_zero = rec(one, comp(zero))

# sign: sign(0) = 0, sign(n) = 1 otherwise
sign = rec(zero, comp(one))

# leq(x,y) is 1 if x <= y else 0
leq = comp(is_zero, sub)

# eq(x,y) is 1 if x == y else 0
eq = comp(mul, leq, comp(leq, mkproj(1), mkproj(0)))

# neq(x,y) : 1 if x != y else 0
neq = comp(sign, comp(sub, one, comp(eq, mkproj(0), mkproj(1))))

# max/min, overriding the python builtins
max = comp(add, comp(sub, mkproj(0), mkproj(1)), mkproj(1))
min = comp(sub, comp(add, mkproj(0), mkproj(1)), comp(max, mkproj(0), mkproj(1)))

def geq(x, y):
    return comp(leq, mkproj(1), mkproj(0))(x, y)

def lt(x, y):
    return comp(sign, comp(sub, mkproj(1), mkproj(0)))(x, y)

def examples():
    return {
        "pred(0)": pred(0),
        "pred(5)": pred(5),
        "add(3,4)": add(3, 4),
        "mul(3,4)": mul(3, 4),
        "exp(2,5)": exp(2, 5),
        "sub(7,10)": sub(7, 10),
        "sub(10,7)": sub(10, 7),
        "is_zero(0)": is_zero(0),
        "is_zero(9)": is_zero(9),
        "leq(3,7)": leq(3, 7),
        "leq(7,3)": leq(7, 3),
        "eq(9,9)": eq(9, 9),
        "eq(9,8)": eq(9, 8),
    }

if __name__ == "__main__":
    for k,v in examples().items():
        print(f"{k} = {v!r}")

