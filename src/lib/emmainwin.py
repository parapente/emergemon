# -*- coding: utf-8

from PyQt4 import (QtGui, QtCore)
from emreadthread import readThread
import dbus.mainloop.qt
import dbus
from ui.ui_emergemon import Ui_MainWindow

class emMainWidget(QtGui.QMainWindow, Ui_MainWindow):
    logfname = '/home/oscar/emerge.log'

    def __init__(self, parent=None):
        super(emMainWidget, self).__init__(parent)
        
        self.setupUi(self)
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()
        self.fp = QtCore.QFile(self.logfname)

        # Initialize dbus interface for Notifications
        dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        self.busproxy = self.bus.get_object('org.freedesktop.Notifications',
                                           '/org/freedesktop/Notifications')
        self.buspiface = dbus.Interface(self.busproxy, 'org.freedesktop.Notifications')

        if ((not self.fp.exists()) or (not self.fp.open(QtCore.QIODevice.ReadOnly))):
            self.buspiface.Notify('emergeMon',0,'','emergeMon: File not found error!',
                                 "The file " + self.logfname + " doesn't exist or you don't have access to it! The app will not be able to show the status of the emerge command.",
                                 '','',-1)
        else:
            self.fwatch = QtCore.QFileSystemWatcher(self)
            self.fwatch.addPath(self.logfname)
            self.thread = readThread()
            self.thread.setLogFile(self.fp)
            self.thread.start()

            # Make appropriate connections
            self.thread.signalStatus.connect(self.slotSetStatus)
            self.thread.signalTotalPackages.connect(self.slotTotalPackages)
            self.thread.signalIncPerc.connect(self.slotIncPerc)
            self.thread.signalResetPerc.connect(self.slotResetPerc)
            self.fwatch.fileChanged.connect(self.thread.slotRead)
            self.trayIcon.activated.connect(self.slotTrayIconActivated)
            self.action_Quit.triggered.connect(self.quitAction.trigger)

        self.curPerc = 0
        self.totalPackages = 0
        self.lastPerc = 0
        self.visible = False

    def createActions(self):
        self.quitAction = QtGui.QAction(QtGui.QIcon(':/emon/images/application-exit.png'), '&Quit', self, triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        self.idleIcon = QtGui.QIcon(':/emon/images/gentoo-logo.svg')

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.idleIcon)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def slotIncPerc(self,num):
        self.curPerc += num / self.totalPackages * 100
        if ((self.curPerc - self.lastPerc) >= 1) or (self.lastPerc == 0): # Update systray icon
            self.pixmap = self.idleIcon.pixmap(256)
            p = QtGui.QPainter(self.pixmap)
            #p.fillRect(QtCore.QRect(0,78,256,100),QtCore.Qt.gray)
            f = QtGui.QFont()
            f.setPointSize(64)
            f.setBold(True)
            p.setFont(f)
            p.drawText(self.pixmap.rect(),QtCore.Qt.AlignCenter,QtCore.QString.number(round(self.curPerc))+'%')
            self.trayIcon.setIcon(QtGui.QIcon(self.pixmap))
            self.lastPerc = self.curPerc
        print 'Perc:',self.curPerc

    def slotTotalPackages(self,num):
        if num != self.totalPackages: # A package failed to build and we have --keep-going
            self.curPerc = 0
            self.lastPerc = 0
            self.totalPackages = num
        print 'TotalPackages:',num

    def slotResetPerc(self):
        self.curPerc = 0
        self.lastPerc = 0
        self.trayIcon.setIcon(self.idleIcon)

    def slotSetStatus(self,line):
        self.trayIcon.setToolTip(line)

    def slotTrayIconActivated(self,reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.visible == False:
                self.show()
                self.visible = True
            else:
                self.hide()
                self.visible = False
