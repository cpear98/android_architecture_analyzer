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
    def __init__(self, name, id):
        self._name = name
        self._id = id

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def to_xml(self):
        raise NotImplementedError("Child classes of Structure must override to_xml")

class Component(Structure):
    """
    Represents a component as a first class entity
    """
    def __init__(self, name="[New Component]"):
        super().__init__(name, str(get_uuid()))
        self._interfaces = set()

    def add_interface(self, interface):
        self._interfaces.add(interface)
        interface.set_parent(self)

    def remove_interface(self, interface):
        self._interfaces.remove(interface)

    def get_interface_in(self):
        # find the first interface with direction "in"
        for interface in self._interfaces:
            if interface.get_direction() == Interface.DIRECTION_IN:
                return interface
        return None

    def get_interface_out(self):
        # find the first interface with direction "out"
        for interface in self._interfaces:
            if interface.get_direction() == Interface.DIRECTION_OUT:
                return interface
        return None

    def add_interface_out(self, interface):
        # we don't actually care about the interface direction here, this method is provided
        # so both Component and Connector have a standard interface for adding Interfaces
        if interface.get_direction() == Interface.DIRECTION_OUT:
            self._interfaces.add(interface)
            interface.set_parent(self)
        else:
            direction = Interface.direction_strings[interface.get_direction()]
            logging.critical(f"Attempted to add an interface with direction {direction} via Component.add_interface_in(self, interface)")
            exit()

    def add_interface_in(self, interface):
        # see comment in add_interface_out
        if interface.get_direction() == Interface.DIRECTION_IN:
            self._interfaces.add(interface)
            interface.set_parent(self)
        else:
            direction = Interface.direction_strings[interface.get_direction()]
            logging.critical(f"Attempted to add an interface with direction {direction} via Component.add_interface_out(self, interface)")
            exit()

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:component")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)
        for interface in self._interfaces:
            el.append(interface.to_xml())
        return el

class Connector(Structure):
    """
    Represents a connector as a first class entity.
    Connectors in ArchStudio are more similar to components and can have names,
    interfaces, and links to other components.
    """
    def __init__(self, name="[New Connector]"):
        super().__init__(name, str(get_uuid()))

        # all connectors should have one incoming interface and one outgoing interface
        self._interface_in = Interface(name=self._name + " Interface In", direction=Interface.DIRECTION_IN, parent=self)
        self._interface_out = Interface(name=self._name + " Interface Out", direction=Interface.DIRECTION_OUT, parent=self)

    def get_interface_in(self):
        return self._interface_in

    def get_interface_out(self):
        return self._interface_out

    def add_interface_out(self, interface):
        # really we "set" the interface rather than add it, but we want a standard interface
        # for adding Interfaces that can be used with either Components or Connectors
        self._interface_out = interface
        self._interface_out.set_parent(self)

    def add_interface_in(self, interface):
        # see comment in add_interface_out
        self._interface_in = interface
        self._interface_in.set_parent(self)

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:connector")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)
        el.append(self._interface_in.to_xml())
        el.append(self._interface_out.to_xml())
        return el

class Interface(Structure):
    """
    Represents a directional interface in ArchStudio. Interfaces can be attached to components or connectors
    and allow links to connect a component/connector to another component/connector
    """

    DIRECTION_NONE      = 0
    DIRECTION_IN        = 1
    DIRECTION_OUT       = 2
    DIRECTION_IN_OUT    = 3

    # set of valid directions for checking membership
    VALID_DIRECTIONS = {
        DIRECTION_NONE,
        DIRECTION_IN,
        DIRECTION_OUT,
        DIRECTION_IN_OUT
    }

    # map of direction strings for converting to xml
    direction_strings = {
        DIRECTION_NONE: "",
        DIRECTION_IN: "in",
        DIRECTION_OUT: "out",
        DIRECTION_IN_OUT: "in-out"
    }

    def __init__(self, name="[New Interface]", direction=DIRECTION_NONE, parent=None):
        super().__init__(name, str(get_uuid()))
        self._direction = direction
        self._parent = parent

    def set_direction(self, direction):
        if direction in Interface.VALID_DIRECTIONS:
            self._direction = direction
        else:
            logging.critical(f"Invalid direction for interface: {direction}")
            exit()

    def get_direction(self):
        return self._direction

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:interface")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)

        direction_string = Interface.direction_strings[self._direction]
        if len(direction_string) > 0:
            el.set("structure_3_0:direction", direction_string)

        return el

