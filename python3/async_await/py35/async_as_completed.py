# asyncio.gathers runs multiples tasks/coroutines concurrently but it gives the results
# in the same order in which tasks were submitted and it will give result only when all the
# tasks are done. If you want res as soon as task is done we need to use asyncio.as_completed


import asyncio
import time
from random import randint

async def say_after(val):
    print("Running ", val)
    sleep_time = randint(0,9)
    print("Sleeping for {} seconds".format(sleep_time))
    await asyncio.sleep(sleep_time)
    print("Done ", val)
    return val ** 2
    

async def main(coros):
    for coro in asyncio.as_completed(coros):
        print("Result is {}".format(await coro))
    
tasks = [
    say_after(1),
    say_after(2),
    say_after(3),
    say_after(4),
]

loop = asyncio.get_event_loop()
loop.run_until_complete(main(tasks))
loop.close()
