from entities import Component, Connector, Interface, Link, Document
from parser import ManifestParser
import argparse


if __name__ == "__main__":
    # setup the argument parser
    arg_parser = argparse.ArgumentParser(description='Extract the architecture from an android application.')

    # positional arguments
    arg_parser.add_argument('manifest', metavar='file1', type=str, help='Path to the manifest file to analyze')
    arg_parser.add_argument('structure', metavar='structure', type=str, help='Name of the base structure for the extracted architecture')

    # optional arguments
    # arg_parser.add_argument('--arg', type=str, help='this is an optional arg')

    # now parse the args
    args = arg_parser.parse_args()

    # get the path to the manifest file to analyze
    manifest = args.manifest

    # get the name of the root structure for our output
    structure = args.structure

    # now init the parser to analyze the manifest
    parser = ManifestParser()

    # parse the manifest
    doc = parser.parse(manifest, structure)

    # write the resulting architecture to an xml file
    doc.write_current_contents()
    