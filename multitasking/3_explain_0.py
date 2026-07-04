from typing import Any
from collections import deque

WAIT_STATE = "WAIT_STATE"
PROMISE_STATE = "PROMISE_STATE"
DONE_STATE = "DONE_STATE"
TASK_STATE_MAP = []


def notify(task_id, task_state):
    if task_id < len(TASK_STATE_MAP):
        TASK_STATE_MAP[task_id] = task_state
    else:  
        TASK_STATE_MAP.insert(task_id, task_state)


current_task_id = None


def task(n):
    print(f"start {n}")
    notify(current_task_id, WAIT_STATE)
    return lambda: print(f"end {n}")


queue = deque[Any]()


def register(tasks):
    for task_id, task in enumerate[Any](tasks):
        task_object = (task_id, task)
        queue.append(task_object)
    while len(queue):
        task_id, popped_task = queue.popleft()
        global current_task_id
        current_task_id = task_id
        # print(f"current_task_id = {current_task_id}")
        callback = popped_task()
        if TASK_STATE_MAP[current_task_id] == WAIT_STATE:
            task_promise_object = (current_task_id, callback)
            queue.append(task_promise_object)
            notify(current_task_id, PROMISE_STATE)
        if TASK_STATE_MAP[current_task_id] == PROMISE_STATE:
            notify(current_task_id, DONE_STATE)


register([lambda x=1: task(x), lambda x=2: task(x), lambda x=3: task(x)])
