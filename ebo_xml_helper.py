from lxml import etree

EBO_XML_ROOT_TAG = 'ObjectSet'
EBO_XML_TYPES_TAG = 'Types'
EBO_XML_TYPES_CHILD_TAG = 'ObjectType'
EBO_XML_EXPORTED_OBJECTS_TAG = 'ExportedObjects'
EBO_XML_EXPORTED_OBJECTS_CHILD_TAG = 'OI'
EBO_XML_EXPORTED_OBJECTS_PROP_TAG = 'PI'
EBO_XML_EXPORTED_OBJECTS_BIND_TAG = 'Reference'
EBO_XML_EXPORTED_OBJECTS_BIND_PATH_ATTR = 'Object'
EBO_XML_EXPORTED_OBJECTS_BIND_PROP_ATTR = 'Property'
EBO_XML_EXPORTED_OBJECTS_UNIT_PROP_ATTR = 'Unit'

SCRIPT_PRG_TYPE_PROP_TAB_TAG = 'PropertyTab'
SCRIPT_PRG_TYPE_VAR_TAG = 'Variable'


##################################### BEGIN: General XML Node Helper Functions ######################################
def xml_node_str(xml_node):
    if(not etree.iselement(xml_node)):
        return ''
    else:
         return etree.tostring(xml_node, pretty_print=True).decode()



def find_xml_node(xml_node, tag, attribute_value_dict, direct_children_only=False):
    """
    Returns the first node under xml_node that matches the criteria. Returns None if no match found.
    :param xml_node: A XML node to iterate over
    :type xml_node: Element
    :param tag: XML Tag of the desired object
    :type tag: str
    :param attribute_value_dict: Dictionary containing desired attribute, value pairs to match. Optional
    :type attribute_value_dict: dict
    """
    if(not etree.iselement(xml_node)): return None
    xpath_expr = _build_xpath_expression(tag, attribute_value_dict, direct_children_only)
    return xml_node.find(xpath_expr)


def findall_xml_nodes(xml_node, tag, attribute_value_dict):
    """
    Returns a list of all nodes under xml_node that match the criteria. Returns empty list if no match found.
    :param root_xml_node: A XML node to iterate over
    :type root_xml_node: Element
    :param tag: XML Tag of the desired object
    :type tag: str
    :param attribute_value_dict: Dictionary containing desired attribute, value pairs to match. Optional
    :type attribute_value_dict: dict
    """  
    xpath_expr = _build_xpath_expression(tag, attribute_value_dict)
    return xml_node.findall(xpath_expr)


def _build_xpath_expression(tag, attribute_value_dict, direct_children_only=False):
    """
    Returns an XPath expressiong string based on the XML tag and attributes/values provided
    :param tag: XML Tag of the desired object
    :type tag: str
    :param attribute_value_dict: Dictionary containing desired attribute, value pairs to match. Optional
    :type attribute_value_dict: dict
    :param direct_children_only: Optional. if set to True, XPath expression will be limited to direct-children nodes only
    :type direct_children_only: bool
    """  
    xpath_expr =  ("./" + tag) if (direct_children_only==True) else (".//" + tag)
    
    if(len(attribute_value_dict) > 0 and type(attribute_value_dict) == dict):
        attr_value_pairs = []
        for attr, val in attribute_value_dict.items(): #combine all pairs as xpath and append to list
            if(val == None):
                attr_value_pairs.append('@' + attr)
            else:
                attr_value_pairs.append('@' + attr + '="' + val +'"')
        attr_xpath_expr = " and ".join(attr_value_pairs)
        xpath_expr += '[' + attr_xpath_expr + ']'
    return xpath_expr



def create_ebo_xml_node(tag, **kwargs):
        return etree.Element(tag, **kwargs)




def _test_build_xpath_expression():
    attr = {'Name':'BACnetName', 'Value':'SaTmp'}
    xpr = _build_xpath_expression('PI', attr, direct_children_only=True)
    print('XPATH:', xpr)

    attr = {'Name':'Value', 'Unit':None}
    xpr = _build_xpath_expression('PI', attr, direct_children_only=False)
    print('XPATH:', xpr)