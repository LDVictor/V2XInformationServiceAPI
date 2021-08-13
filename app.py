from flask import Flask
from flask_restful import Api
from resources.v2xmsg import V2XMsg

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
import v2v-library.MobileApps.StreamingApp.PythonStreamingService.client
import v2v-library.MobileApps.StreamingApp.PythonStreamingService.server

app = Flask(__name__)
api = Api(app)

api.add_resource(V2XMsg, '/queries/provisioning_info')
api.add_resource(V2XMsg, '/publish_v2x_message')

# implementacao do Menu

print("V2X Menu - by Victor Emanuel Farias")
print(".....")
print("Selecione uma opção:")
print(".....")
print("1 - Enviar mensagem de streaming de RSU para veículo")
print(".....")
print("2 - Enviar mensagem de streaming de veículo para RSU")

 def enviaMensagem(self):

     logging.basicConfig(level=logging.INFO)

     protocolo_coap = await Context.create_client_context()
     requisicao = Message(code=GET, uri="coap://localhost/other/separate")

     # implementar comunicacao V2X aqui

     msg = {
          "msgContent": "string", # colocar referencia para a mensagem da aplicacao
          "msgEncodeFormat": "string",
          "msgType": 1,
          "stdOrganization": "ETSI"
            }

     post_vis = requests.post('http://127.0.0.1:5000/publish_v2x_message/vehicle_01', data=msg)
     print("A resposta do POST VIS eh " + post_vis.text)

     get_vis = requests.get('http://127.0.0.1:5000/queries/provisioning_info/vehicle_01')
     print("A resposta do GET VIS eh " + get_vis.text)

     # implementacao do CoAP

     try:
         response = await protocolo.request(requisicao).response
     except Exception as e:
         print('Falha ao buscar recurso: ')
         print('e')
     else:
         print('Resultado: %s\n%r'%(requisicao.code, requisicao.payload))


if __name__ == '__main__':
    app.run(debug=True)
