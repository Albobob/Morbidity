import datetime
import string
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openpyxl import load_workbook
from models.population_group import PopulationGroup
from models.territorial_unit import TerritorialUnit
from models.district import District
from models.rus_total import RusTotal
from models.geo_category import GeoCategory

from models.report.measles_immunization_report.vaccinated_measles import VaccinatedMeasles

# Подключаемся к БД
engine = create_engine(f"{config.SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Всего
total = session.query(PopulationGroup).filter_by(name='total').first()
total_id = total.id
# Дети
children = session.query(PopulationGroup).filter_by(name='00-17').first()
children_id = children.id
# Взрослые
adult = session.query(PopulationGroup).filter_by(name='18+').first()
adult_id = adult.id
# Мигранты
migrants = session.query(PopulationGroup).filter_by(name='мигранты').first()
migrants_id = migrants.id

# Открываем XL
wb = load_workbook(filename='TemplateMeasles.xlsx', data_only=True)
abc = list(string.ascii_lowercase)


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


def insert(rg_id, rows):
    date = datetime.date(2023, 3, 29)

    total_unvac = decode(wb, 'tmp', abc[2], rows)
    total_vac_subjects = decode(wb, 'tmp', abc[5], rows)
    total_vac_measles = decode(wb, 'tmp', abc[9], rows)
    session.add(VaccinatedMeasles(rg_id, date, total_id, total_vac_measles, total_unvac, total_vac_subjects))

    children_unvac = decode(wb, 'tmp', abc[3], rows)
    children_vac_subjects = decode(wb, 'tmp', abc[6], rows)
    children_vac_measles = decode(wb, 'tmp', abc[10], rows)
    session.add(
        VaccinatedMeasles(rg_id, date, children_id, children_vac_measles, children_unvac, children_vac_subjects))

    adult_unvac = decode(wb, 'tmp', abc[4], rows)
    adult_vac_subjects = decode(wb, 'tmp', abc[7], rows)
    adult_vac_measles = decode(wb, 'tmp', abc[11], rows)
    session.add(VaccinatedMeasles(rg_id, date, adult_id, adult_vac_measles, adult_unvac, adult_vac_subjects))

    migrants_unvac = None
    migrants_vac_subjects = decode(wb, 'tmp', abc[8], rows)
    migrants_vac_measles = decode(wb, 'tmp', abc[12], rows)
    session.add(
        VaccinatedMeasles(rg_id, date, migrants_id, migrants_vac_measles, migrants_unvac, migrants_vac_subjects))


for row in range(9, 101):
    region_name = decode(wb, 'tmp', 'B', row)
    try:
        region = session.query(TerritorialUnit).filter_by(name_ru=f'{region_name}').first()
        rg_id = region.id
        insert(rg_id, row)
    except AttributeError:
        if region_name == 'Кемеровская область - Кузбасс':
            region_name = 'Кемеровская область'

        if region_name == 'Ханты-Мансийский автономный округ-Югра':
            region_name = 'Ханты-Мансийский автономный округ — Югра'

        if region_name == 'Чувашская Республика – Чувашия':
            region_name = 'Чувашская Республика'

        if region_name == 'Республика Татарстан (Татарстан)':
            region_name = 'Республика Татарстан'

        if region_name == 'Республика Северная Осетия-Алания':
            region_name = 'Республика Северная Осетия — Алания'

        if region_name == 'Республика Адыгея (Адыгея)':
            region_name = 'Республика Адыгея'

session.commit()
session.close()
