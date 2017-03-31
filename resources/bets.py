from flask_restful import Resource
from models import *
from flask import jsonify
import models
from flask import request


class Bets(Resource):

    # @login_required
    def get(self):
        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            user = db.session.query(Users).filter(Users.password == password).first()
            bets = user.bets
            user_bets = []
            for bet in bets:
                user_bets.append(bet.my_dict())

            matches = []
            fixtures = db.session.query(Fixtures).all()
            for fixture in fixtures:
                matches.append(fixture.my_dict())

            if user_bets.__len__() > 0:
                for match in matches:
                    for user_bet in user_bets:
                        if match["id"] == user_bet["fixture_id"]:
                            match["bet_amount"] = user_bet["amount"]
                            match["bet_placed_on_team"] = user_bet["team_id"]

            return jsonify(matches)

        else:

            return {"Missing Credentials"}

    def post(self):
        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            user = db.session.query(Users).filter(Users.password == password).first()
            fixture_id = request.values["fixture_id"]
            team_id = request.values["team_id"]
            amount = request.values["amount"]
            bet = db.session.query(models.Bets).filter(models.Bets.user_id == user.id, models.Bets.fixture_id == fixture_id).first()
            if bet is None:
                try:
                    new_bet = Bets(user_id=user["id"], fixture_id=fixture_id, amount=amount, team_id=team_id)
                    db.session.add(new_bet)
                    db.session.commit()
                    return jsonify({"Message": "Bet Placed Successfully", "Status-Code": 200})
                except Exception as ex:
                    return ex.message, 500
            else:
                return "Bet has been already placed, Please update the existing bet."

    def put(self):

        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            user = db.session.query(Users).filter(Users.password == password).first()
            fixture_id = request.values["fixture_id"]
            team_id = request.values["team_id"]
            amount = request.values["amount"]
            bet = db.session.query(models.Bets).filter(models.Bets.user_id == user.id,
                                                       models.Bets.fixture_id == fixture_id).first()
            if bet is not None:
                try:
                    bet.amount = amount
                    bet.team_id = team_id
                    db.session.commit()
                    return jsonify({"Message": "Bet Updated Successfully", "Status-Code": 200})
                except Exception as ex:
                    return ex.message, 500
            else:
                return "Invalid Request"

    def delete(self):
        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            user = db.session.query(Users).filter(Users.password == password).first()
            fixture_id = request.values["fixture_id"]
            bet = db.session.query(models.Bets).filter(models.Bets.user_id == user.id,
                                                       models.Bets.fixture_id == fixture_id).first()
            if bet is not None:
                try:
                    db.session.delete(bet)
                    db.session.commit()
                    return jsonify({"Message": "Bet Deleted Successfully", "Status-Code": 200})
                except Exception as ex:
                    return ex.message, 500
            else:
                return "Invalid Request"









