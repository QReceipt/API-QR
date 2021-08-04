from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace
from models import User

Hello = Namespace('Hello')

@Hello.route('')
@Hello.route('/')
class HelloWorld(Resource):  
    def get(self):
        users = User.query.all()
        return make_response(jsonify({"results":User.serialize_list(users)}), 200)

# api.add_namespace(namespace, '/hello')  

