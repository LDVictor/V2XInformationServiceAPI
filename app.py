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

import BluetoothServer as btserver
import WifiServer as wserver
import WifiClient as wclient
import Wifi
import Database as db
import thread
import time
import json
import sys

app = Flask(__name__)
api = Api(app)

api.add_resource(V2XMsg, '/queries/provisioning_info')
api.add_resource(V2XMsg, '/publish_v2x_message')

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

def enviaMensagem(self, opcao):

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
     protocolo_coap = await Context.create_client_context()
     requisicao = Message(code=POST, uri="coap://localhost/other/separate", data=uuid)

    # Formação da Mensagem V2X
     msg = {
          "msgContent": uuid, # referencia da mensagem da aplicacao de streaming
          "msgEncodeFormat": "string",
          "msgType": 1,
          "stdOrganization": "ETSI"
            }

    # Requisicao do Publish V2X Message da API VIS
     post_vis = requests.post('http://127.0.0.1:5000/publish_v2x_message/vehicle_01', data=msg)
     print("A resposta do POST VIS eh: ")
     print(post_vis.text)

    # Realizando o request
     try:
         response = await protocolo.request(requisicao).response
     except Exception as e:
         print('Falha ao buscar recurso: ')
         print('e')
     else:
         print('Resultado: %s\n%r'%(requisicao.code, requisicao.payload))

##### Funcoes Auxiliares #####

def streamingApplication(self, entity_01, entity_02):

    input = raw_input("Input ya bashaa !!\n")

    endereco = '00:15:83:0C:BF:EB'

    # search for the SampleServer service
    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    uuid = "00000003-0000-1000-8000-00805F9B34FB"
    service_matches = find_service(name = "SampleServer Streaming", uuid = uuid, address = endereco )

    print("Message Streaming: ")
    print(uuid)

    print(service_matches)

    if len(service_matches) == 0:
        print("couldn't find the SampleServer service =(")
        sys.exit(0)

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
        data1 = raw_input()
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



if __name__ == '__main__':
    app.run(debug=True)
