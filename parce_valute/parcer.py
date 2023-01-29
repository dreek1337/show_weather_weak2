import psycopg2
from urllib import request
from xml.etree import ElementTree
from settings import DataSettings, connection_db


def parce_site(
        url: str,
        id_valute: str,
        params=None
) -> dict:
    """
    Парсинг XML сайта
    """
    if params is None:
        params = ['Name', 'Value']

    response = request.urlopen(url).read()
    tree = ElementTree.fromstring(response)

    searched_info = {}
    for i in tree:
        if i.attrib['ID'] != id_valute:
            continue
        else:
            for j in params:
                searched_info[j] = i.find(j).text

    searched_info['Date'] = tree.attrib['Date']

    return searched_info


def add_value_in_db(
        conn: connection_db,
        info: dict,
) -> str:
    """
    Добавление параметров в базу данных
    """
    with conn.cursor() as cur:
        query = "INSERT INTO valute_table (valute_name, valute_value, date_value) VALUES (%s, %s, %s)"
        data = (info.get('Name'), info.get('Value'), info['Date'])
        cur.execute(query, data)
        conn.commit()

        return '\n'.join(i for i in data)
