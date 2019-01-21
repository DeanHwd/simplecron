#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, flash, request, session, url_for, abort, jsonify
import hashlib
import hmac
import json
import base64
from simplecron.db import DatabaseBroker
from simplecron.config import CONN_TIMEOUT, get_conf

au = Blueprint('auth', __name__)
db_file = get_conf('database', 'path')

def _signature(key, msg, mod=hashlib.sha256):
    return hmac.new(key, msg, digestmod=mod).hexdigest()

def login_required(func):

    def auth_wrapped(*args, **kwargs):
        token_list = []
        header = request.headers
        store_data = DatabaseBroker(db_file, CONN_TIMEOUT).query_db('select * from user', full=True)
        if store_data is None:
            return abort(401)

        for i in store_data:
            if isinstance(i['authentication_string'], unicode):
                key = i['created_at'].encode('utf-8')
                msg = i['authentication_string'].encode('utf-8')
            token_list.append(_signature(key, msg))

        try:
            if header['X-Auth-Token'] in token_list:
                return func(*args, **kwargs)
        except Exception as e:
            return abort(401)
        else:
            return abort(401)

    return auth_wrapped

@au.route('/auth/token', methods=['GET'])
def get_token():
    request_header = request.headers

    user = request_header.get('X-Auth-User', None)
    pwd = request_header.get('X-Auth-Password', None)
    if pwd is None or user is None:
        abort(401)

    store_data = DatabaseBroker(db_file, CONN_TIMEOUT).query_db('select * from user where user=?', data=(user, ))
    if not store_data:
        abort(401)

    password_string = store_data['authentication_string']

    if base64.b64encode(pwd) != password_string:
        abort(401)

    c_date = store_data['created_at']
    if isinstance(password_string, unicode):
        password_string = password_string.encode('utf-8')
        c_date = c_date.encode('utf-8')

    s = _signature(c_date, password_string, mod=hashlib.sha256)
    #return json.dumps({'X-Auth-Token': '%s' %(s)})
    return jsonify({'X-Auth-Token': '%s' %(s)})
