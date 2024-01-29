from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.name_of_diseases import NameOfDiseases
from Morbidity.config import SQL_PATH

engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def get_nz_info():
    value = session.query(NameOfDiseases.id, NameOfDiseases.name).all()
    return value

# print(get_tu_info())
