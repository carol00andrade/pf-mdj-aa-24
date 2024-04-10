# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import os
import re
import smtplib
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml.html import document_fromstring

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

## Página dinâmica para exibir notícias filtradas por palavra-chave

@app.route("/noticias")
def noticias():
    palavra_chave = request.args.get('palavra_chave', ' ')
    if not palavra_chave:
        return "Por favor, especifique uma palavra-chave na URL."
    url = 'https://noticias.uol.com.br/'
    palavras_chave_disponiveis = ['afogada', 'agredida', 'agrediu', 'agressão', 'amante', 'arma', 'assassinada', 'assassinadas', 'assassinato', 'assassinou', 'atirou', 'casamento', 'chuta', 'companheiro', 'consentimento', 'corpo', 'deputada', 'esfaqueada', 'esposa', 'estupro', 'ex-marido', 'ex-namorado', 'faca', 'facada', 'feminicídio', 'filha', 'gênero', 'machismo', 'machista', 'matar', 'marido', 'mataram', 'matava', 'matou', 'matamos', 'menina', 'morta', 'mortas', 'mortes', 'morre', 'morreu', 'mordida', 'mulher', 'namorada', 'queimada', 'sexual', 'tapa', 'tiro', 'vítima', 'violência', 'vereadora']
    if palavra_chave not in palavras_chave_disponiveis:
        return "Palavra-chave inválida. Por favor, escolha uma das palavras-chave disponíveis."
    manchetes_selecionadas = raspar_e_selecionar_noticias(url, [palavra_chave])
    noticias_html = manchetes_selecionadas.to_html(index=False)
    return render_template("noticias.html", noticias_html=noticias_html)
    
def raspar_e_selecionar_noticias(url, palavras_chave):
    manchetes = raspar_noticias(url)
    manchetes_selecionadas = selecionar_noticias_com_palavra_chave(manchetes, palavras_chave)
    df = pd.DataFrame(manchetes_selecionadas, columns=['Título', 'Link'])
    return df

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
                break  
    return titulos_selecionados

if __name__ == "__main__":
    app.run(debug=True)

## Dados para conexão no servidor SMTP:

smtp_server = "smtp-relay.brevo.com"
port = 587
email = "carol00andrade@gmail.com"
password = "carol00andrade" 

# Dados para o email que será enviado:
remetente = "Ana Carolina Andrade" 
destinatarios = ["carol00andrade@gmail.com", "alvarojusten@gmail.com"]
titulo = "Raspagem de notícias sobre violência de gênero no UOL"
html = """
<html>
<body>
<h1>Raspagem de notícias sobre violência de gênero no UOL</h1>
<p>Olá, este é um email automático gerado pela raspagem de notícias sobre violência de gênero no site UOL.</p>
</body>
</html>
"""

# Iniciando conexão com o servidor:
server = smtplib.SMTP(smtp_server, port)  # Inicia a conexão com o servidor
server.starttls()  # Altera a comunicação para utilizar criptografia
server.login(email, password)  # Autentica

# Preparando o objeto da mensagem ("documento" do email):
mensagem = MIMEMultipart()
mensagem["From"] = remetente
mensagem["To"] = ",".join(destinatarios)
mensagem["Subject"] = titulo
conteudo_html = MIMEText(html, "html")  # Adiciona a versão em HTML
mensagem.attach(conteudo_html)

# Enviando o email pela conexão já estabelecida:
server.sendmail(remetente, destinatarios, mensagem.as_string())

# Fechando a conexão com o servidor SMTP:
server.quit()
