import os
import argparse
import tempfile
import json


# Функция для чтения данных из хранилища
def get_data(storage_path, key):
    # Читатаем словарь из файла
    with open(storage_path, 'r') as storage:
        dictionary = json.load(storage)

    # В зависимости от того, есть ли нужный ключ, возвращаем либо список значений, либо None
    if key in dictionary:
        return dictionary[key]
    return None


# Функция для записи данных в хранилище
def set_data(storage_path, key, value):
    # Читатаем словарь из файла
    with open(storage_path, 'r') as storage:
        dictionary = json.load(storage)

    # Если ключа нет, то добавляем в словарь пустой список
    if key not in dictionary:
        dictionary[key] = []
    # Добавляем значение в писок
    dictionary[key].append(value)

    # Записываем словарь в хранилище
    with open(storage_path, 'w') as storage:
        json.dump(dictionary, storage)


def main():
    # Объявляем класс парсера
    parser = argparse.ArgumentParser(add_help=True, description='KeyValue storage utility')

    # Объявляем имена передаваемых аргументов
    parser.add_argument('--key', required=True, help='Storage key')
    parser.add_argument('--val', help='Value for storage key')

    # Парсим переданные аргументы
    args = parser.parse_args()

    # Получаем результаты парсинга
    key = args.key
    value = args.val

    # Создаем во временной папке директорию под свои файлы
    files_directory = os.path.join(tempfile.gettempdir(), 'key_value_storage')
    if not os.path.exists(files_directory):
        os.makedirs(files_directory)

    # Если файла нет, то создаем его и записываем туда пустой словарь
    storage_path = os.path.join(files_directory, 'storage.data')
    if not os.path.exists(storage_path):
        with open(storage_path, 'w+') as storage:
            json.dump({}, storage)

    if value is None:
        # Получаем данные из хранилища
        stored_values = get_data(storage_path, key)

        # В зависимости от того, были ли добавлены значения, выводим разные результаты
        if stored_values is not None:
            print(', '.join(stored_values))
        else:
            print(stored_values)
    else:
        # Записываем данные в хранилище
        set_data(storage_path, key, value)


if __name__ == '__main__':
    main()
