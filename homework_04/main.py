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


from homework_04.models import User, Address, Company, Post, async_session, engine, Base
from typing import Union


async def get_json(session, url):
    async with session.get(url) as resp:
        json_data = await resp.json()
        return json_data


async def fill_data(data):
    """ Fill tables with data"""
    print(data)
    async with async_session() as session:
        async with session.begin():
            session.add_all(data)


def prep_data(users: dict, posts: dict) -> list[Union[User, Address, Company, Post]]:
    res = []
    for item in users:
        user = User(
            id=item['id'],
            name=item['name'],
            username=item['username'],
            email=item['email'],
            phone=item['phone'],
            website=item['website'])

        address = Address(
            street=item['address']['street'],
            suite=item['address']['suite'],
            city=item['address']['city'],
            zipcode=item['address']['zipcode'],
            geo_lat=float(item['address']['geo']['lat']),
            geo_lng=float(item['address']['geo']['lng']))

        company = Company(
            name=item['company']['name'],
            catchPhrase=item['company']['catchPhrase'],
            bs=item['company']['bs'])

        user.address = address
        user.company = company
        res.append(user)
        res.append(address)
        res.append(company)

    for item in posts:
        res.append(Post(
            id=item['id'],
            user_id=item['userId'],
            title=item['title'],
            body=item['body']))
    return res


async def async_main():
    # create db tables, in real project should be done with alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    data_list = []
    url_list = [USERS_DATA_URL, POSTS_DATA_URL]

    async with aiohttp.ClientSession() as session:
        users, posts = await asyncio.gather(*[get_json(session, url) for url in url_list])

    rows = prep_data(users, posts)
    await fill_data(rows)


def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

