# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import requests
import BeautifulSoup
import pandas

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

# Página dinâmica

@app.route("/noticias")
def noticias ():
    return render_template("noticias.html")

## Raspador de notícias

def raspar_noticias(url):
    requisicao = requests.get(url)
    html = requisicao.content
    sopa = BeautifulSoup(html, 'html.parser')
    noticias_titulo = sopa.find_all('div', {'class': 'thumb-caption'})
    noticias_link = sopa.find_all('div', {'class': 'thumbnails-wrapper'})
    manchetes = []

    for link, titulo in zip(noticias_link, noticias_titulo):
        link = link.find('a').get('href')
        titulo = titulo.find('h3').text
        manchetes.append([titulo, link])

    return manchetes

def selecionar_noticias_com_palavra_chave(noticias, palavras_chave):
    titulos_selecionados = []
    for titulo, link in noticias:
        for palavra in palavras_chave:
            if palavra in titulo.lower():
                titulos_selecionados.append([titulo, link])
                break  # Interrompe o loop assim que uma palavra-chave for encontrada
    return titulos_selecionados

def raspar_e_selecionar_noticias(url, palavras_chave):
    manchetes = raspar_noticias(url)
    manchetes_selecionadas = selecionar_noticias_com_palavra_chave(manchetes, palavras_chave)
    df = pd.DataFrame(manchetes_selecionadas, columns=['Título', 'Link'])
    return df

url = 'https://noticias.uol.com.br/'
palavras_chave = ['afogada', 'agredida', 'agrediu', 'agressão', 'amante', 'arma', 'assassinada', 'assassinadas', 'assassinato', 'assassinou', 'atirou', 'casamento', 'chuta', 'companheiro', 'consentimento', 'corpo', 'deputada', 'esfaqueada', 'esposa', 'estupro', 'ex-marido', 'ex-namorado', 'faca', 'facada', 'feminicídio', 'filha', 'gênero', 'machismo', 'machista', 'matar', 'marido', 'mataram', 'matava', 'matou', 'matamos', 'menina', 'morta', 'mortas', 'mortes', 'morre', 'morreu', 'mordida', 'mulher', 'namorada', 'queimada', 'sexual', 'tapa', 'tiro', 'vítima', 'violência', 'vereadora']

df_noticias_selecionadas = raspar_e_selecionar_noticias(url, palavras_chave)
print(df_noticias_selecionadas)


