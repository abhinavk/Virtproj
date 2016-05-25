#!/usr/bin/python3
import sys
import os
import subprocess
import libvirt
import math
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, random
from PyQt5 import QtWidgets, QtCore
from ui_domainmon import Ui_MainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import *
from xml.dom import minidom
import time

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class ResourceGraph(MyMplCanvas):
    """The widget which will be in each tab of each tabwidget"""
    def __init__(self, funcdata, lims, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.x = [60-i for i in range(60)]
        self.y = [0 for i in range(60)]
        self.func = funcdata
        self.lims = lims

        self.axes.invert_xaxis()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        # l = [random.randint(0, 10) for i in range(4)]
        self.y.pop(0)
        self.y.append(self.func())
        self.axes.plot(self.x,self.y, 'r')
        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim(self.lims)
        self.draw()


class ResourceDoubleGraph(MyMplCanvas):
    """The widget which will be in each tab of each tabwidget"""
    def __init__(self, funcdata, lims, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.x = [60-i for i in range(60)]
        self.y = [0 for i in range(60)]
        self.z = [0 for i in range(60)]
        self.func = funcdata
        self.lims = lims

        self.axes.invert_xaxis()
                
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        fdata = self.func()
        self.y.pop(0)
        self.y.append(fdata[0])
        self.z.pop(0)
        self.z.append(fdata[1])
        self.axes.plot(self.x, self.y, 'r', self.x, self.z, 'b')
        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim(self.lims)
        self.draw()


class ResourcePentaGraph(MyMplCanvas):
    """The widget which will be in each tab of each tabwidget"""
    def __init__(self, funcdata, lims, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.x = [60-i for i in range(60)]
        self.y1 = [0 for i in range(60)]
        self.y2 = [0 for i in range(60)]
        self.y3 = [0 for i in range(60)]
        self.y4 = [0 for i in range(60)]
        self.y0 = [0 for i in range(60)]
        self.lims = lims
        self.func = funcdata

        self.axes.invert_xaxis()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        fdata = self.func()
        self.y1.pop(0)
        self.y1.append(fdata[1])
        self.y2.pop(0)
        self.y2.append(fdata[2])
        self.y3.pop(0)
        self.y3.append(fdata[3])
        self.y4.pop(0)
        self.y4.append(fdata[4])
        self.y0.pop(0)
        self.y0.append(fdata[0])
        self.axes.plot(self.x, self.y1, 'r', self.x, self.y2, 'b', self.x, self.y3, 'y', self.x, self.y4, 'g', self.x, self.y0, 'k')
        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim(self.lims)
        self.draw()


class DisplayGraphs(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DisplayGraphs, self).__init__()  # To call init function in QtWidgets.QMainWindow WITHOUT using a object
        self.setupUi(self) # To call setupUi function in Ui_MainWindow WITHOUT using a object
        self.qemu_connect()
        self.tabWidget.setCurrentIndex(0)
        self.cdo = None
        self.viewGuestList()
        self.cid = -1
        self.isdFirst = True
        self.isnFirst = True
        
    def draw_init(self, domid):
        # Clear layout first
        if self.tab_info.layout() is not None:
            self.clear_tabs(self.tab_info)
        if self.tab_cpu.layout() is not None:
            self.clear_tabs(self.tab_cpu)
        if self.tab_mem.layout() is not None:
            self.clear_tabs(self.tab_mem)
        if self.tab_memu.layout() is not None:
            self.clear_tabs(self.tab_memu)
        if self.tab_disk.layout() is not None:
            self.clear_tabs(self.tab_disk)
        if self.tab_temp.layout() is not None:
            self.clear_tabs(self.tab_temp)
        
        
        if self.cdo.info()[0] is 1:
            vbox1 = self.make_info_tab() # Info
            vbox2 = self.make_graph_tab(self.get_cpu,[0,100]) # CPU
            # vbox3 = self.make_graph_tab(self.get_mips,[0,20000]) # MIPS
            vbox4 = self.make_graph_tab(self.get_memory) # Memory
            vbox4a = self.make_graph_tab(self.get_memoryu) # Memory
            vbox5 = self.make_disk_tab(self.get_disk_load,0) # Disk
            vbox6 = self.make_network_tab(self.get_network_load,0) # Network
            self.tab_info.setLayout(vbox1)
            self.tab_cpu.setLayout(vbox2)
            # self.tab_mips.setLayout(vbox3)
            self.tab_mem.setLayout(vbox4)
            self.tab_memu.setLayout(vbox4a)
            self.tab_disk.setLayout(vbox5)
            self.tab_temp.setLayout(vbox6)
            # self.isFirst = False
            self.dbutton.close()
            self.dbutton.clicked.connect(self.dbtnstop)
        else:
            self.dbutton.show()
            self.dbutton.clicked.connect(self.dbtnstart)
            self.dbutton.setText("Launch domain")

    def dbtnstop(self):
        os.system("sudo virsh shutdown " + self.cdo.name())
        self.draw_init(self)
        
    def dbtnstart(self):
        self.cdo.create()
        self.draw_init(self)

    def clear_tabs(self, layout):
        ly = layout.layout()
        while ly.count():
            child = ly.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())
        QtCore.QObjectCleanupHandler().add(layout.layout())
    

    def viewGuestList(self):
        all_domains = self.virt_connection.listAllDomains(0) # Get all domains
        if len(all_domains) > 0:
            self.cdo = self.virt_connection.lookupByName(all_domains[0].name())
            self.draw_init(self)
        else:
            self.draw_init(self, -1)
        model = QStandardItemModel(self.listView)
        for domain in all_domains:
            item = QStandardItem(str(domain.name()))
            model.appendRow(item)
        self.listView.clicked.connect(self.handle_click)
        self.listView.setModel(model)
    
    def decodeInfo(self,argument):
        switcher = { 0: "NoState", 1: "Running", 2: "Blocked", 3: "Paused", 4: "Shutdown", 5:"Shutoff", 6: "Crashed" }
        return switcher.get(argument)

    def handle_click(self,i):
        self.label.setText(i.data())
        self.cdo = self.virt_connection.lookupByName(i.data())
        vm_state = self.decodeInfo(self.cdo.info()[0])
        self.label_2.setText(vm_state)
        self.isnFirst = True
        self.isdFirst = True
        self.draw_init(self)
        

    def qemu_connect(self):
        self.virt_connection = libvirt.open("qemu:///system") # Connect Qemu
        # all_domains = self.virt_connection.listAllDomains(0) # Get all domains
        if self.virt_connection is None:
            print("No Qemu instance running.", file=sys.stderr)
            exit(1)
        self.host_info = self.virt_connection.getInfo()

    # def draw_graph(self):
    #     vbox1 = self.make_info_tab() # Info
    #     # vbox2 = self.make_pentagraph_tab(self.get_cpu,[0,100]) # CPU
    #     # vbox3 = self.make_graph_tab(self.get_mips,[0,20000]) # MIPS
    #     # vbox4 = self.make_graph_tab(self.get_memory,[0,8192]) # Memory
    #     # vbox5 = self.make_doublegraph_tab(self.get_disk_load) # Disk
    #     # vbox6 = self.make_graph_tab(self.get_network_load) # Network
    #     self.tab_info.setLayout(vbox1)
    #     # self.tab_cpu.setLayout(vbox2)
    #     # self.tab_mips.setLayout(vbox3)
    #     # self.tab_mem.setLayout(vbox4)
    #     # self.tab_disk.setLayout(vbox5)
    #     # self.tab_temp.setLayout(vbox6)

    def make_graph_tab(self,funcdata=None,lims=None):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceGraph(funcdata,lims,self.main_widget)
        vbox = QVBoxLayout()
        vbox.addWidget(sc)
        return vbox

    def make_disk_tab(self,funcdata=None,lims=None):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceDoubleGraph(funcdata,lims,self.main_widget)
        vbox = QVBoxLayout()
        label_string = "Red: readKB/s \nBlue: writeKB/s"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(sc)
        vbox.addWidget(label)
        return vbox

    def make_network_tab(self,funcdata=None,lims=None):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceDoubleGraph(funcdata,lims,self.main_widget)
        vbox = QVBoxLayout()
        label_string = "Red: readKB/s \nBlue: writeKB/s"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(sc)
        vbox.addWidget(label)
        return vbox

    # For Network Load
    def make_doublegraph_tab(self,funcdata=None,lims=None):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceDoubleGraph(funcdata,lims,self.main_widget)
        vbox = QVBoxLayout()
        label_string = "Red: readKB/s \n Blue: writeKB/s"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(sc)
        vbox.addWidget(label)
        return vbox

    def make_pentagraph_tab(self,funcdata=None,lims=None):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourcePentaGraph(funcdata,lims,self.main_widget)
        vbox = QVBoxLayout()
        label_string = "Red: Core1 \n Blue: Core2 \n Green: Core3 \n Yellow: Core4 \n Black: Total CPU"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(sc)
        vbox.addWidget(label)
        return vbox

    def make_info_tab(self):
        self.main_widget = QtWidgets.QWidget(self)
        vbox = QVBoxLayout()

        # Get all cpu info
        host_info = self.host_info
        label_string = "Domain ID: " + str(self.cdo.ID())
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Host Name label
        # print(dir(self.cdo))
        label_string = "CPU cores alloc: " + str(len(self.cdo.vcpus()[0]))
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Architecture label
        label_string = "CPU core architecture: x86"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create CPU Name label
        # print(dir(self.cdo.OSType))
        label_string = "Operating System type: " + str(self.cdo.OSType())
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Memory size label
        label_string = "Memory allocated: " + str(self.cdo.maxMemory()/1024) + " MB"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Current Clock speed label
        label_string = "Memory currently used: " + str(self.cdo.memoryStats()["rss"]/1024) + " MB"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create CPU Cores label
        rxml = self.cdo.XMLDesc(0)
        xml = minidom.parseString(rxml)
        disks = xml.getElementsByTagName("disk")
        sources = disks[0].childNodes
        for source in sources:
            if source.nodeName == "source":
                label_string = "Disk file: " + str(source.attributes["file"].value)
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create CPU Threads label
        label_string = "CPU Threads: " + str(host_info[6]*host_info[7])
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

         # Create Hypervisor label
        label_string = "Hypervisor: " + self.virt_connection.getType()
        version = " version " + str(self.virt_connection.getVersion())
        label = QtWidgets.QLabel(label_string + version,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create URI label
        if self.cdo.autostart is True:
            autostart = 'Enabled'
        else:
            autostart = 'Disabled'
        label_string = 'Autostarts on boot: ' + autostart
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        return vbox

    # def get_temperature(self):
    #     res = subprocess.check_output('sensors',shell=True)
    #     a = res.decode('utf-8')
    #     diva = a.split('\n')
    #     cpu1 = diva[2].split(' ')[4][1:5]
    #     cpu2 = diva[2].split(' ')[4][1:5]
    #     return (float(cpu1)+float(cpu2))/2

    def get_memory(self):
        stats = self.cdo.memoryStats()
        tmem = stats.get("actual",1)
        cmem = stats.get("rss",0)
        if "unused" in stats:
            cmem = max(0,tmem - stats.get("unused"),totalmem)

        pcmem = (cmem/float(tmem))*100
        # pcmem = max(0.0,min(pcmem, 100.0))
        return pcmem

    def get_memoryu(self):
        stats = self.cdo.memoryStats()
        tmem = stats.get("actual",1)
        cmem = stats.get("rss",0)
        if "unused" in stats:
            cmem = max(0,tmem - stats.get("unused"),totalmem)

        return cmem/1024

    def get_disk_load(self):
        rd = 0
        wr = 0
        global prevrd
        global prevwr


        # Some drivers support this method for getting all usage at once
        try:
            rxml = self.cdo.XMLDesc(0)
            xml = minidom.parseString(rxml)
            disks = xml.getElementsByTagName("disk")
            sources = disks[0].childNodes
            for source in sources:
                if source.nodeName == "source":
                    devsrc = source.attributes["file"].value
            io = self.cdo.blockStats(devsrc)
            if io:
                currrd = io[1]/1024
                currwr = io[3]/1024
                rd = currrd - prevrd
                wr = currwr - prevwr
                prevrd, prevwr = currrd, currwr

                if self.isdFirst is True:
                    self.isdFirst = False
                    return 0,0
                return rd, wr
        except libvirt.libvirtError:
            self._summary_disk_stats_skip = True
        return rd, wr

    def zeroout(val):
        if val < 0.1:
            return 0

    # For Network load
    def get_network_load(self):
        
        rd  =0
        wr =0
        global prevnrd
        global prevnwr
        rxml = self.cdo.XMLDesc(0)
        xml = minidom.parseString(rxml)
        disks = xml.getElementsByTagName("interface")
        sources = disks[0].childNodes
        for source in sources:
            if source.nodeName == "target":
                devsrc = source.attributes["dev"].value      
        io = self.cdo.interfaceStats(devsrc)
        if io:
            currnrd = io[1]/1024
            currnwr = io[3]/1024
            rd = currnrd - prevnrd
            wr = currnwr - prevnwr
            prevnrd, prevnwr = currnrd, currnwr
            
            if self.isnFirst is True:
                self.isnFirst = False
                return 0,0
            return rd,wr



    # def get_mips(self):
    #     global agg_cpu_usage
    #     from_stdout = subprocess.check_output('cat /proc/cpuinfo | grep "bogomips"',shell=True)
    #     maxmips = from_stdout.decode('utf-8').split('\n')[0].split(':')[1].strip()
    #     return float(maxmips) * agg_cpu_usage * 0.04

    # def get_cpu(self):
    #     global prevCpuTime
    #     global prevTimestamp
        
    #     now = time.time()
    #     info = self.cdo.info()
    #     guestcpus = info[3]
    #     cpuTime = info[4] - prevCpuTime
    #     cpuTimeCurr = info[4]
    #     pcbase = (((cpuTime)*100.0)/((now - prevTimestamp) * 1000.0 * 1000.0 * 1000.0))
    #     pcdomCpu = guestcpus > 0 and pcbase/guestcpus or 0
    #     pcdomCpu = max(0.0, min(100.0,pcdomCpu))
    #     prevTimestamp = now
    #     prevCpuTime = cpuTime
    #     return pcdomCpu



    def get_cpu(self):
        now = int(round(time.time() * 1000))
        info = self.cdo.info()
        guestcpus = info[3]
        nowcput = info[4]
        
        elapsedTime = now - oldStats['timestamp']
        utilisation = (nowcput - oldStats['usedTime'])/elapsedTime
        utilisation = utilisation/guestcpus
        utilisation = utilisation/1000000
        oldStats['timestamp'] = now
        oldStats['usedTime'] = nowcput
        # print(round(utilisation,2))
        return utilisation*100

prevstat = [[0 for i in range(9)] for i in range(5)]
agg_cpu_usage = 0
prevrd = 0
prevwr =0
prevnrd = 0
prevnwr =0
# prevCpuTime = 0
# prevTimestamp = 0

oldStats = {'timestamp' : 0, 'usedTime' : 0}
elapsedTime = 0

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myui = DisplayGraphs()
    myui.show()
    sys.exit(app.exec_())
