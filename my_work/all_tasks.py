import os
import osa
import re

print('')


def get_dir(file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, file)

    return input_file


def get_temp_list(input_file):
    with open(input_file) as f:
        temp_list = []
        for line in f:
            list_element = line.split()
            temp = int(list_element[0])
            temp_list.append(temp)

    return temp_list


def get_currency_dict(input_file):
    with open(input_file) as f:
        currency_dict = {}
        for line in f:
            list_element = line.split()
            currency_key = int(list_element[1])
            currency_value = list_element[2]
            currency_dict[currency_key] = currency_value

    return currency_dict


def get_length_list(input_file):
    with open(input_file) as f:
        length_list = []
        for line in f:
            list_element = line.split()
            length = list_element[1]
            formatted_length = re.sub(r',', '', length)
            length_list.append(float(formatted_length))

    return length_list


def get_ave_temp(temp_list):
    from_unit = 'degreeFahrenheit'
    to_unit = 'degreeCelsius'
    arith_mean_temp = sum(temp_list)/len(temp_list)
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')

    return client.service.ConvertTemp(arith_mean_temp, from_unit, to_unit)


def get_sum_money(currency_dict):
    to_unit = 'RUB'
    rub_list = []
    for key, value in currency_dict.items():
        client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
        currency_change = client.service.ConvertToNum("", value, to_unit, key, True, "", "")
        rub_list.append(currency_change)
    result = sum(rub_list)

    return result


def get_sum_distance(length_list):
    from_unit = 'Miles'
    to_unit = 'Kilometers'
    sum_length = sum(length_list)
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    result = client.service.ChangeLengthUnit(sum_length, from_unit, to_unit)

    return round(result, 2)


def main():
    files = ['temps.txt', 'currencies.txt', 'travel.txt']
    for file in files:
        file_dir = get_dir(file)
        if file == 'temps.txt':
            temp_list = get_temp_list(file_dir)
            print('Средняя арифметическая температура по Цельсию за неделю: {}'.format(get_ave_temp(temp_list)))
        elif file == 'currencies.txt':
            currency_dict = get_currency_dict(file_dir)
            print('На путешествие потрачено {} рублей'.format(get_sum_money(currency_dict)))
        elif file == 'travel.txt':
            length_list = get_length_list(file_dir)
            print('Суммарное расстояние пути {} киллометров'.format(get_sum_distance(length_list)))


main()







