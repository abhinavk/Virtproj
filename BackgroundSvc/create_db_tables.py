#!/usr/bin/python3
import sqlite3

# create a new database
conn = sqlite3.connect('RawData.db')
c = conn.cursor()

# create host table
c.execute('''CREATE TABLE hostData  (dated TEXT, timed TEXT, cpu REAL, mem REAL, temp REAL, power REAL, netRead REAL, netWrite REAL) ''')

# create vm's tables
c.execute('''CREATE TABLE domDataVM1(dated TEXT, timed TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
c.execute('''CREATE TABLE domDataVM2(dated TEXT, timed TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
c.execute('''CREATE TABLE domDataVM3(dated TEXT, timed TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
c.execute('''CREATE TABLE domDataVM4(dated TEXT, timed TEXT, cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
