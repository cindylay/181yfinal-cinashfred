import base64
import json
import os

from flask import Flask, request, redirect
from PIL import Image
from psycopg2 import connect
import numpy as np
import torch
import sys

from doc2code import infer_model
import re

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
        # f = request.args.get('myForm')
        # f = request.form['fname']
        # return f
        f = ((str(request.data)[2:-1]))
        # output = get_model_output(f)
        return 'we never got this to work :(', 200
       

# This works on Windows alone, but we have major problems merging Flask 
# with the tensorflow version on both Windows and Mac OS machiens!!!!
def get_model_output(text):
    """Call the model and get the result, for the provided text"""
    
    quoted_text = r'"""' + text + r'"""'

    return infer_model.infer(prompt = quoted_text)

