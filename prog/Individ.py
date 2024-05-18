#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def get_train():
    """
    Запросить данные.
    """
    departure_point = input("Пункт отправления поезда? ")
    number_train = input("Номер поезда? ")
    time_departure = input("Время отправления? ")
    destination = input("Пункт назначения? ")
    return {
        'departure_point': departure_point,
        'number_train': number_train,
        'time_departure': time_departure,
        'destination': destination,
    }


def display_trains(staff):
    """
    Отобразить список поездов.
    """
    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 13,
            '-' * 18,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^13} | {:^18} | {:^14} |'.format(
                "№",
                "Пункт отправления",
                "Номер поезда",
                "Время отправления",
                "Пункт назначения")
        )
        print(line)

        for idx, points in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<13} | {:>18} | {:^14} |'.format(
                    idx, points.get('departure_point', ''),
                    points.get('number_train', ''),
                    points.get('time_departure', ''),
                    points.get('destination', ''))
            )
        print(line)
    else:
        print("Список станций пуст.")


def select_trains(staff, point_user):
    """
    Выбрать нужный поезд.
    """
    result = []
    for train in staff:
        if point_user.lower() == train['destination'].lower():
            result.append(train)

    return result


def save_trains(file_name, staff):
    """
    Сохранить в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_trains(file_name):
    """
    Загрузить из файла JSON и валидировать его.
    """
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "departure_point": {"type": "string"},
                "number_train": {"type": "string"},
                "time_departure": {"type": "string"},
                "destination": {"type": "string"},
            },
            "required": [
                "departure_point",
                "number_train",
                "time_departure",
                "destination",
            ],
        },
    }

    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)  # чтение данных из файла

    try:
        # Валидация файла
        validate(instance=data, schema=schema)
        print("JSON-файл прошел валидацию.")
    except ValidationError as e:
        print(f"Ошибка валидации {e.message}")
    return data


def main():
    """
    Главная функция программы.
    """
    # Список поездов.
    trains = []
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()
        # Выполнить действие в соответствие с командой.
        if command == "exit":
            break

        elif command == "add":
            # Запросить данные о поезде.
            train = get_train()
            # Добавить словарь в список.
            trains.append(train)
            # Отсортировать список в случае необходимости по времени отправления поезда.
            if len(trains) > 1:
                trains.sort(key=lambda item: item.get('time_departure', ''))

        elif command == "list":
            # Отобразить все поезда.
            display_trains(trains)
        elif command.startswith("select "):
            # Разбить команду на части для выделения станции.
            point_command = command.split(maxsplit=1)
            point_user = point_command[1]
            # Выбрать поезда с заданным пунктом назначения.
            selected = select_trains(trains, point_user)
            # Отобразить выбранные поезда.
            display_trains(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_trains(file_name, trains)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Загрузить данные из файла с заданным именем.
            trains = load_trains(file_name)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить поезд;")
            print("list - вывести список поездов;")
            print("select <станция> - запросить поезда направляющиеся в пункт;")
            print("help - отобразить справку;")
            print("load <имя файла> - загрузить данные из файла;")
            print("save <имя файла> - сохранить данные в файл;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()