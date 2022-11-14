from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from pprint import pprint


def get_str_years(years):
    if len(str(years)) == 1:
        if years == 1: return 'год'
        elif years in (2,3,4): return 'года'
        else: return 'лет'
    elif len(str(years)) == 2 and (years // 10) == 1: return 'лет'
    else:
        return get_str_years(years % (10**(len(str(years))-1)))


birth_year = 1920
now_year = int(datetime.datetime.now().strftime('%Y'))
together_years = now_year - birth_year
ru_years = get_str_years(together_years)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_wines = pandas.read_excel('wine3.xlsx', na_values=' ', keep_default_na=False).to_dict(orient='record')
wines = collections.defaultdict(list)
for wine in excel_wines:

    wines[wine['Категория']].append({'Название': wine['Название'],
                                    'Сорт': wine['Сорт'],
                                    'Цена': wine['Цена'],
                                    'Картинка': wine['Картинка'],
                                     'Акция': wine['Акция'],
                                     })

wine_category = list(wines.keys())

rendered_page = template.render(
    together_years=together_years,
    ru_years=ru_years,
    wine_category = wine_category,
    wines = wines,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
