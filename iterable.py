from itertools import groupby, chain


class Record:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return '<key: {0} value: {1}>'.format(self.key, self.value)

    def __repr__(self):
        return str(self)


def key_selector(record):
    return record.key


def mapper(group_iterator):
    key = group_iterator[0]
    group = list(group_iterator[1])
    return key, group, sum(map(lambda record: record.value, group)) / len(group)


def main():
    records = [
        Record(50, 1),
        Record(20, 1),
        Record(20, 0),
        Record(20, 1),
        Record(50, 0),
        Record(50, 1),
        Record(50, 1),
        Record(10, 1),
        Record(10, 0),
        Record(10, 1),
    ]
    print(records)

    sorted_records = sorted(records, key=key_selector)
    print(
        list(
            chain.from_iterable(
                map(
                    lambda item: item[1],
                    sorted(
                        map(
                            mapper,
                            groupby(sorted_records, key_selector)
                        ),
                        key=lambda item: (-item[2], item[0])
                    )
                )
            )
        )
    )


if __name__ == '__main__':
    main()
