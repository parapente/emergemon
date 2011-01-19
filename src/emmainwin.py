# -*- coding: utf-8

from PyQt4 import (QtGui, QtCore)
from ui_emergemon import Ui_Dialog
import dbus.mainloop.qt
import dbus

class emMainWidget(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(emMainWidget, self).__init__(parent)
        self.setupUi(self)
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()
        self.fp = QtCore.QFile('/var/log/pemerge.log')
        dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        self.busproxy = self.bus.get_object('org.freedesktop.Notifications',
                                           '/org/freedesktop/Notifications')
        self.buspiface = dbus.Interface(self.busproxy, 'org.freedesktop.Notifications')
        if ((not self.fp.exists()) or (not self.fp.open(QtCore.QIODevice.ReadOnly))):
            self.buspiface.Notify('emergeMon',0,'','emergeMon: File not found error!',
                                 "The file emerge.log doesn't exist in /var/log or you don't have access to it! The app will not be able to show the status of the emerge command.",
                                 '','',-1)
        else:
            self.fwatch = QtCore.QFileSystemWatcher(self)
            self.fwatch.addPath('/var/log/emerge.log')

    def createActions(self):
        self.quitAction = QtGui.QAction(QtGui.QIcon(':/emon/images/application-exit.png'), '&Quit', self, triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon(':/emon/images/gentoo-logo.svg'))
        self.trayIcon.setContextMenu(self.trayIconMenu)
