from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class NameOfDiseases(Base):
    __tablename__ = 'name_of_diseases'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    short_name = Column(String(50))
    num_form = Column(Integer, nullable=False)
    krista_id = Column(String(15))
    comment = Column(String(250))

    def __init__(self, name, num_form, krista_id, comment):
        self.name = name
        self.num_form = num_form
        self.krista_id = krista_id
        self.comment = comment
