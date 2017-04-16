#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Standard library import.
import os
import sys
import termios
import fcntl

import time

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.
import cBrickSensors as cBS
import cBrickMotors as cBM

######################

def getCh():
    """
    Wait for a pressed key.
    http://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
    with some changing :
        Don't block while waitng a key.
        Don't lost CTRL-C.
    """
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    # lflag
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

    # turn on non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        ch = sys.stdin.read(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Prevent the old term setting lost.
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return ch

######################

def main(arg):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    bm = cBM.cBrickMotors()
    bs = cBS.cBrickSensors()

    while True:
        print("q to quit")
        k = getCh()
        if k == 'q':
            break

        motors = [m for m in ev3core.list_motors()]
#        motors = ev3core.list_motors()
        print("Motors :")
        print(motors)
#        for m in motors:
#            print("\tPort : {} - driver name : {}".format(m.address, m.driver_name))
#        bs.colorSensorMode = "RGB-RAW"
        bs.update()
        for s in bs.sensors:
            try:
                print(bs.getSensorsInfosFunc[s.driver_name]())
            except:
                pass

        time.sleep(0.5)
        print("-------")

    return 0

######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(rc)
