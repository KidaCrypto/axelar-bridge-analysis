import functools
import aiohttp
import asyncio

def force_async(fn):
    '''
    turns a sync function to async function using threads
    '''
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper

async def get_api_data(session, queryId):
  async with session.get(f"https://node-api.flipsidecrypto.com/api/v2/queries/{queryId}/data/latest") as response:
    return await response.json()
  
async def get_all_data(queryIds):
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        for queryId in queryIds:
            post_tasks.append(get_api_data(session, queryId))
        # now execute them all at once
        return await asyncio.gather(*post_tasks)

#returns unioned data from multiple sources
#example chain data of Ethereum and Arbitrum
async def get_unioned_data_from(queryIds):
    ret = []
    data = await get_all_data(queryIds)
    for chainData in data:
        ret = ret + chainData
    return ret


def get_date(data):
  return data['date']

def get_date_capitalized(data):
  return data['DATE']