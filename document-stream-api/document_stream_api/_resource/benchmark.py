import asyncio
from aiohttp import ClientSession
import time


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r):
    url = "http://localhost:8001/api/account/1"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(700)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

number = 30000
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
start = time.time()
print('--- strart ---')
loop.run_until_complete(future)
print('--- end ---')
print(time.time() - start)
