from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ...base import Base


class VaccinatedMeasles(Base):
    """

    """
    __tablename__ = 'vaccinated_measles'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    vac_measles = Column(Integer)  # Число привитых людей
    unvac_population_measles = Column(Integer)  # Невакцинорованные
    vac_subjects_measles = Column(Integer)  # Число подлежащих вакцинации

    # Название региона
    rg_id = Column(Integer, ForeignKey('territorial_unit.id'), nullable=False)
    relationship('TerritorialUnit')
    # Возрастная группа в популяции
    pg_id = Column(Integer, ForeignKey('population_group.id'), nullable=False)
    relationship('PopulationGroup')

    def __init__(self, rg_id, date, population_group, vac_measles, unvac_population_measles, vac_subjects_measles):
        self.rg_id = rg_id
        self.date = date
        self.pg_id = population_group
        self.vac_measles = vac_measles
        self.unvac_population_measles = unvac_population_measles
        self.vac_subjects_measles = vac_subjects_measles
