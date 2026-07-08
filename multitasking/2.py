# multithreading
import threading
import time

def task(name):
    print(f"{name} started")
    time.sleep(2)   # Simulates I/O
    print(f"{name} finished")

t1 = threading.Thread(target=task, args=("Thread-1",))
t2 = threading.Thread(target=task, args=("Thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("Done")

# from concurrent.futures import ThreadPoolExecutor
# import time

# def work(i):
#     print(f"Starting {i}")
#     time.sleep(2)
#     print(f"Finished {i}")
#     return i * i

# with ThreadPoolExecutor(max_workers=3) as executor:
#     futures = [executor.submit(work, i) for i in range(6)]

#     for future in futures:
#         print(future.result())

# Key points on multithreading
# Shared memory — threads share the same variables/objects (no IPC needed), but this means you need locks to avoid race conditions.
# GIL bottleneck — for CPU-bound tasks, threads don't give real parallelism (they take turns, GIL released/acquired constantly). No speedup, sometimes even slower due to context-switch overhead.
# Great for I/O-bound tasks — network calls, file I/O, DB queries — because the GIL is released during I/O wait, letting other threads run while one waits. Real concurrency benefit here.
# Lightweight — cheaper to create than processes (no separate interpreter/memory duplication).

