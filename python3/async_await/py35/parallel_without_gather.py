import asyncio
import time
from random import randint

async def say_after(val):
    print("Running ", val)
    print("Sleeping for {} seconds".format(1))
    await asyncio.sleep(1)
    print("Done ", val)
    return val ** 2
    

async def main():
    print("Started at {}".format(time.strftime("%I:%M:%p", time.localtime(time.time()))))
    tasks = [asyncio.ensure_future(say_after(i)) for i in range(10)]

    for task in tasks:
        await task

    print("Finished at {}".format(time.strftime("%I:%M:%p", time.localtime(time.time()))))



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
