from sys import argv

from create_weather_info import fetch_weather
from settings import DataSettings
from parce_valute import add_value_in_db

script, city, id_valute = argv


def main():
    fetch_weather(
        data=DataSettings(),
        city=city
    )

    add_value_in_db(
        url='http://www.cbr.ru/scripts/XML_daily.asp',
        id_valute=id_valute,
        data=DataSettings()
    )


if __name__ == '__main__':
    main()
