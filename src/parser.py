from entities import Component, Connector, Interface, Link, Document
import xml.etree.ElementTree as ET
import logging


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

    def parse(self, manifest_file, architecture_name):
        # first open and read the file
        content = self.read_file(manifest_file)

        # check if we successfully read any content
        if content is None:
            # uh oh
            self.logger.critical(f"Could not read content of \"{manifest_file}\"")
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

        for activity in activities:
            name = activity.get(f"{ANDROID_SCHEMA}name")

            if name is None:
                logging.critical(f"Activity {activity} missing name (Attributes: {activity.attrib})")
                exit()

            if not self.use_fully_qualified_names and name.startswith(package_name + "."):
                name = name.replace(package_name + ".", "")
            
            component = Component(name=name)
            doc.add_component(component)

        for service in services:
            pass

        for receiver in receivers:
            pass

        for provider in providers:
            pass

        return doc
