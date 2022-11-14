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

excel_wines = pandas.read_excel('wine2.xlsx', na_values=' ', keep_default_na=False).to_dict(orient='record')
print(excel_wines)
d = collections.defaultdict(list)
for wine in excel_wines:
    d[wine['Категория']].append({wine['Название'],
                                 wine['Сорт'],
                                 wine['Цена'],
                                 wine['Картинка'],
                                 })


pprint(d)
# rendered_page = template.render(
#     together_years=together_years,
#     ru_years=ru_years,
#     excel_wines = excel_wines,
# )
#
# with open('index.html', 'w', encoding="utf8") as file:
#     file.write(rendered_page)
#
#
# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()
