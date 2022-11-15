from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os
from dotenv import load_dotenv


def get_str_years(years):
    if len(str(years)) == 2 and (years // 10) == 1:
        return 'лет'

    if len(str(years)) > 1:
        return get_str_years(years % (10 ** (len(str(years)) - 1)))

    if years == 1:
        return 'год'
    elif years in (2, 3, 4):
        return 'года'
    else:
        return 'лет'


def main():
    load_dotenv()
    foundation_year = int(os.environ['FOUNDATION_YEAR'])
    excel_filepath = os.environ['EXCEL_FILE']
    now_year = datetime.datetime.now().year
    existence_years = now_year - foundation_year
    ru_years = get_str_years(existence_years)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    excel_wines = pandas.read_excel(excel_filepath, na_values=' ', keep_default_na=False).to_dict(orient='record')
    wines = collections.defaultdict(list)
    for wine in excel_wines:

        wines[wine['Категория']].append({'Название': wine['Название'],
                                         'Сорт': wine['Сорт'],
                                         'Цена': wine['Цена'],
                                         'Картинка': wine['Картинка'],
                                         'Акция': wine['Акция'],
                                         })

    rendered_page = template.render(
        existence_years=existence_years,
        ru_years=ru_years,
        wines=wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
