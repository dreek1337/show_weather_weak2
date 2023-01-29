import psycopg2
from settings.validation import DataSettings


def connection_db(settings: DataSettings) -> psycopg2:
    conn = psycopg2.connect(
            host="localhost",
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
    )

    return conn
