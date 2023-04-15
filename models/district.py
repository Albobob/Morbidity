from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(500), nullable=False)
    name_eng = Column(String(500))
    short_name_ru = Column(String(8))
    short_name_eng = Column(String(10))

    rus_total_id = Column(Integer, ForeignKey('rus_total.id'), nullable=False)
    rus_total = relationship('RusTotal', backref='districts')
    geo_category_id = Column(Integer, ForeignKey('geo_category.id'), nullable=False)
    geo_category = relationship('GeoCategory', backref='districts')


    def __init__(self, name_ru, name_eng=None, short_name_ru=None, short_name_eng=None, rus_total_id=None,
                 geo_category_id=None):
        self.name_ru = name_ru
        self.name_eng = name_eng
        self.short_name_ru = short_name_ru
        self.short_name_eng = short_name_eng
        self.rus_total_id = rus_total_id
        self.geo_category_id = geo_category_id

    def __repr__(self):
        return f"<District(id={self.id}, name_ru='{self.name_ru}', name_eng='{self.name_eng}', " \
               f"short_name_ru='{self.short_name_ru}', short_name_eng='{self.short_name_eng}', " \
               f"rus_total_id={self.rus_total_id}, geo_category_id={self.geo_category_id})>"
