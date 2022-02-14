from sqlalchemy import Column, Integer, String, Sequence
from .async_database import Base
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = 'companies'
    __tableargs__ = {'comment': 'Компании'}
    id = Column(Integer, Sequence('company_seq'), primary_key=True)
    name = Column(String(200))
    catchPhrase = Column(String(200))
    bs = Column(String(200))

    def __str__(self):
        return f"{self.__class__.__name__}(" \
               f"__tablename__={self.__tablename__}, " \
               f"id={self.id}, " \
               f"name={self.name}, " \
               f"catchPhrase={self.catchPhrase}, " \
               f"bs={self.bs})"
