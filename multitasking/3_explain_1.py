from collections import deque
from typing import Any, Callable

WAIT_STATE = "WAIT_STATE"
PROMISE_STATE = "PROMISE_STATE"
DONE_STATE = "DONE_STATE"

TASK_STATE_MAP = []


def notify(task_id, state):
    if task_id < len(TASK_STATE_MAP):
        TASK_STATE_MAP[task_id] = state
    else:
        TASK_STATE_MAP.append(state)


class Promise:
    def __init__(self):
        self._then = None

    def then(self, callback: Callable):
        self._then = callback
        return self

    def resolve(self):
        if self._then:
            self._then()


current_task_id = None


def task(n):
    print(f"start {n}")

    notify(current_task_id, WAIT_STATE)

    promise = Promise()
    promise.then(lambda: print(f"end {n}"))

    return promise


queue = deque[Any]()


def register(tasks):
    for task_id, task in enumerate(tasks):
        queue.append((task_id, task))

    while queue:
        task_id, current = queue.popleft()

        global current_task_id
        current_task_id = task_id

        result = current()

        if isinstance(result, Promise):
            if TASK_STATE_MAP[task_id] == WAIT_STATE:
                notify(task_id, PROMISE_STATE)
                queue.append((task_id, result.resolve))
            elif TASK_STATE_MAP[task_id] == PROMISE_STATE:
                result.resolve()
                notify(task_id, DONE_STATE)


register([
    lambda x=1: task(x),
    lambda x=2: task(x),
    lambda x=3: task(x),
])