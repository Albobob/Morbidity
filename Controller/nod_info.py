from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.name_of_diseases import NameOfDiseases

engine = create_engine("sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def get_nz_info():
    value = session.query(NameOfDiseases.id, NameOfDiseases.name).all()
    return value

# print(get_tu_info())
