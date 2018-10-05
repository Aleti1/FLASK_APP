#!/usr/bin/env python3

import MySQLdb


def connection():
    connect = MySQLdb.connect(host='localhost',
                                 user='root',
                                 passwd='1qaz@WSX',
                                 db='shop_table')
    cursor = connect.cursor()
    return  cursor, connect