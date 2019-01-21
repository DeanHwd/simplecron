#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
import argparse
from flask import Blueprint, flash, request, session, url_for, jsonify, abort
from simplecron.db import DatabaseBroker
from simplecron.config import Base_Cfg, get_conf, CONN_TIMEOUT
from simplecron.auth import login_required

cr = Blueprint('cron', __name__)

db_file = get_conf('database', 'path')

def get_dperformance_from_db(data):
    BC = Base_Cfg()
    r_data = {}
    key_list = BC.dp_key_list
    sql = BC.select_d_perform

    if not data:
        return abort(404)

    try:
        check_data = (data.split('device_id=')[-1], )
    except Exception as e:
        return abort(404)

    c_t = DatabaseBroker(db_file, CONN_TIMEOUT).query_db(sql, data=check_data)
    if c_t:
        lastest_data = list(c_t)
        for index, v in enumerate(lastest_data[3:]):
            r_data[key_list[index]] = v.encode('utf-8')

    #return json.dumps(r_data)
    return jsonify(r_data)

def set_dperformance_from_db(data):
    sql = Base_Cfg().insert_d_perform
    try:
        if isinstance(data, str):
            data = json.loads(data)
    except Exception as e:
        try:
            data = eval(data)
        except Exception as e:
            data = ''
    if not isinstance(data, dict):
        return ''

    insert_data = (data['device_id'], time.strftime('%y-%m-%d %H:%M:%S', time.localtime()), data['capacity_total'], data['capacity_used'], data['cpu_usage'], data['memory_usage'], data['nic_tx'], data['nic_rx'], data['throughput_read'], data['throughput_write'], data['iops_read'], data['iops_write'], data['latency_read'], data['latency_write'])

    DatabaseBroker(db_file, CONN_TIMEOUT).insert_db(sql, insert_data)
    return ''

@cr.route('/device/performance', methods=['GET', 'POST'])
@login_required
def d_performance():
    if request.method == 'GET':
        values = request.query_string
        return get_dperformance_from_db(values)
    elif request.method == 'POST':
        data = request.get_data()
        return set_dperformance_from_db(data)
