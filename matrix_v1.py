class Matrix:
    def __init__(self, values):
        self._values = [[x for x in row] for row in values]

        self._rows_count = len(self._values)
        self._columns_count = 0 if self._rows_count == 0 \
            else len(self._values[0])

    def __str__(self):
        return '\n'.join('\t'.join(str(x) for x in row)
                         for row in self._values)

    def size(self):
        return self._rows_count, self._columns_count


def main():
    # Task 1 check 1
    m = Matrix([[1, 0], [0, 1]])
    print(m)
    m = Matrix([[2, 0, 0], [0, 1, 10000]])
    print(m)
    m = Matrix([[-10, 20, 50, 2443], [-5235, 12, 4324, 4234]])
    print(m)

    # Task 1 check 2
    m1 = Matrix([[1, 0, 0], [1, 1, 1], [0, 0, 0]])
    m2 = Matrix([[1, 0, 0], [1, 1, 1], [0, 0, 0]])
    print(str(m1) == str(m2))

    # Task 1 check 3
    m = Matrix([[1, 1, 1], [0, 100, 10]])
    print(str(m) == '1\t1\t1\n0\t100\t10')


if __name__ == '__main__':
    main()
