from lxml import etree
import ebo_xml_helper
from ebo_definitions import EboDefinitions

class EboObject(object):
    EBO_TYPES_HANDLER = EboDefinitions('ebo_definitions.xml')

    def __init__(self, **kwargs):
        if(kwargs.get('xml')):
            self.__init_from_xml(kwargs.get('xml'))
        else:
            self.__init_from_attributes(kwargs.get('NAME'),
                                        kwargs.get('TYPE'),
                                        kwargs.get('DESCR'))
        


    def __init_from_xml(self, xml_node):
        if(not etree.iselement(xml_node)):
            raise Exception("Error! Attempted to create an instance of EboObject from an invalid XML Object")
        else:
            self.name = xml_node.get('NAME')
            self.type = xml_node.get('TYPE')
            self.description = xml_node.get('DESCR')
            self.xml_node = xml_node


    def __init_from_attributes(self, name, typ, descr):
        self.name = name
        self.type = typ
        self.description = descr
        tag = ebo_xml_helper.EBO_XML_EXPORTED_OBJECTS_CHILD_TAG
        self.xml_node = ebo_xml_helper.create_ebo_xml_node(tag, NAME=name, TYPE=typ, DESCR=descr)


    def __repr__(self):
        return ebo_xml_helper.xml_node_str(self.xml_node)


    def get_name(self):
        return self.name


    def get_type(self):
        return self.type


    def get_description(self):
        return self.description


    def get_xml_node(self):
        return self.xml_node


    def get_property_value(self, prop_name, is_embedded_prop=False):
        prop_xml_node = self.find_property_node(prop_name, is_embedded_property=is_embedded_prop)
        if(etree.iselement(prop_xml_node)):
            return prop_xml_node.get('Value')
        return None


    def find_property_node(self, property_name, is_embedded_property=False):
        attributes_dict = {}
        if(is_embedded_property):
            attributes_dict[property_name] = None
        else:
            attributes_dict['Name'] = property_name
        return ebo_xml_helper.find_xml_node(self.xml_node,
                                            ebo_xml_helper.EBO_XML_EXPORTED_OBJECTS_PROP_TAG,
                                            attributes_dict,
                                            direct_children_only=True)

    
    def set_dierct_property(self, property_name, value):
        prop_node = ebo_xml_helper.find_xml_node(self.xml_node,
                                                ebo_xml_helper.EBO_XML_EXPORTED_OBJECTS_PROP_TAG,
                                                {'Name':property_name},
                                                direct_children_only=True)
        if(prop_node is None):
            prop_node = ebo_xml_helper.create_ebo_xml_node(ebo_xml_helper.EBO_XML_EXPORTED_OBJECTS_PROP_TAG,
                                                            Name=property_name,
                                                            Value=value)
            self.xml_node.append(prop_node)
        else:
            prop_node.set('Value', value)


    def set_embedded_property(self, embedded_property_name, embedded_property_value, master_property_name):
        master_prop_node = ebo_xml_helper.find_xml_node(self.xml_node,
                                                ebo_xml_helper.EBO_XML_EXPORTED_OBJECTS_PROP_TAG,
                                                {'Name':master_property_name},
                                                direct_children_only=True)
        if(master_prop_node is None):
            master_prop_node = ebo_xml_helper.create_ebo_xml_node(ebo_xml_helper.EBO_XML_EXPORTED_OBJECTS_PROP_TAG,
                                                            Name=master_property_name,
                                                            Value='')
            master_prop_node.set(embedded_property_name, embedded_property_value)
            self.xml_node.append(master_prop_node)
        else:
            master_prop_node.set(embedded_property_name, embedded_property_value)




def main():
    ebo_obj = EboObject(NAME='SaTmp', TYPE='AI', DESCR='Supply Air Temperature')
    print(ebo_obj)
    ebo_obj.set_dierct_property('BACnetName', 'AHU01_SaTmp')
    print(ebo_obj)
    ebo_obj.set_dierct_property('BACnetName', 'AHU02_SaTmp')
    print(ebo_obj)
    ebo_obj.set_dierct_property('Value', '100.0')
    print(ebo_obj)
    ebo_obj.set_embedded_property('Unit', 'degF', 'Value')
    print(ebo_obj)
    ebo_obj.set_embedded_property('Unit', 'degC', 'Value')
    print(ebo_obj)




main()

        