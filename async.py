import asyncio

async def generate():
    for i in range(100):
        await asyncio.sleep(1)
        yield i

async def hello_world():
    async for contagem in generate():
        print(f"Hello {contagem}")

    
loop = asyncio.get_event_loop()
loop.create_task(hello_world())
loop.call_later(10, loop.stop)
loop.run_forever()

loop.close()
