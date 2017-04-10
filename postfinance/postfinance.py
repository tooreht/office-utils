#!/usr/bin/env python
# -*- coding: utf-8 -*-
from natsort import natsorted
from utils import collect_files, read_subcmd_config

import argparse
import os

import archive
import rename
import tarfile


def update(args):
    archive_cfg = read_subcmd_config('archive')
    rename_cfg = read_subcmd_config('rename')

    args.archive_dir = args.archive_dir or archive_cfg['archive_dir']

    if not os.path.isdir(args.archive_dir):
        raise RuntimeError("archive-dir {} is not a directory".format(args.archive_dir))

    files = filter(tarfile.is_tarfile, collect_files(args.archive_dir))
    latest = natsorted(files, reverse=True)[0]

    args.archive = [latest]
    args.extract_dir = None
    archive.extract(args)

    rename.rename(args)

    args.path = [rename_cfg['out_dir']]
    archive.archive(args)


if __name__ == "__main__":
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    subparsers = parser.add_subparsers(dest='subparser_name', help='Available subcommands. Invoke help flag on subcommands to get more information.')


    # create the parser for the "archive" command
    archive_parser = subparsers.add_parser('archive', description='Archive PostFinance documents.')
    archive_parser.add_argument('path', metavar='<path>', type=str, nargs=1,
                        help='path to directory root for archiving')
    archive_parser.add_argument('--archive-dir', dest='archive_dir', action='store',
                        default=None,
                        help='archive directory')
    archive_parser.set_defaults(func=archive.archive)


    # create the parser for the "extract" command
    extract_parser = subparsers.add_parser('extract', description='Extract PostFinance archive.')
    extract_parser.add_argument('archive', metavar='<archive>', type=argparse.FileType('r'), nargs=1,
                        help='path to archive')
    extract_parser.add_argument('--extract-dir', dest='extract_dir', action='store',
                        default=None,
                        help='extract directory')
    extract_parser.set_defaults(func=archive.extract)


    # create the parser for the "rename" command
    rename_parser = subparsers.add_parser('rename', description='Rename PostFinance documents.')
    rename_parser.add_argument('paths', metavar='<paths>', type=str, nargs='+',
                        help='paths to PDF documents or zip files')
    rename_parser.add_argument('--confirm', action='store_true', help='Confirm renaming')
    rename_parser.set_defaults(func=rename.rename)


    # create the parser for the "update" command
    update_parser = subparsers.add_parser('update', description='Update (backup, rename and archive) PostFinance documents.')
    update_parser.add_argument('paths', metavar='<paths>', type=str, nargs='+',
                        help='paths to PDFs documents or zip files')
    update_parser.add_argument('--archive-dir', dest='archive_dir', action='store',
                        default=None,
                        help='archive directory')
    update_parser.add_argument('--confirm', action='store_true', help='Confirm renaming')
    update_parser.set_defaults(func=update)


    # run parser and invoke subcommand
    args = parser.parse_args()
    args.func(args)
