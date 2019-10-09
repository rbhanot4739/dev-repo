import asyncio

async def coro1():
    await asyncio.sleep(15)
    return "Done"

async def coro2():
    await asyncio.sleep(3)
    return "Coro2 is Done"


def done_callback(future):
    if "Done" in future.result():
        print("Coro1 completed")
        with open("coro1.txt", "w") as ti:
            ti.write(future.result())

def done_callback2(future):
    if "Done" in future.result():
        print("Coro2 completed")
        with open("coro2.txt", "w") as ti:
            ti.write(future.result())
    

task1 = asyncio.ensure_future(coro1())
task1.add_done_callback(done_callback)

task2 = asyncio.ensure_future(coro2())
task2.add_done_callback(done_callback2)

tasks = asyncio.gather(task1, task2) # Gather schedules the tasks in parallel and returns the future object

loop = asyncio.get_event_loop()

loop.run_until_complete(tasks)