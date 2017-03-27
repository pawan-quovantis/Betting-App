from flask_restful import Resource
from models import *
from flask import jsonify
import models


class Bets(Resource):

    # @login_required
    def get(self):
        bets = db.session.query(models.Bets).all()
        response = []
        for bet in bets:
            response.append(bet.my_dict())
        return jsonify(response)
