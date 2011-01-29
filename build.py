#!/usr/bin/env python

import os

commands = ("pyuic4 -o src/ui/ui_emergemon.py src/ui/emergemon.ui",
            "pyrcc4 -o src/ui/emergemon_rc.py src/ui/emergemon.qrc")

for command in commands:
    print command
    ret = os.system(command)
    if ret != 0:
    	print >>sys.stderr, 'Build failed!'
	exit(-2)
