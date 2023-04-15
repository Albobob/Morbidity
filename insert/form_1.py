from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

# Подключаемся к БД
engine = create_engine(f"{config.SQL_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
