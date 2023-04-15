from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class NameOfDiseases(Base):
    __tablename__ = 'name_of_diseases'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    num_form = Column(Integer, nullable=False)
    comment = Column(String(250))

    def __init__(self, name, num_form, comment):
        self.name = name
        self.num_form = num_form
        self.comment = comment
