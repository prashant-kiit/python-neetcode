import asyncio

async def task(n):
    print(f"start {n}")
    await asyncio.sleep(1)   # simulates I/O wait — yields control
    print(f"end {n}")

async def main():
    await asyncio.gather(task(1), task(2), task(3))

asyncio.run(main())

# How it works internally
# Event loop — a single loop that maintains a queue of tasks/coroutines and decides what runs next.
# Coroutines (async def) — special functions that can pause and resume execution (unlike normal functions that run start-to-finish).
# await — the pause point. When a coroutine hits await something_io_bound(), it yields control back to the event loop, saying "I'm waiting, run someone else meanwhile."
# Event loop picks up another ready task, runs it until its next await, and so on — round-robin, cooperative.
# No actual parallel execution — just very fast switching during idle/wait time.

# Cooperative vs Preemptive (key distinction)
# Threading = preemptive — OS decides when to interrupt a thread, can happen anytime.
# Asyncio = cooperative — a task must explicitly yield (via await) — if it doesn't, it blocks the entire event loop, freezing everything else.
# async def bad_task():
#     time.sleep(5)   # ❌ blocking call — freezes the ENTIRE event loop, not just this task
# async def good_task():
#     await asyncio.sleep(5)   # ✅ non-blocking — yields control properly

# Why it's useful — I/O-bound concurrency without threads
# No GIL contention (only one thread anyway)
# No thread-switching/context-switch overhead
# Can handle thousands of concurrent connections efficiently (this is why frameworks like FastAPI, aiohttp use it) — since most time is spent waiting on network/DB, not computing.
# Not useful for CPU-bound work — since there's no real parallelism, a CPU-heavy await-free computation just blocks everything (need multiprocessing for that instead).