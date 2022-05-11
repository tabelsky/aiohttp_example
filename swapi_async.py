import asyncio
import aiohttp
import time
from more_itertools import chunked


URL = 'https://swapi.dev/api/people/'

MAX = 100
PARTITION = 10
SLEEP_TIME = 1


async def health_check():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get('https://swapi.dev/api/') as response:
                    if response.status == 200:
                        print('OK')
                    else:
                        print(response.status)
            except Exception as er:
                print(er)
            await asyncio.sleep(1)


async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}') as response:
        return await response.json()


async def get_people(all_ids, partition, session):
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_person(person_id, session)) for person_id in chunk_ids]
        for task in tasks:
            task_result = await task
            yield task_result


async def main():
    health_check_task = asyncio.create_task(health_check())
    print(health_check_task)
    async with aiohttp.ClientSession() as session:
        async for people in get_people(range(1, MAX +1), PARTITION, session):
            print(len(people))

start = time.time()
asyncio.run(main())
print(time.time() - start)