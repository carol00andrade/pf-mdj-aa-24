# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

## Primeira parte do trabalho

@app.route("/")
def index():
    return render_template("home.html")
    
@app.route("/portfolio")
def portifolio ():
    return render_template("portfolio.html")

@app.route("/curriculo")
def curriculo ():
    return render_template("curriculo.html")
