import sys
import os
import libvirt
import matplotlib
import numpy
from PyQt5 import QtWidgets, QtCore
from ui_mainwindow import Ui_MainWindow
import matplotlib.pyplot as plot
import matplotlib.animation as animation

virt_connection = libvirt.open("qemu:///system")  # Connect Qemu
all_domains = virt_connection.listAllDomains(0)  # Get all domains

if virt_connection is None:
    print("No Qemu instance running.", file=sys.stderr)
    exit(1)


class DisplayGraphs(Ui_MainWindow):
    """UI Class"""

    def __init__(self):
        ui = Ui_MainWindow()
        ui.setupUi(window)
        window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    sys.exit(app.exec_())
