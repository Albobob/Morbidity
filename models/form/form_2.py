from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import Base


class FormTwo(Base):
    __tablename__ = 'form_2'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    value = Column(Integer, nullable=False)

    # Название региона
    rg_id = Column(Integer, ForeignKey('territorial_unit.id'), nullable=False)
    relationship('TerritorialUnit', backref='form_2')
    # Название нозологии
    nod_id = Column(Integer, ForeignKey('name_of_diseases.id'), nullable=False)
    relationship('NameOfDiseases', backref='form_2')
    # Возрастная группа в популяции
    pg_id = Column(Integer, ForeignKey('population_group.id'), nullable=False)
    relationship('PopulationGroup', backref='form_2')
    # Тип показателя (Интенсивный/Экстенсивный)
    type_value = Column(Integer, ForeignKey('type_value.id'), nullable=False)
    relationship('TypeValue',  backref='form_2')

    def __init__(self, date, name_of_diseases, population_group, type_value, value):
        self.date = date
        self.nod_id = name_of_diseases
        self.pg_id = population_group
        self.type_value = type_value
        self.value = value

    pass
