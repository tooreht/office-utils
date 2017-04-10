# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter

import io


def pdf_to_text(path):
    # Open a PDF document.
    with open(path, 'rb') as fp:

        # Create a PDF parser object associated with the StringIO object
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Define parameters to the PDF device objet 
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
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
