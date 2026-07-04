import asyncio

async def task(n):
    print(f"start {n}")
    await asyncio.sleep(1)   # simulates I/O wait — yields control
    print(f"end {n}")

async def main():
    await asyncio.gather(task(1), task(2), task(3))

asyncio.run(main())