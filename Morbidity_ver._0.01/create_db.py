# -*- coding: utf-8 -*-
import datetime
from openpyxl import load_workbook
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
# География
from models.geo_category import GeoCategory
from models.rus_total import RusTotal
from models.district import District
from models.territorial_unit import TerritorialUnit
# Показатели
from models.population_group import PopulationGroup
from models.type_value import TypeValue
# Форма №1
from models.form.form_1 import FormOne
from models.form.name_of_diseases import NameOfDiseases
# Отчеты
from models.report.measles_immunization_report.vaccinated_measles import VaccinatedMeasles


engine = create_engine(f"{config.SQL_PATH}", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

categories = [('Страна', 'Country'),
              ('Округ', 'District'),
              ('Республика', 'Republic'),
              ('Край', 'Territories'),
              ('Автономный округ', 'Autonomous Area '),
              ('Область', 'Region'),
              ('Автономная область', 'Autonomous Region'),
              ('Город федерального значения', 'City'),
              ]

# Добавляем виды территориального деления
for category in categories:
    gc = GeoCategory(category[0], category[1])
    session.add(gc)

# Добавляем РФ
session.add(RusTotal('Российская Федерация', 'Russian Federation', 1))

districts = [('Центральный федеральный округ', 'Central Federal District', 'ЦФО', 'CFD'),
             ('Северо-Западный федеральный округ', 'Northwestern Federal District', 'СЗФО', 'NW-FD'),
             ('Южный федеральный округ', 'Southern Federal District', 'ЮФО', 'SFD'),
             ('Северо-Кавказский федеральный округ', 'North Caucasus Federal District', 'СКФО', 'NCD'),
             ('Приволжский федеральный округ', 'Privolzhsky Federal District', 'ПФО', 'PFD'),
             ('Уральский федеральный округ', 'Urals Federal District', 'УФО', 'UFD'),
             ('Сибирский федеральный округ', 'Siberian Federal District', 'СФО', 'SibFD'),
             ('Дальневосточный федеральный округ', 'Fareast Federal District', 'ДФО', 'FED')]

# Добавляем округа
for district in districts:
    ds = District(district[0], district[1], district[2], district[3], 1, 2)
    session.add(ds)

territorial_units = [

    ("Белгородская область", "Belgorod Region", 1, 6),
    ("Брянская область", "Bryansk Region", 1, 6),
    ("Владимирская область", "Vladimir Region", 1, 6),
    ("Воронежская область", "Voronezh Region", 1, 6),
    ("Ивановская область", "Ivanovo Region", 1, 6),
    ("Калужская область", "Kaluga Region", 1, 6),
    ("Костромская область", "Kostroma Region", 1, 6),
    ("Курская область", "Kursk Region", 1, 6),
    ("Липецкая область", "Lipetsk Region", 1, 6),
    ("Московская область", "Moscow Region", 1, 6),
    ("Орловская область", "Orel Region", 1, 6),
    ("Рязанская область", "Ryazan Region", 1, 6),
    ("Смоленская область", "Smolensk Region", 1, 6),
    ("Тамбовская область", "Tambov Region", 1, 6),
    ("Тверская область", "Tver Region", 1, 6),
    ('Тверская область', "Tula Region", 1, 6),
    ("Ярославска область", "Yaroslavl Region", 1, 6),
    ("Москва", "Moscow", 1, 8),

    ('Республика Карелия', 'Republic of Karelia', 2, 3),
    ('Республика Коми', 'Kodi Republic', 2, 3),
    ('Архангельская область', 'Arkhangelsk Region', 2, 6),
    ('Ненецкий автономный округ', 'Nenets Autonomous Area', 2, 5),
    ('Вологодская область', 'Vologda Region', 2, 6),
    ('Калининградская область', 'Kaliningrad Region', 2, 6),
    ('Ленинградская область', 'Leningrad Region', 2, 6),
    ('Мурманская область', 'Murmansk Region', 2, 6),
    ('Новгородская область', 'Novgorod Region', 2, 6),
    ('Псковская область', 'Pskov Region', 2, 6),
    ('Санкт-Петербург', 'St Petersburg', 2, 8),

    ('Республика Адыгея', 'Republic of Adygea', 3, 3),
    ('Республика Калмыкия', 'Republic of Kalmykia', 3, 3),
    ('Республика Крым', 'Republic of Crimea', 3, 3),
    ('Краснодарский край', 'Krasnodar Territory', 3, 4),
    ('Астраханская область', 'Astrakhan Region', 3, 6),
    ('Волгоградская область', 'Volgograd Region', 3, 6),
    ('Ростовская область', 'Rostov Region', 3, 6),
    ('Севастополь', 'City of Sevastopol', 3, 8),

    ('Республика Дагестан', 'Republic of Dagestan', 4, 3),
    ('Республика Ингушетия', 'Republic of Ingushetia', 4, 3),
    ('Кабардино-Балкарская Республика', 'Kabardino-Balkarian Republic', 4, 3),
    ('Карачаево-Черкесская Республика', 'Karachayevo-Circassian Republic', 4, 3),
    ('Республика Северная Осетия — Алания', 'Republic of North Ossetia – Alania', 4, 3),
    ('Чеченская Республика', 'Chechen Republic', 4, 3),
    ('Ставропольский край', 'Stavropol Territory', 4, 4),

    ("Республика Башкортостан", "Republic of Bashkortostan", 5, 3),
    ("Республика Марий Эл", "Republic of Mari El", 5, 3),
    ("Республика Мордовия", "Republic of Mordovia", 5, 3),
    ("Республика Татарстан", "Republic of Tatarstan", 5, 3),
    ("Удмуртская Республика", "Republic of Udmurtia", 5, 3),
    ("Чувашская Республика", "Chuvash Republic", 5, 3),
    ("Пермский край", "Perm Territory", 5, 4),
    ("Кировская область", "Kirov Region", 5, 6),
    ("Нижегородская область", "Nizhny Novgorod Region", 5, 6),
    ("Оренбургская область", "Orenburg Region", 5, 6),
    ("Пензенская область", "Penza Region", 5, 6),
    ("Самарская область", "Samara Region", 5, 6),
    ("Саратовская область", "Saratov Region", 5, 6),
    ("Ульяновская область", "Ulyanovsk Region", 5, 6),

    ("Курганская область", "Kurgan Region", 6, 6),
    ("Свердловская область", "Sverdlovsk Region", 6, 6),
    ("Тюменская область", "Tyumen Region", 6, 6),
    ("Ханты-Мансийский автономный округ — Югра", "Khanty-Mansi Autonomous Area – Yugra", 6, 5),
    ("Ямало-Ненецкий автономный округ", "Yamalo-Nenets Autonomous Area", 6, 5),
    ("Челябинская область", "Chelyabinsk Region", 6, 6),

    ("Республика Алтай", "Altai Republic", 7, 3),
    ("Республика Тыва", "Tuva Republic", 7, 3),
    ("Республика Хакасия", "Khakassia Republic", 7, 3),
    ("Алтайский край", "Altai Territory", 7, 4),
    ("Красноярский край", "Krasnoyarsk Territory", 7, 4),
    ("Иркутская область", "Irkutsk Region", 7, 6),
    ("Кемеровская область", "Kemerovo Region", 7, 4),
    ("Новосибирская область", "Novosibirsk Region", 7, 6),
    ("Омская область", "Omsk Region", 7, 6),
    ("Томская область", "Tomsk Region", 7, 6),

    ("Республика Бурятия", "Republic of Buryatia", 8, 3),
    ("Республика Саха (Якутия)", "Republic of Sakha (Yakutia)", 8, 3),
    ("Забайкальский край", "Transbaikal Territory", 8, 4),
    ("Камчатский край", "Kamchatka Territory", 8, 4),
    ("Приморский край", "Primorsky Territory", 8, 4),
    ("Хабаровский край", "Khabarovsk Territory", 8, 4),
    ("Амурская область", "Amur Region", 8, 6),
    ("Магаданская область", "Magadan Region", 8, 6),
    ("Сахалинская область", "Sakhalin Region", 8, 6),
    ("Еврейская автономная область", "Jewish Autonomous Region", 8, 7),
    ("Чукотский автономный округ", "Chukotka Autonomous Area", 8, 5)
]

# Добавляем Регионы
for unit in territorial_units:
    ter = TerritorialUnit(unit[0], unit[1], unit[2], unit[3])
    session.add(ter)

population_group = [

    ('total', 'всё население'),
    ('00-01', 'детское население: новорожденные'),
    ('01-02', 'детское население: от 1 года до 2 лет'),
    ('03-06', 'детское население от 3 до 6 лет (детский сад)'),
    ('00-14', 'детское население до 14 лет'),
    ('00-17', 'детское население 0-17 лет (включительно)'),
    ('18+', 'взрослое население'),
    ('мигранты', None)
]

for group in population_group:
    gr = PopulationGroup(group[0], group[1])
    session.add(gr)

# Добавляем типы значений для формы 1
session.add(TypeValue('Абсолютное значение', None))
session.add(TypeValue('Показатель на 100 тыс. населения', None))


wb = load_workbook(filename='tmp.xlsx')


def decode(work_book, sheet, coll, rows):
    """ Функция для чтения из EXEL. На вход подается:
        work_book = файл EXEL,
        sheet = страница,
        коардинаты ячейки(колонка и строчка)
        coll = колонка,
        rows = строчка
    """
    sheet = work_book[f'{sheet}']
    value_cell = sheet[f'{coll}{rows}'].value
    return value_cell



session.commit()
session.close()
