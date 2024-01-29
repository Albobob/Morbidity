from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class GeoCategory(Base):
    __tablename__ = 'geo_category'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(500))
    name_eng = Column(String(500))

    def __init__(self, name_ru, name_eng):
        self.name_ru = name_ru
        self.name_eng = name_eng

    def __repr__(self):
        return f"<GeoCategory(id={self.id}, name={self.name}, name_eng={self.name_eng})>"


