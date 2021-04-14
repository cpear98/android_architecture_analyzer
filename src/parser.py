from entities import Component, Connector, Interface, Link, Document


class ManifestParser:
    def __init__(self):
        pass

    def parse(self, manifest_file, architecture_name):
        # TODO: method stub
        return Document(architecture_name + ".xml", architecture_name)
        