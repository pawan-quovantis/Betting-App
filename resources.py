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


class Matches(Resource):

    # @login_required
    def get(self):
        fixtures = db.session.query(Fixtures).all()
        response = []
        for fixture in fixtures:
            response.append(fixture.my_dict())
        return jsonify(response)


class Bets(Resource):

    # @login_required
    def get(self):
        bets = db.session.query(models.Bets).all()
        response = []
        for bet in bets:
            response.append(bet.my_dict())
        return jsonify(response)


class BettingHistory(Resource):

    # @login_required
    def get(self):
        betting_history = db.session.query(UserBettingHistory).all()
        response = []
        for history in betting_history:
            response.append(history.my_dict())
        return jsonify(response)


class Teams(Resource):

    # @login_required
    def get(self):
        teams = db.session.query(models.Teams).all()
        response = []
        for team in teams:
            response.append(team.my_dict())
        return jsonify(response)

