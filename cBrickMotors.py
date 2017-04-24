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
        for port in self.portsMotors:
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
        Don't forget to invoke cBrickPorts.scan() before call it.
        @parameter : none.
        @return : none.
        """
        self.motors = {p:self.__bp.ports[p] for p in self.portsMotors}

    def getMotorsInfos(self, motor):
        """
        Return informations about the motor according to its type.
        @parameter : motor = the motor's object which to know informations.
        @return : the dictionnary of values about motor, or False if something wrong.
        """
        getMotorsInfos = {"lego-ev3-m-motor": self.__getMotorsInfos,
                          "lego-ev3-l-motor": self.__getMotorsInfos,
                         }
        return getMotorsInfos[motor[0].driver_name](motor[0])


    # Private methods.

    def __getMotorsInfos(self, motor):
        """
        Return the values of this kind of motor.
        @parameter : motor = the motor's object which to know informations.
        @return : Dictionnary of values from this kind of motor. If problem occurs, return False.
        """
        ret = {}
        try:
            # see library documentation for what to use, and why the try/except using.
            ret["name"] = motor.driver_name
            ret["address"] = motor.address
            ret["commands"] = motor.commands
            try:
                ret["count_per_m"] = motor.count_per_m
            except:
                pass
            try:
                ret["count_per_rot"] = motor.count_per_rot
            except:
                pass
            ret["duty_cycle"] = motor.duty_cycle
            ret["duty_cycle_sp"] = motor.duty_cycle_sp
            try:
                ret["full_travel_count"] = motor.full_travel_count
            except:
                pass
            ret["max_speed"] = motor.max_speed
            ret["polarity"] = motor.polarity
            ret["position"] = motor.position

        except Exception as e:
            pass
            if self.debug:
                print("getMotorsInfos() : can't read motor device => {}.\nMaybe removed while reading.".format(e))
            ret = False

        return ret


if __name__ == "__main__":
    help(cBrickMotors)

