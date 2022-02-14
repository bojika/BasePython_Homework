from sqlalchemy import Column, ForeignKey, Integer, String, Text
from .async_database import Base
from .mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Post(TimestampMixin, Base):
    __tableargs__ = {'comment': 'Посты'}
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    title = Column(String(200))
    body = Column(Text)
    user = relationship("User", back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(" \
               f"__tablename__={self.__tablename__}, " \
               f"id={self.id}, " \
               f"user_id={self.user_id}, " \
               f"title={self.title}, " \
               f"body={self.body!r}, " \
               f"created_at={self.created_at!r})"

    # By default, f-strings will use __str__(), but you can
    # make sure they use __repr__() if you include the conversion flag !r
