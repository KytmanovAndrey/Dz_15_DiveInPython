"""
Возьмите любые 1-3 задания из прошлых домашних заданий. Добавьте к ним логирование ошибок и полезной информации.
Также реализуйте возможность запуска из командной строки с передачей параметров. Данная промежуточная аттестация
оценивается по системе "зачет" / "не зачет" "Зачет" ставится, если Слушатель успешно выполнил задание. "Незачет"
ставится, если Слушатель не выполнил задание. Критерии оценивания: 1 - Слушатель написал корректный код для задачи,
добавил к ним логирование ошибок и полезной информации.
"""

# Управление информацией о сотрудниках и их возрасте Семинар 13 Задача 3
#
# В организации есть два типа людей: сотрудники и обычные люди.
# Каждый человек (и сотрудник, и обычный) имеет следующие атрибуты:
#
# Фамилия (строка, не пустая) Имя (строка, не пустая) Отчество (строка, не пустая)
# Возраст (целое положительное число) Сотрудники имеют также уникальный идентификационный номер (ID),
# который должен быть шестизначным положительным целым числом.
#
# Ваша задача:
#
# Создать класс Person, который будет иметь атрибуты и методы для управления данными о людях
# (Фамилия, Имя, Отчество, Возраст). Класс должен проверять валидность входных данных и
# генерировать исключения InvalidNameError и InvalidAgeError, если данные неверные.
#
# Создать класс Employee, который будет наследовать класс Person и добавлять уникальный идентификационный номер (ID).
# ласс Employee также должен проверять валидность ID и генерировать исключение InvalidIdError, если ID неверный.
#
# Добавить метод birthday в класс Person, который будет увеличивать возраст человека на 1 год.
#
# Добавить метод get_level в класс Employee, который будет возвращать уровень сотрудника на основе суммы цифр
# в его ID (по остатку от деления на 7).
#
# Создать несколько объектов класса Person и Employee с разными данными и проверить,
# что исключения работают корректно при передаче неверных данных.

import logging
import argparse

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" ' \
         'в строке {lineno:03d} функция "{funcName}()" ' \
         'в {created} секунд записала сообщение: {msg}'

logging.basicConfig(format=FORMAT, style='{', level=logging.NOTSET, filemode='a', filename='task_01dz.log',
                    encoding='utf-8')
logger = logging.getLogger('task_01dz')


class InvalidNameError(ValueError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        logger.critical(f'Invalid name: {self.name}. Name should be a non-empty string.')
        return f'Invalid name: {self.name}. Name should be a non-empty string.'


class InvalidAgeError(ValueError):
    def __init__(self, age):
        self.age = age

    def __str__(self):
        logger.critical(f'Invalid age: {self.age}. Age should be a positive integer.')
        return f'Invalid age: {self.age}. Age should be a positive integer.'


class InvalidIdError(ValueError):
    def __init__(self, emp_id):
        self.emp_id = emp_id

    def __str__(self):
        logger.critical(f'Invalid emp_id: {self.emp_id}. Id should be a 6-digit positive integer '
                        f'between 100000 and 999999.')
        return f'Invalid emp_id: {self.emp_id}. Id should be a 6-digit positive integer between 100000 and 999999.'


class Person:
    def __init__(self, last_name: str, first_name: str, patronymic: str, age: int):
        if not isinstance(last_name, str) or len(last_name.strip()) == 0:
            raise InvalidNameError(last_name)
        if not isinstance(first_name, str) or len(first_name.strip()) == 0:
            raise InvalidNameError(first_name)
        if not isinstance(patronymic, str) or len(patronymic.strip()) == 0:
            raise InvalidNameError(patronymic)
        if not isinstance(age, int) or age <= 0:
            raise InvalidAgeError(age)

        self.last_name = last_name.title()
        self.first_name = first_name.title()
        self.patronymic = patronymic.title()
        self._age = age

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def birthday(self):
        if self._age >= 99:
            logger.error(f'Person {self.full_name()} reached limit of age. Unable to increase.')
        else:
            self._age += 1
            logger.info(f'Person {self.full_name()} increased age to {self._age}.')

    def get_age(self):
        return self._age


class Employee(Person):
    MAX_LEVEL = 7

    def __init__(self, last_name: str, first_name: str, patronymic: str, age: int, emp_id: int):
        super().__init__(last_name, first_name, patronymic, age)
        if not isinstance(emp_id, int) or emp_id < 100_000 or emp_id > 999_999:
            raise InvalidIdError(emp_id)

        self.emp_id = emp_id
        logger.info(f'Employee {self.full_name(), self.get_age()} with id {self.emp_id} created.')

    def get_level(self):
        s = sum(int(num) for num in str(self.emp_id))
        level = s % self.MAX_LEVEL
        logger.info(f'Employee {self.full_name(), self.get_age()} with {self.emp_id} received {level} level.')
        return level


def parse():
    parser = argparse.ArgumentParser(description='Введите ФИО, возраст, id',
                                     epilog='Пример: python task_01dz.py Bob Johnson Brown 100 234567')
    parser.add_argument('l', help='Фамилия')
    parser.add_argument('f', help='Имя')
    parser.add_argument('p', help='Отчество')
    parser.add_argument('a', help='Возраст')
    parser.add_argument('i', help='Идентификатор шестизначный')
    args = parser.parse_args()
    args.a = int(args.a)
    if args.a >= 100:
        logger.error(f'Entered wrong age {args.a} via terminal')
        args.a = 99
    emp_01 = Employee(args.l, args.f, args.p, int(args.a), int(args.i))
    print(f'{emp_01.full_name()}, age - {emp_01.get_age()}, id - {emp_01.emp_id}, level - {emp_01.get_level()}')


# python task_01dz.py Bob Johnson Brown 100 234567
# python task_01dz.py Ivanov Ivan Ivanovic 40 1234567

if __name__ == '__main__':
    parse()

    # employee1 = Employee("Bob", "Johnson", "Brown", 98, 234567)
    # employee1.birthday()
    # employee1.get_level()
    # employee1.birthday()
    # employee2 = Employee("Ivanov", "Ivan", "Ivanovic", 40, 1234567)
