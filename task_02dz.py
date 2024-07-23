"""
Возьмите любые 1-3 задания из прошлых домашних заданий. Добавьте к ним логирование ошибок и полезной информации.
Также реализуйте возможность запуска из командной строки с передачей параметров. Данная промежуточная аттестация
оценивается по системе "зачет" / "не зачет" "Зачет" ставится, если Слушатель успешно выполнил задание. "Незачет"
ставится, если Слушатель не выполнил задание. Критерии оценивания: 1 - Слушатель написал корректный код для задачи,
добавил к ним логирование ошибок и полезной информации.
"""
# Преобразование ключей и значений словаря Семинар 4 Задача 2
#
# Напишите функцию key_params, принимающую на вход только ключевые параметры и возвращающую словарь,
# где ключ - значение переданного аргумента, а значение - имя аргумента.
# Если ключ не хешируем, используйте его строковое представление.
#
# Пример использования.
# На входе:
#
#
# params = key_params(a=1, b='hello', c=[1, 2, 3], d={})
# print(params)
#
# На выходе:
#
#
# {1: 'a', 'hello': 'b', '[1, 2, 3]': 'c', '{}': 'd'}

import logging
import argparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('task_02dz')


def key_params(**kwargs):
    inverted_dict = {}
    for key, value in kwargs.items():
        try:
            hash_val = hash(value)
            logger.debug(f'объект {value} имеет адрес в памяти {id(value) = }')
            logger.info(f'объект {value} - хешируемый (immutable), его преобразование в хеш-сумму {hash_val}')
        except TypeError as e:
            logger.error(f'{value} - изменяемый объект, {e}')
            value = str(value)
        inverted_dict[value] = key
    return inverted_dict


def parse():
    parser = argparse.ArgumentParser(
        description="""
        Введите все ключи-значения в виде одной большой строки c двойными кавычками, разделяя ключевые аргументы 
        запятыми и пробелами (как аргументы в скобках у функции в коде Python).
        'Пример: python task_02dz.py "a=\'1\', b=\'hello\', c=[1, 2, 3], d={}, e=2"',
        """,

        epilog='Меняет местами ключ-значение. Если ключ не хешируем, возвращается его строковое представление'
    )
    parser.add_argument('param',
                        help='Пример: python task_02dz.py "a=\'1\', b=\'hello\', c=[1, 2, 3], d={}, e=2"')
    args = parser.parse_args()
    code_str = 'key_params(' + args.param + ')'
    print(eval(code_str))


# python task_02dz.py "a='1', b='hello', c=[1, 2, 3], d={}, e=2"

if __name__ == '__main__':
    parse()

    # params = key_params(a='1', b='hello', c=[1, 2, 3], d={}, e=2)
    # print(params)
