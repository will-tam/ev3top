# Standard library import.

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.


class cBrickMotors():
    """
    Class for motors manipulations.

    Public attributes:

        portsMotors = the ports assigned to the motors.
        motors = discovered plugged motors list.
        getMotorsInfos = an associate motors / function dictionnary, to get informations about motors.
        debug = true to print exceptions, everelse false (default).
    """

    # Private attributes.
    # __bp = instance of the brick's ports object (from class cBrickPorts). Defined in construtor.


    # Public methods.

    def __init__(self, bp):
        """
        Constructor.
        @parameter : bp = instance of the brick's ports object (from class cBrickPorts).
        @return : none.
        """
        self.__bp = bp

        self.getMotorsInfos = {"lego-ev3-m-motor": self.__getMotorsInfos,
                               "lego-ev3-l-motor": self.__getMotorsInfos,
                              }

        self.portsMotors = ["outA", "outB", "outC", "outD", ]

        self.update()

        self.debug = False

    def __str__(self):
        """
        When use print() on this class
        @parameters : none.
        @return : the string to print.
        """
        ret = "Motors :\n"
        motorsPorts = [p for p in self.motors.keys()]
        motorsPorts.sort()
        for port in motorsPorts:
            motor = self.motors[port]
            if motor:
                ret += "\t{} => {} - Port : {} - driver name : {}\n".format(str(motor),\
                                                                            repr(motor),\
                                                                            motor.address,\
                                                                            motor.driver_name)
            else:
                ret += "\t{} => None\n".format(port)

        return ret

    def update(self):
        """
        Discover and update the motors plugged on the brick.
        @parameter : none.
        @return : none.
        """
        self.motors = {p : self.__bp.ports[p] for p in self.portsMotors}


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
            self.__motor = ev3core.Motor()
            if self.debug:
                print("__getMotorsInfos() : can't read motor device => {}. New object instanced".format(e))
            ret = False

        return ret


if __name__ == "__main__":
    help(cBrickMotors)

