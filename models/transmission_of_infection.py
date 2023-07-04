from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class TransmissionOfInfection(Base):
    __tablename__ = 'transmission_of_infection'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(500))

    def __init__(self, name_ru):
        self.name_ru = name_ru


    def __repr__(self):
        return f"<transmission_of_infection(id={self.id}, name={self.name})>"