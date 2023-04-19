from datetime import datetime
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
from SMP import get_smp

engine = create_engine("sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

##############
date_first = 2010
date_last = 2019
nz_input = 29
rg_id_1 = 90
rg_id_2 = 91
rg_id_3 = 3


########

def get_data(date_first: int, date_last: int, nz_input: int, rg_id: int) -> list:
    df = datetime.strptime(f"{date_first}-01-01", "%Y-%m-%d")
    dl = datetime.strptime(f"{date_last}-01-01", "%Y-%m-%d")
    value = session.query(FormTwo.value).filter(
        FormTwo.rg_id == rg_id,
        FormTwo.date.between(df, dl),
        FormTwo.nod_id == nz_input,
        FormTwo.pg_id == 1,
        FormTwo.type_value == 2
    ).all()
    return [i[0] for i in value if i[0] is not None]


data_1 = get_data(date_first, date_last, nz_input, rg_id_1)
data_2 = get_data(date_first, date_last, nz_input, rg_id_2)
data_3 = get_data(date_first, date_last, nz_input, rg_id_3)

