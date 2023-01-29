import requests
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
                                          f"q={location}&limit=5&appid={appid}&lang={lang}&units=metric")

        coordinate = api_req_coordinate.json()[0]['lat'], api_req_coordinate.json()[0]['lon']

    weather_info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?'
                                f'lat={coordinate[0]}&lon={coordinate[1]}&&appid={appid}&lang={lang}&units=metric')

    res = ShowWeather(**weather_info.json())

    return res.__dict__


def fetch_weather(
        conn: connection_db,
        info: get_weather,
) -> str:
    """
    Проверка на наличие данных в бд, и в случае чего запись данных в бд
    """

    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM show_weather WHERE created_at + '1 hour' > now() AND city = '{info['name']}';")
        res = cur.fetchall()
        if res:
            result = '\n'.join(str(i) for i in res[0][1:-1])
            return result
        else:
            query = "INSERT INTO show_weather (weather, city, temperature) VALUES (%s, %s, %s)"
            data = (info['weather'], info['name'], info['main'])
            cur.execute(query, data)
            conn.commit()

            return '\n'.join(str(i) for i in data)
