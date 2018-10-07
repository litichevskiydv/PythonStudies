class Matrix:
    def __init__(self, values):
        self.values = [[x for x in row] for row in values]

        self._rows_count = len(self.values)
        self._columns_count = 0 if self._rows_count == 0 \
            else len(self.values[0])

    def __str__(self):
        return '\n'.join('\t'.join(str(x) for x in row)
                         for row in self.values)

    def __add__(self, other):
        return Matrix(
            map(
                lambda self_row, other_row:
                map(lambda x, y: x + y, self_row, other_row),
                self.values,
                other.values
            )
        )

    def __mul__(self, number):
        return Matrix([[number * x for x in row]
                       for row in self.values])

    def __rmul__(self, number):
        return self.__mul__(number)

    def size(self):
        return self._rows_count, self._columns_count


def main():
    # Task 2 check 1
    m = Matrix([[10, 10], [0, 0], [1, 1]])
    print(m.size())

    # Task 2 check 2
    m1 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    m2 = Matrix([[0, 1, 0], [20, 0, -1], [-1, -2, 0]])
    print(m1 + m2)

    # Task 2 check 3
    m = Matrix([[1, 1, 0], [0, 2, 10], [10, 15, 30]])
    alpha = 15
    print(m * alpha)
    print(alpha * m)


if __name__ == '__main__':
    main()
