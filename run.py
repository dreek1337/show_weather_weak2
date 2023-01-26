from create_weather_info import fetch_weather
from settings import DataSettings
from parce_valute import parce_site, add_value_in_db


def main():
    add_value_in_db(
        url='http://www.cbr.ru/scripts/XML_daily.asp',
        id_valute='R01010',
        data=DataSettings()
    )
    fetch_weather(
        data=DataSettings(),
        city='Moscow'
    )


if __name__ == '__main__':
    main()
