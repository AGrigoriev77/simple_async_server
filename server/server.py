#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 asgrig11
import json
from flask import Flask, request, jsonify

from action import Action

app = Flask(__name__)


@app.route('/task/add', methods=['POST'])
def add_task():
    response = action.add_task(json.loads(request.json))
    return jsonify({'response': response}), 201


@app.route('/task/get/<id>', methods=['GET'])
def get_result(id):
    response = action.get_result(id)
    return jsonify({'response': response}), 200


@app.route('/task/status/<id>', methods=['GET'])
def get_status(id):
    response = action.get_status(id)
    return jsonify({'response': response}), 200


if __name__ == '__main__':
    action = Action()
    app.run()
