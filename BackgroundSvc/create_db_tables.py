#!/usr/bin/python3
import sqlite3

# create a new database
conn = sqlite3.connect('RawData.db')
c = conn.cursor()

# create host table
c.execute('''CREATE TABLE hostData  (date TEXT, time TEXT, cpu REAL, mem REAL, temp REAL, power REAL, netRead REAL, netWrite REAL) ''')

# create vm's tables
c.execute('''CREATE TABLE domDataVM1(date TEXT, time TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
c.execute('''CREATE TABLE domDataVM2(date TEXT, time TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
c.execute('''CREATE TABLE domDataVM3(date TEXT, time TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
c.execute('''CREATE TABLE domDataVM4(date TEXT, time TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
