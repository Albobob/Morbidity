import datetime
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
# adult = session.query(PopulationGroup).filter_by(name='18+')
# adult_id = adult.id
# Мигранты
# migrants = session.query(PopulationGroup).filter_by(name='мигранты')
# migrants_id = migrants.id

# Открываем XL
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


def insert(rg_id):
    date = datetime.date(2023, 3, 29)

    total_vac_measles = decode(wb, 'tmp', 'B', 12)
    total_unvac = decode(wb, 'tmp', 'E', 12)
    total_vac_subjects = decode(wb, 'tmp', 'I', 12)
    session.add(VaccinatedMeasles(rg_id, date, total_id, total_vac_measles, total_unvac, total_vac_subjects))

    children_vac_measles = decode(wb, 'tmp', 'C', 12)
    children_unvac = decode(wb, 'tmp', 'F', 12)
    children_vac_subjects = decode(wb, 'tmp', 'J', 12)
    session.add(VaccinatedMeasles(rg_id, date, 6, children_vac_measles, children_unvac, children_vac_subjects))

    adult_vac_measles = decode(wb, 'tmp', 'D', 12)
    adult_unvac = decode(wb, 'tmp', 'G', 12)
    adult_vac_subjects = decode(wb, 'tmp', 'K', 12)
    session.add(VaccinatedMeasles(rg_id, date, 7, adult_vac_measles, adult_unvac, adult_vac_subjects))

    migrants_vac_measles = None
    migrants_unvac = decode(wb, 'tmp', 'H', 12)
    migrants_vac_subjects = decode(wb, 'tmp', 'L', 12)
    session.add(VaccinatedMeasles(rg_id, date, 8, migrants_vac_measles, migrants_unvac, migrants_vac_subjects))


insert(1)

session.commit()
session.close()
