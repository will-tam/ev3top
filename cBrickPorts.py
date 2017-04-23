# Standard library import.

# Third-part library import.
import ev3dev.ev3 as ev3ev3
import ev3dev.core as ev3core
import ev3dev.brickpi as ev3bp
import ev3dev.helper as ev3h

# Project library import.


class cBrickPorts():
    """
    Class for ports manipulations.

    Public attributes:

        ports = dictionnary of devices plugged in corresponding port.
    """

    # Private attributes.


    # Public methods.

    def __init__(self):
        """
        Constructor.
        @parameter : none.
        @return : none.
        """
        self.ports = {"in1" : None,
                      "in2" : None,
                      "in3" : None,
                      "in4" : None,
                      "outA" : None,
                      "outB" : None,
                      "outC" : None,
                      "outD" : None,
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
        # The other way (reset self.ports, for d in devices: self.ports[d.address] = d) isn't so faster.

        try:
            devices = [d for d in ev3core.list_motors()]
            devices.extend([d for d in ev3core.list_sensors()])

            portsEnabled = {d.address:d for d in devices}

            for p in self.ports.keys():
                if p in portsEnabled.keys():
                    self.ports[p] = portsEnabled[p]
                else:
                    self.ports[p] = None

        except Exception as e:
            pass


    # Private methods.


if __name__ == "__main__":
    help(cBrickPorts)

