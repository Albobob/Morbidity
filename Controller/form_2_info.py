import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.form_2 import FormTwo
from Morbidity.config import SQL_PATH
from sqlalchemy import func

engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def get_fprm_2_info(date, name_of_diseases_id, population_group):
    result = session.query(FormTwo).filter(
        FormTwo.date == date,
        FormTwo.nod_id == name_of_diseases_id,
        FormTwo.type_value == 2,
        FormTwo.pg_id == population_group
    )
    result_dict = [r.to_dict() for r in result]
    return result_dict


def get_min_max_year():
    min_year = session.query(func.extract('year', FormTwo.date)).order_by(FormTwo.date).first()
    max_year = session.query(func.extract('year', FormTwo.date)).order_by(FormTwo.date.desc()).first()
    return min_year[0], max_year[0]
    pass


print(get_min_max_year())
