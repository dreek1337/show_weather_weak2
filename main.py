import requests
from settings import KEY


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
def get_weather(location: str, appid: str = KEY) -> dict:
    """
    Контроллер, для получения данных о погоде, в определенном городе
    """
    if not location[0].isalpha():
        coordinate = location.split(', ')
    else:
        api_req_coordinate = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?"
                                          f"q={location}&limit=5&appid={appid}")

        coordinate = api_req_coordinate.json()[0]['lat'], api_req_coordinate.json()[0]['lon']

    weather_info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?'
                                f'lat={coordinate[0]}&lon={coordinate[1]}&&appid={appid}')

    return weather_info.json()
