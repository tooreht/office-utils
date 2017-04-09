# PostFinance documents handler

The `postfinance.py` script handels documents form PostFinance e-banking service.

- Renaming: e.g. `rep302565461_20140101_p8803.pdf` => `Ausbildungskonto/ausbildung_20140101.pdf`
- Archiving: Add renamed document structure into a compressed archive.
- Updating: Update archive with new renamed document structure

It detects the document type by searching for a keyword in the PDF document (e.g. "Ausbildungskonto"). It renames and moves the files to a directory structure with subfolders for each type. The rename mapping can be configured in `rename/config.yml`.

## Prequisites

- Python Interpreter (Python 2.7 only, due to pdfminer package)

## Install

```
virtualenv ~/.virtualenvs/office-utils
pip install -r requirements.txt
```

## Usage

### Overview

```
(office-utils)❯ /postfinance.py --help
usage: PROG [-h] {archive,extract,rename,update} ...

positional arguments:
  {archive,extract,rename,update}
                        Available subcommands. Invoke help flag on subcommands
                        to get more information.

optional arguments:
  -h, --help            show this help message and exit
```

### Subcommands

**Archive**

```
(office-utils)❯ ./postfinance.py archive --help
usage: PROG archive [-h] [--archive-dir ARCHIVE_DIR] <path>

Archive PostFinance documents.

positional arguments:
  <path>                path to directory root for archiving

optional arguments:
  -h, --help            show this help message and exit
  --archive-dir ARCHIVE_DIR
                        archive directory
```

**Extract**

```
(office-utils)❯ ./postfinance.py extract --help
usage: PROG extract [-h] [--extract-dir EXTRACT_DIR] <archive>

Extract PostFinance archive.

positional arguments:
  <archive>             path to archive

optional arguments:
  -h, --help            show this help message and exit
  --extract-dir EXTRACT_DIR
                        extract directory
```

**Rename**

```
(office-utils)❯ ./postfinance.py rename --help
usage: PROG rename [-h] [--confirm] <paths> [<paths> ...]

Rename PostFinance documents.

positional arguments:
  <paths>     paths to PDF documents or zip files

optional arguments:
  -h, --help  show this help message and exit
  --confirm   Confirm renaming
```

**Update**

```
(office-utils)❯ ./postfinance.py update --help
usage: PROG update [-h] [--archive-dir ARCHIVE_DIR] [--confirm]
                   <paths> [<paths> ...]

Update (backup, rename and archive) PostFinance documents.

positional arguments:
  <paths>               paths to PDFs documents or zip files

optional arguments:
  -h, --help            show this help message and exit
  --archive-dir ARCHIVE_DIR
                        archive directory
  --confirm             Confirm renaming
```

## Resources:
- [PDF](https://quantcorner.wordpress.com/2014/03/16/parsing-pdf-files-with-python-and-pdfminer/)
- [Lowercase all files in directory](http://stackoverflow.com/questions/13051871/change-filenames-to-lowercase-in-ubuntu-in-all-subdirectories)
    ```
    for i in $(find . -type f -name "*[A-Z]*"); do mv "$i" "$(echo $i | tr A-Z a-z)"; done
    ```