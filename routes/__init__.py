from flask import Flask
from flask_restx import Resource, Api
from .hello import Hello
from .qr import QR

app = Flask (__name__,static_url_path='',static_folder='./static')
api = Api(app)

api.add_namespace(Hello,'/hello')
api.add_namespace(QR,'/qr')
