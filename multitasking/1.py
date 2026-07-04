# multiprocessing: Run code across multiple separate processes, 
# each with its own Python interpreter and memory space, instead of multiple threads within one process. 
# This bypasses the GIL (Global Interpreter Lock) entirely — since each process has its own GIL.

from multiprocessing import Process, Pool
from concurrent.futures import ProcessPoolExecutor

def square(n):
    print(n * n)

def getSquare(n):
    return n * n


if __name__ == "__main__": # without this, infinite recursive process spawning
    # Single Process, no pool
    p1 = Process(target=square, args=(5,))
    p2 = Process(target=square, args=(10,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    # Process Pool
    with Pool(4) as p:
        results = p.map(getSquare, [1, 2, 3, 4, 5])
        print(results)
    # Process Pool uisng executor service
    with ProcessPoolExecutor() as executor:
        results = list[int](executor.map(square, [1, 2, 3, 4]))

# | Aspect              | Multiprocessing                                          | Multithreading                                           |
# | ------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
# | **Memory**          | Separate memory space per process                        | Shared memory space                                      |
# | **GIL**             | Each process has its own GIL — no contention             | Single GIL shared — bottleneck for CPU-bound tasks       |
# | **Best for**        | CPU-bound tasks (heavy computation)                      | I/O-bound tasks (network, file, DB calls)                |
# | **Communication**   | Needs IPC (Queue, Pipe, shared memory) — higher overhead | Direct shared variables (requires synchronization/locks) |
# | **Overhead**        | Higher (process creation, memory duplication)            | Lower (lightweight threads)                              |
# | **Crash isolation** | One process crashing usually doesn't affect others       | A thread crash can affect the entire process             |

# Multitasking by fork and spawn
# | Feature        | `fork`                                         | `spawn`                                          |
# | -------------- | ---------------------------------------------- | ------------------------------------------------ |
# | Child creation | Copies the parent process                      | Starts a completely new Python process           |
# | Memory         | Child inherits parent's memory (Copy-on-Write) | No memory inherited                              |
# | Speed          | Faster                                         | Slower                                           |
# | Platform       | Unix/Linux/macOS                               | Windows (default), also available on Unix        |
# | Globals        | Child already has global variables             | Everything is re-imported                        |
# | Threads        | Can be problematic if parent has threads       | Safe with threads                                |
# | Startup        | Continues from the point of `fork()`           | Starts execution from the beginning (`__main__`) |

# Common tools in the multiprocessing module
# * Process — spawn an individual process
# * Pool — manage a pool of worker processes, distribute tasks (very commonly used):
# * Queue / Pipe — safe inter-process communication (since processes don't share memory, you can't just pass objects directly)
# * shared_memory / Value / Array — for sharing primitive data across processes without full serialization overhead
# * Lock — synchronization when accessing shared resources (e.g., shared counters)



