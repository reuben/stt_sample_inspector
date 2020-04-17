# -*- coding: utf-8 -*-
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
    if df is not None:
        here = Path(__file__).parent
        df, _ = read_csv_and_absolutify(here / "sample_data" / "ldc93s1.csv")

    app.config["df"] = df

    # Register blueprints
    app.register_blueprint(inspect.bp)

    @app.route("/")
    def index():
        return redirect(url_for("inspect.index", row_index=0))

    return app


def run_server(dataframe):
    app = create_app(dataframe)
    app.run()
    return app.config["df"]
