#!/usr/bin/python
# -*- coding: utf-8

__author__="Theofilos Intzoglou"
__date__ ="$18 Ιαν 2011 5:24:40 μμ$"

import sys
import signal
from lib.emmainwin import emMainWidget
from PyQt4 import QtGui

signal.signal(signal.SIGINT, signal.SIG_DFL) # Break on control-c

if __name__ == "__main__":
    print "EmergeMon Starting... Check your systray!"
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    widget = emMainWidget()
    #widget.show()

    sys.exit(app.exec_())