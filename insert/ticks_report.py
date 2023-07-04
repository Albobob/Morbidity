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

ROOT = 'C:/Users/SimonyanAR.FCGIE/Desktop/p/Morbidity/insert/DATA'


def get_files(directory):
    """Получить имена файлов в каталоге."""
    files = os.listdir(directory)
    for file_name in files:
        print(file_name)
    return files


def process_files(files):
    """Обрабатывает файлы и заполняет дату, неделю, id и другие параметры."""
    for wk in files:
        week = wk[:2:]
        for row in range(12, 30):
            pass
    # Ваш обрабатывающий код здесь


def main():
    """Главная функция для обработки файлов в каталоге ROOT."""
    for year in os.listdir(ROOT):
        path = os.path.join(ROOT, year)
        # print(path)
        os.chdir(path)
        files = get_files(path)
        process_files(files)


print(main())
