import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.form_2 import FormTwo
from Morbidity.config import SQL_PATH
from sqlalchemy import func

engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def get_fprm_2_info(date: str, name_of_diseases_id: int, population_group: int):
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


def get_top_5_regions(year: int, nz_id: int):
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 12, 31)

    result = session.query(FormTwo.rg_id, func.max(FormTwo.value)).filter(
        FormTwo.date.between(start_date, end_date),
        FormTwo.nod_id == nz_id,
        FormTwo.type_value == 2,
        FormTwo.pg_id == 1,
        FormTwo.value != 0,
        FormTwo.rg_id < 90
    ).group_by(FormTwo.rg_id).order_by(func.max(FormTwo.value).desc()).limit(5).all()

    return result


def get_down_5_regions(year: int, nz_id: int):
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 12, 31)

    result = session.query(FormTwo.rg_id, func.max(FormTwo.value)).filter(
        FormTwo.date.between(start_date, end_date),
        FormTwo.nod_id == nz_id,
        FormTwo.type_value == 2,
        FormTwo.pg_id == 1,
        FormTwo.value != 0,
        FormTwo.rg_id < 90
    ).group_by(FormTwo.rg_id).order_by(func.max(FormTwo.value).asc()).limit(5).all()

    return result
