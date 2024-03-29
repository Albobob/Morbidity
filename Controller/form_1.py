import datetime
import string
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from openpyxl import load_workbook
from pprint import pprint
from Morbidity.models.form.name_of_diseases import NameOfDiseases
from Morbidity.models.geo_category import GeoCategory
from Morbidity.models.rus_total import RusTotal
from Morbidity.models.district import District
from Morbidity.models.territorial_unit import TerritorialUnit
from Morbidity.models.population_group import PopulationGroup
from Morbidity.models.type_value import TypeValue
from Morbidity.models.form.form_2 import FormTwo
from Morbidity.config import SQL_PATH

abc = list(string.ascii_lowercase)
# Подключаемся к БД
engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# всё население
total = session.query(PopulationGroup).filter_by(name='total').first()
total_id = total.id
# детское население 0-17 лет (включительно)
group_5 = session.query(PopulationGroup).filter_by(name='00-17').first()
group_5 = group_5.id
# детское население 0-17 лет (включительно)
group_6 = session.query(PopulationGroup).filter_by(name='00-14').first()
group_6 = group_6.id
# детское население: новорожденные
group_2 = session.query(PopulationGroup).filter_by(name='00-01').first()
group_2 = group_2.id
# детское население: от 1 года до 2 лет
group_3 = session.query(PopulationGroup).filter_by(name='01-02').first()
group_3 = group_3.id
# детское население от 3 до 6 лет
group_4 = session.query(PopulationGroup).filter_by(name='03-06').first()
group_4 = group_4.id
type_value_abs = session.query(TypeValue).filter_by(name='Абсолютное значение').first()
type_value_abs_id = type_value_abs.id
type_value_rate = session.query(TypeValue).filter_by(name='Показатель на 100 тыс. населения').first()
type_value_rate_id = type_value_rate.id

ls = {}


def x():
    for y in range(13):
        date = datetime.datetime(2010 + y, 1, 1)
        print(f'__________________________Форма 2___{date.strftime("%Y Год")}_____________________________________')
        for d in range(1, 9):
            query = session.query(District.name_ru, func.sum(FormTwo.value), ) \
                .join(TerritorialUnit, FormTwo.rg_id == TerritorialUnit.id) \
                .join(District, TerritorialUnit.district_id == District.id) \
                .join(RusTotal, RusTotal.id == District.rus_total_id) \
                .filter(District.id == d, FormTwo.nod_id == 7, FormTwo.pg_id == 1, FormTwo.type_value == 1,
                        FormTwo.date == date).all()
            print(query[0][1])


def y():
    for nz in range(1, 109):
        name_nz = session.query(NameOfDiseases.name).filter(NameOfDiseases.id == nz).all()
        print(f'__________{nz}__{name_nz[0][0]}__________')
        for i in range(1, 86):
            name = session.query(TerritorialUnit.name_ru).filter(TerritorialUnit.id == i).all()

            query = session.query(func.extract('year', FormTwo.date)) \
                .join(TerritorialUnit, FormTwo.rg_id == TerritorialUnit.id) \
                .filter(TerritorialUnit.id == i, FormTwo.nod_id == nz, FormTwo.pg_id == 1,
                        FormTwo.type_value == 1).all()
            if len(query) != 13:
                print(f'{name[0][0]} - {len(query)}')


# y()

session.commit()
session.close()
