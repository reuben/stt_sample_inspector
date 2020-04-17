# -*- coding: utf-8 -*-
import argparse
import sys
from pathlib import Path

from stt_sample_inspector import __version__
from stt_sample_inspector.server import run_server
from stt_sample_inspector.utils import read_csv_and_absolutify


def parse_args(args):
    parser = argparse.ArgumentParser(description="Run the tool.")
    parser.add_argument(
        "--version",
        action="version",
        version="stt_sample_inspector {}".format(__version__),
    )
    parser.add_argument("in_csv_file", help="Path to input CSV file.")
    parser.add_argument("out_csv_file", help="Path to save modified CSV file.")
    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    df, orig_cols = read_csv_and_absolutify(args.in_csv_file)
    new_df = run_server(df)
    new_df.loc[:, orig_cols].to_csv(args.out_csv_file, index=False)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
