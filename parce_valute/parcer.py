import psycopg2
from urllib import request
from xml.etree import ElementTree
from settings import DataSettings, connection_db


def parce_site(
        url: str,
        id_valute: str,
        params=None
) -> list[str]:
    """
    Парсинг XML сайта
    """
    if params is None:
        params = ['Name', 'Value']

    response = request.urlopen(url).read()
    tree = ElementTree.fromstring(response)

    searched_info = []
    for i in tree:
        if i.attrib['ID'] != id_valute:
            continue
        else:
            for j in params:
                searched_info.append(i.find(j).text)
    searched_info += [tree.attrib['Date']]

    print_info = '\n'.join(i for i in searched_info)
    print(print_info)
    print('-----END-----')

    return searched_info


@connection_db
def add_value_in_db(
        conn: psycopg2,
        data: DataSettings,
        url: str,
        id_valute: str
) -> None:
    """
    Добавление параметров в базу данных
    """
    info = parce_site(url=url, id_valute=id_valute)
    with conn.cursor() as cur:
        query = "INSERT INTO valute_table (valute_name, valute_value, date_value) VALUES (%s, %s, %s)"
        data = (info[0], info[1], info[2])
        cur.execute(query, data)
        conn.commit()
