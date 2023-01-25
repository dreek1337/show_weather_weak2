import requests
import psycopg2
from pydantic import BaseModel, BaseSettings, Field
from settings import KEY


class DataSettings(BaseSettings):
    """
    Валидация данных для подключения к базе данных
    """
    db_user: str = Field(..., env='DATABASE_USER')
    db_password: str = Field(..., env='DATABASE_PASSWORD')
    db_name: str = Field(..., env='DATABASE_DB')
    db_port: int = Field(5432, env='DATABASE_PORT')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ShowWeather(BaseModel):
    """
    Валидация данных для записи в базу данных
    """
    city: str
    weather: str
    temp: int
    cod: int

    def __init__(self, **data):
        super().__init__(**data)


database_settings: dict = DataSettings().dict()


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

    city = dict_info['name']
    weather = dict_info['weather'][0]['description'].capitalize()
    temp = round(dict_info['main']['temp'] - 273, 0)
    cod = dict_info['cod']

    res = ShowWeather(city=city, weather=weather, temp=temp, cod=cod)

    add_weather(city=city, weather=weather, temp=temp, cod=cod)

    return res.__dict__


def add_weather(*args, **kwargs) -> None:
    """
    Проверка и запись в базу данных
    """
    if kwargs['cod'] < 300:
        with psycopg2.connect(
            host="localhost",
            database=database_settings['db_name'],
            user=database_settings['db_user'],
            password=database_settings['db_password'],
        ) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO show_weather (weather, city, temperature) VALUES (%s, %s, %s)"
                data = (kwargs['weather'], kwargs['city'], kwargs['temp'])
                cur.execute(query, data)
                conn.commit()
    else:
        pass
