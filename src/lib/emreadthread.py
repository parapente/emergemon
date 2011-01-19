# -*- coding: utf-8

from PyQt4 import QtCore

class readThread(QtCore.QThread):
    # Define new signals
    signalStatus = QtCore.pyqtSignal(QtCore.QString)
    signalTotalPackages = QtCore.pyqtSignal(int)
    signalIncPerc = QtCore.pyqtSignal(float)
    signalResetPerc = QtCore.pyqtSignal()

    def setLogFile(self,fp):
        self.fp = fp

    def run(self):
        self.fp.seek(self.fp.size())
        self.textStream = QtCore.QTextStream(self.fp)
        self.exec_()

    def slotRead(self):
        ok = True
        while(ok):
            line = self.textStream.readLine()
            if (line.isNull()):
                ok = False
            else:
                self.parseLine(line)

    def parseLine(self,line):
        self.signalStatus.emit(line)
        pos = line.indexOf('>>>')
        if (pos != -1): # Get total number of packages
            pos = line.indexOf('of')
            if (pos != -1):
                tmp = line
                tmp.remove(0,pos+3)
                pos = tmp.indexOf(')')
                tmp.truncate(pos)
                self.signalTotalPackages.emit(tmp.toInt()[0])
        pos = line.indexOf('===')
        if (pos != -1):
            if line.contains('Merging'): # We are about in the middle
                self.signalIncPerc.emit(0.5)
            if line.contains('Post-Build'):
                self.signalIncPerc.emit(0.4)
        pos = line.indexOf(':::')
        if (pos != -1): # Another package is completed
            self.signalIncPerc.emit(0.1)
        pos = line.indexOf('***')
        if (pos != -1):
            self.signalResetPerc.emit()
