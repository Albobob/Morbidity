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
Base.metadata.create_all(engine)
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
    region_dict = {'Москва': 'г. Москва', 'Санкт-Петербург': 'г. Санкт-Петербург',
                   'Республика Адыгея (Адыгея)': 'Республика Адыгея',
                   'Кемеровская область - Кузбасс': 'Кемеровская область',
                   'Ханты-Манийский автономный округ-Югра': 'Ханты-Мансийский автономный округ — Югра',
                   'Ханты-Мансийский АО': 'Ханты-Мансийский автономный округ — Югра',
                   'Ямало-Ненецкий АО': 'Ямало-Ненецкий автономный округ',
                   'Чувашская Республика – Чувашия': 'Чувашская Республика',
                   'Республика Татарстан (Татарстан)': 'Республика Татарстан',
                   'Республика Северная Осетия-Алания': 'Республика Северная Осетия — Алания',
                   'Республика Северная Осетия': 'Республика Северная Осетия — Алания',
                   'Республика Саха ( Якутия )': 'Республика Саха (Якутия)',
                   'Еврейская АО': 'Еврейская автономная область',
                   'Чукотский АО': 'Чукотский автономный округ'}
    return region_dict.get(name, name)


def insert_contacted(date, value, week: int, rg_id: int, pg_id: int):
    session.add(Contacted(date, rg_id, pg_id, value, week))


def insert_tick(date, rg_id: int, pg_id: int, value, toi_id: int, nod_id: int):
    session.add(TickMorbidityRate(date, rg_id, pg_id, value, toi_id, nod_id))
    pass


data = []

ROOT = 'C:/Users/SimonyanAR.FCGIE/Desktop/p/Morbidity/insert/DATA'


def get_files(directory: str):
    """Получить имена файлов в каталоге."""
    files = os.listdir(directory)
    for file_name in files:
        print(file_name)
    return files


def process_files(year: int, files, field: str, pg_id: int, toi_id, nod_id):
    """Обрабатывает файлы и заполняет дату, неделю, id и другие параметры."""
    for wk in files:
        week = int(wk[:2:])
        date = datetime.date(int(year), 1, 1) + datetime.timedelta(weeks=week - 1, days=4)
        print(date.strftime("%d.%m.%Y"))
        wb = load_workbook(f'{wk}', data_only=True)
        for row in range(12, 30):
            decoded_value = decode(wb, "Табл1", field, row)
            if decoded_value is not None and decoded_value > 0:
                name = decode(wb, "Табл1", "B", row)
                name_bd = session.query(TerritorialUnit).filter_by(name_ru=f'{name}').first()
                region_name = true_region_name(name) if name_bd is None else name
                try:
                    region = session.query(TerritorialUnit).filter_by(name_ru=region_name).first()
                    rg_id = region.id
                    value = decoded_value
                    if field in ('D', 'E',):
                        insert_contacted(date, value, week, rg_id, pg_id)
                        print(f'insert_contacted\ndate: {date}\nvalue: {value}\nweek:{week}\n'
                              f'name:{name}\nrg_id: {rg_id}\npg_id {pg_id}\ntoi_id {toi_id}')
                    elif field in ('AN', 'AO', 'AS', 'AT', 'BK', 'BL', 'BN', 'BO', 'BQ', 'BR'):
                        print('insert_tick')
                        insert_tick(date, rg_id, pg_id, value, toi_id, nod_id)
                    wb.close()
                except AttributeError:
                    wb.close()
                    print(f"EROR - {region_name}")


def main():
    """Главная функция для обработки файлов в каталоге ROOT."""
    for year in os.listdir(ROOT):
        path = os.path.join(ROOT, year)
        # print(year)
        os.chdir(path)
        files = get_files(path)
        '''1. ОБРАЩАЕМОСТЬ ПОСТРАДАВШИХ ОТ УКУСОВ КЛЕЩЕЙ.'''
        process_files(int(year), files, 'D', 1, None, None)
        process_files(int(year), files, 'E', 6, None, None)
        '''2. ЗАБОЛЕВАЕМОСТЬ ИНФЕКЦИЯМИ, ПЕРЕДАЮЩИМИСЯ КЛЕЩАМИ '''
        process_files(int(year), files, 'AN', 1, 1, 113)  # Взрослые трансмиссивным путем
        process_files(int(year), files, 'AO', 6, 1, 113)  # Дети трансмиссивным путем
        process_files(int(year), files, 'AS', 1, 2, 113)  # Взрослые алиментарным путем
        process_files(int(year), files, 'AT', 6, 2, 113)  # Дети алиментарным путем
        process_files(int(year), files, 'BK', 1, None, 110)  # ИКБ
        process_files(int(year), files, 'BL', 6, None, 110)  # ИКБ
        process_files(int(year), files, 'BN', 1, None, 111)  # МЭЧ
        process_files(int(year), files, 'BO', 6, None, 111)  # МЭЧ
        process_files(int(year), files, 'BQ', 1, None, 112)  # ГАЧ
        process_files(int(year), files, 'BR', 6, None, 112)  # ГАЧ


print(main())
