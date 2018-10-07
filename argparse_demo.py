import argparse


# Программа запускается с аргументами --key 123 --val 456
def main():
    # Объявляем класс парсера
    parser = argparse.ArgumentParser()

    # Объявляем имена передаваемых аргументов
    parser.add_argument('--key')
    parser.add_argument('--val')

    # Парсим переданные аргументы
    args = parser.parse_args()

    # Получаем результаты парсинга
    key = args.key
    value = args.val

    if key is None:
        print('Key is None')
    else:
        print('Key={}'.format(key))

    if value is None:
        print('Value is None')
    else:
        print('Value={}'.format(value))


if __name__ == '__main__':
    main()
