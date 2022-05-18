#from flask import Flask
from pymongo import MongoClient
import pymongo
from datetime import datetime, timedelta
from concurrent import futures
import time
import logging
import json
from interfaces import User_pb2, User_pb2_grpc
import grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CRUD(User_pb2_grpc.UserServicer):

    def Connection(self):
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = MongoClient(CONNECTION_STRING)
        db = client['crud-grpc']
        employee = db.employees

        return employee

    def Insert(self, request, context):
        employee = self.Connection()
        today = datetime.today()

        data_insert = {
            'username': request.username,
            'name': request.name,
            'email': request.email,
            'dob': request.dob,
            #'created_at': today - timedelta(days=200)
        }

        employee.insert_one(data_insert)
        return User_pb2.StatusResponse(message='Success Insert Data With Username: ' + request.username)

    def List(self, request, context):
        employee = self.Connection()

        employees = employee.find({})

        for data in employees:
            if data is not None:
                listdata = User_pb2.DataResponse(
                    username=data["username"],
                    name=data["name"],
                    email=data["email"],
                    dob=data["dob"],
                    #created_at=["created_at"]
                )
                yield listdata

    def Show(self, request, context):
        employee = self.Connection()

        employees = employee.find_one({"username": request.username})

        return User_pb2.DataResponse(
            username=employees["username"],
            name=employees["name"],
            email=employees["email"],
            dob=employees["dob"],
            #created_at=employees["created_at"]
        )

    def Update(self, request, context):
        employee = self.Connection()

        data_update = {
            'name': request.name,
            'email': request.email,
            'dob': request.dob
        }
        employee.replace_one({"username": request.username}, data_update)

        return User_pb2.StatusResponse(message='Success Update Data With username: ' + request.username)

    def Delete(self, request, context):
        employee = self.Connection()

        employee.delete_one({'username': request.username})

        return User_pb2.StatusResponse(message="Success Delete Data With username: " + request.username)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    User_pb2_grpc.add_UserServicer_to_server(CRUD(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    print('Starting Server...')
    logging.basicConfig()
    serve()


