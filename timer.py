"""Function for thread who call the client every x time to call the api."""
import asyncio
import sched
import time


def check_call(sc, data, loop):
    """schedule the first call."""
    s = sched.scheduler(time.time, time.sleep)
    check_call_run(sc, data, loop, s)


def check_call_run(sc, data, loop, s):
    """Call on_time and schedule another call main part."""
    asyncio.run_coroutine_threadsafe(data.on_time(), loop)
    s.enter(sc, 1, check_call_run, (sc, data, loop, s,))
    s.run()
