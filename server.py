from flask import Flask, request
from flask_restful import Api, Resource,reqparse
import hashlib
import json

app = Flask(__name__)
api = Api(app)

import random
import time

class Server():
    def __init__(self):
        self.clients = {}

    def get_client_token(self,user):
        return self.clients.get(user,None)

    def add_client(self,user):
        base = str(random.random())+user+time.strftime("%H:%M:%S")
        base = base.encode("utf-8")
        token = hashlib.md5(base).hexdigest()
        self.clients[user] = token
        return token

    def is_valid_token(self,user,token):
        if not user in self.clients:
            return False

        return self.clients[user] == token

class Login(Resource):
    def __init__ (self,server):
        self.server = server

    def get(self):
        args = request.json
        if not args:
            return None,414 #FIXME

        user_id = args["user_id"]
        token = self.server.add_client(user_id)
        data = {}
        data["user_id"] = user_id
        data["token"] = token
        data["data"] = args
        return data,200

class Hello_World (Resource):
    def __init__(self, server):
        self.server = server

    def get(self):
        args = request.json
        if not args:
            return None,414 #FIXME

        user_id = args["user_id"]
        token = args["token"]

        if not self.server.is_valid_token(user_id,token):
            return "Invalid Token",415 #FIXME

        data = {}
        data["Message"] = "Hello World!"
        return data,200

server = Server()
api.add_resource(Login, '/api/v1.0/login',resource_class_kwargs={ 'server': server })
api.add_resource(Hello_World, '/api/v1.0/helloWorld',resource_class_kwargs={ 'server': server })
