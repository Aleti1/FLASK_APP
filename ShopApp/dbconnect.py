#!/usr/bin/env python3

import MySQLdb


def connection():
    connect = MySQLdb.connect(host='localhost',
                                 user='root',
                                 passwd='',
                                 db='shop_table')
    cursor = connect.cursor()
    return  cursor, connect