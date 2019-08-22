#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 asgrig11
from collections import defaultdict
from enum import Enum
from threading import Thread
from queue import Queue
from time import sleep

NOT_FOUND = 'NOT FOUND'


class STATUS(Enum):
    queued = 'QUEUED'
    progress = 'IN PROGRESS'
    complete = 'COMPLETE'


class Action:
    SMALL_DELAY = 3
    BIG_DELAY = 7

    def __init__(self):
        self.task = defaultdict(dict)
        self.queue = Queue()
        self.thread = Thread(target=self.run_forever, daemon=True)
        self.thread.start()

    def get_task_id(self) -> str:
        return f'task_{len(self.task.keys()) + 1}'

    def add_task(self, task: dict) -> str:
        task_id = self.get_task_id()
        task.update(dict(status=STATUS.queued, task_id=task_id))
        self.task[task_id].update(task)
        self.queue.put(task)
        return task_id

    def get_result(self, task_id: str) -> str:
        result = self.task.get(task_id, None)
        if not result or result.get('status') != STATUS.complete:
            return NOT_FOUND
        return result.get('result')

    def get_status(self, id_task: str) -> str:
        result = self.task.get(id_task, None)
        if not result:
            return NOT_FOUND
        return result.get('status').value

    def execute_action(self, params=None) -> None:
        if not params:
            return
        result = None
        if params.get('cmd') == 'reverse':
            result = self.reverse(params.get('string'))
        if params.get('cmd') == 'swap':
            result = self.swap(params.get('string'))
        self.task[params.get('task_id')].update(dict(result=result, status=STATUS.complete))

    def run_forever(self) -> None:
        while True:
            while not self.queue.empty():
                task = self.queue.get()
                self.task[task.get('task_id')].update(dict(status=STATUS.progress))
                try:
                    self.execute_action(task)
                except Exception:
                    raise ValueError("Exception while executing action: %s", task)

    def reverse(self, string: str) -> str:
        sleep(self.SMALL_DELAY)
        return string[::-1]

    def swap(self, string: str) -> str:
        sleep(self.BIG_DELAY)
        return ''.join([string[i:i + 2][::-1] for i in range(0, len(string), 2)])
