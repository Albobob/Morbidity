from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class PopulationGroup(Base):
    __tablename__ = 'population_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    comment = Column(String(250))

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return f"<PopulationGroup(id={self.id}, name='{self.name}', comment='{self.cmment}')>"



