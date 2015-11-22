# Operating System Requisites
import sys
import os

# For connection to Qemu
import libvirt

# To use matlab function in python
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plot
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Extension to the Python, adding support for large, multi-dimensional arrays and matrices, also operations on these arrays and matrices. 
from numpy import arange, random

# For GUI
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

class cpu_usage(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class cpu_utilisation(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class memory_usage(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class memory_utilisation(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class storage_usage(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class storage_utilisation(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class network_usage(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class network_utilisation(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class power_usage(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class power_utilisation(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class DisplayGraphs(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DisplayGraphs, self).__init__()                                   # To call init function in QtWidgets.QMainWindow WITHOUT using a object
        self.setupUi(self)                                                      # To call setupUi function in Ui_MainWindow WITHOUT using a object
        self.qemu_connect()
        self.draw_graph()

    def qemu_connect(self):
        virt_connection = libvirt.open("qemu:///system")                        # Connect Qemu
        all_domains = virt_connection.listAllDomains(0)                         # Get all domains
        if virt_connection is None:
            print("No Qemu instance running.", file=sys.stderr)
            exit(1)
    
    def draw_graph(self):
        vbox1 = self.makeTab1()
        vbox2 = self.makeTab2()
        self.tab.setLayout(vbox1)
        self.tab_2.setLayout(vbox2)
        
        vbox3 = self.makeTab3()
        vbox4 = self.makeTab4()
        self.tab_3.setLayout(vbox3)
        self.tab_4.setLayout(vbox4)
        
        vbox5 = self.makeTab5()
        vbox6 = self.makeTab6()
        self.tab_5.setLayout(vbox5)
        self.tab_6.setLayout(vbox6)

        vbox7 = self.makeTab7()
        vbox8 = self.makeTab8()
        self.tab_7.setLayout(vbox7)
        self.tab_8.setLayout(vbox8)

        vbox9 = self.makeTab9()
        vbox10 = self.makeTab10()
        self.tab_9.setLayout(vbox9)
        self.tab_10.setLayout(vbox10)

    def makeTab1(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = cpu_usage(self.main_widget)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(sc)
        return vbox1

    def makeTab2(self):
        self.main_widget = QtWidgets.QWidget(self)        
        dc = cpu_utilisation(self.main_widget)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(dc)
        return vbox2
            
    def makeTab3(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = memory_usage(self.main_widget)
        vbox3 = QVBoxLayout()
        vbox3.addWidget(sc)
        return vbox3

    def makeTab4(self):
        self.main_widget = QtWidgets.QWidget(self)        
        dc = memory_utilisation(self.main_widget)
        vbox4 = QVBoxLayout()
        vbox4.addWidget(dc)
        return vbox4
    
    def makeTab5(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = storage_usage(self.main_widget)
        vbox5 = QVBoxLayout()
        vbox5.addWidget(sc)
        return vbox5

    def makeTab6(self):
        self.main_widget = QtWidgets.QWidget(self)        
        dc = storage_utilisation(self.main_widget)
        vbox6 = QVBoxLayout()
        vbox6.addWidget(dc)
        return vbox6

    def makeTab7(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = network_usage(self.main_widget)
        vbox7 = QVBoxLayout()
        vbox7.addWidget(sc)
        return vbox7

    def makeTab8(self):
        self.main_widget = QtWidgets.QWidget(self)        
        dc = network_utilisation(self.main_widget)
        vbox8 = QVBoxLayout()
        vbox8.addWidget(dc)
        return vbox8

    def makeTab9(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = power_usage(self.main_widget)
        vbox9 = QVBoxLayout()
        vbox9.addWidget(sc)
        return vbox9

    def makeTab10(self):
        self.main_widget = QtWidgets.QWidget(self)        
        dc = power_utilisation(self.main_widget)
        vbox10 = QVBoxLayout()
        vbox10.addWidget(dc)
        return vbox10

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QMainWindow()                                          # All default functions to be called if DisplayGraphs class was not defined are here
    # ui = Ui_MainWindow()
    # ui.setupUi(window)
    # window.show()
    myui = DisplayGraphs()
    myui.show()
    sys.exit(app.exec_())
