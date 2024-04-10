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

## Página dinâmica (Raspador de notícias)

#UOL

import requests
from bs4 import BeautifulSoup
import pandas as pd

requisicao=requests.get('https://noticias.uol.com.br/')

html=requisicao.content

sopa=BeautifulSoup(html)

sopa

noticias_titulo=sopa.findAll('div', {'class':'thumb-caption'})
noticias_link=sopa.findAll('div', {'class':'thumbnails-wrapper'})

noticias_titulo

noticias_link

titulo=noticias_titulo[0].find('h3').text

titulo

link=noticias_link[0].find('a').get('href')

link

manchetes=[]

for link, titulo in zip(noticias_link, noticias_titulo):
  link =link.find('a').get('href')
  titulo= titulo.find('h3').text
  manchetes.append([titulo,link])

manchetes

uol=pd.DataFrame(manchetes, columns=['Título','Link'])

uol

uol['Título'].str.lower()

uol['Título']=uol['Título'].str.lower()

uol_lista_titulo = uol['Título'].to_list()

uol_lista_titulo

lista_palavras = ['afogada', 'agredida', 'agrediu', 'agressão', 'amante', 'arma', 'assassinada', 'assassinadas', 'assassinato', 'assassinou', 'atirou', 'casamento', 'chuta', 'companheiro', 'consentimento', 'corpo', 'deputada', 'esfaqueada', 'esposa', 'estupro', 'ex-marido', 'ex-namorado', 'faca', 'facada', 'feminicídio', 'filha', 'gênero', 'machismo', 'machista', 'matar', 'marido', 'mataram', 'matava', 'matou', 'matamos', 'menina', 'morta', 'mortas', 'mortes', 'morre', 'morreu', 'mordida', 'mulher', 'namorada', 'queimada', 'sexual', 'tapa','tiro', 'vítima', 'violência', 'vereadora']

titulos_selecionados = []
for titulo in uol_lista_titulo:
  for palavra in lista_palavras:
    if palavra in titulo:
      titulos_selecionados.append(titulo)

titulos_selecionados

mask=uol['Título'].isin(titulos_selecionados)
df_filtrado_uol=uol[mask]

df_filtrado_uol['Veículo']="Uol"

df_filtrado_uol

#CNN

import requests
from bs4 import BeautifulSoup
import pandas as pd

requisicao_cnn=requests.get('https://www.cnnbrasil.com.br/')

html_cnn=requisicao_cnn.content

sopa_cnn=BeautifulSoup(html_cnn)

sopa_cnn

noticias_cnn= sopa_cnn.findAll('li', {'class':'block__news__item has--thumb'})

link_cnn=noticias_cnn[0].find('a').get('href')

link_cnn

titulo_cnn=noticias_cnn[0].find('a').text

titulo_cnn

manchetes_cnn=[]

for i in noticias_cnn:
  titulo_cnn=i.find('a').text
  link_cnn=i.find('a').get('href')
  manchetes_cnn.append([titulo_cnn,link_cnn])

manchetes_cnn

cnn=pd.DataFrame(manchetes_cnn,columns=['Título','Link'])

cnn

cnn['Título'].str.lower()

cnn['Título']=cnn['Título'].str.lower()

cnn_lista_titulo=cnn['Título'].to_list()

cnn_lista_titulo

lista_palavras = ['afogada', 'agredida', 'agrediu', 'agressão', 'amante', 'arma', 'assassinada', 'assassinadas', 'assassinato', 'assassinou', 'atirou', 'casamento', 'chuta', 'companheiro', 'consentimento', 'corpo', 'deputada', 'esfaqueada', 'esposa', 'estupro', 'ex-marido', 'ex-namorado', 'faca', 'facada', 'feminicídio', 'filha', 'gênero', 'machismo', 'machista', 'matar', 'marido', 'mataram', 'matava', 'matou', 'matamos', 'menina', 'morta', 'mortas', 'mortes', 'morre', 'morreu', 'mordida', 'mulher', 'namorada', 'queimada', 'sexual', 'tapa','tiro', 'vítima', 'violência', 'vereadora']

titulos_selecionados_cnn= []
for titulo in cnn_lista_titulo:
  for palavra in lista_palavras:
    if palavra in titulo:
      titulos_selecionados_cnn.append(titulo)

titulos_selecionados_cnn

mask=cnn['Título'].isin(titulos_selecionados_cnn)
df_filtrado_cnn=cnn[mask]

df_filtrado_cnn['Veículo']="CNN"

df_filtrado_cnn

#Final

import datetime

df_filtrado_uol.loc[:, 'quando'] = pd.Series([datetime.datetime.now()] * len(df_filtrado_uol))
df_filtrado_cnn.loc[:, 'quando'] = pd.Series([datetime.datetime.now()] * len(df_filtrado_cnn))

a_vida_delas = pd.concat([df_filtrado_uol, df_filtrado_cnn])

a_vida_delas
