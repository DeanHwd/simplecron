#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time
import logging
import os
from simplecron.config import Base_Cfg, base_user, base_pwd

#LOG = logging.getLogger(__file__)

def get_db_connection(path, timeout=30, okay_to_create=False):
    try:
        connect_time = time.time()
        conn = sqlite3.connect(path, timeout=timeout)
        if path != ':memory:' and not okay_to_create:
            stat = os.stat(path)
            if stat.st_size == 0 and stat.st_ctime >= connect_time:
                os.unlink(path)
        conn.row_factory = sqlite3.Row
    except Exception as e:
        #LOG.error(e)
        raise sqlite3.DatabaseError('sql missing')

    return conn

class DatabaseBroker(object):

    def __init__(self, db_file, timeout):
        self.conn = None
        self.db_file = db_file
        self.timeout = timeout

    def initialize(self):
        if self.db_file == ':memory:':
            conn = get_db_connection(self.db_file, self.timeout)
        else:
            conn = sqlite3.connect(self.db_file, timeout=self.timeout)

        conn.executescript("""
            DROP TABLE IF EXISTS user;
            CREATE TABLE user (
                user TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                authentication_string TEXT NOT NULL
            );
            DROP TABLE IF EXISTS device_p;
            CREATE TABLE device_p (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                updated_at DATETIME NOT NULL,
                capacity_total TEXT DEFAULT 0,
                capacity_used TEXT DEFAULT 0,
                cpu_usage TEXT DEFAULT 0,
                memory_usage TEXT DEFAULT 0,
                nic_tx TEXT DEFAULT 0,
                nic_rx TEXT DEFAULT 0,
                throughput_read TEXT DEFAULT 0,
                throughput_write TEXT DEFAULT 0,
                iops_read TEXT DEFAULT 0,
                iops_write TEXT DEFAULT 0,
                latency_read TEXT DEFAULT 0,
                latency_write TEXT DEFAULT 0
            );
            DROP TABLE IF EXISTS device_s;
            CREATE TABLE device_s (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                updated_at DATETIME NOT NULL,
                component_type TEXT NOT NULL,
                component_status TEXT NOT NULL,
                description TEXT NOT NULL,
                main_param TEXT NOT NULL
            );
            DROP TABLE IF EXISTS volume_p;
            CREATE TABLE volume_p (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                updated_at DATETIME NOT NULL,
                volume_uuid TEXT DEFAULT 0,
                volume_name TEXT DEFAULT 0,
                capacity_total DEFAULT 0,
                capacity_used TEXT DEFAULT 0,
                throughput_read DEFAULT 0,
                throughput_write TEXT DEFAULT 0,
                iops_read TEXT DEFAULT 0,
                iops_write TEXT DEFAULT 0,
                latency_read TEXT DEFAULT 0,
                latency_write TEXT DEFAULT 0
            );
            """)
        conn.commit()
        conn.close()
        self.insert_db(Base_Cfg().create_user, (base_user, time.strftime('%y-%m-%d %H:%M:%S', time.localtime()), base_pwd))

    def insert_db(self, sql, data):
        try:
            with get_db_connection(self.db_file, self.timeout) as conn:
                conn.cursor().execute(sql, data)
                conn.commit()
        except Exception as e:
            #LOG.error(e)
            raise

    def query_db(self, sql, data=None, full=False):
        r_data = None
        try:
            with get_db_connection(self.db_file, self.timeout) as conn:
                cur = conn.cursor()
                if data:
                    cur.execute(sql, data)
                else:
                    cur.execute(sql)
                r_data = cur.fetchall()
        except Exception as e:
            #LOG.error(e)
            raise
        finally:
            return r_data[0] if r_data and not full else r_data
