# -*- coding: utf-8 -*-
import datetime
from openpyxl import load_workbook

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.base import Base
# География
from Morbidity.models.geo_category import GeoCategory
from Morbidity.models.rus_total import RusTotal
from Morbidity.models.district import District
from Morbidity.models.territorial_unit import TerritorialUnit
# Показатели
from Morbidity.models.population_group import PopulationGroup
from Morbidity.models.type_value import TypeValue
# Форма №1
from Morbidity.models.form.form_1 import FormOne
from Morbidity.models.form.name_of_diseases import NameOfDiseases
from Morbidity.models.form.form_2 import FormTwo
# Отчеты
from Morbidity.models.report.measles_immunization_report.vaccinated_measles import VaccinatedMeasles

engine = create_engine(f"sqlite:///database.db", echo=True)
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
             ('Дальневосточный федеральный округ', 'Fareast Federal District', 'ДФО', 'FED'),
             ('Крымский федеральный округ', 'Crimean Federal District', 'КФО', 'CrED')]

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
    ('Тульская область', "Tula Region", 1, 6),
    ("Ярославская область", "Yaroslavl Region", 1, 6),
    ("г. Москва", "Moscow", 1, 8),

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
    ('г. Санкт-Петербург', 'St Petersburg', 2, 8),

    ('Республика Адыгея', 'Republic of Adygea', 3, 3),
    ('Республика Калмыкия', 'Republic of Kalmykia', 3, 3),
    ('Республика Крым', 'Republic of Crimea', 3, 3),
    ('Краснодарский край', 'Krasnodar Territory', 3, 4),
    ('Астраханская область', 'Astrakhan Region', 3, 6),
    ('Волгоградская область', 'Volgograd Region', 3, 6),
    ('Ростовская область', 'Rostov Region', 3, 6),
    ('г. Севастополь', 'City of Sevastopol', 3, 8),

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
    ("Чукотский автономный округ", "Chukotka Autonomous Area", 8, 5),

    ("Донецкая Народная Республика", "Donetsk People's Republic", 9, 3),
    ("Луганская Народная Республика", "Luhansk People's Republic", 9, 3),
    ("Запорожская область", "Zaporozhye region", 9, 6),
    ("Херсонская область", "Kherson region", 9, 6),

]

# Добавляем Регионы
for unit in territorial_units:
    ter = TerritorialUnit(unit[0], unit[1], unit[2], unit[3])
    session.add(ter)

population_group = [

    ('total', 'всё население'),
    ('00-01', 'детское население: новорожденные'),
    ('01-02', 'детское население: от 1 года до 2 лет'),
    ('03-06', 'детское население от 3 до 6 лет'),
    ('00-14', 'детское население до 14 лет'),
    ('00-17', 'детское население 0-17 лет (включительно)'),
    ('18+', 'взрослое население'),
    ('мигранты', None),
    ('переселенцы', 'Пребывающие из новых территорий РФ')
]

for group in population_group:
    gr = PopulationGroup(group[0], group[1])
    session.add(gr)

