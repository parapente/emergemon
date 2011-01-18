# -*- coding: utf-8

from PyQt4 import QtGui
from ui_emergemon import Ui_Dialog

class emMainWidget(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(emMainWidget, self).__init__()
        self.setupUi(self)
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()

    def createActions(self):
        self.quitAction = QtGui.QAction(QtGui.QIcon(':/emon/images/application-exit.png'), '&Quit', self, triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon(':/emon/images/gentoo-logo.svg'))
        self.trayIcon.setContextMenu(self.trayIconMenu)
