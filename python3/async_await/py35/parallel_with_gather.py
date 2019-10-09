import asyncio
import time
from random import randint

async def say_after(val):
    print("Running ", val)
    print("Sleeping for {} seconds".format(1))
    await asyncio.sleep(1)
    print("Done ", val)
    return val ** 2
    


tasks = asyncio.gather(
    say_after(1),
    say_after(2),
    say_after(3),
    say_after(4),
    say_after(2),
    say_after(3),
    say_after(4),
)

print(tasks)

loop = asyncio.get_event_loop()
res = loop.run_until_complete(tasks)
print("Result is ", res)
loop.close()
