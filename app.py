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

## Página dinâmica (Raspador)

requisicao=requests.get('https://noticias.uol.com.br/')

html=requisicao.content

sopa=BeautifulSoup(html)

sopa

noticias_titulo=sopa.findAll('div', {'class':'thumb-caption'})
noticias_link=sopa.findAll('div', {'class':'thumbnails-wrapper'})

noticias_titulo

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
