from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Morbidity.models.geo_category import GeoCategory
from Morbidity.models.rus_total import RusTotal
from Morbidity.models.district import District
from Morbidity.models.territorial_unit import TerritorialUnit
from Morbidity.config import SQL_PATH
from flask import jsonify
from pprint import pprint

engine = create_engine(f"{SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def get_tu_info():
    result = session.query(TerritorialUnit).all()
    result_dict = [r.to_dict() for r in result]
    return result_dict



