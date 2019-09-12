from ebo_object import EboObject

class EboPointValue(EboObject):
    def __init__(self, **kwargs):
        super(EboPointValue, self).__init__(**kwargs)


    @classmethod
    def create_bacnet_analog_input(cls, name, descr='', unit=None, retain_level=False):
        point_object = cls(NAME=name, TYPE='', DESCR=descr)
        if(unit is not None):
            point_object.set_embedded_property('Unit', unit, 'Value')
        if(retain_level is not None):
            point_object.set_embedded_property('RetainLevel', retain_level, 'Value')
        return point_object
        