class Link(Structure):
    """
    Represents a link between two interfaces in ArchStudio
    """
    def __init__(self, name="[New Link]", start=None, end=None):
        super().__init__(name, str(get_uuid()))

        # start point should be an interface with direction "out"
        self._start = start

        # end point should be an interface with direction "in"
        self._end = end

    def __str__(self):
        string = ""
        if self._start is not None:
            if self._start.get_parent() is not None:
                string = self._start.get_parent().get_name()
            else:
                string = "Interface " + self._start.get_id()
        string += " --> "
        if self._end is not None:
            if self._end.get_parent() is not None:
                string += self._end.get_parent().get_name()
            else:
                string += "Interface " + self._end.get_id()
        return string

    def set_start(self, start):
        if type(start) is Interface:
            self._start = start
        elif type(start) in (Connector, Component):
            self._start = start.get_interface_in()
        else:
            logging.critical(f"Invalid start point type {type(start)}")
            exit()

    def set_end(self, end):
        if type(end) is Interface:
            self._end = end
        elif type(end) in (Connector, Component):
            self._end = start.get_interface_out()
        else:
            logging.critical(f"Invalid end point type {type(end)}")
            exit()

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_start_component(self):
        return self._start.get_parent() 

    def get_end_component(self):
        return self._end.get_parent()

    def to_xml(self):
        # TODO: method stub
        el = Element("structure_3_0:link")
        el.set("structure_3_0:id", self._id)
        el.set("structure_3_0:name", self._name)

        # Need start and end components
        if self._start is None or self._end is None:
            logging.critical(f"Link {self._name} ({self._id}) missing start and/or end points")
            exit()

        point1 = SubElement(el, "structure_3_0:point1")
        point2 = SubElement(el, "structure_3_0:point2")

        point1.text = self._start.get_id()
        point2.text = self._end.get_id()

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
        self.connectors = set()
        self.links = set()
        self._bus = None

    def add_bus(self):
        # don't add a new bus if we already have one
        if self._bus is None:
            bus = Connector(name="Implicit Message Bus")
            self._bus = bus 
            self.entities.add(bus)
            self.connectors.add(bus)
        return self._bus

    def remove_bus(self):
        bus = self._bus 
        self.entities.remove(bus)
        self.connectors.remove(bus)
        self._bus = None

    def get_bus(self):
        return self._bus

    def get_connectors(self):
        return self.connectors

    def add_component(self, component):
        self.components.add(component)
        self.entities.add(component)

    def add_connector(self, connector):
        self.connectors.add(connector)
        self.entities.add(connector)

    def get_component_from_simple_name(self, simple_name):
        for component in self.components:
            name = component.get_name()
            if name.split(".")[-1] == simple_name:
                return component
        return None

    def get_components(self):
        return self.components

    def get_links(self):
        return self.links

    def add_link(self, start, end):
        # verify the start point
        interface_out = None
        if type(start) is Interface and start.get_direction() == Interface.DIRECTION_OUT:
            interface_out = start
        elif type(start) in (Component, Connector):
            interface_out = start.get_interface_out()

            # now make sure interface_out is not None and create a new interface if it is
            if interface_out is None:
                interface_out = Interface(direction=Interface.DIRECTION_OUT)
                start.add_interface_out(interface_out)
        else:
            logging.critical(f"Invalid type for start point {type(start)}")
            exit()

        # verify the end point
        interface_in = None
        if type(end) is Interface and end.get_direction() == Interface.DIRECTION_IN:
            interface_in = end
        elif type(end) in (Component, Connector):
            interface_in = end.get_interface_in()

            # now make sure interface_out is not None and create a new interface if it is
            if interface_in is None:
                interface_in = Interface(direction=Interface.DIRECTION_IN)
                end.add_interface_in(interface_in)
        else:
            logging.critical(f"Invalid type for end point {type(end)}")
            exit()

        link = Link(start=interface_out, end=interface_in)
        self.entities.add(link)
        self.links.add(link)

    def remove_link(self, link=None, start=None, end=None):
        if link is not None:
            self.entities.remove(link)
            self.links.remove(link)
        else:
            # TODO: get link using start and end points then remove it
            pass

    def get_link(self, sender, receiver):
        logging.debug(f"Checking for link between {sender} and {receiver}")
        for link in self.links:
            start_int = link.get_start()
            start_comp = link.get_start_component()
            end_int = link.get_end()
            end_comp = link.get_end_component()
            logging.debug(f"Checking link {start_comp if start_comp is not None else start_int} -> {end_comp if end_comp is not None else end_int}")
            match = True
            # check if sender is the same
            if type(sender) is Interface:
                match = match and sender == start_int
            elif type(sender) in (Component, Connector):
                match = match and sender == start_comp
            else:
                match = False

            # check if receiver is the same
            if type(receiver) is Interface:
                match = match and receiver == end_int
            elif type(receiver) in (Component, Connector):
                match = match and receiver == end_comp
            else:
                match = False

            if match:
                return link
                
        return None

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
            