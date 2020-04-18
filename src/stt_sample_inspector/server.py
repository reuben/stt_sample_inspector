# -*- coding: utf-8 -*-
import base64
import os
from functools import partial
from pathlib import Path

import pandas
from flask import (
    Blueprint,
    Flask,
    current_app,
    g,
    render_template,
    request,
    session,
    redirect,
    url_for,
)

from . import inspect
from .utils import read_csv_and_absolutify


def create_app(df=None, flask_test_config=None):
    app = Flask(__name__)

    # If no dataframe specified, create dummy one for development
    if df is None:
        here = Path(__file__).parent
        df, _ = read_csv_and_absolutify(here / "sample_data" / "ldc93s1.csv")

    app.config["df"] = df

    # Hash the DataFrame and use this as a global URL prefix to avoid stale caches
    df_hash = str(hash(tuple(pandas.util.hash_pandas_object(df))))
    b64_hash = (
        base64.urlsafe_b64encode(df_hash.encode("ascii"))
        .decode("ascii")
        .replace("=", "")
    )

    # Register blueprints
    app.register_blueprint(
        inspect.bp, url_prefix="/{}/{}".format(b64_hash, inspect.bp.url_prefix)
    )

    @app.route("/")
    def index():
        return redirect(url_for("inspect.index", row_index=0))

    @app.route("/finish", methods=["GET", "POST"])
    def finish():
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            raise RuntimeError("Not running with the Werkzeug Server.")
        func()
        return "Server shutting down..."

    return app


def run_server(dataframe):
    app = create_app(dataframe)
    app.run()
    return app.config["df"]
