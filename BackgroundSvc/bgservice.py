#!/usr/bin/python3
import os
import sys
import libvirt
import sqlite3
import subprocess
import time
import datetime
from multiprocessing import Process
from xml.dom import minidom



# data-type to store values of all parameters of all vm's and host for 60 seconds
class RawData:
    def __init__(self):
        self.datestamp = None
        self.timestamp = None

        self.hostTemp = 0
        self.hostCPU = [ 0 for i in range(60) ]
        self.hostMEM = [ 0 for i in range(60) ]
        self.hostNETREAD = [ 0 for i in range(60) ]
        self.hostNETWRITE = [ 0 for i in range(60) ]

        self.vmCPU = [[] for i in range(4)]
        self.vmMEM = [[] for i in range(4)]
        self.vmNETREAD = [[] for i in range(4)]
        self.vmNETWRITE = [[] for i in range(4)]

    def update(self):
        for i in range(4):
            self.vmCPU[i] = []
            self.vmMEM[i] = []
            self.vmNETREAD[i] = []
            self.vmNETWRITE[i] = []
        self.datestamp = time.strftime('%Y-%m-%d')
        self.timestamp = time.strftime('%H:%M:%S')
    


# write the average of the stored 60 seconds values into database
def writeData(rdObj):
    vmcpu = []
    vmmem = []
    vmnetRead = []
    vmnetWrite = []

    conn = sqlite3.connect('RawData.db')
    c = conn.cursor()

    # for i in range(60):
    #     rdObj.hostCPU[i] = (rdObj.vmCPU[0][i] + rdObj.vmCPU[1][i] + rdObj.vmCPU[2][i] + rdObj.vmCPU[3][i])/4
    #     rdObj.hostMEM[i] = rdObj.vmMEM[0][i] + rdObj.vmMEM[1][i] + rdObj.vmMEM[2][i] + rdObj.vmMEM[3][i]
    #     rdObj.hostNETREAD[i] = rdObj.vmNETREAD[0][i] + rdObj.vmNETREAD[1][i] + rdObj.vmNETREAD[2][i] + rdObj.vmNETREAD[3][i]
    #     rdObj.hostNETWRITE[i] = rdObj.vmNETWRITE[0][i] + rdObj.vmNETWRITE[1][i] + rdObj.vmNETWRITE[2][i] + rdObj.vmNETWRITE[3][i]
    # 
    # temp = round(rdObj.hostTemp, 2)
    # cpu = float(sum(rdObj.hostCPU))/len(rdObj.hostCPU)
    # mem = float(sum(rdObj.hostMEM))/len(rdObj.hostMEM)
    # power = (1.5 * cpu)/60

    for i in range(4):
        vmcpu.append(float(sum(rdObj.vmCPU[i]))/len(rdObj.vmCPU[i]))
        vmmem.append(float(sum(rdObj.vmMEM[i]))/len(rdObj.vmMEM[i]))
        vmnetRead.append(float(sum(rdObj.vmNETREAD[i]))/len(rdObj.vmNETREAD[i]))
        vmnetWrite.append(float(sum(rdObj.vmNETWRITE[i]))/len(rdObj.vmNETWRITE[i]))
    
    cpu = float(sum(vmcpu)/4)
    # temp = rdObj.hostTemp
    mem = float(sum(vmmem))
    power = float((1.500*cpu)/60)
    # print(power)
    netrd = float(sum(vmnetRead))
    netwr = float(sum(vmnetWrite))


    
    c.execute("INSERT INTO hostData VALUES (?,?,?,?,?,?,?,?);",(rdObj.datestamp, rdObj.timestamp, cpu, mem, rdObj.hostTemp, power, netrd, netwr))
    c.execute("INSERT INTO domDataVM1 VALUES (?,?,?,?,?,?);",(rdObj.datestamp, rdObj.timestamp, vmcpu[0], vmmem[0], vmnetRead[0], vmnetWrite[0]))
    c.execute("INSERT INTO domDataVM2 VALUES (?,?,?,?,?,?);",(rdObj.datestamp, rdObj.timestamp, vmcpu[1], vmmem[1], vmnetRead[1], vmnetWrite[1]))
    c.execute("INSERT INTO domDataVM3 VALUES (?,?,?,?,?,?);",(rdObj.datestamp, rdObj.timestamp, vmcpu[2], vmmem[2], vmnetRead[2], vmnetWrite[2]))
    c.execute("INSERT INTO domDataVM4 VALUES (?,?,?,?,?,?);",(rdObj.datestamp, rdObj.timestamp, vmcpu[3], vmmem[3], vmnetRead[3], vmnetWrite[3]))

    # print("write done!!")

    conn.commit()
    conn.close()
    # print("Write ended at " + datetime.datetime.now().strftime("%M:%S.%f"))



