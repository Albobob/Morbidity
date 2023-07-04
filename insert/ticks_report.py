import datetime
import string
import os
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openpyxl import load_workbook
from Morbidity.models.population_group import PopulationGroup
from Morbidity.models.territorial_unit import TerritorialUnit
from Morbidity.models.district import District
from Morbidity.models.rus_total import RusTotal
from Morbidity.models.geo_category import GeoCategory
from Morbidity.models.base import Base

from Morbidity.models.report.ticks.tick_morbidity_rate import TickMorbidityRate
from Morbidity.models.report.ticks.contacted import Contacted
from Morbidity.models.transmission_of_infection import TransmissionOfInfection

# Подключаемся к БД
engine = create_engine(f"{config.SQL_PATH}", echo=False)
#
# Base.metadata.create_all(engine)
#
Session = sessionmaker(bind=engine)
session = Session()


#
# # session.add(TransmissionOfInfection('инфицирован трансмиссивным путем'))
# # session.add(TransmissionOfInfection('инфицирован алиментарным путем'))
#


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


def true_region_name(name: str) -> str:
    true_name = None
    if name == 'Москва':
        true_name = 'г. Москва'
        return true_name

    if name == 'Санкт-Петербург':
        true_name = 'г.Санкт-Петербург'
        return true_name

    if name == 'Республика Адыгея (Адыгея)':
        true_name = 'Республика Адыгея'
        return true_name

    if name == 'Кемеровская область - Кузбасс':
        true_name = 'Кемеровская область'
        return true_name

    if name == 'Ханты-Мансийский автономный округ-Югра' or 'Ханты-Мансийский АО':
        true_name = 'Ханты-Мансийский автономный округ — Югра'
        return true_name

    if name == 'Ямало-Ненецкий АО':
        true_name = 'Ямало-Ненецкий автономный округ'
        return true_name

    if name == 'Чувашская Республика – Чувашия':
        true_name = 'Чувашская Республика'
        return true_name

    if name == 'Республика Татарстан (Татарстан)':
        true_name = 'Республика Татарстан'
        return true_name

    if name == 'Республика Северная Осетия-Алания' or 'Республика Северная Осетия':
        true_name = 'Республика Северная Осетия — Алания'
        return true_name

    if name == 'Республика Саха ( Якутия )':
        true_name = 'Республика Саха (Якутия)'
        return true_name

    if name == 'Еврейская АО':
        true_name = 'Еврейская автономная область'
        return true_name

    if name == 'Чукотский АО':
        true_name = 'Чукотский автономный округ'
        return true_name


def insert_contacted(date: str, value, week: int, rg_id: int, pg_id: int):
    session.add(Contacted(date, rg_id, pg_id, value, week))


def insert_tick(date: str, rg_id: int, pg_id: int, value, toi_id: int):
    session.add(TickMorbidityRate(date, rg_id, pg_id, value, toi_id))
    pass


data = []

