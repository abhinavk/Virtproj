#!/usr/bin/python3
import sys
import subprocess
import libvirt
import math
import matplotlib
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


class ResourceGraph(MyMplCanvas):
    """The widget which will be in each tab of each tabwidget"""
    def __init__(self, funcdata, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.x = [i for i in range(60)]
        self.y = [0 for i in range(60)]
        self.func = funcdata

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        # l = [random.randint(0, 10) for i in range(4)]
        self.y.pop(0)
        self.y.append(self.func())
        self.axes.plot(self.x,self.y, 'r')
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

    def draw_graph(self):
        vbox1 = self.make_info_tab() # Info
        vbox2 = self.make_graph_tab() # CPU
        vbox3 = self.make_graph_tab() # MIPS
        vbox4 = self.make_graph_tab(self.virt_connection.getFreeMemory) #Memory
        vbox5 = self.make_graph_tab() # Disk
        vbox6 = self.make_graph_tab(self.get_temperature) # Temperature
        self.tab_info.setLayout(vbox1)
        self.tab_cpu.setLayout(vbox2)
        self.tab_mips.setLayout(vbox3)
        self.tab_mem.setLayout(vbox4)
        self.tab_disk.setLayout(vbox5)
        self.tab_temp.setLayout(vbox6)

    def make_graph_tab(self,funcdata=None):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceGraph(funcdata,self.main_widget)
        vbox = QVBoxLayout()
        vbox.addWidget(sc)
        return vbox

    def make_info_tab(self):
        self.main_widget = QtWidgets.QWidget(self)
        vbox = QVBoxLayout()

        # Get all cpu info
        host_info = self.virt_connection.getInfo()

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myui = DisplayGraphs()
    myui.show()
    sys.exit(app.exec_())
