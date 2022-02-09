"""
Домашнее задание №3
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import aiohttp
import asyncio
import sys
from jsonplaceholder_requests import *

import time
from blog.models import *
from typing import Union

async def get_json(session, url):
    async with session.get(url) as resp:
        json_data = await resp.json()
        return json_data


async def fill_data(data: list[Union[User, Post]]):
    ''' Write users or posts to DB'''
    async with async_session() as session:
        async with session.begin():
            session.add_all(data)

async def fill_data_1(user: User, post: Post):
    ''' Write users or posts to DB'''
    print(user, post)
    async with async_session() as session:
        async with session.begin():
            session.add(user)
            session.add(post)

async def fill_data_2(users: dict, posts: dict):
    async with async_session() as session:
        async with session.begin():
            for user in users:
                session.add(User(id=user['id'],
                                 name=user['name'],
                                 username=user['username'],
                                 email=user['email']))
            for post in posts:
                session.add(Post(id=post['id'],
                                 user_id=post['userId'],
                                 title=post['title'],
                                 body=post['body']))





def mapper(url, data):
    res = []
    if url == POSTS_DATA_URL:
        return Post(id=data['id'],
                    user_id=data['userId'],
                    title=data['title'],
                    body=data['body'])
    if url == USERS_DATA_URL:
        return User(id=data['id'],
                    name=data['name'],
                    username=data['username'],
                    email=data['email'])


async def main():
    # create db tables, in real project should be done with alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    data_list = []
    url_list = [USERS_DATA_URL, POSTS_DATA_URL]

    async with aiohttp.ClientSession() as session:
        data_list = await asyncio.gather(*[get_json(session, url) for url in url_list])
        users, posts = data_list
    rows = [mapper(url, item) for url, data in zip(url_list, data_list) for item in data]
    for row in rows:
        print(row)

    await fill_data_2(users, posts)
    #await fill_data_1(rows[0], rows[10])
    # await fill_data(rows[:10])
    # await fill_data(rows[10:])

if __name__ == "__main__":
#
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
#    print("--- %s seconds ---" % (time.time() - start_time))

