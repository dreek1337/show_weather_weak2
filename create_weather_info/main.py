import requests
import psycopg2
from settings import DataSettings, ShowWeather, connection_db


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
def get_weather(
        location: str,
        appid: str,
        lang: str = 'ru',
) -> dict:
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


@connection_db
def feature_weather(
        conn: psycopg2,
        data: DataSettings,
        city: str = '',
        lang: str = 'ru',
) -> str:
    """
    Проверка на наличие данных в бд, и в случае чего запись данных в бд
    """
    info = get_weather(location=city, appid=data.KEY)

    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM show_weather WHERE created_at + '1 hour' > now() AND city = '{info['city']}';")
        res = cur.fetchall()

        if res:
            result = '\n'.join(str(i) for i in res[0][1:-1])
            return result
        else:
            query = "INSERT INTO show_weather (weather, city, temperature) VALUES (%s, %s, %s)"
            data = (info['weather'], info['city'], info['temp'])
            cur.execute(query, data)
            conn.commit()
            return '\n'.join(str(i) for i in data)
