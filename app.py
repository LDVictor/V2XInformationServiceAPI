from flask import Flask
from flask_restful import Api
from resources.v2xmsg import V2XMsg
from models.vehicle import VehicleModel
from models.rsu import RSUModel
from bluetooth import *

# import para requisicao

import requests

# imports da aiocoap

from aiocoap import *
import logging
import asyncio

# imports da biblioteca V2X

import Bluetooth.BluetoothServer as btserver
import Wifi.WifiServer as wserver
import Wifi.WifiClient as wclient
import Wifi.Wifi
import DBModule.Database as db
#import thread
import time
import json
import sys

## Funções ##

def enviaMensagem(opcao):

     logging.basicConfig(level=logging.INFO)

     # Instancia do veiculo e RSU

     veiculo = VehicleModel("vehicle_01", "Car", "120.0", "0.0", "0.0")

     print("Criando veiculo com OBU: ")
     print(veiculo.json)
     print(" ")

     road_site_unit = RSUModel("rsu_01", "RSU", "0.1", "0.1")

     print("Criando RSU: ")
     print(road_site_unit.json)
     print(" ")

     # Chamada da aplicação V2X de Streaming

     if opcao == "1":
         uuid = streamingApplication(veiculo, road_site_unit, opcao)
     else:
         uuid = streamingApplication(road_site_unit, veiculo, opcao)

    # Protocolo CoAP de comunicação
     #protocolo_coap = await Context.create_client_context()
     url_coap = "coap://localhost/other/separate/";
     requisicao = Message(code=POST, uri=url_coap)
     print ("POST CoAP on " + url_coap)

    # Formação da Mensagem V2X
     msg = {
          "msgContent": uuid, # referencia da mensagem da aplicacao de streaming
          "msgEncodeFormat": "string",
          "msgType": 1,
          "stdOrganization": "ETSI"
            }

    # Requisicao do Publish V2X Message da API VIS
     post_vis = requests.post('http://127.0.0.1:5000/publish_v2x_message/vehicle_01', data=msg)
     print("A resposta da API VIS eh: ")
     print(post_vis.text)

    # Realizando o request
     try:
         response = protocolo.request(requisicao).response
     except Exception as e:
         print('Resultado: %s\n%r'%(requisicao.code, requisicao.payload))
         #print('Falha ao buscar recurso: ')
         #print('e')
     else:
         print('Resultado: %s\n%r'%(requisicao.code, requisicao.payload))

##### Funcoes Auxiliares #####

def streamingApplication(self, entity_01, entity_02):

    #input = input("Input ya bashaa !!\n")

    endereco = '00:15:83:0C:BF:EB'

    # search for the SampleServer service
    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    uuid = "00000003-0000-1000-8000-00805F9B34FB"
    service_matches = find_service(name = "SampleServer Streaming", uuid = uuid, address = endereco)

    print("Message Streaming: ")

    print(service_matches)

    if len(service_matches) == 0:
        print("connecting to StreamingServer service =)")
        #sys.exit(0)
        if opcao == "2":
            print("request")
            return "request"
        elif opcao == "1":
            print(uuid)
            return uuid

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    sock=BluetoothSocket( RFCOMM )
    sock.connect((host, port))

    print("connected.  type stuff at port " + str(port))
    while True:
        data1 = input()
        #if len(data1) == 0: break
        sock.send(data1)
    #while True:
    #   data1 = sock.recv(1024)
    #   if len(data1) == 0: break
    #   print("Received [%s]" %data1)

    if opcao == "1":
        return "request"
    else:
        return uuid

    sock.close()


# implementacao do Menu

print("V2X Menu - por Victor Emanuel Farias")
print(".....")
print("Selecione uma opção:")
print(".....")
print("1 - Enviar mensagem de streaming de RSU para veículo")
print(".....")
print("2 - Enviar mensagem de streaming de veículo para RSU")

opcao = input()

if opcao == "1":
    enviaMensagem(opcao)
elif opcao == "2":
    enviaMensagem(opcao)
else:
    print("Opção não reconhecida. Digite 1 ou 2.")
