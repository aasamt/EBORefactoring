from ebo_point_value import EboPointValue
from bacnet_object import BACnetObject


class BACnetPointValue(EboPointValue, BACnetObject):
    def __init__(self, **kwargs):
        super(BACnetPointValue, self).__init__(**kwargs)


    @classmethod
    def BACnetAnalogInput(cls, name, descr='', unit=None, retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.ANALOG_INPUT_TYPE, DESCR=descr)
        if(unit is not None):
            point_object.set_unit(unit)
        return point_object


    @classmethod
    def BACnetAnalogOutput(cls, name, descr='', unit=None, retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.ANALOG_OUTPUT_TYPE, DESCR=descr)
        if(unit is not None):
            point_object.set_unit(unit)
        if(retainlevel is not None):
            point_object.set_retainlevel(retainlevel)
        return point_object


    @classmethod
    def BACnetAnalogValue(cls, name, descr='', unit=None, retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.ANALOG_VALUE_TYPE, DESCR=descr)
        if(unit is not None):
            point_object.set_unit(unit)
        if(retainlevel is not None):
            point_object.set_retainlevel(retainlevel)
        return point_object

    
    @classmethod
    def BACnetDigitalInput(cls, name, descr=''):
        return cls(NAME=name, TYPE=cls.DIGITAL_INPUT_TYPE, DESCR=descr)


    @classmethod
    def BACnetDigitalOutput(cls, name, descr='', retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.DIGITAL_OUTPUT_TYPE, DESCR=descr)
        if(retainlevel is not None):
            point_object.set_retainlevel(retainlevel)
        return point_object


    @classmethod
    def BACnetDigitalValue(cls, name, descr='', retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.DIGITAL_VALUE_TYPE, DESCR=descr)
        if(retainlevel is not None):
            point_object.set_retainlevel(retainlevel)
        return point_object