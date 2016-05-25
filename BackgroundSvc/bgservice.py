#!/usr/bin/python3
import os
import sys
import libvirt
import sqlite3
import subprocess
import time

def get_temperature():
    res = subprocess.check_output('sensors',shell=True)
    a = res.decode('utf-8')
    diva = a.split('\n')
    cpu1 = diva[2].split(' ')[4][1:5]
    cpu2 = diva[2].split(' ')[4][1:5]
    return (float(cpu1)+float(cpu2))/2

def writeData():
	global c, d, conn
	# cur.execute("insert into contacts (name, phone, email) values (?, ?, ?);",(name, phone, email))
	temparature = round(d.temp, 2)
	print(temparature)
	c.execute("INSERT INTO data VALUES (?);",(temparature,))
	conn.commit()

def readData():
	global d
	d.temp = get_temperature()
	for i in range(60):
		d.cpu[i],d.mem[i] = get_per_sec_info()
		time.sleep(1)

class Data:
	def __init__(self):
		self.temp = 0
		self.cpu = []
		self.mem = []

def get_cpu():
	pass

def get_mem():
	pass

if __name__ == "__main__":

    self.virt_connection = libvirt.open("qemu:///system") # Connect Qemu
    # all_domains = self.virt_connection.listAllDomains(0) # Get all domains
    if self.virt_connection is None:
        print("No Qemu instance running.", file=sys.stderr)
        sys.exit(0)

    all_domains = self.virt_connection.listAllDomains(0) # Get all domains


	conn = sqlite3.connect('dataDB.db')
	c = conn.cursor()
	# c.execute('''CREATE TABLE data(temp REAL)''')
	d = Data()
	while True:
		readData()
		writeData()
	conn.close()


