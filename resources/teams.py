from flask_restful import Resource
from models import *
from flask import jsonify
import models


class Teams(Resource):

    # @login_required
    def get(self):
        teams = db.session.query(models.Teams).all()
        response = []
        for team in teams:
            response.append(team.my_dict())
        return jsonify(response)

