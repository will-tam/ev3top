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
import cBrickPorts as cBP
import cBrickMotors as cBM
import cBrickSensors as cBS

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
    try:    # Instantiate brick ports object.
        bp = cBP.cBrickPorts()
    except Exception as e:
        print("Exception occured on bp init instance:", e)
        return 1

    try:    # Instantiate brick motors object.
        bm = cBM.cBrickMotors(bp)
        bm.debug = True
    except Exception as e:
        print("Exception occured on bm init instance:", e)
        return 1

    try:    # Instantiate brick sensors object.
        bs = cBS.cBrickSensors(bp)
        bs.debug = True
    except Exception as e:
        print("Exception occured on bs init instance:", e)
        return 1

    while True:
        print("q to quit")
        k = getCh()
        if k == 'q':
            break

        bp.scan()       # Scan ports to detect which device is plugged.

#        TODO : À DÉGAGER APRÈS OPTIMISATION DE cBrickMotors.scan()
#        print(bp.ports)
#        return 0

        bm.update()     # Update the motors ports (bm.motors).
        bs.update()     # Update the sensors ports (bs.sensors).

        print("Motors infos :")
        for port in bm.portsMotors:
            motor = bm.motors[port]
            if motor:
                motorInfo = bm.getMotorsInfos(motor)
                print(motorInfo)

        print("")

        print("Sensors infos:")
        for port in bs.portsSensors:
            sensor = bs.sensors[port]
            if sensor:
                sensorInfo = bs.getSensorsInfos(sensor)
                print(sensorInfo)

        print("")

#        bs.irSensorMode = "IR-SEEK"  # TODO : Comment changer le mode. Il faut passer par le port !?
#        bs.colorSensorMode = "RGB-RAW"

        time.sleep(0.5)

    return 0

######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(rc)
