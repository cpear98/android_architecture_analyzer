from entities import Component, Connector, Interface, Link, Document
import xml.etree.ElementTree as ET


class ManifestParser:
    def __init__(self, debug=False):
        self.DEBUG = debug

    def read_file(self, manifest_file):
        try:
            with open(manifest_file, "r") as f:
                content = f.read()
                return content
        except Exception as e:
            return None

    def get_element_tree(self, content):
        return ET.fromstring(content)

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
            print(f"ERROR: Could not read content of \"{manifest_file}\"")
            exit()

        # now parse the string to a tree
        tree = self.get_element_tree(content)

        # get Android app components
        activities = self.get_activities(tree)
        services = self.get_services(tree)
        receivers = self.get_receivers(tree)
        providers = self.get_providers(tree)

        if self.DEBUG:
            print(f"Activities: {activities}")
            print(f"Services: {services}")
            print(f"Receivers: {receivers}")
            print(f"Providers: {providers}")

        return Document(architecture_name + ".xml", architecture_name)
