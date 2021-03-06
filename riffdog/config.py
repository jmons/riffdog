from enum import Enum

class ScanMode(Enum):
    """
    Mode of operation of scanner
    """

    LIGHT = 1
    DEEP = 2

class StateStorage(Enum):
    AWS_S3 = 1
    FILE = 2


class RDConfig:
    """
    RiffDog Config Object for controlling the scan.
    """

    class __RDConfig:
        _configurations = None

        @property
        def elements_to_scan(self):
            if self.included_resources:
                resources = (x for x in self.included_resources)
            else:
                resources = (x for x in self.base_elements_to_scan if x not in self.excluded_resources)
            return resources

        def __init__(self):

            self._configurations = {}
            
            # Set defaults and must-have settings
            self.external_resource_libs = [
                'riffdog_aws',
                #'riffdog_cloudflare'
            ]

            self.state_file_locations = []

            self.excluded_resources = []
            self.included_resources = []

            self.base_elements_to_scan = []

            self.scan_mode = ScanMode.LIGHT

        def __getattr__(self, name):
            if not name == "_configurations":
                return self._configurations[name]
            else:
                raise KeyError("_configurations is restricted keyword for config")

        def __setattr__(self, name, value):
            if name =="_configurations":
                super().__setattr__(name, value)
            else:
                self._configurations[name] = value

            
    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not RDConfig.instance:
            RDConfig.instance = RDConfig.__RDConfig()
        return RDConfig.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

