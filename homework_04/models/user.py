from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .async_database import Base
from .mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tableargs__ = {'comment': 'Пользователи'}
    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True)
    posts = relationship("Post", back_populates="user")
    address = relationship("Address", back_populates="user")
    address_id = Column(Integer, ForeignKey('addresses.id'))
    phone = Column(String(150))
    website = Column(String(150))
    company = relationship("Company", back_populates="users")
    company_id = Column(Integer, ForeignKey('companies.id'))

    def __str__(self):
        return f"{self.__class__.__name__}(" \
               f"__tablename__={self.__tablename__}, " \
               f"id={self.id}, " \
               f"name={self.name!r}, " \
               f"username={self.username}, " \
               f"email={self.email}, " \
               f"created_at={self.created_at!r})"
