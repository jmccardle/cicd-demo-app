"""cicd-demo-app: a small web app built, scanned and deployed by the cicd-ref-arch platform.

It keeps a guestbook in memory (each pod has its own, and scale-to-zero empties it: that is
the point of a demo, not a bug). Everything here belongs to the app's developers; the
platform only needs cicd.yaml, deploy/ and the Dockerfile to follow its contract.
"""
import datetime as dt
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for

VERSION = "0.2.0"

app = Flask(__name__)
entries: list[dict] = []


def info() -> dict:
    return {"app": "demo", "version": VERSION,
            "commit": os.environ.get("APP_COMMIT", "dev"),
            "env": os.environ.get("APP_ENV", "local")}


@app.get("/")
def index():
    return render_template("index.html", info=info(), entries=list(reversed(entries[-20:])))


@app.post("/sign")
def sign():
    name = (request.form.get("name") or "").strip()[:40] or "anonymous"
    message = (request.form.get("message") or "").strip()[:280]
    if message:
        entries.append({"name": name, "message": message,
                        "at": dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S UTC")})
    return redirect(url_for("index"))


@app.get("/api/info")
def api_info():
    return jsonify({**info(), "entries": len(entries)})


@app.get("/healthz")
def healthz():
    return "ok\n"
