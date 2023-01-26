from pydantic import BaseSettings, BaseModel, Field


class DataSettings(BaseSettings):
    """
    Валидация данных для подключения к базе данных
    """
    KEY: str = Field(..., env='API_KEY')
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
