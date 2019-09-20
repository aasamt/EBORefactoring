from ebo_object import EboObject

class EboPointValue(EboObject):
    def __init__(self, **kwargs):
        super(EboPointValue, self).__init__(**kwargs)
        

    def get_retainlevel(self):
        return self.get_property_value('RetainLevel', is_embedded_prop=True)


    def set_retainlevel(self, retainlevel):
        self.set_embedded_property('RetainLevel', retainlevel, 'Value')


    def get_unit(self):
        return self.get_property_value('Unit', is_embedded_prop=True)


    def set_unit(self, unit):
        if(self.EBO_TYPES_HANDLER.is_type_analog(self.get_type())):
            self.set_embedded_property("Unit", unit, 'Value')


    @classmethod
    def EboAnalogValue(cls, name, descr='', unit=None, retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.EBO_TYPES_HANDLER.get_ebo_analog_value_type(), DESCR=descr)
        if(unit is not None):
            point_object.set_unit(unit)
        if(retainlevel is not None):
            point_object.set_retainlevel(retainlevel)
        return point_object


    @classmethod
    def EboDigitalValue(cls, name, descr='', retainlevel=None):
        point_object = cls(NAME=name, TYPE=cls.EBO_TYPES_HANDLER.get_ebo_digital_value_type(), DESCR=descr)
        if(retainlevel is not None):
            point_object.set_retainlevel(retainlevel)
        return point_object