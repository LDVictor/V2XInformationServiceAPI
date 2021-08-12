from aiocoap import *
import logging
import asyncio

msg = Message(code=GET, uri="coap://localhost/other/separate")

logging.basicConfig(level=logging.INFO)

async def main():

    protocolo = await Context.create_client_context()
    requisicao = Message(code=GET, uri='coap://localhost/time')

    try:
        response = await protocol.request(requisicao).response
    except Exception as e:
        print('Falha ao buscar recurso: ')
        print(e)
    else:
        print('Resultado: %s\n%r'%(response.code, response.payload))
    
