import base64
import json
import os

from flask import Flask, request, redirect
from PIL import Image
from psycopg2 import connect
import numpy as np
import torch

from database import encode_hex, fetch_from_database, insert_into_database
from model.infer_model import InferModel
from model.preprocess import *

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    """Redirect to our site's actual page"""
    return redirect("/static/index.html")


@app.route("/api/ephemeral", methods=["GET", "POST"])
def ephemeral():
    """The basic API endpoint. It takes the provided image, converts it into
    LaTeX, and returns the result.

    It will return a 400 error if the user didn't supply an image or if the
    image is invalid. If the user sends a GET request to this URL, then we
    redirect them to the
    """
    if request.method == "POST":
        try:
            f = request.files["image"]
            image = Image.open(f)
        except IOError:
            return "not a valid image", 400
        except KeyError:
            return "no image was provided", 400
        return get_model_output(image)
    else:
        return redirect("/")


@app.route("/api/upload", methods=["POST"])
def upload():
    """The api endpoint for the user to save their image to the server.

    It takes the image and the LaTeX (the user provides it to this call),
    and then it returns the key for the newly uploaded image and LaTeX.
    """
    try:
        f = request.files["image"]
    except KeyError:
        return "no image was provided", 400
    try:
        latex = request.form["latex"]
    except KeyError:
        return "no latex was provided", 400
    conn = connect(os.environ["DATABASE_URL"], sslmode="require")
    image = encode_hex(f)
    key = insert_into_database(conn, image, latex)
    return key


@app.route("/api/download")
def download():
    """Fetch an already-uploaded image by its key"""
    conn = connect(os.environ["DATABASE_URL"], sslmode="require")
    key = request.args.get("image")
    if key is None:
        return "No key provided", 404
    else:
        res = fetch_from_database(conn, key)
        if res is None:
            return "No such image", 404
        image, latex = res
        return json.dumps({"image": base64.b64encode(image).decode(), "latex": latex})


learned_model = InferModel()


def get_model_output(image):
    """Call the model and get the result, for the provided image"""
    # Preprocess the image - change its size and coloring to match the training set
    converted_image = invertImageColor(image)
    resized_image = resizeImage(converted_image)
    # Now we can send the image through the model and return the result
    image_data = torch.from_numpy(np.array(resized_image)).type(torch.FloatTensor)
    return learned_model.infer(image_data)
