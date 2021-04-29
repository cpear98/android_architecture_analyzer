from entities import Component, Connector, Interface, Link, Document
from manifest_parser import ManifestParser
import argparse
import logging


# Simple terminal formatted text values
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    # setup the argument parser
    arg_parser = argparse.ArgumentParser(description='Extract the architecture from an android application.')

    # positional arguments
    arg_parser.add_argument('manifest', metavar='file1', type=str, help='Path to the manifest file to analyze')
    arg_parser.add_argument('structure', metavar='structure', type=str, help='Name of the base structure for the extracted architecture')

    # optional arguments
    arg_parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='Run the program in debug mode')
    arg_parser.add_argument('--src', dest='src_dir', type=str, help='Path to the source code corresponding to the provided manifest file')

    # now parse the args
    args = arg_parser.parse_args()

    # get the path to the manifest file to analyze
    manifest = args.manifest

    # get the name of the root structure for our output
    structure = args.structure

    # check if we should run in debug mode
    DEBUG = args.debug

    # check if the user provided a path to source code
    src_dir = args.src_dir

    # instantiate a logger to be used throughout the application
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # now init the parser to analyze the manifest
    parser = ManifestParser()

    # parse the manifest
    doc = parser.parse(manifest, structure, src_dir=src_dir)

    # write the resulting architecture to an xml file
    file_name = doc.write_current_contents()

    # we wrote to the file without error so notify the user
    print(f"{bcolors.OKGREEN}[SUCCESS]{bcolors.ENDC} Output written to {bcolors.UNDERLINE}{file_name}{bcolors.ENDC}")
