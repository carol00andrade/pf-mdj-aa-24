# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import requests

app = Flask(__name__)

## Parte 1

@app.route("/")
def index():
    return render_template("home.html")
    
@app.route("/portfolio")
def portifolio ():
    return render_template("portfolio.html")

@app.route("/curriculo")
def curriculo ():
    return render_template("curriculo.html")

@app.route("/noticias")
def noticias ():
    return render_template("noticias.html")
