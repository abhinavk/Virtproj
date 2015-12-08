#!/usr/bin/python3
import sys
import libvirt
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
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class DisplayGraphs(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DisplayGraphs, self).__init__()
        self.setupUi(self)
        self.qemu_connect()
        self.draw_graph()

    def qemu_connect(self):
        virt_connection = libvirt.open("qemu:///system")
        all_domains = virt_connection.listAllDomains(0)
        if virt_connection is None:
            print("No Qemu instance running.", file=sys.stderr)
            exit(1)
    
    def draw_graph(self):
        vbox1 = self.make_tab()
        vbox2 = self.make_tab()
        self.tab.setLayout(vbox1)
        self.tab_2.setLayout(vbox2)
        vbox3 = self.make_tab()
        vbox4 = self.make_tab()
        self.tab_3.setLayout(vbox3)
        self.tab_4.setLayout(vbox4)
        vbox5 = self.make_tab()
        vbox6 = self.make_tab()
        self.tab_5.setLayout(vbox5)
        self.tab_6.setLayout(vbox6)
        vbox7 = self.make_tab()
        vbox8 = self.make_tab()
        self.tab_7.setLayout(vbox7)
        self.tab_8.setLayout(vbox8)
        vbox9 = self.make_tab()
        vbox10 = self.make_tab()
        self.tab_9.setLayout(vbox9)
        self.tab_10.setLayout(vbox10)

    def make_tab(self):
        self.main_widget = QtWidgets.QWidget(self)
        sc = ResourceGraph(None,self.main_widget)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(sc)
        return vbox1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myui = DisplayGraphs()
    myui.show()
    sys.exit(app.exec_())
