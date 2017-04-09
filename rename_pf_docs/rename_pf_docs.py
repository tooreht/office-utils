#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

"""
############################
PostFinance document renamer
############################

This script renames downloaded documents form PostFinance e-banking based on its types:
  e.g.: 'rep302565461_20140101_p8803.pdf' => 'ausbildung_20140101.pdf'

It detects the type by searching for a string in the PDF document (e.g. "Ausbildungskonto").
It renames and moves the files to a directory structure with subfolders for each type.
See detect_doc_type fn below.

Resources:
- https://quantcorner.wordpress.com/2014/03/16/parsing-pdf-files-with-python-and-pdfminer/
- http://stackoverflow.com/questions/13051871/change-filenames-to-lowercase-in-ubuntu-in-all-subdirectories
    ```for i in $(find . -type f -name "*[A-Z]*"); do mv "$i" "$(echo $i | tr A-Z a-z)"; done```
"""

import argparse
import os
import operator
import shutil
import six
import sys

from distutils.util import strtobool
from StringIO import StringIO


# CONSTANTS

TMP_DIR = os.path.join(os.sep, 'tmp', 'rename_pf_docs')
IN_DIR = os.path.join(TMP_DIR, 'in')
OUT_DIR = os.path.join(TMP_DIR, 'out')


def parsePDF(path):
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.layout import LAParams
    from pdfminer.converter import  TextConverter
    
    # Open a PDF document.
    fp = open(path, 'rb')

    # Create a PDF parser object associated with the StringIO object
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Define parameters to the PDF device objet 
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    codec = 'utf-8'

    # Create a PDF device object
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    # Create a PDF interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pages = []
    # Process each page contained in the document
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        pages.append(retstr.getvalue())

    return pages

def detect_doc_type(text, parts, ext):
    text = unicode(text, errors='replace')
    if 'Vorsorgekonto 3a' in text:
        fmt, v = os.path.join('3a', '3a_{}'), (parts[2],)
    elif 'Ausbildungskonto' in text:
        fmt, v = os.path.join('Ausbildungskonto', 'ausbildung_{}'), (parts[1],)
    elif 'Depositokonto' in text:
        fmt, v = os.path.join('Depositokonto', 'deposito_{}'), (parts[1],)
    elif 'Sparkonto' in text:
        fmt, v = os.path.join('Sparkonto', 'sparkonto_{}'), (parts[1],)
    elif 'Verarbeitungsmeldung' in text:
        fmt, v = os.path.join('Verarbeitungsmeldungen', 'vm_{}'), (parts[1],)
    elif 'Zahlungsbestätigung' in text:
        fmt, v = os.path.join('Zahlungsbestätigungen', 'zb_{}'), (parts[1],)
    else:
        fmt, v = os.path.join('Misc', 'misc_{}'), (parts[1],)

    if 'Zinsabschluss' in text:
        fmt += '_zinsabschluss'

    fmt += '{}'
    v += (ext,)
    return fmt.format(*v)

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

def rename_file(file):
    first_page = parsePDF(file)[0]  # The doc type is on the first page

    directory, filename = os.path.split(file)
    basename, file_extension = os.path.splitext(filename)
    parts = basename.split('_')
    new_filename = detect_doc_type(first_page, parts, file_extension)

    new_file = os.path.join(OUT_DIR, new_filename)

    if query_yes_no('Rename {} to {}?'.format(file, new_file)):
        os.renames(file, new_file)

def unzip(file, directory):
    import zipfile

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(directory)

def prepeare_file(file):
    import mimetypes

    mime, encoding = mimetypes.guess_type(file)
    if mime == 'application/zip':
        unzip(file, IN_DIR)
    elif mime == 'application/pdf':
        shutil.move(file, IN_DIR)
    else:
        print('Unexpected document type: {}'.format(mime))

def dir_walker(directory):
    f = []
    for root, dirs, files in os.walk(directory):
        f.extend(map(lambda f: os.path.join(root, f), files))
    return f

def collect_files(path):
    if os.path.isfile(path):
        return os.path.abspath(path)

    return dir_walker(path)

def main(args):
    # Create temporary directory and subfolder
    if not os.path.exists(TMP_DIR):
        os.makedirs(IN_DIR)
        os.makedirs(OUT_DIR)

    # Collect all files from paths
    files = reduce(operator.add, map(collect_files, args.paths))

    # Prepeare files for processing
    map(prepeare_file, files)

    # Rename files
    map(rename_file, dir_walker(IN_DIR))  # filter(os.path.isfile, os.listdir(IN_DIR)))

if __name__ == "__main__":
    # Support Python 2 and 3 input
    # Default to Python 3's input()
    get_input = input

    # If this is Python 2, use raw_input()
    if sys.version_info[:2] <= (2, 7):
        get_input = raw_input


    parser = argparse.ArgumentParser(description='Rename Postfinance documents for archiving.')
    parser.add_argument('paths', metavar='<path>', type=six.text_type, nargs='+',
                        help='paths to pf documents')
    parser.add_argument('-o' '--outdir', dest='output', action='store',
                        default=OUT_DIR,
                        help='destination path')

    args = parser.parse_args()

    main(args)
