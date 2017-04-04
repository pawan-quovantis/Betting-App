from flask_restful import Resource
from models import *
from flask import jsonify
import models
from flask import request


class Fixtures(Resource):

    def get(self):

        if hasattr(request, 'authorization'):
            password = request.headers["authorization"]
            try:
                user = db.session.query(Users).filter(Users.password == password).first()
                bets = user.bets
                user_bets = []
                for bet in bets:
                    user_bets.append(bet.my_dict())

                all_bets = db.session.query(models.Bets).all()
                all_bets_array = []
                for bet in all_bets:
                    all_bets_array.append(bet.my_dict())

                matches = []
                fixtures = db.session.query(models.Fixtures).all()
                for fixture in fixtures:
                    fixture_object = fixture.my_dict()
                    fixture_object["home_team"] = fixture.home_team.team_name
                    fixture_object["away_team"] = fixture.away_team.team_name

                    matches.append(fixture_object)

                if user_bets.__len__() > 0:
                    for match in matches:
                        for user_bet in user_bets:
                            if match["id"] == user_bet["fixture_id"]:
                                match["bet_amount"] = user_bet["amount"]
                                match["bet_placed_on_team"] = user_bet["team_id"]

                        bets_on_home_team = 0
                        bets_on_away_team = 0
                        for bet in all_bets_array:
                            if match["id"] == bet["fixture_id"]:
                                if match["home_team_id"] == bet["team_id"]:
                                    bets_on_home_team += bet["amount"]
                                elif match["away_team_id"] == bet["team_id"]:
                                    bets_on_away_team += bet["amount"]

                        match["bets_on_home_team"] = bets_on_home_team
                        match["bets_on_away_team"] = bets_on_away_team
                return jsonify(matches)

            except Exception as ex:
                return ex.message, 500

        else:
            return {"Missing Credentials"}
