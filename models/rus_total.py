from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class RusTotal(Base):
    __tablename__ = 'rus_total'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(500), nullable=False)
    name_eng = Column(String(500))

    geo_category_id = Column(Integer, ForeignKey('geo_category.id'), nullable=False)
    geo_category = relationship('GeoCategory', backref='rus_total')


    def __init__(self, name_ru, name_eng, geo_category_id):
        self.name_ru = name_ru
        self.name_eng = name_eng
        self.geo_category_id = geo_category_id

    def __repr__(self):
        return f"<RusTotal(id={self.id}, name_ru='{self.name_ru}', name_eng='{self.name_eng}', " \
               f"short_name_ru='{self.short_name_ru}', short_name_eng='{self.short_name_eng}')>"
