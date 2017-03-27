from flask_restful import Resource
from models import *
from flask import jsonify


class BettingHistory(Resource):

    # @login_required
    def get(self):
        betting_history = db.session.query(UserBettingHistory).all()
        response = []
        for history in betting_history:
            response.append(history.my_dict())
        return jsonify(response)

