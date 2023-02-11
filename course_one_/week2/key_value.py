""" Вашей задачей будет написать реализацию утилитыstorage.py.

Утилита может вызваться со следующими параметрами:

--key <имя ключа> , где <имя ключа> - ключ по которому сохраняются/получаются значения

--val <значение>, где <значение> - сохраняемое значение.

Если при запуске утилиты переданы оба ключа, происходит добавление переданного значения по ключу и сохранение данных в файле. Если передано только имя ключа, происходит чтение файла хранилища и вывод на печать значений, которые были сохранены по данному ключу.  Обратите внимание, что значения по одному ключу не перезаписываются, а добавляются к уже сохраненным. Другими словами - по одному ключу могут храниться несколько значений. При выводе на печать, значения выводятся в порядке их добавления в хранилище

Поздравляем с первой полноценной программой на Python в рамках нашего курса! Она была заметно сложнее предыдущих и помогла вам разобраться сразу с несколькими моментами. Хорошим подходом было бы разбить свою программу на функции — обратите внимание, все команды вынесены в отдельные функции, а read_data мы используем в нескольких местах. Ключевым моментом в разработке любого приложения является выбор подходящей структуры данных. В этом примере логичным вариантом было использовать словарь, потому что он по сути и является key-value хранилищем, а значения просто хранить в списке.

Также в этом задании мы использовали модуль argparse для считывания аргументов командной строки и json для хранения данных в файле. Самым простым подходом было просто перечитывать при каждом обращении файл, преобразуя его в словарь, добавляя значения при необходимости. Модуль os помогает нам в проверке существования файла хранилища при первом запуске программы. В Python богатая стандартная библиотека, очень важно представлять себе, какие модули помогут нам в решении наших задач, и уметь быстро разбираться в документации к новым функциям.
"""

import argparse
import json
import os
import tempfile


def read_data(storage_path):
    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, 'r') as file:
        raw_data = file.read()
        if raw_data:
            return json.loads(raw_data)
        return {}


def write_data(storage_path, data):
    with open(storage_path, 'w') as f:
        f.write(json.dumps(data))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Key')
    parser.add_argument('--val', help='Value')
    return parser.parse_args()


def put(storage_path, key, value):
    data = read_data(storage_path)
    data[key] = data.get(key, list())
    data[key].append(value)
    write_data(storage_path, data)


def get(storage_path, key):
    data = read_data(storage_path)
    return data.get(key, [])


def main(storage_path):
    args = parse()

    if args.key and args.val:
        put(storage_path, args.key, args.val)
    elif args.key:
        print(*get(storage_path, args.key), sep=', ')
    else:
        print('The program is called with invalid parameters.')


if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    main(storage_path)
