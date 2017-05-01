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
import CBrickPorts as CBP
import CBrickMotors as CBM
import CBrickSensors as CBS

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
        bp = CBP.CBrickPorts()
    except Exception as e:
        print("Exception occured on bp init instance:", e)
        return 1

    try:    # Instantiate brick motors object.
        bm = CBM.CBrickMotors(bp)
        bm.debug = True
    except Exception as e:
        print("Exception occured on bm init instance:", e)
        return 1

    try:    # Instantiate brick sensors object.
        bs = CBS.CBrickSensors(bp)
        bs.debug = True
    except Exception as e:
        print("Exception occured on bs init instance:", e)
        return 1

    bp.start()

    while True:
        print("q to quit")
        k = getCh()
        if k == 'q':
            bp.quit = True
            for port in bm.portsMotors:
                bm.motorCommand = [port, "reset"]
            break

        t0 = time.time()

        bm.update()     # Update the motors ports (bm.motors).
        bs.update()     # Update the sensors ports (bs.sensors).

        print("Motors infos :")
        for port in bm.portsMotors:
            motor = bm.motors[port]
            if motor:
                motorInfo = bm.getMotorsInfos(motor)
                print(motorInfo)

#        bm.motorSpeed = ["outB", 50]
#        bm.motorPosition = ["outB", "50"]
#        bm.motorCommand = ["outB", "run-to-rel-pos"]

        print("")

        print("Sensors infos:")
        for port in bs.portsSensors:
            sensor = bs.sensors[port]
            if sensor:
                sensorInfo = bs.getSensorsInfos(sensor)
                print(sensorInfo)

        print("")

#        bs.irSensorMode = ["in2", "IR-SEEK"]
#        bs.colorSensorMode = ["in4", "COL-AMBIENT"]

        t1 = time.time()
        print("Temps total :", t1 - t0)

        time.sleep(0.5)

    bp.join()

    return 0

def mainAlternative(arg):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    while True:
        print("q to quit")
        k = getCh()
        if k == 'q':
            break

        legoPort = ev3core.LegoPort(address='in3')

        print("{} - {} => {}".format(str(legoPort), repr(legoPort), dir(legoPort)))

        print("legoPort.address=>", legoPort.address)
        print("legoPort.driver_name=>", legoPort.driver_name)
        print("legoPort.mode=>", legoPort.mode)
        print("legoPort.modes=>", legoPort.modes)
        print("legoPort.status =>", legoPort.status)

        time.sleep(0.5)

    return 0


######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
#    rc = mainAlternative(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(rc)