root = 'C:/Users/SimonyanAR.FCGIE/Desktop/p/Morbidity/insert/DATA'
for year in os.listdir(root):
    path = os.path.join(root, year)
    print(path)
    os.chdir(path)
    files = os.listdir()
    for f in files:
        print(f)
    for week in os.listdir():
        for row in range(12, 30):
            wb = load_workbook(f'{week}', data_only=True)
            date = datetime.date(int(year), 1, 1) + datetime.timedelta(weeks=int(week[0:2:]) - 1, days=4)

            dc_contact = {
                'date': None,
                'week': None,
                'name': None,
                'rg_id': None,
                'pg_id': None,
                'value': None,
            }
            dc_tick_morbidity_rate = {
                'date': None,
                'week': None,
                'name': None,
                'rg_id': None,
                'pg_id': None,
                'value': None,
                'toi_id': None,
            }
            '''1. ОБРАЩАЕМОСТЬ ПОСТРАДАВШИХ ОТ УКУСОВ КЛЕЩЕЙ.'''
            if decode(wb, "Табл1", "d", row) is not None:
                if decode(wb, "Табл1", "d", row) > 0:
                    name = decode(wb, "Табл1", "b", row)
                    value_all = decode(wb, "Табл1", "d", row)
                    pg_id = 1
                    name_bd = session.query(TerritorialUnit).filter_by(name_ru=f'{name}').first()
                    if name_bd is None:
                        region_name = true_region_name(name)
                    else:
                        region_name = name
                    try:
                        region = session.query(TerritorialUnit).filter_by(name_ru=f'{region_name}').first()
                        rg_id = region.id
                        print(f'date: {date}\nvalue: {value_all}\nweek:{week[0:2:]}\n'
                              f'name:{name}\nrg_id: {rg_id}\npg_id{pg_id}')
                        dc_contact['date'] = date
                        dc_contact['week'] = week
                        dc_contact['name'] = name
                        dc_contact['rg_id'] = rg_id
                        dc_contact['pg_id'] = pg_id
                        dc_contact['value'] = value_all
                        data.append(dc_contact)

                        # insert(date, value_all, week, rg_id, pg_id)

                    except AttributeError:
                        print(f"EROR - {region_name}")
            if decode(wb, "Табл1", "e", row) is not None:
                if decode(wb, "Табл1", "e", row) > 0:
                    value_chl = decode(wb, "Табл1", "e", row)
                    pg_id = 6
                    name = decode(wb, "Табл1", "b", row)
                    name_bd = session.query(TerritorialUnit).filter_by(name_ru=f'{name}').first()
                    if name_bd is None:
                        region_name = true_region_name(name)
                    else:
                        region_name = name
                    try:
                        region = session.query(TerritorialUnit).filter_by(name_ru=f'{region_name}').first()
                        rg_id = region.id

                        print(f'date: {date}\nvalue: {value_chl}\nweek:{week[0:2:]}\n'
                              f'name:{name}\nrg_id: {rg_id}\npg_id {pg_id}')

                        dc_contact['date'] = date
                        dc_contact['week'] = week
                        dc_contact['name'] = name
                        dc_contact['rg_id'] = rg_id
                        dc_contact['pg_id'] = pg_id
                        dc_contact['value'] = value_chl
                        data.append(dc_contact)

                        # insert(date, value_chl, week, rg_id, pg_id)
                    except AttributeError:
                        print(f"EROR - {region_name}")

            '''2. ЗАБОЛЕВАЕМОСТЬ ИНФЕКЦИЯМИ, ПЕРЕДАЮЩИМИСЯ КЛЕЩАМИ '''
            if decode(wb, "Табл1", "AN", row) is not None:
                if decode(wb, "Табл1", "AN", row) > 0:
                    value_all = decode(wb, "Табл1", "AN", row)  # КВЭ
                    pg_id = 1
                    toi_id = 1
                    name = decode(wb, "Табл1", "b", row)
                    name_bd = session.query(TerritorialUnit).filter_by(name_ru=f'{name}').first()
                    if name_bd is None:
                        region_name = true_region_name(name)
                    else:
                        region_name = name
                    try:
                        region = session.query(TerritorialUnit).filter_by(name_ru=f'{region_name}').first()
                        rg_id = region.id


                        print(f'date: {date}\nvalue: {value_all}\nweek:{week[0:2:]}\n'
                              f'name:{name}\nrg_id: {rg_id}\npg_id {pg_id}\ntoi_id {toi_id}')

                        dc_tick_morbidity_rate['date'] = date
                        dc_tick_morbidity_rate['week'] = week
                        dc_tick_morbidity_rate['name'] = name
                        dc_tick_morbidity_rate['rg_id'] = rg_id
                        dc_tick_morbidity_rate['pg_id'] = pg_id
                        dc_tick_morbidity_rate['value'] = value_all
                        dc_tick_morbidity_rate['toi_id'] = toi_id
                        data.append(dc_tick_morbidity_rate)

                        # insert(date, value_chl, week, rg_id, pg_id)
                    except AttributeError:
                        print(f"EROR - {region_name}")
            wb.close()

# session.commit()
# session.close()
