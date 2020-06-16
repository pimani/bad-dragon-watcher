"""Function for thread who call the client every x time to call the api."""
import asyncio
import time


def check_call(sc, data, loop):
    """schedule the first call."""
    last_check = time.time()
    asyncio.run_coroutine_threadsafe(data.on_time(), loop)
    while True:
        if time.time() - last_check >= sc:
            asyncio.run_coroutine_threadsafe(data.on_time(), loop)
            last_check = time.time()
        time.sleep(2)
