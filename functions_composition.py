def f(x):
    return x + 2


def g(x):
    return x - 3


def compose(f, g):
    return lambda x: f(g(x))


class Composable(object):
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __and__(self, other):
        return Composable(compose(self.fn, other))



print((Composable(lambda x: x * 2) & f & g & g)(17) == 26)
print(compose(f, g)(3) == 2)
print(f(g(3)) == 2)