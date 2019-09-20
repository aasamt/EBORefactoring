from lxml import etree
import ebo_xml_parser as eboparser

DATA_OBJECT_XML_TAG = 'DataObject'

DATA_OBJECT_DIGITAL_SIGNAL      = 'digital'
DATA_OBJECT_ANALOG_SIGNAL       = 'analog'
DATA_OBJECT_MULTISTATE_SIGNAL   = 'multistate'

DATA_OBJECT_INPUT_TYPE  = 'input'
DATA_OBJECT_OUTPUT_TYPE = 'output'

DATA_OBJECT_AS_DEVICE_ATTRIBUTE         = 'AS'
DATA_OBJECT_AS_BACNET_DEVICE_ATTRIBUTE  = 'BACnet'
DATA_OBJECT_B3_DEVICE_ATRIBUTE          = 'B3'


class EboDefinitions:
    def __init__(self, definition_file_path):
        self.defintions_root = self._open_ebo_definitions_file(definition_file_path)
        self.data_definitions = self._get_definition('Data')
        if(etree.iselement(self.data_definitions) == False):
            raise Exception("Error. Something went wrong in loading the EBO definitions XML file.")


#################### Begin: Helper/Internal Functions ####################
    def _open_ebo_definitions_file(self, definition_file_path):
        try:
            tree = etree.parse(definition_file_path)
            root = tree.getroot()
            return root
        except FileNotFoundError as fnf_error:
            print("Error! EBO Defintions file not found.")
            print("EBO definitions filepath given:", definition_file_path)
            print(fnf_error)
            return None
        except Exception as e:
            print("Error encountered while attempting to read the EBO definitions file.")
            print("EBO definitions filepath given:", definition_file_path)
            print(e)
            return None
    

    def _get_definition(self, definition_name):
        if(etree.iselement(self.defintions_root) == False):
            return None
        return self.defintions_root.find(definition_name)


    #Returns True or False if the xml_node matches the tag,
    #and macthes all attributes in the attributes_dict
    def _xml_node_attributes_compare(self, xml_node, tag, attributes_dict):
        if(etree.iselement(xml_node) == False):
            return False
        if(xml_node.tag != tag):
            return False
        for k,v in attributes_dict.items():
            if(xml_node.get(k) != v):
                return False
        return True


    #Finds and returns an XML node that matches the given tag,
    #and all attributes in the attributes_dict. Returns None if not found.
    def _find_xml_node(self, parent_xml_node, tag, attributes_dict):
        for child_xml_node in parent_xml_node:
            if(self._xml_node_attributes_compare(child_xml_node, tag, attributes_dict) == True):
                return child_xml_node
        return None


    def _get_data_obj_xml_node(self, ebo_data_type):
        for data_obj in self.data_definitions:
            if(data_obj.tag == DATA_OBJECT_XML_TAG):
                if(data_obj.get('Name') == ebo_data_type):
                    return data_obj
        return None


    #For a given data-object xml node (DataObject item), returns a dictionary containing its basic attributes
    def _get_data_obj_xml_node_attr_dict(self, data_obj_xml_node):
        attr = {
            'Signal':data_obj_xml_node.get('Signal'),
            'Type':data_obj_xml_node.get('Type'),
            'Device':data_obj_xml_node.get('Device')
        }
        return attr
##################### End: Helper/Internal Functions #####################



