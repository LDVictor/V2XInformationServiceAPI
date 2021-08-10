from flask_restful import Resource, reqparse

lista_v2xmsg = []
lista_elementos = [
    'vehicle_01',
    'vehicle_02',
    'vehicle_03',
    'vehicle_04',
    'rsu_01',
    'rsu_02'
]

class V2XMsg(Resource):

    # argumentos do recebimento do JSON
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('msgContent')
    argumentos.add_argument('msgEncodeFormat')
    argumentos.add_argument('msgType')
    argumentos.add_argument('stdOrganization')

    # funcoes auxiliares
    def isNulo(self, v2x_message):
        return v2x_message['msgContent'] == None and v2x_message['msgEncodeFormat'] == None and v2x_message['msgType'] == None and v2x_message['stdOrganization'] == None

    def find_message(self, credential):
        for v2xmsg in lista_v2xmsg:
            if v2xmsg['msgType'] == credential:
                return v2xmsg
            return None

    # funcao get: retorna o JSON requisitado da provisioning info
    def get(self, credential):

        v2xmsg = V2XMsg.find_message(credential)

        if v2xmsg:
            return v2xmsg

        return {'message': 'Provisioning info not found.'}, 404 # not found

    # funcao post: retorna o JSON de response
    def post(self, credential):

        dados = V2XMsg.argumentos.parse_args()

        v2x_message = {
        'msgContent': dados['msgContent'],
        'msgEncodeFormat': dados['msgEncodeFormat'],
        'msgType': dados['msgType'],
        'stdOrganization': dados['stdOrganization']
        }

        if isNulo(v2x_message):
            return "No Content", 204

        elif credential not in lista_elementos:
            erro = {
            'detail': 'used when the client did not submit credentials.',
            'instance': 'Error',
            'status': 0,
            'title': 'Unauthorized',
            'type': 'Error 401'
            }

            return erro, 401

        elif credential == None:
            erro = {
            'detail': 'used when a client provided a URI that cannot be mapped to a valid resource URI.',
            'instance': 'Error',
            'status': 0,
            'title': 'Not Found',
            'type': 'Error 404'
            }

            return erro, 401

        else:
            lista_v2xmsg.append(v2x_message)
            return "Message sent successfully.", 200
