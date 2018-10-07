class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        super().__init__('Matrices dimensions are not equal')

        self.matrix1 = matrix1
        self.matrix2 = matrix2


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
        if self.size() != other.size():
            raise MatrixError(self, other)

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

    def transpose(self):
        values = []
        for j in range(0, self._columns_count):
            values.append([None] * self._rows_count)

        for i in range(0, self._rows_count):
            for j in range(0, self._columns_count):
                values[j][i] = self.values[i][j]

        self.values = values
        self._rows_count = len(self.values)
        self._columns_count = 0 if self._rows_count == 0 \
            else len(self.values[0])
        return self

    @staticmethod
    def transposed(matrix):
        return Matrix(matrix.values).transpose()


def main():
    # Task 3 check 1
    # Check exception to add method
    m1 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    m2 = Matrix([[0, 1, 0], [20, 0, -1], [-1, -2, 0]])
    print(m1 + m2)

    m2 = Matrix([[0, 1, 0], [20, 0, -1]])
    try:
        m = m1 + m2
        print('WA\n' + str(m))
    except MatrixError as e:
        print(e.matrix1)
        print(e.matrix2)

    print('--------------------------')
    # Task 3 check 2
    m = Matrix([[10, 10], [0, 0], [1, 1]])
    print(m)
    m1 = m.transpose()
    print(m)
    print(m1)

    print('--------------------------')
    # Task 3 check 3
    m = Matrix([[10, 10], [0, 0], [1, 1]])
    print(m)
    print(Matrix.transposed(m))
    print(m)


if __name__ == '__main__':
    main()
