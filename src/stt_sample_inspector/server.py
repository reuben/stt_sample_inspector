# -*- coding: utf-8 -*-
import logging

from flask import Flask, render_template

_logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def run_server():
    app.run()
