#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
from simplecron.config import Base_Cfg
from simplecron import utils
import logging
import re
import os

port = '8065'
user = 'kxuser'
password = 'kx123456'

def load_manage():
    return utils.get_manage()

def collect_d_per_data():
    tmp_file = '/tmp/_tmphdi_info'
    param_dict = {}
    k_list = Base_Cfg().dp_key_list
    default_r = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    Cmd = 'neucli3 device performance'
    res, out, err = utils.execute(Cmd)
    if not res:
        default_r = out.readlines()[-1].strip().split()

    res1, out1, err1 = utils.execute('get_hdi_tool -f %s' %(tmp_file))

    try:
        d_id = re.findall(r'\[(.*?)\]', out1.read())[0]
    except IndexError as e:
        d_id = ''

    if os.path.exists(tmp_file):
        os.unlink(tmp_file)

    param_dict['device_id'] = d_id

    for index, v in enumerate(k_list):
        param_dict[v] = default_r[index]

    ip = load_manage()
    auth_url = 'http://' + ip + ':' + port + '/auth/token'
    auth_header = {
                    "X-Auth-User" : user,
                    "X-Auth-Password" : password
                }

    res = requests.get(auth_url, headers=auth_header)
    if res.status_code == 200:
        auth_token = res.json()[u'X-Auth-Token']
        auth_token = auth_token.encode('utf-8')
    else:
        return

    p_url = 'http://' + ip + ':' + port + '/device/performance'
    headers = {'X-Auth-Token' : auth_token}
    tries = 0
    while tries < 3:
        try:
            requests.post(p_url, data=json.dumps(param_dict), headers=headers)
        except Exception as e:
            time.sleep(1)
            tries += 1
        else:
            break

def run():
    while True:
        sec = time.strftime('%S', time.localtime())
        if int(sec) in range(30, 32):
            collect_d_per_data()
        time.sleep(2)

if __name__ == '__main__':
    run()
