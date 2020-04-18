# -*- coding: utf-8 -*-
import io
import os
import base64

import librosa
import librosa.display
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from flask import (
    Blueprint,
    Flask,
    current_app,
    g,
    make_response,
    render_template,
    request,
    send_file,
    session,
    redirect,
    url_for,
)

bp = Blueprint("inspect", __name__, url_prefix="/inspect")


@bp.route("/audio/<int:row_index>")
def audio(row_index):
    row = current_app.config["df"].iloc[row_index]
    response = make_response(send_file(row["abs_wav_filename"], mimetype="audio/wav"))
    response.cache_control.public = True
    response.cache_control.max_age = 600
    return response


def get_next_prev(row_index):
    df = current_app.config["df"]
    assert 0 <= row_index < len(df)
    has_next = (row_index + 1) < len(df)
    next_url = url_for(".index", row_index=min(row_index + 1, len(df)))
    has_prev = (row_index - 1) >= 0
    prev_url = url_for(".index", row_index=max(row_index - 1, 0))
    return has_next, next_url, has_prev, prev_url


def do_index_get(row_index):
    df = current_app.config["df"]
    if not 0 <= row_index < len(df):
        return "bad index", 404

    row = df.iloc[row_index]
    orig_filename = row["wav_filename"]
    abs_filename = row["abs_wav_filename"]

    samples, rate = librosa.load(abs_filename)
    S = librosa.feature.melspectrogram(
        y=samples, sr=rate, n_fft=512, hop_length=320, fmax=rate / 2
    )
    plt.figure(figsize=(12, 4))
    img = librosa.display.specshow(
        librosa.power_to_db(S, ref=np.max), y_axis="mel", fmax=rate / 2, x_axis="time"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel spectrogram")
    plt.tight_layout()
    with io.BytesIO() as fout:
        plt.savefig(fout, dpi=150)
        plt.gca().clear()
        b64_encoded = base64.b64encode(fout.getbuffer()).decode("ascii")
        b64_jpeg = "data:image/jpeg;base64,{}".format(b64_encoded)

    transcript = row["transcript"]

    has_next, next_url, has_prev, prev_url = get_next_prev(row_index)

    response = make_response(
        render_template(
            "inspect.html",
            filename=orig_filename,
            spectrogram=b64_jpeg,
            transcript=transcript,
            audio_url=url_for(".audio", row_index=row_index),
            cur_idx=row_index + 1,
            num_samples=len(df),
            has_next=has_next,
            next_url=next_url,
            has_prev=has_prev,
            prev_url=prev_url,
        )
    )
    response.cache_control.public = True
    response.cache_control.max_age = 600
    return response


def do_index_post(row_index):
    df = current_app.config["df"]
    new_transcript = request.form["transcript"]
    df.loc[row_index, "transcript"] = new_transcript
    has_next, next_url, _, _ = get_next_prev(row_index)
    cur_url = url_for(".index", row_index=row_index)
    return redirect(next_url if has_next else cur_url)


@bp.route("/<int:row_index>", methods=["GET", "POST"])
def index(row_index):
    if request.method == "GET":
        return do_index_get(row_index)
    else:
        return do_index_post(row_index)


@bp.route("/finish", methods=["GET", "POST"])
def finish():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down..."
