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

    # Public attributes.
        sensors = discovered sensors list.
        getSensorsInfos = an associate sensors / function dictionnary, to get informations about sensors.
        debug = true to print exceptions, everelse false (default).

    # Properties
        colorSensorMode = mode for the color sensor. (setter only)
        irSensorMode = mode for the ir sensor. (setter only)

    """

    # Private attributes.
    #__touchSensor ; __irSensor ; __colorSensor = instance of the sensors.


    # Public methods.

    def __init__(self):
        """
        Constructor.
        @parameter : none.
        @return : none.
        """
        self.getSensorsInfosFunc = {"lego-ev3-touch": self.__getTouchInfos,
                                    "lego-ev3-ir": self.__getIrInfos,
                                    "lego-ev3-color": self.__getColorInfos,
                                   }

        self.__touchSensor = ev3core.TouchSensor()
        self.__irSensor = ev3core.InfraredSensor()
        self.__colorSensor = ev3core.ColorSensor()

        self.sensors = []

        self.debug = False

    def __str__(self):
        """
        When use print() on this class
        @parameters : none.
        @return : the stringto print.
        """
        ret = "Sensors :\n"
        for s in self.sensors:
            ret += "\t{} => {} - Port : {} - driver name : {}\n".format(str(s),\
                                                                        repr(s),\
                                                                        s.address,\
                                                                        s.driver_name)
        return ret

    def update(self):
        """
        Discover and update the sensors plugged on the brick.
        @parameter : none.
        @return : none.
        """
        self.sensors = [s for s in ev3core.list_sensors()]


    # Private methods.

    def __getTouchInfos(self):
        """
        Return the values of this sensor.
        @parameter : none.
        @return : Dictionnary of values from this sensor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = self.__touchSensor.driver_name
            ret["address"] = self.__touchSensor.address
            ret["value0"] = self.__touchSensor.value(0)
            ret["pressed"] = True if self.__touchSensor.is_pressed else False
        except Exception as e:
            self.__touchSensor = ev3core.TouchSensor()
            if self.debug:
                print("__getTouchInfos() : can't read touch sensor device => {}. New object instanced".format(e))
            ret = False

        return ret

    def __getIrInfos(self):
        """
        Return the values of this sensor.
        @parameter : none.
        @return : Dictionnary of values from this sensor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = self.__irSensor.driver_name
            ret["address"] = self.__irSensor.address
            ret["modes"] = self.__irSensor.modes
            ret["mode"] = self.__irSensor.mode
            if ret["mode"] in ["IR-PROX", "IR-REM-A"]:
                vals = self.__irSensor.value(0)
            elif ret["mode"] in ["IR-REMOTE", "IR-S-ALT"]:
                vals = [self.__irSensor.value(i) for i in range(0, 4)]
            elif ret["mode"] == "IR-SEEK":
                vals = [self.__irSensor.value(i) for i in range(0, 8)]
            elif ret["mode"] == "IR-CAL":
                vals = [self.__irSensor.value(i) for i in range(0, 2)]
            else:
                vals = None
            ret["values"] = vals
            ret["proximity"] = self.__irSensor.proximity

        except Exception as e:
            self.__irSensor = ev3core.InfraredSensor()
            if self.debug:
                print("__getIrInfos() : can't read touch sensor device => {}. New object instanced".format(e))
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

    def __getColorInfos(self):
        """
        Return the values of this sensor.
        @parameter : none.
        @return : Dictionnary of values from this sensor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = self.__colorSensor.driver_name
            ret["address"] = self.__colorSensor.address
            ret["modes"] = self.__colorSensor.modes
            ret["mode"] = self.__colorSensor.mode
            if ret["mode"] in ["COL-REFLECT", "COL-AMBIENT", "COL-COLOR"]:
                vals = self.__colorSensor.value(0)
            elif ret["mode"] == "REF-RAW":
                vals = [self.__colorSensor.value(i) for i in range(0, 2)]
            elif ret["mode"] == "RGB-RAW":
                vals = [self.__colorSensor.value(i) for i in range(0, 3)]
            elif ret["mode"] == "COL-CAL":
                vals = [self.__colorSensor.value(i) for i in range(0, 4)]
            else:
                vals = None
            ret["values"] = vals
            ret["ambient_light_intensity"] = self.__colorSensor.ambient_light_intensity
            ret["raw"] = self.__colorSensor.raw
            ret["color"] = self.__colorSensor.color
            ret["red"] = self.__colorSensor.red
            ret["green"] = self.__colorSensor.green
            ret["blue"] = self.__colorSensor.blue
            ret["reflected_light_intensity"] = self.__colorSensor.reflected_light_intensity

        except Exception as e:
            self.__colorSensor = ev3core.ColorSensor()
            if self.debug:
                print("__getColorInfos() : can't read touch sensor device => {}. New object instanced".format(e))
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
