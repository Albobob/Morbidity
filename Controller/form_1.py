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

abc = list(string.ascii_lowercase)
# Подключаемся к БД
engine = create_engine("sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db", echo=False)
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

date = datetime.datetime(2010, 1, 1)

for i in range(1,9):
    query = session.query(District.name_ru, func.sum(FormTwo.value), ). \
        join(TerritorialUnit, FormTwo.rg_id == TerritorialUnit.id) \
        .join(District, TerritorialUnit.district_id == District.id) \
        .filter(District.id == i, FormTwo.nod_id == 9, FormTwo.pg_id == 1, FormTwo.type_value == 1,
                FormTwo.date == date).all()
    pprint(query)



session.commit()
session.close()
