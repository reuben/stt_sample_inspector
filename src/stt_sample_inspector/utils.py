# -*- coding: utf-8 -*-
from functools import partial
from pathlib import Path

import pandas


def absolutify_path(root_dir, rel_path):
    rel_path = Path(rel_path)
    if rel_path.is_absolute():
        return rel_path
    return (root_dir / rel_path).resolve()


def create_abs_column(df, root_dir):
    df["abs_wav_filename"] = df["wav_filename"].apply(
        partial(absolutify_path, root_dir)
    )


def read_csv_and_absolutify(csv_path):
    csv_path = Path(csv_path)
    df = pandas.read_csv(csv_path)
    orig_cols = df.columns
    create_abs_column(df, csv_path.parent)
    return df, orig_cols
