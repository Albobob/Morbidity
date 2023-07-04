from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Morbidity.models.base import Base


class TickMorbidityRate(Base):
    __tablename__ = 'tick_morbidity_rate'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    value = Column(Integer, nullable=False)
    # Название региона
    rg_id = Column(Integer, ForeignKey('territorial_unit.id'), nullable=False)
    relationship('TerritorialUnit', backref='tick_morbidity_rate')
    # Возрастная группа в популяции
    pg_id = Column(Integer, ForeignKey('population_group.id'), nullable=False)
    relationship('PopulationGroup', backref='tick_morbidity_rate')

    toi_id = Column(Integer, ForeignKey('transmission_of_infection.id'), nullable=True)
    relationship('TransmissionOfInfection', backref='tick_morbidity_rate')

    nod_id = Column(Integer, ForeignKey('transmission_of_infection.id'), nullable=False)
    relationship('NameOfDiseases', backref='tick_morbidity_rate')

    def __init__(self, date, rg_id, population_group, value, transmission_of_infection, nod_id):
        self.date = date
        self.rg_id = rg_id
        self.pg_id = population_group
        self.value = value
        self.toi_id = transmission_of_infection
        self.nod_id = nod_id

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'rg_id': self.rg_id,
            'pg_id': self.pg_id,
            'value': self.value,
            'toi_id': self.toi_id,
            'nod_id': self.nod_id,
        }
