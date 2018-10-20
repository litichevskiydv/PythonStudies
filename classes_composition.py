class X:
    def __init__(self):
        self.count = 5
        self.y = Y(self)

    def add2(self):
        self.count += 2


class Y:
    def __init__(self, parent):
        self.parent = parent

    def modify(self):
        self.parent.add2()


x = X()
x.y.modify()
print(x.count)
x1 = X()
x1.y.modify()
print(x1.count)
