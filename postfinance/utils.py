# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from distutils.util import strtobool

import os
import ruamel.yaml
import sys
import zipfile

# Support Python 2 and 3 input
# Default to Python 3's input()
get_input = input

# If this is Python 2, use raw_input()
if sys.version_info[:2] <= (2, 7):
    get_input = raw_input


def collect_files(path):
    fl = []
    if os.path.isfile(path):
        fl.append(os.path.abspath(path))

    for root, dirs, files in os.walk(path):
        fl.extend(map(lambda f: os.path.join(root, f), files))
    return fl

def query_yes_no(question, default=None):
    """Ask a yes/no question via cmd and return answer."""
    print("{} [y/n]".format(question), end=" ")

    while True:
        try:
            i = get_input()
            print(i)
            return strtobool(i.lower())
        except ValueError:
            if isinstance(default, bool):
                print("using default: {}".format('y' if default else 'n'))
                return default
            print("Please respond with 'y' or 'n'.")

def read_subcmd_config(subcmd):
    path = os.path.join(subcmd, "config.yml")
    with open(path, 'r') as yml:
        return ruamel.yaml.load(yml, ruamel.yaml.RoundTripLoader)

def unzip(file, directory):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(directory)
