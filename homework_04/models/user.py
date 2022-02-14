from sqlalchemy import Column, Sequence, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .async_database import Base
from .mixins import TimestampMixin

'''
{
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
        "street": "Kulas Light",
        "suite": "Apt. 556",
        "city": "Gwenborough",
        "zipcode": "92998-3874",
        "geo": {
            "lat": "-37.3159",
            "lng": "81.1496"
        }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
        "name": "Romaguera-Crona",
        "catchPhrase": "Multi-layered client-server neural-net",
        "bs": "harness real-time e-markets"
    }
}
'''


class User(TimestampMixin, Base):
    __tableargs__ = {'comment': 'Пользователи'}
    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True)
    posts = relationship("Post", back_populates="user")
    address = relationship("Address")
    address_id = Column(Integer, ForeignKey('addresses.id'))
    phone = Column(String(150))
    website = Column(String(150))
    company = relationship("Company")
    company_id = Column(Integer, ForeignKey('companies.id'))

    def __str__(self):
        return f"{self.__class__.__name__}(" \
               f"__tablename__={self.__tablename__}, " \
               f"id={self.id}, " \
               f"name={self.name!r}, " \
               f"username={self.username}, " \
               f"email={self.email}, " \
               f"created_at={self.created_at!r})"