# Standard library import.

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.


class CBrickPorts():
    """
    Class for ports interface.

    Public attributes:

        ports = dictionnary of tupples of devices plugged in corresponding port, type of device.
    """

    # Private attributes.


    # Public methods.

    def __init__(self):
        """
        Constructor.
        @parameter : none.
        @return : none.
        """
        self.ports = {"in1" : (None, None),
                      "in2" : (None, None),
                      "in3" : (None, None),
                      "in4" : (None, None),
                      "outA" : (None, None),
                      "outB" : (None, None),
                      "outC" : (None, None),
                      "outD" : (None, None),
                     }

    def __str__(self):
        """
        When use print() on this class
        @parameters : none.
        @return : the string to print.
        """
        ret = "Ports :\n"
        ports = [p for p in self.ports.keys()]
        ports.sort()
        for port in ports:
            if self.ports[port] :
                ret += "\t{} => {} - Port : {} - driver name : {}\n".format(port,\
                                                                            repr(self.ports[port]),\
                                                                            self.ports[port].address,\
                                                                            self.ports[port].driver_name)
            else:
                ret += "\t{} => None\n".format(port)
        return ret

    def scan(self):
        """
        Scan for the divices plugged in the brick.
        Discovered devices are registered in self.ports public attribute.
        Have to be called before using any others cBrickMotors || cBrickSensors methodes.
        @parameter : none.
        @return : none.
        """
        # The other way (reset self.ports, for d in devices: self.ports[d.address] = d) isn't faster.

#        TODO : !!!! VOIR POUR OPTIMISATION PLUS PROFONDE !!!!
        try:
            portsEnabledDevices = {device.address:device for device in [device for device in ev3core.list_motors()] + [device for device in ev3core.list_sensors()]}
            for p in self.ports.keys():
                self.ports[p] = (portsEnabledDevices[p], portsEnabledDevices[p].driver_name)\
                    if p in portsEnabledDevices.keys()\
                    else None

        except:
            pass


if __name__ == "__main__":
    help(CBrickPorts)
