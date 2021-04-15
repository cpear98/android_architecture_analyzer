from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import uuid
import os
import logging


def get_uuid():
    """
    Get a random 128 bit UUID
    """
    return uuid.uuid4()

class Structure:
    """
    Represents a <structure /> tag in an ArchStudio xml document
    """
    def __init__(self):
        pass

    def to_xml(self):
        raise NotImplementedError("Child classes of Structure must override to_xml")

class Component(Structure):
    """
    Represents a component as a first class entity
    """
    def __init__(self, name="[New Component]"):
        self._name = name
        self._id = str(get_uuid())

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:component")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)
        return el

class Connector(Structure):
    """
    Represents a connector as a first class entity.
    Connectors in ArchStudio are more similar to components and can have names,
    interfaces, and links to other components.
    """
    def __init__(self, name="[New Connector]"):
        self._name = name
        self._id = str(get_uuid()) 

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:connector")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)
        return el

class Interface(Structure):
    """
    Represents a directional interface in ArchStudio. Interfaces can be attached to components or connectors
    and allow links to connect a component/connector to another component/connector
    """
    def __init__(self, name="[New Interface]"):
        self._name = name
        self._id = str(get_uuid()) 

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:interface")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)
        return el

class Link(Structure):
    """
    Represents a link between two interfaces in ArchStudio
    """
    def __init__(self, name="[New Link]"):
        self._name = name
        self._id = str(get_uuid()) 

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:link")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)
        return el

class Document:
    """
    Represents an ArchStudio document object
    """
    def __init__(self, file_name, structure_name):
        # TODO: method stub
        self.output_file_name = file_name
        self.main_structure_name = structure_name
        self.entities = set()
        self.components = set()

    def add_component(self, component):
        self.components.add(component)
        self.entities.add(component)

    def to_xml(self):
        # xadlcore is the root tag of the document
        # we are using xADL version 3.0
        xadlcore = Element("xadlcore_3_0:xADL")
        xadlcore.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        xadlcore.set("xmlns:hints_3_0", "http://www.archstudio.org/xadl3/schemas/hints-3.0.xsd")
        xadlcore.set("xmlns:structure_3_0", "http://www.archstudio.org/xadl3/schemas/structure-3.0.xsd")
        xadlcore.set("xmlns:xadlcore_3_0", "http://www.archstudio.org/xadl3/schemas/xadlcore-3.0.xsd")

        # this it the main structure for our architecture
        # every structure requires a unique ID
        body = SubElement(xadlcore, "structure_3_0:structure")
        body.set("structure_3_0:id", str(get_uuid()))
        body.set("structure_3_0:name", self.main_structure_name)

        # Add additional structure to the document
        for entity in self.entities:
            body.append(entity.to_xml())

        # parse to a string, encode as utf-8 and return a bytes object
        return minidom.parseString(tostring(xadlcore)).toprettyxml(indent="    ", encoding="UTF-8")

    def write_current_contents(self):
        project_root = os.path.dirname(os.path.realpath(__file__ + "/.."))
        output_dir = project_root + "/output/" + self.main_structure_name

        logging.debug(f"Checking if output directory {output_dir} exists")

        if not os.path.exists(output_dir):
            logging.debug(f"Path does not exist. Creating directory {output_dir}")
            os.mkdir(output_dir)

        out_file = output_dir + "/" + self.output_file_name

        # to_xml returns a bytes object so we open file with "write bytes" mode
        with open(out_file, "wb") as f:
            f.write(self.to_xml())

        # return the name of the file we wrote to so we can report its location to the user
        return out_file
            