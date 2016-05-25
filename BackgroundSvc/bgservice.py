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
    global c, d
    temparature = round(d.temp, 2)
    cpu = float(sum(d.cpu))/len(d.cpu)
    mem = float(sum(d.mem))/len(d.mem)
    power = (1.5 * cpu)/60
    print(str(temparature) + "  " + str(cpu) + "  " + str(mem))
    c.execute("INSERT INTO hostData VALUES (?,?,?,?);",(temparature, cpu, mem, power))
    
    # c.execute("INSERT INTO domDataVM1 VALUES (?,?,?,?);",(cpu, mem, netRead, netWrite))
    # c.execute("INSERT INTO domDataVM2 VALUES (?,?,?,?);",(cpu, mem, netRead, netWrite))
    # c.execute("INSERT INTO domDataVM3 VALUES (?,?,?,?);",(cpu, mem, netRead, netWrite))
    # c.execute("INSERT INTO domDataVM4 VALUES (?,?,?,?);",(cpu, mem, netRead, netWrite))

    conn.commit()

def readData():
    global d
    d.temp = get_temperature()
    for i in range(60):
        d.cpu[i],d.mem[i] = get_per_sec_info()
        time.sleep(1)

class HostData:
    def __init__(self):
        self.temp = 0
        self.cpu = [ 0 for i in range(60) ]
        self.mem = [ 0 for i in range(60) ]

def get_per_sec_info():
    global virt_connection,cdo
    # vm = []
    local_cpu = []
    local_mem = []
    
    for i in range(4):
        cdo = virt_connection.lookupByID(i+2)
        local_cpu.append(get_cpu(i+2))
        local_mem.append(get_mem())

    cpu_ind,mem_ind = local_cpu,local_mem
    
    cpu = (cpu_ind[0] + cpu_ind[1] + cpu_ind[2] + cpu_ind[3])/4
    mem = mem_ind[0] + mem_ind[1] + mem_ind[2] + mem_ind[3]
    return cpu, mem


cpu_ind = []
mem_ind = []
netRead = [0, 0, 0, 0]
netWrite = [0, 0, 0, 0]

def get_mem():
    global cdo
    stats = cdo.memoryStats()
    tmem = stats.get("actual",1)
    cmem = stats.get("rss",0)
    if "unused" in stats:
        cmem = max(0,tmem - stats.get("unused"),totalmem)
    return cmem/1024



def get_cpu(i):
    global cdo
    now = int(round(time.time() * 1000))
    info = cdo.info()
    guestcpus = info[3]
    nowcput = info[4]
    
    elapsedTime[i-2] = now - oldStats[i-2]['timestamp']
    utilisation = (nowcput - oldStats[i-2]['usedTime'])/elapsedTime[i-2]
    utilisation = utilisation/guestcpus
    utilisation = utilisation/1000000
    oldStats[i-2]['timestamp'] = now
    oldStats[i-2]['usedTime'] = nowcput
    print("cpu utilisation  ")
    print(round(utilisation,2))
    return utilisation*100

oldStats = [{'timestamp' : 0, 'usedTime' : 0} for i in range(4)]
elapsedTime = [0 for i in range(4)]




if __name__ == "__main__":
    virt_connection = libvirt.open("qemu:///system") # Connect Qemu
    # all_domains = self.virt_connection.listAllDomains(0) # Get all domains
    if virt_connection is None:
        print("No Qemu instance running.", file=sys.stderr)
        sys.exit(0)
    all_domains = virt_connection.listAllDomains(0) # Get all domains
    cdo = None
    conn = sqlite3.connect('dataDB.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE hostData(temp REAL, cpu REAL, mem REAL, power REAL)''')

    # c.execute('''CREATE TABLE domDataVM1(cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
    # c.execute('''CREATE TABLE domDataVM2(cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
    # c.execute('''CREATE TABLE domDataVM3(cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')
    # c.execute('''CREATE TABLE domDataVM4(cpu REAL, mem REAL, netRead REAL, netWrite REAL)''')

    d = HostData()
    while True:
        readData()
        writeData()
    conn.close()
