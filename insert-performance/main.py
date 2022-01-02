import asyncio
from datetime import datetime

import asyncpg

from application import Application
from storage.storage import Storage


async def init_database_pool():
    return await asyncpg.create_pool(host='localhost', user='postgres', password='JKl12s85N02LA', database='insert-performance')


async def init_storage(database_connection_pool):
    storage = Storage(database_connection_pool)
    await storage.initialize()
    return storage


async def start_application():
    database_connection_pool = await init_database_pool()
    Application.storage = await init_storage(database_connection_pool)
    for i in range(100):
        timestamp = datetime.now()
        # for j in range(1000):
        #     await Application.storage.create_task_data(i*j + j, i, '1sdkasdkasdmasdqwreqwdasdxaseqwe')
        tasks = []
        for j in range(1000):
            tasks.append((i*j + j, i, '1sdkasdkasdmasdqwreqwdasdxaseqwe'))
        await Application.storage.create_1000_tasks_data(tasks)
        print(datetime.now() - timestamp)

    print('Finished')

    while True:
        await asyncio.sleep(3600)


async def stop_application():
    print('Stop requested')


if __name__ == '__main__':
    try:
        asyncio.run(start_application())
    except KeyboardInterrupt:
        asyncio.run(stop_application())