######################## Begin: Utility Functions ########################

    #Returns the BACnet equivalent TYPE string for a given data (point or value) TYPE string
    #Returns None if no match found
    def get_bacnet_point_value_equivalent_type(self, ebo_data_type):
        ebo_data_ref_xml_node = self._get_data_obj_xml_node(ebo_data_type)
        attr = self._get_data_obj_xml_node_attr_dict(ebo_data_ref_xml_node)
        attr['Device'] = DATA_OBJECT_AS_BACNET_DEVICE_ATTRIBUTE
        if(etree.iselement(self.data_definitions)):
            bacnet_equiv_xml_node = self._find_xml_node(self.data_definitions, 
                                                        DATA_OBJECT_XML_TAG, 
                                                        attr)
            if(etree.iselement(bacnet_equiv_xml_node)):
                return bacnet_equiv_xml_node.get('Name')
        return None


    def validate_data_definition(self, ebo_data_type, signals=None, types=None, devices=None):
        if(ebo_data_type == None or type(ebo_data_type) != str or len(ebo_data_type) == 0):
            return False
        data_obj = self._get_data_obj_xml_node(ebo_data_type) #Find the corresponding data-object (xml-node) that matches the given EBO type (str)
        if(data_obj is None):
            return False
        else:
            data_obj_attr_dict = self._get_data_obj_xml_node_attr_dict(data_obj)
            checks = [
                signals is None or data_obj_attr_dict['Signal'] in signals,
                types is None or data_obj_attr_dict['Type'] in types,
                devices is None or data_obj_attr_dict['Device'] in devices]
            if(all(checks)): #if ALL checks are TRUE then validated (return TRUE)
                return True
        return False


    #Returns True if the given EBO object type string is a point or value type string
    #Returns False otherwise
    def is_type_point_or_value(self, ebo_data_type):
        return self.validate_data_definition(ebo_data_type)


    #Returns True if the given EBO XML node is a point or value object XML node
    #Returns False otherwise
    def is_node_point_or_value(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node)
        return self.validate_data_definition(ebo_data_type)

    
    #Returns True if the given EBO object type string is a pdigital point or value
    #Returns False otherwise
    def is_type_digital(self, ebo_data_type):
        return self.validate_data_definition(ebo_data_type, signals=[DATA_OBJECT_DIGITAL_SIGNAL])


    #Returns True if the given EBO XML node is a digital point or value object XML node
    #Returns False otherwise
    def is_node_digital(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node)
        return self.validate_data_definition(ebo_data_type, signals=[DATA_OBJECT_DIGITAL_SIGNAL])
    

    #Returns True if the given EBO object type string is an analog point or value
    #Returns False otherwise
    def is_type_analog(self, ebo_data_type):
        return self.validate_data_definition(ebo_data_type, signals=[DATA_OBJECT_ANALOG_SIGNAL])


    #Returns True if the given EBO XML node is an analog point or value object XML node
    #Returns False otherwise
    def is_node_analog(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node)
        return self.validate_data_definition(ebo_data_type, signals=[DATA_OBJECT_ANALOG_SIGNAL])


    #Returns True if the given EBO object type string is a multistate point or value
    #Returns False otherwise
    def is_type_multistate(self, ebo_data_type):
        return self.validate_data_definition(ebo_data_type, signals=[DATA_OBJECT_MULTISTATE_SIGNAL])


    #Returns True if the given EBO XML node is a multistate point or value object XML node
    #Returns False otherwise
    def is_node_multistate(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node)
        return self.validate_data_definition(ebo_data_type, signals=[DATA_OBJECT_MULTISTATE_SIGNAL])


    #Returns True if a given EBO object type string is an IO Point (of any type or device)
    #Returns False otherwise
    def is_type_io_point(self, ebo_data_type):
        return self.validate_data_definition(ebo_data_type, types=[DATA_OBJECT_INPUT_TYPE, DATA_OBJECT_OUTPUT_TYPE])


    #Returns True if a given EBO XML node is an IO Point (of any type or device),
    #Returns False otherwise
    def is_node_io_point(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node) #Get the EBO type string
        return self.validate_data_definition(ebo_data_type, types=[DATA_OBJECT_INPUT_TYPE, DATA_OBJECT_OUTPUT_TYPE])


    #Returns True if a given EBO object type string is an AS (AS-P or AS-B) IO Bus Point,
    #Returns False otherwise
    def is_type_as_io_point(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node) #Get the EBO type string
        return self.validate_data_definition(ebo_data_type, types=[DATA_OBJECT_INPUT_TYPE, DATA_OBJECT_OUTPUT_TYPE], devices=[DATA_OBJECT_AS_DEVICE_ATTRIBUTE])


    #Returns True if a given EBO XML node is an AS (AS-P or AS-B) IO Bus Point,
    #Returns False otherwise
    def is_node_as_io_point(self, ebo_xml_node):
        if(etree.iselement(ebo_xml_node) == False):
            return False
        ebo_data_type = eboparser.get_node_type(ebo_xml_node) #Get the EBO type string
        return self.validate_data_definition(ebo_data_type, types=[DATA_OBJECT_INPUT_TYPE, DATA_OBJECT_OUTPUT_TYPE], devices=[DATA_OBJECT_AS_DEVICE_ATTRIBUTE])
######################### End: Utility Functions #########################



####################### Begin: Object Type Getters #######################
    def get_ebo_analog_value_type(self):
        #TODO
        return None


    def get_ebo_digital_value_type(self):
        #TODO
        return None


######################## End: Object Type Getters ########################


def test_bacnet_pt_value_converter():
    ebc = EboDefinitions("ebo_definitions.xml")
    bt = ebc.get_bacnet_point_value_equivalent_type("io.point.DigitalInput")
    print(bt)
    bt = ebc.get_bacnet_point_value_equivalent_type("bacnet.b3.point.analog.Output")
    print(bt)
    bt = ebc.get_bacnet_point_value_equivalent_type("io.point.DigitalInputNoLED")
    print(bt)