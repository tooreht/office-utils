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
See detect_doc_type fn below.

Resources:
- https://quantcorner.wordpress.com/2014/03/16/parsing-pdf-files-with-python-and-pdfminer/
- http://stackoverflow.com/questions/13051871/change-filenames-to-lowercase-in-ubuntu-in-all-subdirectories
    ```for i in $(find . -type f -name "*[A-Z]*"); do mv "$i" "$(echo $i | tr A-Z a-z)"; done```
"""

import argparse
import sys
import os

from distutils.util import strtobool
from StringIO import StringIO

try:
    basestring
except NameError:
    # python 3 unicode text
    text_type = str
else:
    # python 2 unicode text
    text_type = unicode

# Support Python 2 and 3 input
# Default to Python 3's input()
get_input = input

# If this is Python 2, use raw_input()
if sys.version_info[:2] <= (2, 7):
    get_input = raw_input


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
    if 'Ausbildungskonto' in text:
        fmt, v = 'ausbildung_{}', (parts[1],)
    elif 'Sparkonto' in text:
        fmt, v = 'sparkonto_{}', (parts[1],)
    elif 'Depositokonto' in text:
        fmt, v = 'deposito_{}', (parts[1],)
    elif 'Verarbeitungsmeldung' in text:
        fmt, v = 'vm_{}', (parts[1],)
    elif 'Zahlungsbestätigung' in text:
        fmt, v = 'zb_{}', (parts[1],)
    elif 'Vorsorgekonto 3a' in text:
        fmt, v = '3a_{}', (parts[2],)
    else:
        fmt, v = 'misc_{}', (parts[1],)

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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Rename Postfinance documents for archiving.')
    parser.add_argument('files', metavar='<file>', type=text_type, nargs='+',
                        help='files to rename')
    parser.add_argument('-o', dest='output', action='store',
                        default=None,
                        help='destination path')

    args = parser.parse_args()

    for path in args.files:
        first_page = parsePDF(path)[0]  # The doc type is on the first page

        directory, filename = os.path.split(path)
        basename, file_extension = os.path.splitext(filename)
        parts = basename.split('_')
        new_filename = detect_doc_type(first_page, parts, file_extension)

        if args.output is None:
            output_directory = directory
        else:
            output_directory = args.output

        new_path = os.path.join(output_directory, new_filename)

        if query_yes_no('Rename {} to {}?'.format(path, new_path)):
            os.rename(path, new_path)
