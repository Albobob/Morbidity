from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.form.form_2 import FormTwo

engine = create_engine("sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db", echo=False)
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


# print(get_smp(2010, 2019, 29, 1))
