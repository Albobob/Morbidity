import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.form_2 import FormTwo
from Morbidity.config import SQL_PATH

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


print(get_fprm_2_info('2009-12-20 00:00:00', 1, 1))
