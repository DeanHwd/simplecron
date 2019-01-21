#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import argparse
import os
from simplecron.config import get_conf, CONN_TIMEOUT
from simplecron.db import DatabaseBroker
from simplecron.task import task

app = Flask(__name__)
db_file = get_conf('database', 'path')

def Apalication():
    if db_file is None:
        raise

    if os.path.exists(db_file):
        stat = os.stat(db_file)
        if stat.st_size == 0:
            DatabaseBroker(db_file, CONN_TIMEOUT).initialize()
    else:
        DatabaseBroker(db_file, CONN_TIMEOUT).initialize()
    
    @app.route('/')
    def index():
        return 'TEST'

    from simplecron import cron
    from simplecron import auth
    app.register_blueprint(cron.cr)
    app.register_blueprint(auth.au)
    return app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--runserver',
                        dest='SERVER',
                        default='127.0.0.1',
                        help='The server the licensed')

    parser.add_argument('-p', '--port',
                        dest='PORT',
                        default='8065',
                        help='The port of server')

    parser.add_argument('-g', '--logfile',
                        dest='LOGFILE',
                        default='/var/log/simplecronerver.log',
                        help='specify the log file')

    parser.add_argument('-d', '--debug',
                        dest='DEBUG',
                        default=False,
                        help='Shows debugging output.')

    args = parser.parse_args()

    if db_file is None:
        raise

    if os.path.exists(db_file):
        stat = os.stat(db_file)
        if stat.st_size == 0:
            DatabaseBroker(db_file, CONN_TIMEOUT).initialize()
    else:
        DatabaseBroker(db_file, CONN_TIMEOUT).initialize()

    from simplecron import cron
    from simplecron import auth
    app.register_blueprint(cron.cr)
    app.register_blueprint(auth.au)

    app.run(host=args.SERVER, port=args.PORT, debug=args.DEBUG)

if __name__ == "__main__":
    main()
