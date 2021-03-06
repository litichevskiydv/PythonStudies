import json
import functools


# Основной код декоратора
def to_json(func):
    @functools.wraps(func)  # Вызов специяльного декоратора, который сохранит имя декорируемой фнкции в стеке вызовов
    # Создание новой функции, в качестве параметров передаются аргументы лекорируемой функции
    def func_wrapper(*args, **kwds):
        # Получение значение декорируемой функции
        value = func(*args, **kwds)

        # Если полученное значение не содержит свойство __dict__, то оно является экземпляром
        # одного из примитивных типов языка. Его можно сериализовать без всяких ухищрений
        if not hasattr(value, '__dict__'):
            return json.dumps(value)

        # Если полученное значение содержит свойство __dict__, то оно является экземпояром некоторого класса.
        # Поэтому сериализуется его свойство __dict__ (в нем хранятся заданные пользователем значения)
        return json.dumps(value.__dict__)

    # Возвращается созданная функция
    return func_wrapper


@to_json
def get_data(value):
    return {'data': value}


def main():
    print(get_data(543))


if __name__ == '__main__':
    main()
