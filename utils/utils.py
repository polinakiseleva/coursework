import time
import requests
from operator import itemgetter

URL = 'https://file.notion.so/f/s/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?spaceId=0771f0bb-b4cb-4a14-bc05-94cbd33fc70d&table=block&id=f11058ed-10ad-42ea-a13d-aad1945e5421&expirationTimestamp=1678728125732&signature=nJUaFdh0rWbfW6wkhBzipP7HrtRtbqWMqcmIIehJAco&downloadName=operations.json'

def json_get(par):
    """
    Функция для получения исходных данных
    :return: Списковый словарь
    """
    responce = requests.get(par)
    return responce.json()


def check_dict(list_data):
    """
    Функция для проверки наличия пустых словарей в исходном
    :param list_data: Списковый словарь
    :return: Подготовленный списковый словарь без пустых словарей
    """
    list1 = []
    for x in list_data:
        if len(x) != 0:
            list1.append(x)
        else:
            continue
    return list1


def sort_by_time(data_dict, key="date"):
    """
    Функция сортирует словарь по переданному ключу (в нашем случае по дате)
    :param data_dict: Словарь, который нужно отсортировать
    :param key: Ключ, по которому будем сортировать (по умолчанию - дата)
    :return: Отсортированный по дате словарь
    """
    sorted_data = sorted(data_dict, key=itemgetter(key), reverse=True)
    return sorted_data


def date_edit(data_dict):
    """
    Функция преобразовывает полученную дату к стандартному виду
    :param data_dict: Словарь, в котором дата представлена в виде ГГГГ.ММ.ДД
    :return: Словарь, в котором дата представлена в виде ДД.ММ.ГГГГ
    """
    source = data_dict.get('date')
    if source:
        raw_date = source[: source.find('T')]
        format_date = time.strptime(raw_date, "%Y-%m-%d")
        new_format_date = time.strftime("%d.%m.%Y", format_date)
    else:
        new_format_date = 'Ошибка при прочтении даты'
    return new_format_date


def users_account_edit(dict):
    """
    Функция выводит название банковской карты или счета и зашифровывает эту информацию
    :param dict: Словарь с информацией о банковской карте или счете пользователя
    :return: Наименование и зашифрованный номер карты или счета
    """
    payment = dict.get('from')
    if payment:
        if len(payment.split()) == 3:
            account_num = payment.split()[2]
            num_output = f'{" ".join(payment.split()[0:2])} {account_num[:4]} ' \
                         f'{account_num[4:6]}** **** {account_num[-4:]}'
        elif len(payment.split()) == 2:
            account_num = payment.split()[1]
            if len(payment.split()[1]) == 16:
                num_output = f'{payment.split()[0]} {account_num[:4]} ' \
                             f'{account_num[4:6]}** **** {account_num[-4:]}'
            elif len(payment.split()[1]) == 20:
                num_output = f'{payment.split()[0]} {account_num[:4]} ' \
                             f'{account_num[4:6]}** **** **** {account_num[-4:]}'
    else:
        num_output = 'Счет открыт'
    return num_output


def beneficiary_account_editor(data_dict):
    """
    Функция преобразовывает счет получателя так, что на экран выводятся
    6 последних цифр номера счета в формате **1234
    :param data_dict: Словарь, в котором содержится информация о названии карты
    или счета и сам набор цифр
    :return: Наименование карты или счета и последние цифры в формате **1234
    """
    source = data_dict.get('to')

    if len(source.split(' ')) == 2:
        name_card = source.split()[0]
        account_number = source.split()[1]

    elif len(source.split(' ')) == 3:
        name_card = ' '.join(source.split()[0:2])
        account_number = source.split(' ')[2]

    account_number = list(account_number[-6:])
    account_number[:2] = '**'
    coded_account = ''.join(account_number)

    return f'{name_card} {coded_account}'


def output_of_the_last_transactions(data):
    """
    Функция экранирует последние 5 операций, которые прошли успешно
    :param data: Словарь, в котором есть информация о всех
    операциях (EXECUTED и CANCELED)
    :return: Список успешных операций
    """
    new_list = []
    for i in data:
        if i['state'] == "EXECUTED":
            new_list.append(i)
    return new_list[:5]
