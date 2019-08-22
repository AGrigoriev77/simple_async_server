#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 asgrig11
import argparse
from time import sleep

import requests
import json

EXPECTED = 'COMPLETE'
SERVER = 'http://localhost:5000'


def is_batch_mode(args) -> bool:
    return args.func.__name__ == 'batch'


def add_task(args):
    path = 'task/add'
    task_data = dict(cmd=args.cmd, string=args.string)
    resp = requests.post(f'{SERVER}/{path}', json=json.dumps(task_data))
    response = resp.json().get('response')
    if is_batch_mode(args):
        return response
    print(response)


def get_result(args):
    path = f'task/get/{args.task_id}'
    resp = requests.get(f'{SERVER}/{path}')
    response = resp.json().get('response')
    if is_batch_mode(args):
        return response
    print(response)


def get_status(args):
    path = f'task/status/{args.task_id}'
    resp = requests.get(f'{SERVER}/{path}')
    response = resp.json().get('response')
    if is_batch_mode(args):
        return response
    print(response)


def batch(args):
    args.task_id = add_task(args)
    print(f'Task id: {args.task_id}')
    status = get_status(args)
    print(f'Task id: {args.task_id} status: {status}')
    while not status == EXPECTED:
        status = get_status(args)
        print(f'Task id: {args.task_id} status: {status}')
        sleep(1)
    print(f'Task id: {args.task_id} result: {get_result(args)}')


def prepare_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser_add = subparser.add_parser('add', help='Append new task with parameters')
    parser_add.add_argument('cmd', choices=['reverse', 'swap'], help="command for process: reverse or swap")
    parser_add.add_argument('string', help="string for process")
    parser_add.set_defaults(func=add_task)

    parser_get = subparser.add_parser('get', help='Get the result of execution by task_id')
    parser_get.add_argument('task_id', help="task id for get result")
    parser_get.set_defaults(func=get_result)

    parser_status = subparser.add_parser('status', help='Check the status by task_id')
    parser_status.add_argument('task_id', help="task id for check status")
    parser_status.set_defaults(func=get_status)

    parser_batch = subparser.add_parser('batch', help='Run batch mode')
    parser_batch.add_argument('cmd', choices=['reverse', 'swap'], help="command for process: reverse or swap")
    parser_batch.add_argument('string', help="string for process")
    parser_batch.set_defaults(func=batch)

    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    args.func(args)
