from flask_restful import reqparse, abort, Api, Resource
from models import *
from flask import jsonify
import models


class Users(Resource):

    # @login_required
    def get(self):
        users = db.session.query(models.Users).all()
        response = []
        for user in users:
            response.append(user.my_dict())
        return jsonify(response)

