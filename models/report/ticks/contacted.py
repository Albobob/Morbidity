from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Morbidity.models.base import Base


class Contacted(Base):
    __tablename__ = 'contacted'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    value = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    # Название региона
    rg_id = Column(Integer, ForeignKey('territorial_unit.id'), nullable=False)
    relationship('TerritorialUnit', backref='contacted')
    # Возрастная группа в популяции
    pg_id = Column(Integer, ForeignKey('population_group.id'), nullable=False)
    relationship('PopulationGroup', backref='contacted')

    def __init__(self, date, rg_id, population_group, value, week):
        self.date = date
        self.rg_id = rg_id
        self.pg_id = population_group
        self.value = value
        self.week = week

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'rg_id': self.rg_id,
            'pg_id': self.pg_id,
            'value': self.value,
            'week': self.week
        }
