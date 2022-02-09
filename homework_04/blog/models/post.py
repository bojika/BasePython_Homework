from sqlalchemy import Column, ForeignKey, Integer, String, Text
from .async_database import Base
from .mixins import TimestampMixin

'''
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
'''


class Post(TimestampMixin, Base):
    __tablename__ = "posts"
    __tableargs__ = {'comment': 'Посты'}
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    title = Column(String(200))
    body = Column(Text)


    # def __init__(self, user_id, id, title, body):
    #     self.user_id = user_id
    #     self.id = id
    #     self.title = title
    #     self.body = body

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
