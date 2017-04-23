# Standard library import.

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.


class cBrickSensors():
    """
    Class for sensors manipulations.

    Public attributes:

        portsSensors = the ports assigned to the sensors.
        sensors = discovered sensors list.
        debug = true to print exceptions, everelse false (default).

    Properties:

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
#        self.getSensorsInfosFunc = {"lego-ev3-touch": self.__getTouchInfos,
#                                    "lego-ev3-ir": self.__getIrInfos,
#                                    "lego-ev3-color": self.__getColorInfos,
#                                   }
#
#        self.__touchSensor = ev3core.TouchSensor()
#        self.__irSensor = ev3core.InfraredSensor()
#        self.__colorSensor = ev3core.ColorSensor()
#
#        self.sensors = []
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
        self.sensors = {p : self.__bs.ports[p] for p in self.portsSensors}

    def getSensorsInfos(self, sensor):
        """
        Return informations about the sensor according to its type.
        @parameter : sensor = the sensor's object which to know informations.
        @return : the dictionnary of values about sensor, or False if something wrong.
        """
        getSensorsInfosFunc = {"lego-ev3-touch": self.__getTouchInfos,
                               "lego-ev3-ir": self.__getIrInfos,
                               "lego-ev3-color": self.__getColorInfos,
                              }

        return getSensorsInfosFunc[sensor.driver_name](sensor)


    # Private methods.

    def __getTouchInfos(self, sensor):
        """
        Return the values of this sensor.
        @parameter : sensor = the sensor's object which to know informations.
        @return : Dictionnary of values from this sensor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = sensor.driver_name
            ret["address"] = sensor.address
            ret["value0"] = ssensor.value(0)
            ret["pressed"] = True if sensor.is_pressed else False
        except Exception as e:
            pass
            if self.debug:
                print("getSensorsInfos() : can't read Touch sensor device => {}.\nMaybe unplugged".format(e))
            ret = False

        return ret

    def __getIrInfos(self, sensor):
        """
        Return the values of this sensor.
        @@parameter : sensor = the sensor's object which to know informations.
        @return : Dictionnary of values from this sensor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = sensor.driver_name
            ret["address"] = sensor.address
            ret["modes"] = sensor.modes
            ret["mode"] = sensor.mode
            if ret["mode"] in ["IR-PROX", "IR-REM-A"]:
                vals = sensor.value(0)
            elif ret["mode"] in ["IR-REMOTE", "IR-S-ALT"]:
                vals = [sensor.value(i) for i in range(0, 4)]
            elif ret["mode"] == "IR-SEEK":
                vals = [sensor.value(i) for i in range(0, 8)]
            elif ret["mode"] == "IR-CAL":
                vals = [sensor.value(i) for i in range(0, 2)]
            else:
                vals = None
            ret["values"] = vals
            ret["proximity"] = sensor.proximity

        except Exception as e:
            pass
            if self.debug:
                print("getSensorsInfos() : can't read IR sensor device => {}.\nMaybe unplugged".format(e))
            ret = False

        return ret

    def __setIrSensorMode(self, mode):
        """
        Setter of the mode to the IR sensor.
        @parameter : mode.
        @return : None.
        """
        try:
            self.__irSensor.mode = mode

        except Exception as e:
            if self.debug:
                print("Can't change IR sensor mode cause :", e)
            else:
                pass

    def __getColorInfos(self, sensor):
        """
        Return the values of this sensor.
        @parameter : sensor = the sensor's object which to know informations.
        @return : Dictionnary of values from this sensor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = sensor.driver_name
            ret["address"] = sensor.address
            ret["modes"] = sensor.modes
            ret["mode"] = sensor.mode
            if ret["mode"] in ["COL-REFLECT", "COL-AMBIENT", "COL-COLOR"]:
                vals = sensor.value(0)
            elif ret["mode"] == "REF-RAW":
                vals = [sensor.value(i) for i in range(0, 2)]
            elif ret["mode"] == "RGB-RAW":
                vals = [sensor.value(i) for i in range(0, 3)]
            elif ret["mode"] == "COL-CAL":
                vals = [sensor.value(i) for i in range(0, 4)]
            else:
                vals = None
            ret["values"] = vals
            ret["ambient_light_intensity"] = sensor.ambient_light_intensity
            ret["raw"] = sensor.raw
            ret["color"] = sensor.color
            ret["red"] = sensor.red
            ret["green"] = sensor.green
            ret["blue"] = sensor.blue
            ret["reflected_light_intensity"] = sensor.reflected_light_intensity

        except Exception as e:
            pass
            if self.debug:
                print("getSensorsInfos() : can't read Color sensor device => {}.\nMaybe unplugged".format(e))
            ret = False

        return ret

    def __setColorSensorMode(self, mode):
        """
        Setter of the mode to the Color sensor.
        @parameter : mode.
        @return : None.
        """
        try:
            self.__colorSensor.mode = mode

        except Exception as e:
            if self.debug:
                print("Can't change color sensor mode cause :", e)
            else:
                pass


    # Properties
    # Only setters.
    colorSensorMode = property(None, __setColorSensorMode)
    irSensorMode = property(None, __setIrSensorMode)


if __name__ == "__main__":
    help(cBrickSensors)
