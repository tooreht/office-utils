# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from pdf import pdf_to_text
from utils import collect_files, query_yes_no, read_subcmd_config, unzip

import functools
import mimetypes
import operator
import os
import shutil


def rename(args):
    # Read subcommand config
    cfg = read_subcmd_config(__name__)  # args.subparser_name

    # Create temporary directory and subfolders
    if not os.path.exists(cfg['in_dir']):
        os.makedirs(cfg['in_dir'])
    if not os.path.exists(cfg['out_dir']):
        os.makedirs(cfg['out_dir'])

    # Collect all files from paths
    files = reduce(operator.add, map(collect_files, args.paths))

    # Prepeare files for processing
    map(functools.partial(prepeare_file, in_dir=cfg['in_dir']), files)

    # Rename files
    return map(functools.partial(
            rename_file,
            out_dir=cfg['out_dir'],
            mapping=cfg['mapping'],
            # cache search keys before renaming
            search_keys=[(k, v['key']) for k, v in cfg['mapping'].iteritems()],
            confirm=args.confirm
        ),
        collect_files(cfg['in_dir'])
    )

def prepeare_file(file, in_dir):
    mime, encoding = mimetypes.guess_type(file)
    if mime == 'application/zip':
        unzip(file, in_dir)
    elif mime == 'application/pdf':
        shutil.move(file, in_dir)
    else:
        print('Unexpected document type {} for file {}'.format(mime, file))

def rename_file(file, out_dir, mapping, search_keys, confirm):
    directory, filename = os.path.split(file)
    basename, file_extension = os.path.splitext(filename)
    parts = basename.split('_')

    first_page = pdf_to_text(file)[0]  # The doc type is on the first page
    new_filename = detect_doc_type(first_page, parts, file_extension, mapping, search_keys)
    new_file = os.path.join(out_dir, new_filename)

    if not confirm or query_yes_no('Rename {} to {}?'.format(file, new_file), default=not confirm):
        if os.path.exists(new_file):
            if query_yes_no("File {} already exists, overwrite?".format(new_file), default=not confirm):
                os.renames(file, new_file)
                return new_file
            else:
                print("Skipping {}".format(new_file))
        else:
            os.renames(file, new_file)
            return new_file
    else:
        print("Skipping {}".format(new_file))

def detect_doc_type(text, parts, ext, mapping, search_keys):
    text = unicode(text, errors='replace')
    hits = filter(lambda k: k[1] in text, search_keys)
    fmt, v = '{}_{{}}', None
    for k, v in hits:
        m = mapping[k]
        fmt, v = os.path.join(m['dir'], fmt.format(m['file'])), (parts[m['idx']],)

    if 'Zinsabschluss' in text:
        fmt += '_zinsabschluss'

    fmt += '{}'
    v += (ext,)
    return fmt.format(*v)
