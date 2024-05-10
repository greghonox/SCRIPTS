import asyncio, time

async def country():
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    for key in keys:
        yield key
        await asyncio.sleep(1)
        print('await next')

async def get():
    async for i in country():
        print(i)    
        
async def main():
    print(f'{time.ctime()} iniciando')
    await asyncio.sleep(1)
    print(f'{time.ctime()} fim')

def blocking():
    time.sleep(0.5)
    print(f'{time.ctime()} Hello from a thread!')
    
     
loop = asyncio.get_event_loop()
tasks = loop.create_task(main())

loop.run_in_executor(None, blocking)
loop.run_until_complete(tasks)

pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()


async def echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.transport._extra['peername']
    print('New connection. {}'.format(peer))
    try:
        while data := await reader.readline():
            writer.write(data.upper())
            await writer.drain()
        print('Leaving Connection. {}'.format(peer))
    except asyncio.CancelledError:
        print('Connection dropped! {}'.format(peer))
        
        
async def server(host='127.0.0.1', port=8000):
    print('init server')
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()

print('gather:')
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.run_until_complete(get())
loop.run_until_complete(server())
loop.close()
