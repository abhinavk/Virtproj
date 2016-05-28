#!/usr/bin/python3
import sys
import subprocess
import libvirt
import math
import matplotlib
import sqlite3
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, random
from PyQt5 import QtWidgets, QtCore
from ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QVBoxLayout

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

class PowerResourceGraph(MyMplCanvas):
    """The widget which will be in each tab of each tabwidget"""
    def __init__(self, funcdata, lims, timerv = 1000, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.x = [60-i for i in range(60)]
        self.y = [0 for i in range(60)]
        self.func = funcdata
        self.lims = lims

        self.axes.invert_xaxis()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(timerv)

    def update_figure(self):
        # l = [random.randint(0, 10) for i in range(4)]
        self.y = self.func()
        self.axes.plot(self.x,self.y, 'r')
        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim(self.lims)
        self.draw()

class ResourceGraph(MyMplCanvas):
    """The widget which will be in each tab of each tabwidget"""
    def __init__(self, funcdata, lims, timerv = 1000, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.x = [60-i for i in range(60)]
        self.y = [0 for i in range(60)]
        self.func = funcdata
        self.lims = lims

        self.axes.invert_xaxis()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(timerv)

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
        self.draw_graph()
        self.tabWidget.setCurrentIndex(0)

    def qemu_connect(self):
        self.virt_connection = libvirt.open("qemu:///system") # Connect Qemu
        all_domains = self.virt_connection.listAllDomains(0) # Get all domains
        if self.virt_connection is None:
            print("No Qemu instance running.", file=sys.stderr)
            exit(1)
        self.host_info = self.virt_connection.getInfo()

    def draw_graph(self):
        vbox1 = self.make_info_tab() # Info
        vbox2 = self.make_pentagraph_tab(self.get_cpu,[0,100]) # CPU
        vbox3 = self.make_graph_tab(self.get_mips,[0,20000]) # MIPS
        vbox4 = self.make_graph_tab(self.get_memory,[0,8192]) #Memory
        vbox5 = self.make_doublegraph_tab(self.get_disk_load) # Disk
        vbox6 = self.make_graph_tab(self.get_temperature,[20,80]) # Temperature
        vbox7 = self.make_powergraph_tab(self.get_power, timerv=1000)
        self.tab_info.setLayout(vbox1)
        self.tab_cpu.setLayout(vbox2)
        self.tab_mips.setLayout(vbox3)
        self.tab_mem.setLayout(vbox4)
        self.tab_disk.setLayout(vbox5)
        self.tab_temp.setLayout(vbox6)
        self.tab_power.setLayout(vbox7)

    def get_power(self):
        x = sqlite3.connect("./BackgroundSvc/RawData.db")
        xc = x.cursor()
        xc.execute("SELECT tmp.power from (SELECT (dated || ' ' || timed) as datetimed, power from hostData) as tmp where datetime(tmp.datetimed) < datetime('now','localtime') and datetime(tmp.datetimed) >= datetime('now','-2 hours','localtime') ORDER BY tmp.datetimed DESC LIMIT 60")
        power = xc.fetchall()
        power = [x[0] for x in power]
        print(len(power))

        x.close()
        return power

    def make_graph_tab(self,funcdata=None,lims=None, timerv=1000):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceGraph(funcdata,lims,timerv,self.main_widget)
        vbox = QVBoxLayout()
        vbox.addWidget(sc)
        return vbox

    def make_powergraph_tab(self,funcdata=None,lims=None, timerv=1000):
        self.main_widget = QtWidgets.QWidget(self)
        sc = PowerResourceGraph(funcdata,lims,timerv,self.main_widget)
        vbox = QVBoxLayout()
        vbox.addWidget(sc)
        return vbox

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

        # Create Host Name label
        label_string = "Host name: " + self.virt_connection.getHostname()
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Architecture label
        label_string = "CPU Architecture: " + host_info[0]
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create CPU Name label
        from_stdout = subprocess.check_output('cat /proc/cpuinfo | grep "model name"',shell=True)
        model = from_stdout.decode('utf-8').split('\n')[0].split(':')[1].strip()
        label_string = "CPU Model: " + model
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Memory size label
        label_string = "Memory size: " + str(host_info[1]) + " MB"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create Current Clock speed label
        label_string = "Current CPU Clock: " + str(host_info[3]) + " MHz"
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        # Create CPU Cores label
        label_string = "CPU Cores: " + str(host_info[6])
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
        encrypted = "(Unecrypted)" if self.virt_connection.isEncrypted() else "(Encrypted)"
        label_string = 'Connected over ' + self.virt_connection.getURI() + encrypted
        label = QtWidgets.QLabel(label_string,self)
        label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(label)

        return vbox

    def get_temperature(self):
        res = subprocess.check_output('sensors',shell=True)
        a = res.decode('utf-8')
        diva = a.split('\n')
        cpu1 = diva[2].split(' ')[4][1:5]
        cpu2 = diva[2].split(' ')[4][1:5]
        return (float(cpu1)+float(cpu2))/2

    def get_memory(self):
        free_mem = self.host_info[1] - self.virt_connection.getFreeMemory()//(1024*1024)
        return free_mem

    def get_disk_load(self):
        res = subprocess.check_output('iostat -dx /dev/sda', shell=True)
        disk_utilization = res.decode('utf-8').split('\n')[3].split()
        # 5 - readKB/s ; 6 - writeKB/s
        return (float(disk_utilization[5]),float(disk_utilization[6]))

    def get_mips(self):
        global agg_cpu_usage
        from_stdout = subprocess.check_output('cat /proc/cpuinfo | grep "bogomips"',shell=True)
        maxmips = from_stdout.decode('utf-8').split('\n')[0].split(':')[1].strip()
        return float(maxmips) * agg_cpu_usage * 0.04

    def get_cpu(self):
        global prevstat
        global agg_cpu_usage
        res = subprocess.check_output('cat /proc/stat', shell=True)
        cpustatin = []
        result = []
        for i in range(5):
            cpustatin.append(res.decode('utf-8').split('\n')[i].split())

            cpustat = [int(j) for j in cpustatin[i][1:9]]
            cpustat.insert(0,0)
            prev_idle = prevstat[i][4] + prevstat[i][5]
            idle = cpustat[4] + cpustat[5]

            prev_non_idle = prevstat[i][1] + prevstat[i][2] + prevstat[i][3] + prevstat[i][6] + prevstat[i][7] + prevstat[i][8]
            non_idle = cpustat[1] + cpustat[2] + cpustat[3] + cpustat[6] + cpustat[7] + cpustat[8]

            prev_total = prev_idle + prev_non_idle
            total = idle + non_idle

            totald = total - prev_total
            idled = idle - prev_idle
            prevstat[i][4], prevstat[i][5] = cpustat[4], cpustat[5]
            prevstat[i][1], prevstat[i][2], prevstat[i][3], prevstat[i][6], prevstat[i][7], prevstat[i][8] = cpustat[1], cpustat[2], cpustat[3], cpustat[6], cpustat[7], cpustat[8]

            result.append((totald - idled)/totald*100)
        agg_cpu_usage = result[0]
        return result

prevstat = [[0 for i in range(9)] for i in range(5)]
agg_cpu_usage = 0

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myui = DisplayGraphs()
    myui.show()
    sys.exit(app.exec_())
