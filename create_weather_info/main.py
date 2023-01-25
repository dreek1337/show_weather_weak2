import requests
import psycopg2
from settings import KEY

from settings import DataSettings, ShowWeather


def retry(func):
    def inner(*args, **kwargs):
        """
        Повторный запрос данных, в случае ошибки.
        """
        start_func = func(*args, **kwargs)

        for i in range(10):
            if int(start_func.get('cod')) > 300:
                start_func = func(*args, **kwargs)
            else:
                return start_func

        raise 'Сервер не смог дать ответ'

    return inner


@retry
def get_weather(location: str, lang: str = 'ru', appid: str = KEY) -> dict:
    """
    Контроллер, для получения данных о погоде, в определенном городе
    """
    if not location[0].isalpha():
        coordinate = location.split(', ')
    else:
        api_req_coordinate = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?"
                                          f"q={location}&limit=5&appid={appid}&lang={lang}")

        coordinate = api_req_coordinate.json()[0]['lat'], api_req_coordinate.json()[0]['lon']

    weather_info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?'
                                f'lat={coordinate[0]}&lon={coordinate[1]}&&appid={appid}&lang={lang}')

    dict_info = weather_info.json()

    result = dict(
        city=dict_info['name'],
        weather=dict_info['weather'][0]['description'].capitalize(),
        temp=round(dict_info['main']['temp'] - 273, 0),
        cod=dict_info['cod'],
    )
    res = ShowWeather(**result)

    return res.__dict__


'''def add_weather(data: DataSettings, res: dict) -> None:
    """
    Запись в базу данных
    """
    with psycopg2.connect(
            host="localhost",
            database=data.db_name,
            user=data.db_user,
            password=data.db_password,
    ) as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO show_weather (weather, city, temperature) VALUES (%s, %s, %s)"
            data = (res['weather'], res['city'], res['temp'])
            cur.execute(query, data)
            conn.commit()'''


def feature_weather(data: DataSettings, city: str = '', lang: str = 'ru'):
    """
    Проверка на наличие данных в бд, и в случае чего запись данных в бд
    """
    info = get_weather(city)

    with psycopg2.connect(
            host="localhost",
            database=data.db_name,
            user=data.db_user,
            password=data.db_password,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT created_at FROM show_weather')
            res = cur.fetchall()
            if res < res_1:
                return 'То что есть в бд, если не нужно создавать запись'
            else:
                query = "INSERT INTO show_weather (weather, city, temperature) VALUES (%s, %s, %s)"
                data = (info['weather'], info['city'], info['temp'])
                cur.execute(query, data)
                conn.commit()
                return 'Хорошо оформленные данные))'
