"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""


from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr, DeclarativeMeta
from homework_04 import config


# Specifying echo=True upon the engine initialization will enable us to see generated SQL queries in the console.
# We should disable the "expire on commit" behavior of sessions with expire_on_commit=False. This is because in async
# settings, we don't want SQLAlchemy to issue new SQL queries to the database when accessing already committed objects.
engine = create_async_engine(config.SQLA_CONN_ASYNC_URI, echo=True)
# engine = create_async_engine(DATABASE_URL, future=True, echo=True) # что такое future, зачем оно нужно?
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base:
    @declared_attr
    def __tablename__(cls):
        """
        TODO: it's not enough to add "s" to make a plural but it works for Users and Posts
        """
        return f'{cls.__name__.lower()}s'

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self)


Base: DeclarativeMeta = declarative_base(bind=engine, cls=Base)
