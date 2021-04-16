from entities import Component, Connector, Interface, Link, Document
import xml.etree.ElementTree as ET
import logging
import re


ANDROID_SCHEMA = "{http://schemas.android.com/apk/res/android}"

class ManifestParser:
    def __init__(self, use_fully_qualified_names=False):
        self.use_fully_qualified_names = use_fully_qualified_names

    def read_file(self, manifest_file):
        try:
            with open(manifest_file, "r") as f:
                content = f.read()
                return content
        except Exception as e:
            return None

    def get_element_tree(self, content):
        return ET.fromstring(content)

    def get_package_name(self, tree):
        return tree.get("package")

    def get_tags_from_app(self, tree, tag):
        return tree.find("application").findall(tag)

    def get_activities(self, tree):
        return self.get_tags_from_app(tree, "activity")

    def get_services(self, tree):
        # TODO: method stub
        return self.get_tags_from_app(tree, "service")

    def get_receivers(self, tree):
        # TODO: method stub
        return self.get_tags_from_app(tree, "receiver")

    def get_providers(self, tree):
        # TODO: method stub
        return self.get_tags_from_app(tree, "provider")

    def get_intent_filters(self, element):
        return element.findall("intent-filter")

    def parse_component(self, doc, xml_component, package_name, component_type, src_dir=None):
        name = xml_component.get(f"{ANDROID_SCHEMA}name")
        fully_qualified_name = name

        if name is None:
            logging.critical(f"{component_type} {xml_component} missing name (Attributes: {xml_component.attrib})")
            exit()

        if not self.use_fully_qualified_names and name.startswith(package_name + "."):
            name = name.replace(package_name + ".", "")
        
        component = Component(name=name)
        doc.add_component(component)

        filters = self.get_intent_filters(xml_component)

        if filters is not None and len(filters) > 0:
            # we can receive implicit intents from the android system, so make sure the doc contains
            # a message bus and connect us to it
            bus = doc.get_bus()
            if bus is None:
                bus = doc.add_bus()

            # create a new in-bound interface for the component
            interface_in = Interface(direction=Interface.DIRECTION_IN)
            component.add_interface_in(interface_in)
            doc.add_link(bus, interface_in)

        # now attempt to process source code if a destination was provided
        if src_dir is not None:
            # append a trailing forward slash if we need to
            if src_dir[-1] != "/":
                src_dir += "/"

            # get the relative path to the Java class for this component
            file_path = src_dir + fully_qualified_name.replace(".", "/") + ".java"

            logging.debug(f"Parsing source file {file_path}")

            src_string = None
            with open(file_path, "rb") as f:
                src_string = str(f.read())

            if src_string is None:
                logging.error(f"Could not read content from {file_path}")
                return
            
            #print(src_string)

            # TODO: currently does not match intents like:
            # new Intent (...);
            # new Intent(this, someFunc());

            regex = "new Intent\\([^\\)]*\\)" #(\\.[^\\)]*\\))?"
            occurences = re.findall(regex, src_string)

            logging.debug(f"Occurences of Intents in {file_path}: {occurences}")

            # now check each Intent and see if it is an implicit or explicit Intent
            links_to_add = set()
            for intent in occurences:
                if intent.startswith("new Intent(this,"):
                    # we have an explicit intent
                    # we can't build the link to other components yet in case we haven't created them,
                    # so store the link we will need to be created later
                    sender = name 

                    # get rid of the constructor call
                    receiver = intent.replace("new Intent(this,", "")

                    # trim any excess whitespace
                    receiver = receiver.strip()

                    # remove the trailing parentheses
                    receiver = receiver[:-1]

                    # get rid of the Java .class extension
                    receiver = receiver.replace(".class", "")

                    logging.debug(f"Extracted explicit Intent: {sender} -> {receiver}")
                    links_to_add.add((sender, receiver))

                elif intent.startswith("new Intent(Intent.") or intent.startswith("new Intent(android.content.Intent."):
                    # we have an implicit intent
                    # create a link from this component to the Android system message bus
                    bus = doc.get_bus()
                    if bus is None:
                        bus = doc.add_bus()

                    # create a new out-bound interface for the component
                    if doc.get_link(component, bus) is None:
                        interface_out = Interface(direction=Interface.DIRECTION_OUT)
                        component.add_interface_out(interface_out)
                        doc.add_link(interface_out, bus)
                else:
                    # we don't recognize or don't support this syntax
                    # complain about it so we can fix it or add support
                    logging.error(f"Unsupported syntax in {file_path}: {intent}")
            return links_to_add
        else:
            # we didn't parse source code so we don't have any additional links to add later
            return set()

    def parse(self, manifest_file, architecture_name, src_dir=None):
        # first open and read the file
        content = self.read_file(manifest_file)

        # check if we successfully read any content
        if content is None:
            # uh oh
            logging.critical(f"Could not read content of \"{manifest_file}\"")
            exit()

        # now parse the string to a tree
        tree = self.get_element_tree(content)

        package_name = self.get_package_name(tree)
        
        logging.debug(f"Package name: {package_name}")

        # get Android app components
        activities = self.get_activities(tree)
        services = self.get_services(tree)
        receivers = self.get_receivers(tree)
        providers = self.get_providers(tree)

        logging.debug(f"Activities: {activities}")
        logging.debug(f"Services: {services}")
        logging.debug(f"Receivers: {receivers}")
        logging.debug(f"Providers: {providers}")

        # create a document
        doc = Document(architecture_name + ".xml", architecture_name)

        # now create entities for components in the manifest
        # iterate over each list separately because it doesn't take any longer and we may want to handle each
        # differently in the future

        links_to_add = set()
        for activity in activities:
            links_to_add.update(self.parse_component(doc, activity, package_name, "Activity", src_dir=src_dir))

        for service in services:
            links_to_add.update(self.parse_component(doc, service, package_name, "Service", src_dir=src_dir))

        for receiver in receivers:
            links_to_add.update(self.parse_component(doc, service, package_name, "Receiver", src_dir=src_dir))

        for provider in providers:
            # TODO: may need to handle content provider differently as it has access to a data store and serves content
            links_to_add.update(self.parse_component(doc, service, package_name, "Provider", src_dir=src_dir))

        logging.debug(f"Adding links {links_to_add}")

        for link in links_to_add:
            sender_simple_name = link[0].split(".")[-1]
            receiver_simple_name = link[1].split(".")[-1]
            
            # get the sender and receiver components
            sender = doc.get_component_from_simple_name(sender_simple_name)
            receiver = doc.get_component_from_simple_name(receiver_simple_name)

            # add interfaces to each
            sender_interface_out = Interface(direction=Interface.DIRECTION_OUT)
            sender.add_interface_out(sender_interface_out)
            receiver_interface_in = Interface(direction=Interface.DIRECTION_IN)
            receiver.add_interface_in(receiver_interface_in)

            # now add a connector to represent the explicit intent
            connector = Connector(name=f"Explicit Intent from {sender_simple_name} to {receiver_simple_name}")
            doc.add_connector(connector)

            # finally add a link from the sender to the connector, and from the connector to the receiver
            doc.add_link(sender_interface_out, connector)
            doc.add_link(connector, receiver_interface_in)

        return doc
