import json
import string


def main():
    key_str = string.ascii_uppercase
    print(key_str)

    n = 0
    for m in key_str:
        n += 1
        test_dict = (m, n)
        print(test_dict)
        # В файл записываем пары через запятую. Писать словари нет смысла,
        # поскольку в них всегда будет по одному ключу
        test_dict_json = json.dumps(test_dict) + ','
        print(test_dict_json)
        # Для дозаписи используем режим a+. Если файла нет, то он создастся, если есть - то откроется
        # и запись будет проихводиться в конец
        with open('test_dict_json2.txt', 'a+') as f:
            f.write(test_dict_json)

    # При чтении данных их файл убираем лишнюю запятую после последней пары
    # и окаймляем квадратными скобками, чтобы десериализовывать данные как массив пар
    with open('test_dict_json2.txt', 'r') as f:
        json_data = '[' + f.read().strip(',') + ']'

    # Десириализовываем данные как массив пар.
    # После этой операции для поиска данных по заданному ключц нужно перебрать все пары в файле
    parsed_json = json.loads(json_data)
    print(type(parsed_json), parsed_json)


if __name__ == '__main__':
    main()
