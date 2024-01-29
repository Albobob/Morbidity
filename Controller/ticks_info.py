import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.report.ticks.contacted import Contacted
from Morbidity.config import SQL_PATH
from sqlalchemy import func, distinct, case

engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def contacted_sum_total(year, week, pg_id: int):
    start_date = datetime.datetime(year, 1, 1)
    end_date = start_date + datetime.timedelta(weeks=week - 1, days=5)

    previous_year = year - 1
    previous_start_date = datetime.datetime(previous_year, 1, 1)
    previous_end_date = previous_start_date + datetime.timedelta(weeks=week - 1, days=5)

    query_current_year = session.query(func.sum(Contacted.value)).filter(
        Contacted.pg_id == pg_id,
        Contacted.rg_id < 90,
        Contacted.value != 0,
        Contacted.date.between(start_date, end_date))

    query_previous_year = session.query(func.sum(Contacted.value)).filter(
        Contacted.pg_id == pg_id,
        Contacted.rg_id < 90,
        Contacted.value != 0,
        Contacted.date.between(previous_start_date, previous_end_date))

    current_value = query_current_year.scalar()
    previous_value = query_previous_year.scalar()
    return {
        'current_value': current_value,
        'current_date': end_date.strftime("%d.%m.%Y"),
        'previous_value': previous_value,
        'previous_date': previous_end_date.strftime("%d.%m.%Y")
    }


def get_rg_ids(year, week):
    start_date = datetime.datetime(year, 1, 1)
    end_date = start_date + datetime.timedelta(weeks=week - 1, days=5)

    previous_year = year - 1
    previous_start_date = datetime.datetime(previous_year, 1, 1)
    previous_end_date = previous_start_date + datetime.timedelta(weeks=week - 1, days=5)
    rg_ids = session.query(Contacted.rg_id).distinct().filter(
        Contacted.rg_id < 90,
        Contacted.value != 0,
        Contacted.date.between(start_date, end_date))

    previous_rg_ids = session.query(Contacted.rg_id).distinct().filter(
        Contacted.rg_id < 90,
        Contacted.value != 0,
        Contacted.date.between(previous_start_date, previous_end_date))

    current_rg_list = [i[0] for i in rg_ids.all()]
    previous_rg_list = [i[0] for i in previous_rg_ids.all()]

    current_value = len(current_rg_list)
    previous_value = len(previous_rg_list)

    return {
        'current_rg_list': current_rg_list,
        'current_rg_ids': current_value,
        'current_date': end_date.strftime("%d.%m.%Y"),
        'previous_rg_list': previous_rg_list,
        'previous_rg_ids': previous_value,
        'previous_date': previous_end_date.strftime("%d.%m.%Y")
    }


def get_min_max_year_week():
    min_year = session.query(func.extract('year', Contacted.date)).order_by(Contacted.date).first()
    max_year = session.query(func.extract('year', Contacted.date)).order_by(Contacted.date.desc()).first()

    min_week = session.query(Contacted.week).order_by(Contacted.week).first()
    max_week = session.query(Contacted.week).order_by(Contacted.week.desc()).first()

    return min_year[0], max_year[0], min_week[0], max_week[0]


def get_average_value(min_year, year, week):
    value_list = []
    for i in range(min_year, year + 1):
        value = contacted_sum_total(i, week, 1)['current_value']
        value_list.append(value)
    return round(sum(value_list) / len(value_list))


def get_min_max_value(min_year, year, week):
    value_list = []
    for i in range(min_year, year + 1):
        value = contacted_sum_total(i, week, 1)['current_value']
        value_list.append(value)
    return {
        'min': min(value_list),
        'max': max(value_list),
    }


print(get_average_value(2012, 2020, 20))
