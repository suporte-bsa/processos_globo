import sys
from .models import *
import shutil
import os 
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup
import csv   
from csv import writer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADERS = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'portal.stf.jus.br',
'Referer':'https://www.google.com/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
 }

#Aqui tem todos os métodos do site.

def get_incidente_id(classe, numero):
    url = "http://portal.stf.jus.br/processos/listarProcessos.asp?classe=" + classe + "&numeroProcesso=" + numero
    response_andamento = client.get(url, headers=HEADERS, timeout=(9.05,6))
    
    redirect_url = response_processo.history[0].headers['location']
    incidente_id = redirect_url.split('=', 1)[1]

    return incidente_id


def get_data_atualizacao(incidente_id):

    client = requests.session()
    url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id
    response_andamento = client.get(url, headers=HEADERS, timeout=(9.05,6))
    print("- - - Get data atualização")
    html_page = response_andamento.content
    print("- - - Get descricao atualizacao")
    
    soup = BeautifulSoup(html_page, 'html.parser')

    andamento_data = soup.find("div", {"class": "andamento-data"}).get_text()
    andamento_nome = soup.find("h5", {"class": "andamento-nome"}).get_text()
    return andamento_data, andamento_nome 

def enviar_emails(classe, numero, descricao, descricao_atualizacao, data_atualizacao, incidente_id, email):
    # Conexao com o servidor do Gmail, utilizando login e senha:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('youremail@example.com', 'password')

        # Informacoes de remetentes e destinatarios:
    sender = 'youremail@example.com'
    to_addresses = email
    #use isso para teste
    #cc_addresses = 'email1@email, email2@email'
    #bcc_addresses = 'email3@email, email4@email'
    #recipients_addresses = to_addresses.split(",") + cc_addresses.split(",") + bcc_addresses.split(",")
    recipients_addresses = to_addresses
        # Assunto do e-mail:
    subject = str(descricao)

        # Corpo do e-mail:
    message = '<html><body><p>Olá!</p><p>O seguinte processo foi atualizado: ' + str(classe) + ' ' + str(numero) + \
                '</p><p>Descrição da atualização: ' + str(descricao_atualizacao) + ' em: ' + str(data_atualizacao) + \
                '.</p><p>Para acompanhar o processo, <a href="http://portal.stf.jus.br/processos/detalhe.asp?incidente=' + str(incidente_id) + '">clique aqui</a>.</p>' + \
                '<p>Atenciosamente, Tecnologia Brasília.</p></body></html>' 
        
        # Montagem do e-mail:
    msg = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = to_addresses
    msg['Cc'] = cc_addresses
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html', 'utf-8'))

    text = msg.as_string()

        # Envio do e-mail para os destinatarios:
    server.sendmail(sender, recipients_addresses, text)

    # Finalizacao da conexao com o Gmail apos o envio de todos os e-mails:
    server.quit()

    # Limpa o arquivo "updates.csv" para a proxima consulta:

    return
def enviar_notificacoes(classe, numero, descricao, descricao_atualizacao, data_atualizacao, incidente_id, email):
    bot_message = 'Atualização: ' + str(descricao) + '. Descrição: ' + str(descricao_atualizacao) + ' em: ' + str(data_atualizacao) + '. Link: http://portal.stf.jus.br/processos/detalhe.asp?incidente=' + str(incidente_id)
    bot_token = 'token'
    bot_chatID = 'chat_id'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message 

    response = requests.get(send_text)

    return response.json()
