# %%
import asyncio


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")

    writer.write(data)
    await writer.drain()

    print(f"Sent {message!r} to {addr!r}")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Server running on {addr}")
    async with server:
        await server.serve_forever()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.call_later(10, loop.stop)
loop.run_forever()
loop.close()