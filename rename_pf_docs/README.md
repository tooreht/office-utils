# PostFinance document renamer

This script renames downloaded documents form PostFinance e-banking to its corresponding types:
  e.g.: 'rep302565461_20140101_p8803.pdf' => 'ausbildung_20140101.pdf'

It detects the type by searching for a string in the PDF document (e.g. "Ausbildungskonto").
See detect_doc_type fn below.

## Prequisites

- Python Interpreter (Python 2.7 only, due to pdfminer package)

## Install

```
virtualenv ~/.virtualenvs/office-utils
pip install -r requirements.txt
```

## Usage

```
(office-utils)❯ rename_pf_docs.py --help
usage: rename_pf_docs.py [-h] [-o OUTPUT] <file> [<file> ...]

Rename downloaded documents form PostFinance e-banking based on its types.

positional arguments:
  <file>      files to rename

optional arguments:
  -h, --help  show this help message and exit
  -o OUTPUT   destination path
```