# read data of the vm's and host from API's(libvirt and sensors)
def readData():
    global rdObj
    rdObj.hostTemp = get_temperature()
    for i in range(60):
        timebegin = time.time()
        get_per_sec_info()
        time.sleep(1-(time.time()-timebegin))



# get details of all vm's cpu utilisation, memory usage, network read and write, PER SECOND!
def get_per_sec_info():
    global virt_connection, cdo, rdObj
    for i in range(4):
        cdo = virt_connection.lookupByID(i+2)
        rdObj.vmCPU[i].append(get_cpu(i+2))
        rdObj.vmMEM[i].append(get_mem())
        temp = get_network_load(i+2)
        rdObj.vmNETREAD[i].append(temp[0])
        rdObj.vmNETWRITE[i].append(temp[1])



# get temparature of the host using 'sensors' file
def get_temperature():
    res = subprocess.check_output('sensors',shell=True)
    a = res.decode('utf-8')
    diva = a.split('\n')
    cpu1 = diva[2].split(' ')[4][1:5]
    cpu2 = diva[2].split(' ')[4][1:5]
    return (float(cpu1)+float(cpu2))/2



# get memory usage of a vm in the host
def get_mem():
    global cdo
    stats = cdo.memoryStats()
    tmem = stats.get("actual",1)
    cmem = stats.get("rss",0)
    if "unused" in stats:
        cmem = max(0,tmem - stats.get("unused"),totalmem)
    return cmem/1024



# get cpu utilisaion of the vm in the host 
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
    # print("cpu utilisation  ")
    # print(round(utilisation,2))
    return utilisation*100

oldStats = [{'timestamp' : 0, 'usedTime' : 0} for i in range(4)]
elapsedTime = [0 for i in range(4)]



# get network read and write speed(in KBps)
def get_network_load(i):
    global cdo
    rd  = 0
    wr = 0
    global prevnrd
    global prevnwr
    rxml = cdo.XMLDesc(0)
    xml = minidom.parseString(rxml)
    disks = xml.getElementsByTagName("interface")
    sources = disks[0].childNodes
    for source in sources:
        if source.nodeName == "target":
            devsrc = source.attributes["dev"].value      
    io = cdo.interfaceStats(devsrc)
    if io:
        currnrd = io[1]/1024
        currnwr = io[3]/1024
        rd = currnrd - prevnrd[i-2]
        wr = currnwr - prevnwr[i-2]
        prevnrd[i-2], prevnwr[i-2] = currnrd, currnwr
        return rd,wr

prevnrd = [ 0 for i in range(4) ]
prevnwr = [ 0 for i in range(4) ]



if __name__ == "__main__":
    virt_connection = libvirt.open("qemu:///system") # Connect Qemu
    all_domains = virt_connection.listAllDomains(0) # Get all domains
    print(all_domains)
    
    cdo = None

    rdObj = RawData()
    while True:
        rdObj.update() # to update the timestamp
        # print("Read started at " + datetime.datetime.now().strftime("%M:%S.%f"))
        readData()
        # print("Write started at " + datetime.datetime.now().strftime("%M:%S.%f"))
        write_process = Process(target=writeData, args=(rdObj,))
        write_process.start()
