# PostFinance document renamer

This script renames downloaded documents form PostFinance e-banking to its corresponding types:
  e.g.: 'rep302565461_20140101_p8803.pdf' => 'ausbildung_20140101.pdf'

It detects the type by searching for a string in the PDF document (e.g. "Ausbildungskonto").
It renames and moves the files to a directory structure with subfolders for each type.
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
usage: rename_pf_docs.py [-h] [-o--outdir OUTPUT] <path> [<path> ...]

Rename Postfinance documents for archiving.

positional arguments:
  <path>             paths to pf documents

optional arguments:
  -h, --help         show this help message and exit
  -o--outdir OUTPUT  destination path
```
