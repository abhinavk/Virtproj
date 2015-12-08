# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setObjectName("listView")
        self.horizontalLayout.addWidget(self.listView)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 568, 525))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_info = QtWidgets.QWidget()
        self.tab_info.setObjectName("tab_info")
        self.tabWidget.addTab(self.tab_info, "")
        self.tab_cpu = QtWidgets.QWidget()
        self.tab_cpu.setObjectName("tab_cpu")
        self.tabWidget.addTab(self.tab_cpu, "")
        self.tab_mips = QtWidgets.QWidget()
        self.tab_mips.setObjectName("tab_mips")
        self.tabWidget.addTab(self.tab_mips, "")
        self.tab_mem = QtWidgets.QWidget()
        self.tab_mem.setObjectName("tab_mem")
        self.tabWidget.addTab(self.tab_mem, "")
        self.tab_disk = QtWidgets.QWidget()
        self.tab_disk.setObjectName("tab_disk")
        self.tabWidget.addTab(self.tab_disk, "")
        self.tab_temp = QtWidgets.QWidget()
        self.tab_temp.setObjectName("tab_temp")
        self.tabWidget.addTab(self.tab_temp, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen_GitHub = QtWidgets.QAction(MainWindow)
        self.actionOpen_GitHub.setObjectName("actionOpen_GitHub")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionOpen_GitHub)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Project Virt"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_info), _translate("MainWindow", "Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_cpu), _translate("MainWindow", "CPU"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mips), _translate("MainWindow", "MIPS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mem), _translate("MainWindow", "Memory"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_disk), _translate("MainWindow", "Disk"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_temp), _translate("MainWindow", "Temp"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionOpen_GitHub.setText(_translate("MainWindow", "Open GitHub"))
        self.actionAbout.setText(_translate("MainWindow", "About..."))

