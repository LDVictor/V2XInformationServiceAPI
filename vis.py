from flask import Flask
from flask_restful import Api
from resources.v2xmsg import V2XMsg

app = Flask(__name__)
api = Api(app)

#api.add_resource(V2XMsg, '/queries/provisioning_info')
api.add_resource(V2XMsg, '/publish_v2x_message/<string:credential>')

if __name__ == '__main__':
    app.run(debug=True)
