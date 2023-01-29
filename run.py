from sys import argv

from create_weather_info import fetch_weather
from settings import DataSettings, connection_db
from parce_valute import add_value_in_db, parce_site
from create_weather_info.main import get_weather

'script, city, id_valute = argv'


def main():
    print('----START----')
    print(fetch_weather(
        conn=connection_db(DataSettings()),
        info=get_weather(
            location='Moscow',
            appid=DataSettings().KEY
        ),
    ))

    print('------------')

    print(add_value_in_db(
        conn=connection_db(DataSettings()),
        info=parce_site(
            url='http://www.cbr.ru/scripts/XML_daily.asp',
            id_valute='R01010'
        ),
    ))
    print('-----END-----')


if __name__ == '__main__':
    main()
