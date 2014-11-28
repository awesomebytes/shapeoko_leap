#!/usr/bin/env python 

from lib.grblstuff import setup_logging, hello_grbl, do_command
from lib.getch import getch

print "connecting"
grbl = hello_grbl("/dev/ttyACM0", None)
print "connected"

print "Setting absolute mode"
do_command(grbl, "G90")
print "Done."

command = "G00 X-10.0 Y-10.0"
print "sending " + command
#do_command(grbl, "G91") # incremental step mode
do_command(grbl, command)
command2 = "G00 X10.0 Y10.0"
do_command(grbl, command2)
grbl.close()
print "Done."