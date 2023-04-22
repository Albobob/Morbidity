from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class TerritorialUnit(Base):
    __tablename__ = 'territorial_unit'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(500), nullable=True)
    name_eng = Column(String(500))

    district_id = Column(Integer, ForeignKey('districts.id'), nullable=True)
    district = relationship('District', backref='territorial_unit')
    geo_category_id = Column(Integer, ForeignKey('geo_category.id'), nullable=True)
    geo_category = relationship('GeoCategory', backref='territorial_units')

    def __init__(self, name_ru, name_eng, district_id, geo_category_id):
        self.name_ru = name_ru
        self.name_eng = name_eng
        self.district_id = district_id
        self.geo_category_id = geo_category_id

    def to_dict(self):
        return {
            'id': self.id,
            'name_ru': self.name_ru,
            'name_eng': self.name_eng,
            'district_id': self.district_id,
            'geo_category_id': self.geo_category_id,
        }

    def __repr__(self):
        return f"<TerritorialUnit(id={self.id}, name_ru='{self.name_ru}', name_eng='{self.name_eng}')>"
