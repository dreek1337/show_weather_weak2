from xml.etree import ElementTree
from urllib import request


def parce_site(url: str, id_valute: str, params=None) -> list[str]:
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

    return searched_info + [tree.attrib['Date']]


print(parce_site(url='http://www.cbr.ru/scripts/XML_daily.asp', id_valute='R01010'))