name_of_diseases_dc = {'1.02.01.01.00': 'Брюшной тиф',
                       '1.02.01.02.00': 'Паратифы А,В,С и неуточненный',
                       '1.02.01.03.00': 'Бактерионосители брюшного тифа, паратифов',
                       '1.02.01.04.00': 'Холера',
                       '1.02.01.05.00': 'Вибриононосители холеры',
                       '1.02.01.06.00': 'Другие сальмонеллезные инфекции',
                       '1.02.01.06.01': '  из них вызванные: сальмонеллами группы B',
                       '1.02.01.06.02': '  сальмонеллами группы C',
                       '1.02.01.06.03': '  сальмонеллами группы Д',
                       '1.02.01.07.00': 'Бактериальная дизентерия (шигеллез)',
                       '1.02.01.07.01': '  из нее бактериологически подтвержденная',
                       '1.02.01.07.02': '    из нее вызванная: шигеллами Зонне',
                       '1.02.01.07.03': '    шигеллами Флекснера',
                       '1.02.01.08.00': 'Бактерионосители дизентерии',
                       '1.02.01.09.00': 'Другие острые кишечные инфекции, вызванные установленными '
                                        'бактериальными, вирусными возбудителями, а также пищевые '
                                        'токсикоинфекции установленной этиологии',
                       '1.02.01.09.01': '  из них: вызванные установленными бактериальными '
                                        'возбудителями',
                       '1.02.01.09.02': '    из них: кишечными палочками (эшерихиями)',
                       '1.02.01.09.03': '    кампилобактериями',
                       '1.02.01.09.04': '    иерсиниями энтероколитика',
                       '1.02.01.09.05': '  вызванные вирусами',
                       '1.02.01.09.06': '    из них: ротавирусами',
                       '1.02.01.09.07': '    вирусом Норволк',
                       '1.02.01.10.00': 'Острые кишечные инфекции, вызванные неустановленными '
                                        'инфекционными возбудителями, пищевые токсикоинфекции '
                                        'неустановленной этиологии',
                       '1.02.01.11.00': 'Острый паралитический полиомиелит, включая ассоциированный '
                                        'с вакциной',
                       '1.02.01.12.00': 'Острые вялые параличи',
                       '1.02.01.13.00': 'Энтеровирусные инфекции',
                       '1.02.01.13.01': '  из них энтеровирусный менингит',
                       '1.02.01.14.00': 'Острые гепатиты - всего',
                       '1.02.01.14.01': '  из них: острый гепатит А',
                       '1.02.01.14.02': '  острый гепатит В',
                       '1.02.01.14.03': '  острый гепатит С',
                       '1.02.01.14.04': '  острый гепатит Е',
                       '1.02.01.15.00': 'Хронические вирусные гепатиты (впервые установленные) – '
                                        'всего',
                       '1.02.01.15.01': '  из них: хронический вирусный гепатит В',
                       '1.02.01.15.02': '  хронический вирусный гепатит С',
                       '1.02.01.16.00': '*** Носительство возбудителя вирусного гепатита В',
                       '1.02.01.17.00': 'Дифтерия',
                       '1.02.01.18.00': 'Бактерионосители токсигенных штаммов дифтерии',
                       '1.02.01.19.00': 'Коклюш',
                       '1.02.01.19.01': '  из него коклюш, вызванный Bordetella parapertussis',
                       '1.02.01.20.00': 'Стрептококковая инфекция (впервые выявленная)',
                       '1.02.01.20.01': '  из них: скарлатина',
                       '1.02.01.20.02': '  стрептококковая септицемия',
                       '1.02.01.21.00': 'Ветряная оспа',
                       '1.02.01.23.00': 'Корь',
                       '1.02.01.24.00': 'Краснуха',
                       '1.02.01.25.00': 'Синдром врожденной краснухи (СВК)',
                       '1.02.01.26.00': 'Паротит эпидемический',
                       '1.02.01.27.00': 'Генерализованные формы менингококковой инфекции',
                       '1.02.01.27.02': '*** Менингококковая инфекция',
                       '1.02.01.28.00': 'Гемофильная инфекция',
                       '1.02.01.29.00': 'Столбняк',
                       '1.02.01.30.00': 'Туляремия',
                       '1.02.01.31.00': 'Сибирская язва',
                       '1.02.01.32.00': 'Бруцеллез, впервые выявленный',
                       '1.02.01.33.00': 'Вирусные лихорадки, передаваемые членистоногими и вирусные '
                                        'геморрагические лихорадки',
                       '1.02.01.33.01': '  из них: лихорадка Западного Нила',
                       '1.02.01.33.02': '  Крымская геморрагическая лихорадка',
                       '1.02.01.33.03': '  геморрагическая лихорадка с почечным синдромом',
                       '1.02.01.33.04': '  Омская геморрагическая лихорадка',
                       '1.02.01.33.05': '  лихорадка денге',
                       '1.02.01.34.00': 'Клещевой вирусный энцефалит',
                       '1.02.01.35.00': 'Клещевой боррелиоз (болезнь Лайма)',
                       '1.02.01.36.00': 'Псевдотуберкулез',
                       '1.02.01.37.00': 'Лептоспироз',
                       '1.02.01.38.00': 'Бешенство',
                       '1.02.01.39.00': 'Укусы, ослюнения, оцарапывания животными',
                       '1.02.01.39.01': '  из них дикими животными',
                       '1.02.01.40.00': 'Укусы клещами',
                       '1.02.01.41.00': 'Орнитоз (пситтакоз)',
                       '1.02.01.42.00': 'Риккетсиозы',
                       '1.02.01.42.01': '  из них: эпидемический сыпной тиф',
                       '1.02.01.42.02': '  болезнь Брилля',
                       '1.02.01.42.03': '  лихорадка Ку',
                       '1.02.01.42.04': '  сибирский клещевой тиф',
                       '1.02.01.42.05': '  астраханская пятнистая лихорадка',
                       '1.02.01.42.06': '  риккетсиоз, вызываемый Anaplasma phagocytophilum',
                       '1.02.01.42.07': '  риккетсиоз, вызываемый Ehrlichia chaffeensis и Ehrlichia '
                                        'muris',
                       '1.02.01.43.00': 'Педикулез',
                       '1.02.01.44.00': 'Листериоз',
                       '1.02.01.45.00': 'Легионеллез',
                       '1.02.01.46.00': 'Инфекционный мононуклеоз',
                       '1.02.01.47.00': 'Туберкулез (впервые выявленный) активные формы',
                       '1.02.01.47.01': '  из него туберкулез органов дыхания',
                       '1.02.01.47.02': '    из него бациллярные формы',
                       '1.02.01.48.00': 'Сифилис (впервые выявленный) - все формы',
                       '1.02.01.49.00': 'Гонококковая инфекция',
                       '1.02.01.50.00': 'Болезнь, вызванная вирусом иммунодефицита человека (ВИЧ) и '
                                        'бессимптомный инфекционный статус, вызванный ВИЧ',
                       '1.02.01.51.00': 'Острые инфекции верхних дыхательных путей множественной и '
                                        'неуточненной локализации',
                       '1.02.01.52.00': 'Грипп',
                       '1.02.01.53.00': 'Пневмония (внебольничная)',
                       '1.02.01.53.01': '  из нее: вирусная',
                       '1.02.01.53.02': '  бактериальная',
                       '1.02.01.53.03': '  из нее: вызванная пневмококками',
                       '1.02.01.55.00': 'Цитомегаловирусная болезнь',
                       '1.02.01.56.00': 'Врожденная цитомегаловирусная инфекция',
                       '1.02.01.57.00': 'Дерматофития, вызванная грибами рода Microsporum',
                       '1.02.01.58.00': 'Чесотка',
                       '1.02.01.59.00': 'Дерматофития, вызванная грибами рода Trichophyton',
                       '1.02.01.60.00': 'Поствакцинальные осложнения',
                       '1.02.01.22.00': 'Опоясывающий лишай'}

for i in name_of_diseases_dc:
    krista_id = i
    name = name_of_diseases_dc[i]
    num_form = 2
    session.add(NameOfDiseases(name, num_form, krista_id, None))

# Добавляем типы значений для формы 1
session.add(TypeValue('Абсолютное значение', None))
session.add(TypeValue('Показатель на 100 тыс. населения', None))

session.commit()
session.close()
