#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser, NoSectionError, NoOptionError
import os
import base64

base_config = '/etc/neucli/simplecron.conf'
CONN_TIMEOUT = 30
base_user = 'kxuser'
base_pwd = base64.b64encode('kx123456')

def get_conf(sect, value):

    if not os.path.exists(base_config):
        with open(base_config, 'w') as f:
            f.write('')

    cf = ConfigParser()
    cf.read(base_config)
    try:
        return cf.get(sect, value)
    except (NoSectionError, NoOptionError) as e:
        return None

class Base_Cfg(object):

    dp_key_list = ['capacity_total', 'capacity_used', 'cpu_usage', 'memory_usage', 'nic_tx', 'nic_rx', 'throughput_read', 'throughput_write', 'iops_read', 'iops_write', 'latency_read', 'latency_write']

    create_user = 'INSERT INTO user VALUES (?, ?, ?);'
    insert_d_perform = 'INSERT INTO device_p (device_id, \
                                              updated_at, \
                                              capacity_total, \
                                              capacity_used, \
                                              cpu_usage, \
                                              memory_usage, \
                                              nic_tx, \
                                              nic_rx, \
                                              throughput_read, \
                                              throughput_write, \
                                              iops_read, \
                                              iops_write, \
                                              latency_read, \
                                              latency_write) \
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

    select_d_perform = 'SELECT * FROM device_p WHERE device_id=? ORDER BY updated_at DESC LIMIT 1;'
