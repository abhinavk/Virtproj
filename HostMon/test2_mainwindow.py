#!/usr/bin/python3
import sys
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
        super(DisplayGraphs, self).__init__()                                   # To call init function in QtWidgets.QMainWindow WITHOUT using a object
        self.setupUi(self)                                                      # To call setupUi function in Ui_MainWindow WITHOUT using a object
        self.qemu_connect()
        self.draw_graph()
        self.tabWidget.setCurrentIndex(0)

    def qemu_connect(self):
        self.virt_connection = libvirt.open("qemu:///system")                        # Connect Qemu
        all_domains = self.virt_connection.listAllDomains(0)                         # Get all domains
        if self.virt_connection is None:
            print("No Qemu instance running.", file=sys.stderr)
            exit(1)
    
    def draw_graph(self):
        vbox1 = self.make_tab()
        vbox2 = self.make_tab()
        self.tab_info.setLayout(vbox1)
        self.tab_cpu.setLayout(vbox2)
        vbox3 = self.make_tab()
        vbox4 = self.make_tab()
        self.tab_mips.setLayout(vbox3)
        self.tab_mem.setLayout(vbox4)
        vbox5 = self.make_tab()
        vbox6 = self.make_tab()
        self.tab_disk.setLayout(vbox5)
        self.tab_temp.setLayout(vbox6)

    def make_tab(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceGraph(self.virt_connection.getFreeMemory,self.main_widget)
        vbox = QVBoxLayout()
        vbox.addWidget(sc)
        return vbox


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myui = DisplayGraphs()
    myui.show()
    sys.exit(app.exec_())
