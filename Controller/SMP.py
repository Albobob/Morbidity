from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.form_2 import FormTwo
from Morbidity.config import SQL_PATH

engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def get_smp(date_first: int, date_last: int, nz_input: int, rg_id: int) -> float:
    df = datetime.strptime(f"{date_first}-01-01", "%Y-%m-%d")
    dl = datetime.strptime(f"{date_last}-01-01", "%Y-%m-%d")

    value = session.query(FormTwo.value).filter(
        FormTwo.rg_id == rg_id,
        FormTwo.date.between(df, dl),
        FormTwo.nod_id == nz_input,
        FormTwo.pg_id == 1,
        FormTwo.type_value == 2
    ).all()

    if isinstance(value, float):
        return 0.0

    values = [i[0] for i in value if i[0] is not None]

    if len(values) == 0:
        return 0.0

    max_value = max(values)
    min_value = min(values)
    result_list = [i for i in values if i != max_value and i != min_value and i != 0]

    if len(result_list) == 0:
        return 0.0

    return sum(result_list) / len(result_list)


def compare_value(value, smp):
    try:
        deviation = ((value - smp) / smp) * 100

        if deviation > 1:
            if value >= smp * 1.5:
                num_times = round(value / smp, 1)
                return f"выше в {str(num_times).replace('.', ',')} раз"
            else:
                diff_percent = round(deviation, 1)
                return f"выше на {str(diff_percent).replace('.', ',')}%"
        elif deviation < -1:
            if value <= smp * 0.66:
                num_times = round(smp / value, 1)
                return f"ниже в {str(num_times).replace('.', ',')} раз"
            else:
                diff_percent = round(abs(deviation), 1)
                return f"ниже на {str(diff_percent).replace('.', ',')}%"
        else:
            return "на уровне"
    except ZeroDivisionError:
        return None
