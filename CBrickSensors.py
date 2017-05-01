# Standard library import.

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.


class CBrickSensors():
    """
    Class for sensors manipulations.

    Public attributes:

        portsSensors = the ports assigned to the sensors.
        sensors = discovered sensors list.
        debug = true to print exceptions, everelse false (default).

    Properties: (see http://python-ev3dev.readthedocs.io/en/latest/sensors.html)

        colorSensorMode = mode for the color sensor. (setter only)
        irSensorMode = mode for the ir sensor. (setter only)
    """

    # Private attributes.
    # __bs = instance of the brick's ports object (from class cBrickPorts). Defined in construtor.
    #__touchSensor ; __irSensor ; __colorSensor = instance of the sensors.


    # Public methods.

    def __init__(self, bs):
        """
        Constructor.
        @parameter : bs = instance of the brick's ports object (from class cBrickPorts).
        @return : none.
        """
        self.__bs = bs

        self.portsSensors = ["in1", "in2", "in3", "in4", ]
        self.update()

        self.debug = False

    def __str__(self):
        """
        When use print() on this class
        @parameters : none.
        @return : the string to print.
        """
        ret = "Sensors :\n"
        for port in self.portsSensors:
            sensor = self.sensors[port]
            if sensor:
                ret += "\t{} => {} - Port : {} - driver name : {}\n".format(str(sensor),\
                                                                            repr(sensor),\
                                                                            sensor.address,\
                                                                            sensor.driver_name)
            else:
                ret += "\t{} => None\n".format(port)

        return ret

    def update(self):
        """
        Discover and update the sensors plugged on the brick.
        @parameter : none.
        @return : none.
        """
        self.sensors = {p:self.__bs.ports[p] for p in self.portsSensors}

    def getSensorsInfos(self, sensor):
        """
        Return informations about the sensor according to its type.
        @parameter : sensor = the sensor's object which to know informations.
        @return : the dictionnary of values about sensor, or None if something wrong.
        """
        getSensorsInfosFunc = {"lego-ev3-touch": self.__getTouchInfos,
                               "lego-ev3-ir": self.__getIrInfos,
                               "lego-ev3-color": self.__getColorInfos,
                              }
        # As it, because the "Touch sensor" reaction seems different than the others devices.
        try:
            gsif = getSensorsInfosFunc[sensor[1]](sensor[0])
        except Exception as e:
            if self.debug:
                print("getSensorsInfos() : can't read sensor device => {}.\nMaybe removed while reading.".format(e))
            gsif = None

        return gsif


    # Private methods.

    def __getTouchInfos(self, sensor):
        """
        Return the values of this sensor.
        @parameter : sensor = the sensor's object which to know informations.
        @return : Dictionnary of values from this sensor. If problem occurs, return {}.
        """
        ret = {}
        touchSensor = ev3core.TouchSensor(sensor.address)

        # see library documentation for what to use, and why the try/except using.
        ret["name"] = touchSensor.driver_name
        ret["address"] = touchSensor.address
        ret["value0"] = touchSensor.value(0)
        ret["pressed"] = True if touchSensor.is_pressed else False
        del(touchSensor)

        return ret

    def __getIrInfos(self, sensor):
        """
        Return the values of this sensor.
        @@parameter : sensor = the sensor's object which to know informations.
        @return : Dictionnary of values from this sensor. If problem occurs, return {}.
        """
        ret = {}
        irSensor = ev3core.InfraredSensor(sensor.address)

        # see library documentation for what to use, and why the try/except using.
        ret["name"] = irSensor.driver_name
        ret["address"] = irSensor.address
        ret["modes"] = irSensor.modes
        ret["mode"] = irSensor.mode
        if ret["mode"] in ["IR-PROX", "IR-REM-A"]:
            vals = irSensor.value(0)
        elif ret["mode"] in ["IR-REMOTE", "IR-S-ALT"]:
            vals = [irSensor.value(i) for i in range(0, 4)]
        elif ret["mode"] == "IR-SEEK":
            vals = [irSensor.value(i) for i in range(0, 8)]
        elif ret["mode"] == "IR-CAL":
            vals = [irSensor.value(i) for i in range(0, 2)]
        else:
            vals = None
        ret["values"] = vals
        ret["proximity"] = irSensor.proximity
        del(irSensor)

        return ret

    def __setIrSensorMode(self, portMode):
        """
        Setter of the mode to the IR sensor.
        @parameter : portMode = list with [port, mode].
        @return : None.
        """
        if type(portMode) is list:
            try:
                irSensor = ev3core.InfraredSensor(portMode[0])
                irSensor.mode = portMode[1]

            except Exception as e:
                if self.debug:
                    print("Can't change IR sensor mode cause :", e)
                else:
                    pass

    def __getColorInfos(self, sensor):
        """
        Return the values of this sensor.
        @parameter : sensor = the sensor's object which to know informations.
        @return : Dictionnary of values from this sensor. If problem occurs, return {}.
        """
        ret = {}
        colorSensor = ev3core.ColorSensor(sensor.address)

        # see library documentation for what to use, and why the try/except using.
        ret["name"] = colorSensor.driver_name
        ret["address"] = colorSensor.address
        ret["modes"] = colorSensor.modes
        ret["mode"] = colorSensor.mode
        if ret["mode"] in ["COL-REFLECT", "COL-AMBIENT", "COL-COLOR"]:
            vals = colorSensor.value(0)
        elif ret["mode"] == "REF-RAW":
            vals = [colorSensor.value(i) for i in range(0, 2)]
        elif ret["mode"] == "RGB-RAW":
            vals = [colorSensor.value(i) for i in range(0, 3)]
        elif ret["mode"] == "COL-CAL":
            vals = [colorSensor.value(i) for i in range(0, 4)]
        else:
            vals = None
        ret["values"] = vals
        ret["ambient_light_intensity"] = colorSensor.ambient_light_intensity
        ret["raw"] = colorSensor.raw
        ret["color"] = colorSensor.color
        ret["red"] = colorSensor.red
        ret["green"] = colorSensor.green
        ret["blue"] = colorSensor.blue
        ret["reflected_light_intensity"] = colorSensor.reflected_light_intensity
        del(colorSensor)

        return ret

    def __setColorSensorMode(self, portMode):
        """
        Setter of the mode to the Color sensor.
        @parameter : portMode = list with [port, mode].
        @return : None.
        """
        if type(portMode) is list:
            try:
                colorSensor = ev3core.ColorSensor(portMode[0])
                colorSensor.mode = portMode[1]

            except Exception as e:
                if self.debug:
                    print("Can't change color sensor mode cause :", e)
                else:
                    pass


    # Properties
    # Only setters.
    irSensorMode = property(None, __setIrSensorMode)
    colorSensorMode = property(None, __setColorSensorMode)


if __name__ == "__main__":
    help(CBrickSensors)
