from ebo_object import EboObject



class BACnetObject(EboObject):
    FOREIGNADDRESS_NUMBER_LENGTH = 8

    ALARM_TYPE =               "bacnet.EventEnrollment"
    ALARM_NOTIFICATION_TYPE =  "bacnet.NotificationClass"

    ANALOG_INPUT_TYPE =        "bacnet.point.analog.Input"
    ANALOG_OUTPUT_TYPE =       "bacnet.point.analog.Output"
    ANALOG_VALUE_TYPE =        "bacnet.point.analog.Value"
    DIGITAL_INPUT_TYPE =       "bacnet.point.digital.Input"
    DIGITAL_OUTPUT_TYPE =      "bacnet.point.digital.Output"
    DIGITAL_VALUE_TYPE =       "bacnet.point.digital.Value"
    MULTISTATE_INPUT_TYPE =    "bacnet.point.multistate.Input"
    MULTISTATE_OUTPUT_TYPE =   "bacnet.point.multistate.Output"
    MULTISTATE_VALUE_TYPE =    "bacnet.point.multistate.Value"

    ANALOG_SCHEDULE_TYPE =     "bacnet.schedule.BACnetAnalogSchedule"
    BOOLEAN_SCHEDULE_TYPE =    "bacnet.schedule.BACnetBooleanSchedule"
    DIGITAL_SCHEDULE_TYPE =    "bacnet.schedule.BACnetDigitalSchedule"
    ENUMERATED_SCHEDULE_TYPE = "bacnet.schedule.BACnetEnumeratedSchedule"
    INTEGER_SCHEDULE_TYPE =    "bacnet.schedule.BACnetIntegerSchedule"
    MULTISTATE_SCHEDULE_TYPE = "bacnet.schedule.BACnetMultistateSchedule"
    CALENDAR_TYPE =            "bacnet.schedule.BACnetCalendar"

    TREND_LOG_TYPE =           "bacnet.TrendLog"

    BACNET_TYPE_PAIRS = {ALARM_TYPE : "event-enrollment",
                        ALARM_NOTIFICATION_TYPE : "notification-class",
                        ANALOG_INPUT_TYPE : "analog-input",
                        ANALOG_OUTPUT_TYPE : "analog-output",
                        ANALOG_VALUE_TYPE : "analog-value",
                        DIGITAL_INPUT_TYPE : "binary-input",
                        DIGITAL_OUTPUT_TYPE : "binary-output",
                        DIGITAL_VALUE_TYPE : "binary-value",
                        MULTISTATE_INPUT_TYPE : "multi-state-input",
                        MULTISTATE_OUTPUT_TYPE : "multi-state-output",
                        MULTISTATE_VALUE_TYPE : "multi-state-value",
                        ANALOG_SCHEDULE_TYPE : "schedule",
                        BOOLEAN_SCHEDULE_TYPE : "schedule",
                        DIGITAL_SCHEDULE_TYPE : "schedule",
                        ENUMERATED_SCHEDULE_TYPE : "schedule",
                        INTEGER_SCHEDULE_TYPE : "schedule",
                        MULTISTATE_SCHEDULE_TYPE : "schedule",
                        CALENDAR_TYPE : "calendar",
                        TREND_LOG_TYPE : "trend-log"}



    def __init__(self, **kwargs):
        super(BACnetObject, self).__init__(**kwargs)


    def get_bacnetname(self):
        return self.get_property_value('BACnet')


    def set_bacnetname(self, bacnetname):
        self.set_dierct_property('BACnetName', bacnetname)

    
    def get_foreignaddress(self):
        return  self.get_property_value('ForeignAddress')


    def get_foreignaddress_as_tuple(self):
        f_add = self.get_property_value('ForeignAddress')
        return self.__split_foreignaddress(f_add)

    
    def set_foreignaddress(self, foreignaddress_number: int):
        foreignaddress_type = BACnetObject.get_foreignaddress_type_equivalent(self.type) #a string
        foreignaddress_string = BACnetObject.create_foreignaddress_string(foreignaddress_type, foreignaddress_number)
        self.set_dierct_property('ForeignAddress', foreignaddress_string)


    def __split_foreignaddress(self, foreignaddress: str):
        if((foreignaddress is None) or len(foreignaddress) == 0):
            return (None, None)
        f_add_arr = foreignaddress.split(',') #split the foreign address into array-parts
        type_part = f_add_arr[0][1:len(f_add_arr[0])]
        number_part = f_add_arr[1].strip()
        number_part = number_part[0:len(number_part)-1]
        return (type_part, number_part)


    @staticmethod
    def create_foreignaddress_string(foreignaddress_type, foreignaddress_number):
        fadd_number_string = str(foreignaddress_number)
        fadd_number_string = ((len(fadd_number_string) - BACnetObject.FOREIGNADDRESS_NUMBER_LENGTH) * " ") + fadd_number_string
        return "&lt;" + foreignaddress_type + "," + fadd_number_string + "&gt;"


    @staticmethod
    def get_foreignaddress_type_equivalent(bacnet_object_type: str):
        return BACnetObject.BACNET_TYPE_PAIRS.get(bacnet_object_type)
