from flask_restful import Resource
from models import *
from flask import jsonify, request
import models


class Users(Resource):

    def get(self):
        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            try:
                users = db.session.query(models.Users).all()
                response = []
                for user in users:
                    score = 0
                    for history in user.user_betting_history:
                        score += history.score

                    user = user.my_dict()
                    user["score"] = score
                    response.append(user)

                response = sorted(response, key=lambda k: k['score'])
                return jsonify(response)

            except Exception as ex:
                return ex.message, 500
        else:
            return "Invalid Request"


class User(Resource):

    def get(self):
        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            try:
                user = db.session.query(models.Users).filter(models.Users.password == password).first()
                user = user.my_dict()
                return jsonify(user)
            except Exception as ex:
                return ex.message, 500

        else:
            return "Invalid Request"
