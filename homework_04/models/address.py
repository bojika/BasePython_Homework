from sqlalchemy import Column, Integer, String, Sequence, Float
from .async_database import Base
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = 'addresses'
    __tableargs__ = {'comment': 'Адреса'}
    id = Column(Integer, Sequence('address_seq'), primary_key=True)
    street = Column(String(200))
    suite = Column(String(200))
    city = Column(String(50))
    zipcode = Column(String(20))
    geo_lat = Column(Float)
    geo_lng = Column(Float)

    def __str__(self):
        return f"{self.__class__.__name__}(" \
               f"__tablename__={self.__tablename__}, " \
               f"id={self.id}, " \
               f"street={self.street}, " \
               f"suite={self.suite}, " \
               f"city={self.city}, " \
               f"geo_lat={self.geo_lat}, " \
               f"geo_lng={self.geo_lng}, " \
               f"zipcode={self.zipcode})"
