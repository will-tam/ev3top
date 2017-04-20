# Standard library import.

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.


class cBrickMotors():
    """
    Class for sensors manipulations.

    # Public attributes.
        motors = discovered motors list.
        getMotorsInfos = an associate motors / function dictionnary, to get informations about motors.
        debug = true to print exceptions, everelse false (default).

    # Properties
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
        self.getMotorsInfos = {"lego-ev3-m-motor": self.__getMotorsInfos,
                               "lego-ev3-l-motor": self.__getMotorsInfos,
                              }

        self.__motor = ev3core.Motor()

        self.motors = []

        self.debug = False

    def __str__(self):
        """
        When use print() on this class
        @parameters : none.
        @return : the stringto print.
        """
        ret = "Motors :\n"
        for m in self.motors:
            ret += "\t{} => {} - Port : {} - driver name : {}\n".format(str(m),\
                                                                        repr(m),\
                                                                        m.address,\
                                                                        m.driver_name)
        return ret

    def update(self):
        """
        Discover and update the motors plugged on the brick.
        @parameter : none.
        @return : none.
        """
        self.motors = [m for m in ev3core.list_motors()]


    # Private methods.

    def __getMotorsInfos(self):
        """
        Return the values of this kind of motor.
        @parameter : none.
        @return : Dictionnary of values from this kind of motor. If problem occurs, return False.
        """
        ret = {}
        try:
            ret["name"] = self.__motor.driver_name
            ret["address"] = self.__motor.address
            ret["commands"] = self.__motor.commands
#            ret["count_per_m"] = self.__motor.count_per_m
            ret["count_per_rot"] = self.__motor.count_per_rot
            ret["duty_cycle"] = self.__motor.duty_cycle
            ret["duty_cycle_sp"] = self.__motor.duty_cycle_sp
#            ret["full_travel_count"]  =self.__motor.full_travel_count
            ret["max_speed"] = self.__motor.max_speed
            ret["polarity"] = self.__motor.polarity
            ret["position"] = self.__motor.position

        except Exception as e:
            self.__irSensor = ev3core.InfraredSensor()
            if self.debug:
                print("__getLarMotor() : can't read medium motor device => {}. New object instanced".format(e))
            ret = False

        return ret


if __name__ == "__main__":
    help(cBrickMotors)

