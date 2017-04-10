# -*- coding: utf-8 -*-
from utils import read_subcmd_config

import datetime
import os
import shutil


def archive(args):
    # Read subcommand config
    cfg = read_subcmd_config(__name__)  # args.subparser_name
    root_dir = args.path[0]
    archive_dir = args.archive_dir or cfg['archive_dir']

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    if os.path.isdir(root_dir):
        dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_name = os.path.join(archive_dir, "{}_{}".format(cfg['archive_name'], dt))
        shutil.make_archive(archive_name, cfg['archive_format'], root_dir)

def extract(args):
    cfg = read_subcmd_config(__name__)  # args.subparser_name
    extract_dir = args.extract_dir or cfg['extract_dir']

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    shutil.unpack_archive(args.archive[0], extract_dir, cfg['archive_format'])
